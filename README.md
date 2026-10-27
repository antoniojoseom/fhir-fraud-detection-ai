# FHIR MIMIC-IV Clinical Fraud & Anomaly Detection (TFG)

Pipeline ETL de alto rendimiento y motor de detección de anomalías clínicas basado en Inteligencia Artificial para la auditoría de prescripciones y administración de medicamentos utilizando estándares **HL7 FHIR** y el dataset **MIMIC-IV**.

---

## 🚀 Arquitectura del Proyecto

Este sistema procesa datos clínicos complejos en formato FHIR (`.ndjson.gz`), los limpia mediante una estrategia de resolución robusta y genera un dataset unificado tabular (`.jsonl`) listo para el entrenamiento de modelos de Machine Learning orientados a la detección de anomalías, desvíos y discrepancias de administración.

### Fuentes de Datos Integradas (MIMIC-IV)

- **MedicationRequest (Recetas):** Entidad central de prescripción médica (~15,4 millones de registros).
- **Patient & Encounter:** Datos demográficos, clases de ingreso y cronología temporal.
- **Condition:** Diagnósticos clínicos asociados (códigos ICD).
- **Procedure:** Intervenciones quirúrgicas y procedimientos clínicos.
- **Medication (Catálogo):** Diccionario oficial de fármacos.
- **MedicationAdministration:** Trazabilidad real de administración para el cálculo de la variable de auditoría (`fue_administrado`).
- **Prescriptions CSV (Cruce Relacional):** Archivo relacional original utilizado para la atribución del médico prescriptor (`order_provider_id`) a través del `pharmacy_id`.

---

## ⚙️ Características Técnicas del ETL

1. **Procesamiento Masivo en Cloud (Colab):** Optimizado para la ejecución sobre Google Drive, procesando más de 15,4 millones de registros completos de MIMIC-IV.
2. **Resolución Triple de Fármacos:**
   - *Vía 1:* Búsqueda directa por ID en el catálogo oficial de farmacia.
   - *Vía 2:* Extracción semántica desde `medicationCodeableConcept` (texto o códigos directos).
   - *Vía 3:* Rescate inteligente de sueros, premezclas intravenosas y fluidos huérfanos (`IV Fluid / Mix`) mediante heurística de posología y vías.
3. **Atribución del Médico Prescriptor:** Cruce con el sistema relacional tradicional mediante `pharmacy_id` para rescatar al profesional responsable en un subconjunto de ~2,4 millones de registros (con estrategia abierta para el análisis global en registros huérfanos de urgencias/ambulatorios).
4. **Cero Pérdida de Integridad:** Consolidación de diagnósticos y procedimientos por identificador de ingreso (`encounter_id`).

---

## 📂 Estructura del Repositorio

```text
fhir-fraud-detection-ai/
│
├── notebooks/
│   └── fhir_to_jsonl.ipynb        # Jupyter Notebook principal con el pipeline ETL y muestras
├── data/                         # Archivos fuente FHIR y dataset de salida (.jsonl)
├── scripts/                      # (Opcional) Scripts auxiliares en Python
├── .gitignore                    # Exclusión de archivos pesados y entornos virtuales
└── README.md                     # Documentación oficial del proyecto