import json
import gzip
import os

# ==========================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================
DATA_DIR = 'data'
OUTPUT_FILE = os.path.join(DATA_DIR, 'medication_request_dataset_full.jsonl')

# Archivos Demográficos y Clínicos
PATIENT_FILE = os.path.join(DATA_DIR, 'MimicPatient.ndjson.gz')
CONDITION_FILE = os.path.join(DATA_DIR, 'MimicCondition.ndjson.gz')
MED_FILE = os.path.join(DATA_DIR, 'MimicMedication.ndjson.gz')
ENCOUNTER_FILE = os.path.join(DATA_DIR, 'MimicEncounter.ndjson.gz')
ENCOUNTER_ED_FILE = os.path.join(DATA_DIR, 'MimicEncounterED.ndjson.gz')

# Archivo Base (Tabla de Hechos)
MED_REQUEST_FILE = os.path.join(DATA_DIR, 'MimicMedicationRequest.ndjson.gz')

# ==========================================
# 2. FUNCIONES DE CARGA (DICCIONARIOS EN RAM)
# ==========================================
def cargar_pacientes(filepath):
    print(f"⏳ Cargando pacientes...")
    diccionario = {}
    if not os.path.exists(filepath): return diccionario
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            paciente = json.loads(line)
            diccionario[paciente.get('id')] = {
                'patient_gender': paciente.get('gender', 'unknown'),
                'patient_birthdate': paciente.get('birthDate', 'unknown')
            }
    return diccionario

def cargar_diagnosticos(filepath):
    print(f"⏳ Cargando diagnósticos...")
    diccionario = {}
    if not os.path.exists(filepath): return diccionario
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            cond = json.loads(line)
            enc_ref = cond.get('encounter', {}).get('reference', '')
            enc_id = enc_ref.split('/')[-1] if '/' in enc_ref else 'unknown'
            codings = cond.get('code', {}).get('coding', [])
            diag_text = codings[0].get('display', 'unknown') if codings else 'unknown'
            
            if enc_id not in diccionario:
                diccionario[enc_id] = diag_text
            elif diag_text not in diccionario[enc_id]:
                diccionario[enc_id] += f" | {diag_text}"
    return diccionario

def cargar_medicamentos(filepath):
    print(f"⏳ Cargando catálogo de medicamentos...")
    diccionario = {}
    if not os.path.exists(filepath): 
        print(f"⚠ No se encontró el archivo {filepath}")
        return diccionario
        
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            med = json.loads(line)
            med_id = med.get('id')
            
            med_name = "unknown"
            
            # Buscamos en la lista de identificadores (donde MIMIC-IV guarda el nombre real)
            identifiers = med.get('identifier', [])
            for ident in identifiers:
                sistema = ident.get('system', '')
                if 'mimic-medication-name' in sistema:
                    med_name = ident.get('value', 'unknown')
                    break # Encontrado, dejamos de buscar
            
            # Fallback de seguridad (por si algún registro antiguo sí usa el estándar FHIR)
            if med_name == "unknown":
                code_obj = med.get('code', {})
                if 'text' in code_obj:
                    med_name = code_obj.get('text')
                        
            diccionario[med_id] = med_name
            
    print(f"✅ {len(diccionario)} medicamentos cargados en el catálogo.")
    return diccionario

def cargar_encounters(filepaths):
    print(f"⏳ Cargando ingresos hospitalarios (Planta y Urgencias)...")
    diccionario = {}
    for filepath in filepaths:
        if not os.path.exists(filepath): continue
        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                enc = json.loads(line)
                enc_id = enc.get('id')
                enc_class = enc.get('class', {}).get('code', 'unknown') # IMP (Inpatient), EMER (Emergency), etc.
                period_start = enc.get('period', {}).get('start', '')
                period_end = enc.get('period', {}).get('end', '')
                diccionario[enc_id] = {
                    'encounter_class': enc_class,
                    'encounter_start': period_start,
                    'encounter_end': period_end
                }
    return diccionario

