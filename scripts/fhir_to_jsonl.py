import gzip
import os
import json
import orjson
import pandas as pd
from collections import defaultdict

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS (RAÍZ DEL PEN DRIVE - ARCHIVOS PLANOS)
# ==========================================
LETRA_PEN = "D:/"

DATA_DIR = 'data'
OUTPUT_FILE = os.path.join('data_procesada', 'medication_request_dataset_full2.jsonl')

# Todos los archivos como .ndjson plano ubicados directamente en la raíz de D:/
PATIENT_FILE = os.path.join(LETRA_PEN, 'MimicPatient.ndjson')
CONDITION_FILES = [
    os.path.join(LETRA_PEN, 'MimicCondition.ndjson'), 
    os.path.join(LETRA_PEN, 'MimicConditionED.ndjson')
]
MED_FILE = os.path.join(LETRA_PEN, 'MimicMedication.ndjson')
ENCOUNTER_FILES = [
    os.path.join(LETRA_PEN, 'MimicEncounter.ndjson'), 
    os.path.join(LETRA_PEN, 'MimicEncounterED.ndjson')
]
ADMIN_FILE = os.path.join(LETRA_PEN, 'MimicMedicationAdministration.ndjson')
MED_REQUEST_FILE = os.path.join(DATA_DIR, 'MimicMedicationRequest.ndjson')
PROCEDURE_FILES = [os.path.join(LETRA_PEN, 'MimicProcedure.ndjson')]

# ==========================================
# 2. HERRAMIENTAS BASE (MOTOR TURBO PARA .ndjson PLANOS)
# ==========================================
def iter_ndjson(path, stats):
    """Lee archivos .ndjson planos con tolerancia a errores."""
    if not os.path.exists(path):
        print(f"⚠️ Aviso: No se encontró {path}")
        return
    
    with open(path, 'rt', encoding='utf-8', errors='ignore') as f:
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
    print(f"⏳ Cargando pacientes desde D:/...")
    diccionario = {}
    for paciente in iter_ndjson(filepath, stats):
        diccionario[paciente.get('id')] = {
            'patient_gender': paciente.get('gender', 'unknown'),
            'patient_birthdate': paciente.get('birthDate', 'unknown')
        }
    return diccionario

def cargar_diagnosticos(filepaths, stats):
    print(f"⏳ Cargando diagnósticos (Alta y Urgencias) desde D:/...")
    por_enc = defaultdict(dict)
    for filepath in filepaths:
        for cond in iter_ndjson(filepath, stats):
            enc_ref = dig(cond, 'encounter', 'reference', default='')
            enc_id = enc_ref.rsplit('/', 1)[-1] if '/' in enc_ref else ''
            
            cod = dig(cond, 'code', 'coding', 0, 'code', default='UNKNOWN')
            txt = dig(cond, 'code', 'coding', 0, 'display', default='No description')
            
            if enc_id:
                por_enc[enc_id][cod] = txt
    return por_enc

def cargar_medicamentos(filepath, stats):
    print(f"⏳ Cargando catálogo de medicamentos desde D:/...")
    diccionario = {}
    for med in iter_ndjson(filepath, stats):
        med_id = med.get('id')
        med_name = "unknown"
        
        identifiers = med.get('identifier', [])
        for ident in identifiers:
            if 'mimic-medication-name' in ident.get('system', ''):
                med_name = ident.get('value', 'unknown')
                break
                
        if med_name == "unknown":
            med_name = dig(med, 'code', 'text', default="unknown")
            
        diccionario[med_id] = med_name
    return diccionario

def cargar_encounters(filepaths, stats):
    print(f"⏳ Cargando ingresos hospitalarios desde D:/...")
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
    print(f"⏳ Cargando registros de administración desde D:/...")
    administradas = set()
    for admin in iter_ndjson(filepath, stats):
        req_ref = dig(admin, 'request', 'reference', default='')
        req_id = req_ref.rsplit('/', 1)[-1] if '/' in req_ref else ''
        if req_id:
            administradas.add(req_id)
    return administradas

