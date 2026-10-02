import gzip
import os
import orjson
from collections import defaultdict

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================
DATA_DIR = 'data'
OUTPUT_FILE = os.path.join(DATA_DIR, 'medication_request_dataset_full.jsonl')

PATIENT_FILE = os.path.join(DATA_DIR, 'MimicPatient.ndjson.gz')
CONDITION_FILES = [os.path.join(DATA_DIR, 'MimicCondition.ndjson.gz'), 
                   os.path.join(DATA_DIR, 'MimicConditionED.ndjson.gz')] # ¡Añadimos Urgencias!
MED_FILE = os.path.join(DATA_DIR, 'MimicMedication.ndjson.gz')
ENCOUNTER_FILES = [os.path.join(DATA_DIR, 'MimicEncounter.ndjson.gz'), 
                   os.path.join(DATA_DIR, 'MimicEncounterED.ndjson.gz')]
ADMIN_FILE = os.path.join(DATA_DIR, 'MimicMedicationAdministration.ndjson.gz') # ¡Nuevo!

MED_REQUEST_FILE = os.path.join(DATA_DIR, 'MimicMedicationRequest.ndjson.gz')

PROCEDURE_FILES = [os.path.join(DATA_DIR, 'MimicProcedure.ndjson.gz')]

# ==========================================
# 2. HERRAMIENTAS BASE (MOTOR TURBO)
# ==========================================
def iter_ndjson(path, stats):
    """Lee .ndjson.gz en binario y parsea a la velocidad de la luz con orjson."""
    if not os.path.exists(path):
        print(f"⚠️ Aviso: No se encontró {path}")
        return
    with gzip.open(path, 'rb') as f:
        for line in f:
            if not line.strip(): continue
            try:
                yield orjson.loads(line)
            except orjson.JSONDecodeError:
                stats['json_errors'] += 1

def dig(d, *path, default=None):
    """Navega por diccionarios anidados de forma segura."""
    for k in path:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return default
    return d

# ==========================================
# 3. FUNCIONES DE CARGA EN RAM (DIMENSIONES)
# ==========================================
def cargar_pacientes(filepath, stats):
    print(f"⏳ Cargando pacientes...")
    diccionario = {}
    for paciente in iter_ndjson(filepath, stats):
        diccionario[paciente.get('id')] = {
            'patient_gender': paciente.get('gender', 'unknown'),
            'patient_birthdate': paciente.get('birthDate', 'unknown')
        }
    return diccionario

def cargar_diagnosticos(filepaths, stats):
    print(f"⏳ Cargando diagnósticos (Alta y Urgencias)...")
    por_enc = defaultdict(dict) # Evita duplicados usando el código ICD
    for filepath in filepaths:
        for cond in iter_ndjson(filepath, stats):
            # Extraer el ID del ingreso
            enc_ref = dig(cond, 'encounter', 'reference', default='')
            enc_id = enc_ref.rsplit('/', 1)[-1] if '/' in enc_ref else ''
            
            # Extraer código ICD y texto
            cod = dig(cond, 'code', 'coding', 0, 'code', default='UNKNOWN')
            txt = dig(cond, 'code', 'coding', 0, 'display', default='No description')
            
            if enc_id:
                # Guardamos "CODIGO: Texto". Si el código se repite, simplemente se pisa.
                por_enc[enc_id][cod] = txt
    return por_enc

def cargar_medicamentos(filepath, stats):
    print(f"⏳ Cargando catálogo de medicamentos (robusto)...")
    diccionario = {}
    for med in iter_ndjson(filepath, stats):
        med_id = med.get('id')
        med_name = "unknown"
        
        # Buscar en 'identifier' por la etiqueta mimic-medication-name
        identifiers = med.get('identifier', [])
        for ident in identifiers:
            if 'mimic-medication-name' in ident.get('system', ''):
                med_name = ident.get('value', 'unknown')
                break
                
        # Fallback de seguridad al bloque 'code'
        if med_name == "unknown":
            med_name = dig(med, 'code', 'text', default="unknown")
            
        diccionario[med_id] = med_name
    return diccionario

def cargar_encounters(filepaths, stats):
    print(f"⏳ Cargando ingresos hospitalarios...")
    diccionario = {}
    for filepath in filepaths:
        for enc in iter_ndjson(filepath, stats):
            diccionario[enc.get('id')] = {
                'encounter_class': dig(enc, 'class', 'code', default='unknown'),
                'encounter_start': dig(enc, 'period', 'start', default=''),
                'encounter_end': dig(enc, 'period', 'end', default='')
            }
    return diccionario

def cargar_administraciones(filepath, stats):
    print(f"⏳ Cargando registros de administración (Detector de Desvío)...")
    administradas = set() # Usamos un Set porque buscar si un elemento existe es instantáneo (O(1))
    for admin in iter_ndjson(filepath, stats):
        req_ref = dig(admin, 'request', 'reference', default='')
        req_id = req_ref.rsplit('/', 1)[-1] if '/' in req_ref else ''
        if req_id:
            administradas.add(req_id)
    return administradas

