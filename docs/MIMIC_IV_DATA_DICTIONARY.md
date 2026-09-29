# 📖 Inventario de Recursos Clínicos (MIMIC-IV on FHIR)

Este documento describe el mapa de recursos extraídos de la demo de **MIMIC-IV on FHIR**. A diferencia de los conjuntos de datos sintéticos (que agrupan todo en un único `Bundle`), la información en MIMIC-IV se distribuye en archivos `.ndjson` independientes clasificados por concepto clínico y departamento del hospital (Urgencias "ED" y Cuidados Intensivos "ICU").

# 💊 1. Eje Central: Medicación y Prescripciones

 Esta es la base principal del pipeline de detección de anomalías. El ciclo del medicamento en MIMIC-IV es extremadamente detallado, permitiendo auditar la trazabilidad completa desde la prescripción hasta la administración.

 - **`MimicMedicationRequest.ndjson`**: La orden médica original. Contiene las recetas y prescripciones formales hechas por el facultativo. _(Archivo principal para la ingesta del pipeline ETL)._
- **`MimicMedication.ndjson`**: Catálogo general que contiene los detalles exactos, códigos y nombres de los fármacos recetados.
- **`MimicMedicationDispense.ndjson`** / **`MimicMedicationDispenseED.ndjson`**: Registros de la farmacia del hospital indicando cuándo se preparó y entregó físicamente el medicamento (planta y Urgencias).
- **`MimicMedicationAdministration.ndjson`** / **`MimicMedicationAdministrationICU.ndjson`**: Registro a pie de cama. Confirma el momento exacto en el que enfermería administró el fármaco al paciente (en planta o en UCI).
- **`MimicMedicationStatementED.ndjson`**: Declaraciones de medicación previas (historial farmacológico reportado por el paciente al llegar a Urgencias).
- **`MimicMedicationMix.ndjson`**: Fórmulas magistrales o mezclas de fluidos intravenosos preparadas internamente en el hospital.

---

 # 👤 2. Eje Demográfico y Espacial

 Datos necesarios para contextualizar al paciente y la ubicación física del presunto fraude o anomalía asistencial.

 - **`MimicPatient.ndjson`**: Datos demográficos maestros de la cohorte (fechas de nacimiento, género, estado civil, fecha de fallecimiento).
- **`MimicOrganization.ndjson`**: Información corporativa de los centros o departamentos sanitarios.
- **`MimicLocation.ndjson`**: Ubicaciones físicas específicas (habitaciones, camas, boxes) donde ocurrió el encuentro o la atención médica.

---

 # 🩺 3\. Eje Clínico: Procedimientos y Observaciones

 Variables y métricas clínicas extraídas para dotar a los modelos de Inteligencia Artificial del contexto necesario para evaluar la coherencia médica (ej. justificación de una medicación específica en base a cirugías o constantes vitales).

 ## Procedimientos Quirúrgicos y Médicos

 - **`MimicProcedure.ndjson`**: Intervenciones y procedimientos realizados en planta general.
- **`MimicProcedureED.ndjson`**: Intervenciones realizadas en Urgencias (Emergency Department).
- **`MimicProcedureICU.ndjson`**: Intervenciones realizadas en la Unidad de Cuidados Intensivos (Intensive Care Unit).

 ## Constantes y Monitorización Continua

 - **`MimicObservationVitalSignsED.ndjson`**: Constantes vitales tomadas en el triaje o a la llegada a Urgencias (tensión arterial, pulso, temperatura, saturación).
- **`MimicObservationChartevents.ndjson`**: Registros continuos y eventos parametrizados anotados por el personal médico (óptimo para modelado de series temporales).
- **`MimicObservationDatetimeevents.ndjson`**: Eventos clínicos específicos con marcas temporales exactas.
- **`MimicObservationOutputevents.ndjson`**: Fluidos corporales expulsados (orina, drenajes), métricas críticas para la evaluación en UCI.

 ## Laboratorio y Analíticas

 - **`MimicObservationLabevents.ndjson`**: Resultados cuantitativos de pruebas analíticas (sangre, orina, etc.).
- **`MimicSpecimen.ndjson`** / **`MimicSpecimenLab.ndjson`**: Registro de las muestras biológicas extraídas al paciente y enviadas al laboratorio para su procesamiento.