# ==========================================
# 3. PROCESAMIENTO MAESTRO (ETL)
# ==========================================
def procesar_recetas(med_req_filepath, output_filepath, pacientes, diagnosticos, medicamentos, encounters):
    print(f"🚀 Cruzando todos los datos para generar el dataset maestro...")
    
    if not os.path.exists(med_req_filepath):
        print(f"❌ Error: No se encuentra {med_req_filepath}")
        return

    with gzip.open(med_req_filepath, 'rt', encoding='utf-8') as f_in, \
         open(output_filepath, 'w', encoding='utf-8') as f_out:
        
        contador = 0
        for line in f_in:
            if not line.strip(): continue
            receta = json.loads(line)
            
            # --- REFERENCIAS (IDs) ---
            patient_id = receta.get('subject', {}).get('reference', '').split('/')[-1]
            encounter_id = receta.get('encounter', {}).get('reference', '').split('/')[-1]
            medication_id = receta.get('medicationReference', {}).get('reference', '').split('/')[-1]
            requester_id = receta.get('requester', {}).get('reference', '').split('/')[-1]
            
            # --- JOINS (CRUCES EN RAM) ---
            datos_paciente = pacientes.get(patient_id, {'patient_gender': 'unknown', 'patient_birthdate': 'unknown'})
            datos_encounter = encounters.get(encounter_id, {'encounter_class': 'unknown', 'encounter_start': '', 'encounter_end': ''})
            diagnosticos_ingreso = diagnosticos.get(encounter_id, 'No diagnosis recorded')
            med_name = medicamentos.get(medication_id, 'unknown')
            
            # --- EXTRACCIÓN DE DOSIS ---
            dosage_text, route_code, timing_code, dose_value, dose_unit = "", "", "", None, ""
            dosage_instructions = receta.get('dosageInstruction', [])
            if dosage_instructions:
                first_dosage = dosage_instructions[0]
                dosage_text = first_dosage.get('text', '')
                route_code = first_dosage.get('route', {}).get('coding', [{}])[0].get('code', '') if first_dosage.get('route', {}).get('coding') else ''
                timing_code = first_dosage.get('timing', {}).get('code', {}).get('coding', [{}])[0].get('code', '') if first_dosage.get('timing', {}).get('code', {}).get('coding') else ''
                dose_and_rate = first_dosage.get('doseAndRate', [])
                if dose_and_rate:
                    dose_qty = dose_and_rate[0].get('doseQuantity', {})
                    dose_value = dose_qty.get('value')
                    dose_unit = dose_qty.get('unit', '')

            # --- FILA PLANA (MAESTRA) ---
            fila_aplanada = {
                # 1. Identificadores Base
                'IdMedicationRequest': receta.get('id'),
                'authoredOn': receta.get('authoredOn'),
                'requester_id': requester_id,
                
                # 2. Contexto del Ingreso Hospitalario
                'encounter_id': encounter_id,
                'encounter_class': datos_encounter['encounter_class'],
                'encounter_start': datos_encounter['encounter_start'],
                'encounter_end': datos_encounter['encounter_end'],
                'encounter_diagnoses': diagnosticos_ingreso,
                
                # 3. Paciente
                'patient_id': patient_id,
                'patient_gender': datos_paciente['patient_gender'],
                'patient_birthdate': datos_paciente['patient_birthdate'],
                
                # 4. Medicación y Dosis
                'medication_id': medication_id,
                'medication_name': med_name,
                'route_code': route_code,
                'timing_code': timing_code,
                'dose_value': dose_value,
                'dose_unit': dose_unit,
                'dosage_text': dosage_text
            }
            
            f_out.write(json.dumps(fila_aplanada) + '\n')
            contador += 1
            
    print(f"✅ ¡Éxito! Se ha generado la tabla maestra con {contador} registros cruzados.")

# ==========================================
# 4. EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    pacientes = cargar_pacientes(PATIENT_FILE)
    diagnosticos = cargar_diagnosticos(CONDITION_FILE)
    medicamentos = cargar_medicamentos(MED_FILE)
    encounters = cargar_encounters([ENCOUNTER_FILE, ENCOUNTER_ED_FILE])
    
    procesar_recetas(MED_REQUEST_FILE, OUTPUT_FILE, pacientes, diagnosticos, medicamentos, encounters)