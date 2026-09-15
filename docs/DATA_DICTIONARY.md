# 📖 Diccionario de Datos (`medication_request_dataset.jsonl`)

Este documento describe la estructura y semántica de los campos aplanados a partir de los recursos HL7 FHIR en el dataset `medication_request_dataset.jsonl`.

## 💊 Receta Médica (`MedicationRequest`)
* **`IdMedicationRequest`**: Identificador único de la prescripción.
* **`status`**: Estado de la receta (`active`, `completed`, `stopped`).
* **`intent`**: Intención clínica (`order`, `plan`).
* **`authoredOn`**: Fecha y hora exacta de la prescripción.
* **`medication_code`**: Código del fármaco (sistema RxNorm / SNOMED).
* **`medication_display`**: Nombre y concentración del medicamento.
* **`dosage_frequency`**: Frecuencia de la toma.
* **`dosage_period`**: Periodo de la frecuencia (ej. cada 1.0 días).
* **`dosage_unit`**: Unidad del periodo (`d` = días, `h` = horas).
* **`dosage_value`**: Cantidad o dosis administrada.

## 🏥 Consulta Médica (`Encounter`)
* **`encounter_id`**: Identificador de la visita médica.
* **`encounter_status`**: Estado de la consulta (`finished`, `arrived`).
* **`encounter_class`**: Tipo de atención (`AMB` = Ambulatoria, `IMP` = Hospitalización).
* **`encounter_start`**: Timestamp de inicio de la consulta.
* **`encounter_end`**: Timestamp de fin de la consulta.
* **`is_valid_time_window`**: **[FLAG AUDITORÍA]** `True` si `authoredOn` está entre `encounter_start` y `encounter_end`.
* **`encounter_type_display`**: Motivo o procedimiento del encuentro.
* **`encounter_provider`**: Organización / centro sanitario.

## 👤 Paciente (`Patient`)
* **`patient_id`**: Identificador del paciente.
* **`patient_name`**: Nombre completo.
* **`patient_gender`**: Género del paciente.
* **`patient_birthdate`**: Fecha de nacimiento.
* **`patient_deceased_datetime`**: Fecha de defunción (si aplica).
* **`patient_city` / `patient_state`**: Ubicación de residencia.

## 👨‍⚕️ Prescriptor (`Practitioner`)
* **`practitioner_id`**: Identificador del profesional sanitario.
* **`practitioner_name`**: Nombre y título del médico.

## 🩺 Diagnóstico (`Condition`)
* **`condition_id`**: Identificador de la patología asociada.
* **`condition_code`**: Código de la enfermedad (SNOMED-CT).
* **`condition_display`**: Nombre clínico de la enfermedad.
* **`condition_onset`**: Fecha de inicio del diagnóstico.

## 💶 Facturación (`Claim`)
* **`has_claim`**: Booleano indicando si existe reclamación financiera.
* **`claim_id`**: Identificador de la reclamación/factura.
* **`claim_total_value`**: Coste total de la prescripción/cobertura.
* **`claim_insurance`**: Nombre de la aseguradora o `NO_INSURANCE`.