def cargar_procedimientos(filepaths, stats):
    print(f"⏳ Cargando procedimientos y quirófanos...")
    por_enc = defaultdict(dict)
    contador_leidos = 0
    contador_mapeados = 0
    
    for filepath in filepaths:
        for proc in iter_ndjson(filepath, stats):
            contador_leidos += 1
            
            # Obtener la referencia del encounter de forma ultra-segura
            enc_ref = dig(proc, 'encounter', 'reference', default='')
            if not enc_ref:
                # Fallback por si viene en otro campo plano
                enc_ref = proc.get('encounter', '')
                if isinstance(enc_ref, dict):
                    enc_ref = enc_ref.get('reference', '')
            
            # Extraer el ID limpio
            enc_id = enc_ref.rsplit('/', 1)[-1] if '/' in enc_ref else str(enc_ref)
            
            cod = dig(proc, 'code', 'coding', 0, 'code', default='UNKNOWN')
            txt = dig(proc, 'code', 'coding', 0, 'display', default='No description')
            
            if enc_id and enc_id != '':
                por_enc[enc_id][cod] = txt
                contador_mapeados += 1

    print(f"🔍 [DEBUG] Procedimientos leídos: {contador_leidos} | Mapeados correctamente a ingresos: {contador_mapeados}")
    return por_enc

# ==========================================
# 4. PROCESAMIENTO MAESTRO (ETL)
# ==========================================
def procesar_recetas(med_req_filepath, output_filepath, pacientes, diagnosticos, procedimientos, medicamentos, encounters, administradas, stats):
    print(f"🚀 Cruzando datos y generando JSONL...")
    
    if not os.path.exists(med_req_filepath):
        print(f"❌ Error: No se encuentra {med_req_filepath}")
        return

    # Usamos modo binario ('wb') para que orjson escriba a máxima velocidad
    with gzip.open(med_req_filepath, 'rb') as f_in, \
         open(output_filepath, 'wb') as f_out:
        
        for line in f_in:
            if not line.strip(): continue
            try:
                receta = orjson.loads(line)
            except orjson.JSONDecodeError:
                stats['json_errors'] += 1
                continue
                
            stats['total_recetas_procesadas'] += 1
            
