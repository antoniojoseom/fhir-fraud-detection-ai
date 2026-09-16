# 🏥 Auditoría e Inteligencia Artificial sobre Historias Clínicas Electrónicas (HL7 FHIR)

Este repositorio contiene la arquitectura de ingeniería de datos, los pipelines ETL y la suite de auditoría clínica preliminar desarrollados para el Trabajo de Fin de Grado (TFG) enfocado en la **detección automatizada de fraudes, anomalías e incoherencias en Historias Clínicas Electrónicas (EHR)** estructuradas bajo el estándar internacional **HL7 FHIR**.

## 📂 Estructura del Proyecto

```text
fhir-fraud-detection-ai/
├── data/                             # Historias clínicas sintéticas originales en formato HL7 FHIR (JSON/Bundles)
├── docs/                             # Documentación técnica, diccionario de datos e informes clínicos
│   ├── DATA_DICTIONARY.md            # Diccionario semántico exhaustivo del dataset JSONL
│   ├── ANALISIS_CLINICO.md           # Informe ejecutivo consolidado de la cohorte analizada
│   ├── medication_request_samples.jsonl # Muestra de 100 registros denormalizados (Previsualizable en GitHub)
│   └── analisis_pacientes/           # Auditoría e historial cronológico individualizado por paciente
│       ├── paciente_1.md
│       ├── paciente_2.md
│       └── ...
├── scripts/                          # Pipelines ETL y herramientas de análisis exploratorio
│   ├── fhir_to_jsonl.py              # Script principal ETL: Extracción recursiva y aplanado a JSONL
│   ├── analisis_inicial.py           # Extracción automatizada de métricas cuantitativas globales
│   └── analisis_detallado.py         # Generador de cronologías asistenciales por paciente
├── notebooks/                        # Entorno reservado para el desarrollo de reglas e IA (Fase 3)
├── .gitignore                        # Exclusión de archivos pesados de datos (.jsonl completos)
└── README.md                         # Visión general y guía del repositorio

````
## Guía de ejecución
Para procesar las historias clínicas de la carpeta data/ y actualizar el dataset aplanado local:
python scripts/fhir_to_jsonl.py
