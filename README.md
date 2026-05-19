# Auditoría de Historias Clínicas Electrónicas en Estándar HL7 FHIR

Este repositorio contiene la fase de ingesta y caracterización de un dataset clínico sintético (10 pacientes) para el desarrollo de mi TFG.

## 📂 Estructura del Proyecto
* `/docs/ANALISIS_CLINICO.md`: **DOCUMENTO PRINCIPAL** Informe ejecutivo y técnico que consolida el análisis de la cohorte. Incluye la caracterización de episodios, detección de anomalías asistenciales y dictámenes de integridad para cada paciente
* `/scripts`: Scripts de Python desarrollados para procesar los JSON (Bundles) y extraer información.
* `/data`: Historias clínicas originales en formato FHIR.
* `/docs/analisis_pacientes`: Informes detallados con la cronología asistencial y episodios de cada paciente.
* `/docs/resumen_datos.txt`: Análisis cuantitativo global de las prescripciones médicas.

## 🛠️ Metodología Técnica
Para cumplir con los requisitos, se ha automatizado la extracción de:
1. **Recuento de Recursos:** Inventario completo de cada Bundle (Encounter, Claim, MedicationRequest, etc.).
2. **Cronología Asistencial:** Identificación de episodios desde el primer encuentro hasta la gestión de patologías crónicas.
3. **Análisis de Prescripciones:** Extracción de metadatos de `MedicationRequest`: Médico prescriptor, dosis, fármaco y frecuencia.

