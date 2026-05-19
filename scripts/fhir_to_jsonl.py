import os
import json

def fhir_bundles_to_jsonl(data_dir, output_file):
    print(f"🚀 Iniciando procesamiento de archivos FHIR (con diagnóstico) en: {data_dir}")
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        total_med_requests = 0
        
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        if not files:
            print("⚠️ No se encontraron archivos .json.")
            return
            
        for file_name in files:
            file_path = os.path.join(data_dir, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as f_in:
                try:
                    bundle = json.load(f_in)
                except json.JSONDecodeError:
                    continue
            
            # 1. ALMACÉN INDEXADO: Añadimos 'conditions' a la memoria temporal
            patients = {}
            practitioners = {}
            encounters = {}
            conditions = {}  # <- NUEVO: Almacén para diagnósticos
            claims_by_prescription = {}
            medication_requests_list = []
            
            entries = bundle.get("entry", [])
            for entry in entries:
                resource = entry.get("resource", {})
                r_type = resource.get("resourceType")
                r_id = resource.get("id")
                
                if not r_type or not r_id:
                    continue
                    
                if r_type == "Patient":
                    patients[r_id] = resource
                elif r_type == "Practitioner":
                    practitioners[r_id] = resource
                elif r_type == "Encounter":
                    encounters[r_id] = resource
                elif r_type == "Condition":
                    conditions[r_id] = resource  # <- NUEVO: Guardamos la enfermedad
                elif r_type == "MedicationRequest":
                    medication_requests_list.append(resource)
                elif r_type == "Claim":
                    presc_ref = resource.get("prescription", {}).get("reference", "")
                    if "urn:uuid:" in presc_ref:
                        presc_id = presc_ref.replace("urn:uuid:", "")
                        claims_by_prescription[presc_id] = resource

            # 2. CONSTRUCTOR DE LÍNEAS
            for med_req in medication_requests_list:
                line_data = {}
                med_req_id = med_req.get("id")
                
                # Datos base de la receta
                line_data["IdMedicationRequest"] = med_req_id
                line_data["status"] = med_req.get("status")
                line_data["intent"] = med_req.get("intent")
                line_data["authoredOn"] = med_req.get("authoredOn")
                
                coding = med_req.get("medicationCodeableConcept", {}).get("coding", [{}])[0]
                line_data["medication_code"] = coding.get("code")
                line_data["medication_display"] = coding.get("display")
                
                dosage = med_req.get("dosageInstruction", [{}])[0]
                timing_repeat = dosage.get("timing", {}).get("repeat", {})
                line_data["dosage_frequency"] = timing_repeat.get("frequency")
                line_data["dosage_period"] = timing_repeat.get("period")
                line_data["dosage_unit"] = timing_repeat.get("periodUnit")
                line_data["dosage_value"] = dosage.get("doseAndRate", [{}])[0].get("doseQuantity", {}).get("value")
                
                # --- NUEVO: Búsqueda Recursiva de la Condición / Diagnóstico ---
                reason_references = med_req.get("reasonReference", [])
                condition_id = None
                condition_code = None
                condition_display = None
                
                if reason_references:
                    # Tomamos la primera referencia médica que justifique la receta
                    cond_ref = reason_references[0].get("reference", "")
                    condition_id = cond_ref.replace("urn:uuid:", "")
                    condition_res = conditions.get(condition_id, {})
                    
                    if condition_res:
                        cond_coding = condition_res.get("code", {}).get("coding", [{}])[0]
                        condition_code = cond_coding.get("code")
                        condition_display = cond_coding.get("display")
                
                line_data["condition_id"] = condition_id
                line_data["condition_code"] = condition_code
                line_data["condition_display"] = condition_display
                
                # Relaciones con Paciente, Médico y Encuentros
                sub_ref = med_req.get("subject", {}).get("reference", "")
                pat_id = sub_ref.replace("urn:uuid:", "")
                patient = patients.get(pat_id, {})
                line_data["patient_id"] = pat_id
                if patient:
                    name_dict = patient.get("name", [{}])[0]
                    line_data["patient_name"] = f"{" ".join(name_dict.get('given', []))} {name_dict.get('family', '')}".strip()
                    line_data["patient_gender"] = patient.get("gender")
                    line_data["patient_birthdate"] = patient.get("birthDate")
                
                req_ref = med_req.get("requester", {}).get("reference", "")
                line_data["practitioner_id"] = req_ref.split("|")[-1] if "|" in req_ref else req_ref.replace("Practitioner/", "")
                line_data["practitioner_name"] = med_req.get("requester", {}).get("display")

                enc_ref = med_req.get("encounter", {}).get("reference", "")
                enc_id = enc_ref.replace("urn:uuid:", "")
                encounter = encounters.get(enc_id, {})
                line_data["encounter_id"] = enc_id
                if encounter:
                    line_data["encounter_status"] = encounter.get("status")
                    line_data["encounter_type"] = encounter.get("type", [{}])[0].get("coding", [{}])[0].get("display")

                # Relación con Claims
                claim = claims_by_prescription.get(med_req_id, {})
                if claim:
                    line_data["has_claim"] = True
                    line_data["claim_id"] = claim.get("id")
                    line_data["claim_total_value"] = claim.get("total", {}).get("value")
                    line_data["claim_currency"] = claim.get("total", {}).get("currency")
                    line_data["claim_insurance"] = claim.get("insurance", [{}])[0].get("coverage", {}).get("display")
                else:
                    line_data["has_claim"] = False

                f_out.write(json.dumps(line_data, ensure_ascii=False) + "\n")
                total_med_requests += 1

        print(f"✨ ¡Hecho! {total_med_requests} registros con diagnósticos en {output_file}")

if __name__ == "__main__":
    fhir_bundles_to_jsonl("./data", "./docs/medication_requests_dataset.jsonl")