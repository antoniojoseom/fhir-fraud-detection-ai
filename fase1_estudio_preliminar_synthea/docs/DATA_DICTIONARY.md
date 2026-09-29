# 📖 Diccionario de Datos (`medication_request_dataset.jsonl`)

Este documento describe la estructura y semántica de los campos aplanados a partir de los recursos HL7 FHIR en el dataset `medication_request_dataset.jsonl`.

## 💊 Receta Médica (`MedicationRequest`)
* **`IdMedicationRequest`**: Identificador único de la prescripción.
* **`status`**: Estado de la receta (ej. `active`, `completed`, `stopped`).
* **`intent`**: Intención clínica (ej. `order`, `plan`).
* **`authoredOn`**: Fecha y hora exacta de la prescripción.
* **`medication_code`**: Código del fármaco (sistema RxNorm / SNOMED).
* **`medication_display`**: Nombre y concentración del medicamento.
* **`medication_text`**: Texto descriptivo de la medicación proporcionado en la receta.
* **`dosage_frequency`**: Frecuencia de la toma (veces por periodo).
* **`dosage_period`**: Periodo de la frecuencia (ej. cada 1.0 días).
* **`dosage_unit`**: Unidad del periodo (`d` = días, `h` = horas).
* **`dosage_as_needed`**: Booleano que indica si el medicamento es "a demanda" (si es necesario).
* **`dosage_value`**: Cantidad o dosis administrada en cada toma.
* **`dosage_value_unit`**: Unidad de la dosis administrada (si aplica).

## 🏥 Consulta Médica (`Encounter`)
* **`encounter_id`**: Identificador de la visita médica.
* **`encounter_status`**: Estado de la consulta (ej. `finished`, `arrived`).
* **`encounter_class`**: Tipo de atención (`AMB` = Ambulatoria, `IMP` = Hospitalización).
* **`encounter_start`**: Timestamp de inicio de la consulta.
* **`encounter_end`**: Timestamp de fin de la consulta.
* **`is_valid_time_window`**: **[FLAG AUDITORÍA]** `True` si `authoredOn` está entre `encounter_start` y `encounter_end`.
* **`encounter_type_code`**: Código clínico del motivo o procedimiento del encuentro (SNOMED-CT).
* **`encounter_type_display`**: Descripción textual del motivo del encuentro.
* **`encounter_provider`**: Organización / centro sanitario donde se realiza el encuentro.
* **`encounter_location`**: Ubicación física específica dentro del centro sanitario.

## 👤 Paciente (`Patient`)
* **`patient_id`**: Identificador del paciente.
* **`patient_name`**: Nombre completo del paciente.
* **`patient_gender`**: Género biológico/registrado del paciente.
* **`patient_birthdate`**: Fecha de nacimiento.
* **`patient_deceased_datetime`**: Fecha y hora de defunción (si aplica, útil para control de fraude post-mortem).
* **`patient_marital_status`**: Estado civil del paciente (ej. `M` = Casado, `S` = Soltero).
* **`patient_city`**: Ciudad de residencia del paciente.
* **`patient_state`**: Estado/Provincia de residencia del paciente.

## 👨‍⚕️ Prescriptor (`Practitioner`)
* **`practitioner_id`**: Identificador único del profesional sanitario.
* **`practitioner_name`**: Nombre y título del médico o proveedor.

## 🩺 Diagnóstico (`Condition`)
* **`condition_id`**: Identificador de la patología asociada.
* **`condition_code`**: Código de la enfermedad (SNOMED-CT).
* **`condition_display`**: Nombre clínico de la enfermedad diagnosticada.
* **`condition_onset`**: Fecha y hora de inicio o diagnóstico del problema de salud.

## 💶 Facturación (`Claim`)
* **`has_claim`**: Booleano indicando si existe reclamación financiera asociada.
* **`claim_id`**: Identificador de la reclamación/factura.
* **`claim_status`**: Estado de la reclamación (ej. `active`).
* **`claim_use`**: Propósito de la reclamación (ej. `claim`).
* **`claim_total_value`**: Coste total facturado por la prescripción.
* **`claim_currency`**: Moneda de facturación (ej. `USD`).
* **`claim_billable_start`**: Fecha de inicio del periodo facturable.
* **`claim_billable_end`**: Fecha de fin del periodo facturable.
* **`claim_insurance`**: Nombre de la aseguradora principal o `NO_INSURANCE`.