def cargar_procedimientos(filepaths, stats):
    print(f"⏳ Cargando procedimientos y quirófanos desde D:/...")
    por_enc = defaultdict(dict)
    contador_leidos = 0
    contador_mapeados = 0
    
    for filepath in filepaths:
        for proc in iter_ndjson(filepath, stats):
            contador_leidos += 1
            enc_ref = dig(proc, 'encounter', 'reference', default='')
            if not enc_ref:
                enc_ref = proc.get('encounter', '')
                if isinstance(enc_ref, dict):
                    enc_ref = enc_ref.get('reference', '')
            
            enc_id = enc_ref.rsplit('/', 1)[-1] if '/' in enc_ref else str(enc_ref)
            cod = dig(proc, 'code', 'coding', 0, 'code', default='UNKNOWN')
            txt = dig(proc, 'code', 'coding', 0, 'display', default='No description')
            
            if enc_id and enc_id != '':
                por_enc[enc_id][cod] = txt
                contador_mapeados += 1

    print(f"🔍 [DEBUG] Procedimientos leídos: {contador_leidos} | Mapeados correctamente: {contador_mapeados}")
    return por_enc

# ==========================================
# 4. PROCESAMIENTO MAESTRO (ETL)
# ==========================================
def procesar_etl_completo():
    ruta_csv = os.path.join(DATA_DIR, 'prescriptions.csv.gz')
    print("⏳ Cargando el mapa de médicos desde local...")
    
    if not os.path.exists(ruta_csv):
        print(f"❌ No se encuentra el archivo CSV en {ruta_csv}")
        return
        
    df = pd.read_csv(ruta_csv, usecols=['pharmacy_id', 'order_provider_id'], dtype=str)
    mapa_medicos = pd.Series(df.order_provider_id.values, index=df.pharmacy_id.astype(str)).to_dict()
    print(f"✅ Mapa de médicos cargado: {len(mapa_medicos)} registros indexados.")

    os.makedirs('data_procesada', exist_ok=True)
    
    if not os.path.exists(MED_REQUEST_FILE):
        print(f"❌ No se encuentra el archivo principal en la raíz de {MED_REQUEST_FILE}")
        return

    stats = defaultdict(int)
    
    pacientes = cargar_pacientes(PATIENT_FILE, stats)
    diagnosticos = cargar_diagnosticos(CONDITION_FILES, stats)
    procedimientos = cargar_procedimientos(PROCEDURE_FILES, stats)
    medicamentos = cargar_medicamentos(MED_FILE, stats)
    encounters = cargar_encounters(ENCOUNTER_FILES, stats)
    administraciones = cargar_administraciones(ADMIN_FILE, stats)

    print(f"🚀 Iniciando ETL completo leyendo desde la raíz de D:/...")
    
    contador_exito = 0
    contador_total = 0
    
    # Usamos un bloque try-except general y lectura segura por líneas con límite o buffer
    with open(MED_REQUEST_FILE, 'rt', encoding='utf-8', errors='ignore') as f_in, \
         open(OUTPUT_FILE, 'wb') as f_out:
        
        for linea in f_in:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            
            try:
                receta = json.loads(linea_limpia)
            except (json.JSONDecodeError, MemoryError):
                stats['json_errors'] += 1
                continue
                
            contador_total += 1
            stats['total_recetas_procesadas'] += 1
            
            req_id = receta.get('id')
            patient_id = dig(receta, 'subject', 'reference', default='').rsplit('/', 1)[-1]
            encounter_id = dig(receta, 'encounter', 'reference', default='').rsplit('/', 1)[-1]
            
            pharmacy_id = None
            for ident in receta.get('identifier', []):
                val = str(ident.get('value', ''))
                if val:
                    pharmacy_id = val
                    break
            
            requester_id = mapa_medicos.get(pharmacy_id, None)
            if requester_id:
                contador_exito += 1
            
            medication_id = dig(receta, 'medicationReference', 'reference', default='').rsplit('/', 1)[-1]
            medication_name = medicamentos.get(medication_id, 'unknown') if medication_id else 'unknown'
            
            if medication_name == 'unknown':
                concept_text = dig(receta, 'medicationCodeableConcept', 'text')
                if concept_text:
                    medication_name = concept_text
                else:
                    concept_display = dig(receta, 'medicationCodeableConcept', 'coding', 0, 'display')
                    concept_code = dig(receta, 'medicationCodeableConcept', 'coding', 0, 'code')
                    if concept_display: medication_name = concept_display
                    elif concept_code: medication_name = concept_code

            if medication_name == 'unknown':
                texto_dosis = dig(receta, 'dosageInstruction', 0, 'text', default='')
                route = dig(receta, 'dosageInstruction', 0, 'route', 'coding', 0, 'code', default='')
                if texto_dosis and (route == 'IV' or any(term in texto_dosis.lower() for term in ['bag', 'bottle', 'premix', 'soln', 'iv', 'infusion'])):
                    medication_name = f"IV Fluid / Mix: {texto_dosis}"
                else:
                    medication_name = f"Unknown Oral/Other: {texto_dosis}" if texto_dosis else "unknown"

            if patient_id not in pacientes: stats['miss_patient'] += 1
            if encounter_id not in encounters: stats['miss_encounter'] += 1
            if medication_name == 'unknown': stats['miss_medication'] += 1
            
            datos_paciente = pacientes.get(patient_id, {'patient_gender': 'unknown', 'patient_birthdate': 'unknown'})
            datos_encounter = encounters.get(encounter_id, {'encounter_class': 'unknown', 'encounter_start': '', 'encounter_end': ''})
            
            dict_diags = diagnosticos.get(encounter_id, {})
            diags_texto = " | ".join([f"{cod}: {txt}" for cod, txt in dict_diags.items()]) if dict_diags else "No diagnosis recorded"

            dict_procs = procedimientos.get(encounter_id, {})
            procs_texto = " | ".join([f"{cod}: {txt}" for cod, txt in dict_procs.items()]) if dict_procs else "No procedure recorded"

            fue_administrado = req_id in administraciones
            
            dosage_text = dig(receta, 'dosageInstruction', 0, 'text', default='')
            route_code = dig(receta, 'dosageInstruction', 0, 'route', 'coding', 0, 'code', default='')
            timing_code = dig(receta, 'dosageInstruction', 0, 'timing', 'code', 'coding', 0, 'code', default='')
            dose_value = dig(receta, 'dosageInstruction', 0, 'doseAndRate', 0, 'doseQuantity', 'value')
            dose_unit = dig(receta, 'dosageInstruction', 0, 'doseAndRate', 0, 'doseQuantity', 'unit', default='')

            fila_aplanada = {
                'IdMedicationRequest': req_id,
                'authoredOn': receta.get('authoredOn'),
                'pharmacy_id': pharmacy_id,
                'order_provider_id': requester_id,
                'fue_administrado': fue_administrado,
                
                'encounter_id': encounter_id,
                'encounter_class': datos_encounter['encounter_class'],
                'encounter_start': datos_encounter['encounter_start'],
                'encounter_end': datos_encounter['encounter_end'],
                'encounter_diagnoses': diags_texto,
                'encounter_procedures': procs_texto,

                'patient_id': patient_id,
                'patient_gender': datos_paciente['patient_gender'],
                'patient_birthdate': datos_paciente['patient_birthdate'],
                
                'medication_id': medication_id,
                'medication_name': medication_name,
                'route_code': route_code,
                'timing_code': timing_code,
                'dose_value': dose_value,
                'dose_unit': dose_unit,
                'dosage_text': dosage_text
            }
            
            f_out.write(orjson.dumps(fila_aplanada) + b'\n')
            
            if contador_total % 500000 == 0:
                print(f"   Procesadas {contador_total} recetas...")

    print(f"\n🎉 ¡ETL completado con éxito desde D:/!")
    print(f"  - Total de recetas procesadas: {contador_total}")
    print(f"  - Con médico vinculado correctamente: {contador_exito}")
    print(f"  - Archivo final guardado en local: {OUTPUT_FILE}")

    print("\n" + "="*40)
    print("📊 REPORTE DE CALIDAD DE DATOS (ETL)")
    print("="*40)
    print(f"Recetas procesadas:     {stats['total_recetas_procesadas']}")
    print(f"Fallos de JSON:         {stats.get('json_errors', 0)}")
    print(f"Cruces fallidos (Pacientes):    {stats['miss_patient']}")
    print(f"Cruces fallidos (Ingresos):     {stats['miss_encounter']}")
    print(f"Cruces fallidos (Medicamentos): {stats['miss_medication']}")
    print("="*40)

# ==========================================
# 5. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    procesar_etl_completo()