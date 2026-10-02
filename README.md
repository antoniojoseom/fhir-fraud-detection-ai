# FHIR MIMIC-IV Clinical Fraud & Anomaly Detection (TFG)

Pipeline ETL de alto rendimiento y motor de detección de anomalías clínicas basado en Inteligencia Artificial para la auditoría de prescripciones y administración de medicamentos utilizando estándares **HL7 FHIR** y el dataset **MIMIC-IV**.

```

---

## 🚀 Arquitectura del Proyecto

Este sistema procesa datos clínicos complejos en formato FHIR (`.ndjson.gz`), los limpia mediante una estrategia de resolución robusta y genera un dataset unificado tabular (`.jsonl`) listo para el entrenamiento de modelos de Machine Learning orientados a la detección de anomalías y discrepancias de administración.

### Fuentes de Datos Integradas (MIMIC-IV)

* **MedicationRequest (Recetas):** Entidad central de prescripción médica.
* **Patient & Encounter:** Datos demográficos, clases de ingreso y cronología temporal.
* **Condition:** Diagnósticos clínicos asociados (códigos ICD de alta y urgencias).
* **Procedure:** Intervenciones quirúrgicas y procedimientos clínicos (quirófanos).
* **Medication (Catálogo):** Diccionario oficial de fármacos.
* **MedicationAdministration:** Trazabilidad real de administración para el cálculo de la variable objetivo (`fue_administrado`).

---

## ⚙️ Características Técnicas del ETL

1. **Procesamiento de Alta Velocidad:** Lectura nativa en binario con `gzip` y parseo optimizado con `orjson`.
2. **Resolución Triple de Fármacos:**
* *Vía 1:* Búsqueda directa por ID en el catálogo oficial de farmacia.
* *Vía 2:* Extracción semántica desde `medicationCodeableConcept` (texto o códigos directos).
* *Vía 3:* Rescate inteligente de sueros, premezclas intravenosas y fluidos huérfanos (`IV Fluid / Mix`) mediante heurística de posología y vías.


3. **Integración Quirúrgica y Diagnóstica:** Agrupación relacional por `encounter_id` para consolidar diagnósticos y quirófanos en cadenas de texto estructuradas.
4. **Cero Pérdida de Integridad:** Tasa de fallo del 0% en cruces relacionales clave.

---

## 📂 Estructura del Repositorio

```text
fhir-fraud-detection-ai/
│
├── data/                         # Archivos fuente FHIR y dataset de salida (.jsonl)
├── scripts/
│   ├── fhir_to_jsonl.py          # Script principal del pipeline ETL
│   ├── auditar.py                # Script de verificación y control de calidad
│   └── make_sample.py            # Script para generar el dataset de muestra
│
├── .gitignore                    # Exclusión de archivos pesados y entornos virtuales
└── README.md                     # Documentación del proyecto

```

---

## 🛠️ Instrucciones de Ejecución

1. **Clonar el repositorio y configurar el entorno:**
```bash
git clone 
cd fhir-fraud-detection-ai

```


2. **Ejecutar el pipeline ETL:**
```bash
python scripts/fhir_to_jsonl.py

```


3. **Auditar la calidad del dataset generado:**
```bash
python scripts/auditar.py

```



---

*Trabajo de Fin de Grado (TFG) - Grado en Ingeniería en Tecnologías de Telecomunicación (E.T.S.I. Sevilla).*

```