# --- REFERENCIAS (IDs) ---
            req_id = receta.get('id')
            patient_id = dig(receta, 'subject', 'reference', default='').rsplit('/', 1)[-1]
            encounter_id = dig(receta, 'encounter', 'reference', default='').rsplit('/', 1)[-1]
            requester_id = dig(receta, 'requester', 'reference', default='').rsplit('/', 1)[-1]
            
            # --- RESOLUCIÓN DEL NOMBRE DEL FÁRMACO (DOBLE VÍA) ---
            # Vía 1: Intentar buscar por ID en el catálogo
            medication_id = dig(receta, 'medicationReference', 'reference', default='').rsplit('/', 1)[-1]
            medication_name = medicamentos.get(medication_id, 'unknown') if medication_id else 'unknown'
            
            # Vía 2 (Fallback): Si falló o no tiene ID, buscar el nombre oculto en la propia receta
            if medication_name == 'unknown':
                concept_text = dig(receta, 'medicationCodeableConcept', 'text')
                if concept_text:
                    medication_name = concept_text
                else:
                    concept_display = dig(receta, 'medicationCodeableConcept', 'coding', 0, 'display')
                    concept_code = dig(receta, 'medicationCodeableConcept', 'coding', 0, 'code')
                    if concept_display: medication_name = concept_display
                    elif concept_code: medication_name = concept_code

           # Vía 3 (Rescate inteligente de Sueros/Mixes IV perdidos en la Demo)
            if medication_name == 'unknown':
                texto_dosis = dig(receta, 'dosageInstruction', 0, 'text', default='')
                route = dig(receta, 'dosageInstruction', 0, 'route', 'coding', 0, 'code', default='')
                
                # Comprobamos si realmente es un fluido/suero o vía IV con términos de bolsa/frasco
                if texto_dosis and (route == 'IV' or any(term in texto_dosis.lower() for term in ['bag', 'bottle', 'premix', 'soln', 'iv', 'infusion'])):
                    medication_name = f"IV Fluid / Mix: {texto_dosis}"
                else:
                    # Si no es un fluido y no tiene nombre, lo dejamos como un medicamento desconocido controlado
                    medication_name = f"Unknown Oral/Other: {texto_dosis}" if texto_dosis else "unknown"

            
            # --- SEGUIMIENTO DE ERRORES (MÉTRICAS) ---
            if patient_id not in pacientes: stats['miss_patient'] += 1
            if encounter_id not in encounters: stats['miss_encounter'] += 1
            # Solo contamos como fallo si después de buscar por todos lados sigue siendo unknown
            if medication_name == 'unknown': 
                stats['miss_medication'] += 1
                # Añade esto para imprimir solo el primer fallo y ver sus tripas
                if stats['miss_medication'] == 1:
                    print("\n🔍 RECETA REBELDE ENCONTRADA:")
                    print(orjson.dumps(receta, option=orjson.OPT_INDENT_2).decode('utf-8'))
                    print("\n")
            
            # --- JOINS EN RAM ---
            datos_paciente = pacientes.get(patient_id, {'patient_gender': 'unknown', 'patient_birthdate': 'unknown'})
            datos_encounter = encounters.get(encounter_id, {'encounter_class': 'unknown', 'encounter_start': '', 'encounter_end': ''})
            
            # Reconstruir diagnósticos a texto limpio (CÓDIGO: Nombre | CÓDIGO2: Nombre2)
            dict_diags = diagnosticos.get(encounter_id, {})
            diags_texto = " | ".join([f"{cod}: {txt}" for cod, txt in dict_diags.items()]) if dict_diags else "No diagnosis recorded"

            # Procedimientos / Quirófanos
            dict_procs = procedimientos.get(encounter_id, {})
            procs_texto = " | ".join([f"{cod}: {txt}" for cod, txt in dict_procs.items()]) if dict_procs else "No procedure recorded"

            # --- BANDERA DE FRAUDE / ANOMALÍA ---
            fue_administrado = req_id in administradas
            
            # --- EXTRACCIÓN DE DOSIS (Usando dig) ---
            dosage_text = dig(receta, 'dosageInstruction', 0, 'text', default='')
            route_code = dig(receta, 'dosageInstruction', 0, 'route', 'coding', 0, 'code', default='')
            timing_code = dig(receta, 'dosageInstruction', 0, 'timing', 'code', 'coding', 0, 'code', default='')
            dose_value = dig(receta, 'dosageInstruction', 0, 'doseAndRate', 0, 'doseQuantity', 'value')
            dose_unit = dig(receta, 'dosageInstruction', 0, 'doseAndRate', 0, 'doseQuantity', 'unit', default='')

            # --- FILA PLANA (MAESTRA) ---
            fila_aplanada = {
                'IdMedicationRequest': req_id,
                'authoredOn': receta.get('authoredOn'),
                'requester_id': requester_id,
                'fue_administrado': fue_administrado, # NUEVA VARIABLE CLAVE
                
                'encounter_id': encounter_id,
                'encounter_class': datos_encounter['encounter_class'],
                'encounter_start': datos_encounter['encounter_start'],
                'encounter_end': datos_encounter['encounter_end'],
                'encounter_diagnoses': diags_texto, # AHORA CON CÓDIGOS ICD
                'encounter_procedures': procs_texto,

                'patient_id': patient_id,
                'patient_gender': datos_paciente['patient_gender'],
                'patient_birthdate': datos_paciente['patient_birthdate'],
                
                'medication_id': medication_id,
                'medication_name': medication_name, # Usamos la variable ya resuelta
                'route_code': route_code,
                'timing_code': timing_code,
                'dose_value': dose_value,
                'dose_unit': dose_unit,
                'dosage_text': dosage_text
            }
            
            # orjson exporta en bytes, le añadimos el salto de línea en bytes (b'\n')
            f_out.write(orjson.dumps(fila_aplanada) + b'\n')
            
    print(f"✅ Procesamiento finalizado.")

# ==========================================
# 5. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # Diccionario para las métricas
    stats = defaultdict(int)
    
    # 1. Cargar todas las dimensiones
    pacientes = cargar_pacientes(PATIENT_FILE, stats)
    diagnosticos = cargar_diagnosticos(CONDITION_FILES, stats)
    procedimientos = cargar_procedimientos(PROCEDURE_FILES, stats)
    medicamentos = cargar_medicamentos(MED_FILE, stats)
    encounters = cargar_encounters(ENCOUNTER_FILES, stats)
    administraciones = cargar_administraciones(ADMIN_FILE, stats)
    
    # 2. Iniciar el cruce maestro
    procesar_recetas(MED_REQUEST_FILE, OUTPUT_FILE, pacientes, diagnosticos, procedimientos, medicamentos, encounters, administraciones, stats)
    
    # 3. Imprimir el Panel de Control
    print("\n" + "="*40)
    print("📊 REPORTE DE CALIDAD DE DATOS (ETL)")
    print("="*40)
    print(f"Recetas procesadas:     {stats['total_recetas_procesadas']}")
    print(f"Fallos de JSON:         {stats.get('json_errors', 0)}")
    print(f"Cruces fallidos (Pacientes):    {stats['miss_patient']}")
    print(f"Cruces fallidos (Ingresos):     {stats['miss_encounter']}")
    print(f"Cruces fallidos (Medicamentos): {stats['miss_medication']}")
    print("="*40)