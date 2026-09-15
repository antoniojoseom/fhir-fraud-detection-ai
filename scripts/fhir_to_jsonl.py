import os
import json

def fhir_bundles_to_jsonl(data_dir, output_file):
    print(f"🚀 Iniciando procesamiento EXHAUSTIVO de archivos FHIR en: {data_dir}")
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        total_med_requests = 0
        
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        if not files:
            print("⚠️ No se encontraron archivos .json en el directorio.")
            return
            
        for file_name in files:
            file_path = os.path.join(data_dir, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as f_in:
                try:
                    bundle = json.load(f_in)
                except json.JSONDecodeError:
                    continue
            
            # 1. INDEXACIÓN EN MEMORIA (Almacenes temporales)
            patients = {}
            practitioners = {}
            encounters = {}
            conditions = {}
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
                    conditions[r_id] = resource
                elif r_type == "MedicationRequest":
                    medication_requests_list.append(resource)
                elif r_type == "Claim":
                    presc_ref = resource.get("prescription", {}).get("reference", "")
                    if "urn:uuid:" in presc_ref:
                        presc_id = presc_ref.replace("urn:uuid:", "")
                        claims_by_prescription[presc_id] = resource

            # 2. CONSTRUCCIÓN DE LA LÍNEA APLANADA
            for med_req in medication_requests_list:
                line_data = {}
                med_req_id = med_req.get("id")
                
                # --- A. DATOS DEL MEDICATIONREQUEST ---
                line_data["IdMedicationRequest"] = med_req_id
                line_data["status"] = med_req.get("status")
                line_data["intent"] = med_req.get("intent")
                line_data["authoredOn"] = med_req.get("authoredOn")
                
                # Medicamento
                coding = med_req.get("medicationCodeableConcept", {}).get("coding", [{}])[0]
                line_data["medication_code"] = coding.get("code")
                line_data["medication_display"] = coding.get("display")
                line_data["medication_text"] = med_req.get("medicationCodeableConcept", {}).get("text")
                
                # Posología / Dosis
                dosage = med_req.get("dosageInstruction", [{}])[0]
                timing_repeat = dosage.get("timing", {}).get("repeat", {})
                line_data["dosage_frequency"] = timing_repeat.get("frequency")
                line_data["dosage_period"] = timing_repeat.get("period")
                line_data["dosage_unit"] = timing_repeat.get("periodUnit")
                line_data["dosage_as_needed"] = dosage.get("asNeededBoolean")
                
                dose_quantity = dosage.get("doseAndRate", [{}])[0].get("doseQuantity", {})
                line_data["dosage_value"] = dose_quantity.get("value")
                line_data["dosage_value_unit"] = dose_quantity.get("unit")

                # --- B. DATOS DEL ENCOUNTER ---
                enc_ref = med_req.get("encounter", {}).get("reference", "")
                enc_id = enc_ref.replace("urn:uuid:", "")
                encounter = encounters.get(enc_id, {})
                
                line_data["encounter_id"] = enc_id
                if encounter:
                    line_data["encounter_status"] = encounter.get("status")
                    line_data["encounter_class"] = encounter.get("class", {}).get("code")
                    
                    # MARCAS DE TIEMPO (start y end) Solicitadas explícitamente por el profesor
                    enc_period = encounter.get("period", {})
                    enc_start = enc_period.get("start")
                    enc_end = enc_period.get("end")

                    line_data["encounter_start"] = enc_start
                    line_data["encounter_end"] = enc_end

                    # --- NUEVO: Cálculo del Flag Booleano ---
                    authored_on = med_req.get("authoredOn")
                    if authored_on and enc_start and enc_end:
                        # Al ser cadenas ISO 8601 (YYYY-MM-DDTHH:MM:SS), se pueden comparar lexicográficamente
                        line_data["is_valid_time_window"] = (enc_start <= authored_on <= enc_end)
                    else:
                        line_data["is_valid_time_window"] = None
                    
                    enc_type_coding = encounter.get("type", [{}])[0].get("coding", [{}])[0]
                    line_data["encounter_type_code"] = enc_type_coding.get("code")
                    line_data["encounter_type_display"] = enc_type_coding.get("display")             
                    line_data["encounter_provider"] = encounter.get("serviceProvider", {}).get("display")
                    line_data["encounter_location"] = encounter.get("location", [{}])[0].get("location", {}).get("display")
                else:
                    line_data["encounter_start"] = None
                    line_data["encounter_end"] = None
                    line_data["is_valid_time_window"] = None

                # --- C. DATOS DEL PATIENT ---
                sub_ref = med_req.get("subject", {}).get("reference", "")
                pat_id = sub_ref.replace("urn:uuid:", "")
                patient = patients.get(pat_id, {})
                
                line_data["patient_id"] = pat_id
                if patient:
                    name_dict = patient.get("name", [{}])[0]
                    given = " ".join(name_dict.get("given", []))
                    family = name_dict.get("family", "")
                    line_data["patient_name"] = f"{given} {family}".strip()
                    line_data["patient_gender"] = patient.get("gender")
                    line_data["patient_birthdate"] = patient.get("birthDate")
                    line_data["patient_deceased_datetime"] = patient.get("deceasedDateTime")
                    line_data["patient_marital_status"] = patient.get("maritalStatus", {}).get("text")
                    
                    addr = patient.get("address", [{}])[0]
                    line_data["patient_city"] = addr.get("city")
                    line_data["patient_state"] = addr.get("state")
                else:
                    line_data["patient_name"] = med_req.get("subject", {}).get("display")

                # --- D. DATOS DEL PRACTITIONER (MÉDICO) ---
                req_ref = med_req.get("requester", {}).get("reference", "")
                pract_id = req_ref.split("|")[-1] if "|" in req_ref else req_ref.replace("Practitioner/", "")
                practitioner = practitioners.get(pract_id, {})
                
                line_data["practitioner_id"] = pract_id
                line_data["practitioner_name"] = med_req.get("requester", {}).get("display")
                if practitioner:
                    pract_name = practitioner.get("name", [{}])[0]
                    p_given = " ".join(pract_name.get("given", []))
                    p_family = pract_name.get("family", "")
                    line_data["practitioner_full_name"] = f"{p_given} {p_family}".strip()
                    line_data["practitioner_gender"] = practitioner.get("gender")

                # --- E. DATOS DE LA CONDITION (DIAGNÓSTICO) ---
                reason_references = med_req.get("reasonReference", [])
                condition_id, condition_code, condition_display, condition_onset = None, None, None, None
                
                if reason_references:
                    cond_ref = reason_references[0].get("reference", "")
                    condition_id = cond_ref.replace("urn:uuid:", "")
                    condition_res = conditions.get(condition_id, {})
                    
                    if condition_res:
                        cond_coding = condition_res.get("code", {}).get("coding", [{}])[0]
                        condition_code = cond_coding.get("code")
                        condition_display = cond_coding.get("display")
                        condition_onset = condition_res.get("onsetDateTime")
                
                line_data["condition_id"] = condition_id
                line_data["condition_code"] = condition_code
                line_data["condition_display"] = condition_display
                line_data["condition_onset"] = condition_onset

                # --- F. DATOS DEL CLAIM (FACTURA / SEGURO) ---
                claim = claims_by_prescription.get(med_req_id, {})
                if claim:
                    line_data["has_claim"] = True
                    line_data["claim_id"] = claim.get("id")
                    line_data["claim_status"] = claim.get("status")
                    line_data["claim_use"] = claim.get("use")
                    line_data["claim_total_value"] = claim.get("total", {}).get("value")
                    line_data["claim_currency"] = claim.get("total", {}).get("currency")
                    
                    bill_period = claim.get("billablePeriod", {})
                    line_data["claim_billable_start"] = bill_period.get("start")
                    line_data["claim_billable_end"] = bill_period.get("end")
                    line_data["claim_insurance"] = claim.get("insurance", [{}])[0].get("coverage", {}).get("display")
                else:
                    line_data["has_claim"] = False

                # ESCRITURA DE LA LÍNEA
                f_out.write(json.dumps(line_data, ensure_ascii=False) + "\n")
                total_med_requests += 1

        print(f"✨ ¡Dataset actualizado! Se han procesado {total_med_requests} registros con TODOS los atributos.")

if __name__ == "__main__":
    fhir_bundles_to_jsonl("./data", "./docs/medication_request_dataset.jsonl")
    # Generar muestra de 100 líneas
    with open("./docs/medication_request_dataset.jsonl", "r", encoding="utf-8") as f_in, \
         open("./docs/medication_request_samples.jsonl", "w", encoding="utf-8") as f_out:
        for i in range(100):
            line = f_in.readline()
            if not line:
                break
            f_out.write(line)
    print("📝 Muestra de 100 líneas actualizada en docs/medication_request_samples.jsonl")