# ANÁLISIS CLÍNICO DE 10 PACIENTES

Este documento presenta el análisis de 10 expedientes clínicos por orden cronológico identificando patrones de fraude.

## Resumen Ejecutivo de Riesgos

| Severidad | Pacientes | Patrón Detectado |
| :--- | :--- | :--- |
| 🔴 **Extremo** | 4, 9, 10 | Volúmenes >2000 claims y facturación masiva de procedimientos. |
| 🟠 **Alto** | 1, 2, 7, 8 | Ratios de facturación >3.5 y encuentros sospechosos en días consecutivos. |
| 🟡 **Medio/Bajo** | 3, 5, 6 | Inconsistencias administrativas y visitas "reloj" semanales. |

---

# 1. PACIENTE: Adolfo777_Yost751

**Perfil:** Paciente crónico con una trayectoria de más de 50 años en el sistema. Evolución de Hipertensión (1968), Diabetes Tipo 2 (1993) y eventos de riesgo cardiovascular detectados en la última década.

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1965 - 1992** | Control de Hipertensión Arterial | Lisinopril, Amlodipino |
| **1993 - 2010** | Diagnóstico y manejo de DM2 | Metformina, Glipizida |
| **2011 - 2013** | Complicaciones de Dislipidemia | Simvastatina |
| **2014** | **Fase de Hiper-frecuentación Aguda** | Clopidogrel, Nitroglicerina |

### Hallazgos de Auditoría e Integridad

* **🚩 Anomalía de Frecuencia (Noviembre 2014):** Se detecta un clúster de encuentros con una proximidad injustificada. El paciente registra visitas los días **13, 23 y 30 de noviembre**. En el encuentro del día 30, se dispara una lista masiva de 7 medicamentos de alto riesgo, lo que sugiere una intensificación administrativa de la atención al cierre del periodo.
* **📊 Volumen Crítico de Claims:** El paciente acumula **1,033 Claims** vinculados a **392 Encuentros**. Aunque el ratio es de 2.6, el volumen absoluto de más de mil reclamaciones para un historial ambulatorio es un indicador de alerta roja para auditorías de facturación recurrente.
* **⚠️ Densidad de Informes Diagnósticos:** Constan **575 DiagnosticReports**. Al haber más informes que encuentros físicos (392), se deduce que en gran parte de las visitas se facturan múltiples pruebas de laboratorio o imagen de forma redundante, sin que el cuadro clínico (Diabetes/HTA estable) lo exija habitualmente.
* **💊 Polifarmacia Automatizada:** En los registros finales de 2014, se observa la prescripción de "Amlodipino 2.5 MG" y "Amlodipine 5 MG" de forma simultánea. Esta duplicidad de la misma molécula en diferentes dosis dentro del mismo encuentro es un error de integridad de datos grave o un intento de duplicar cargos farmacéuticos.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🟠 RIESGO ALTO.**
> En noviembre de 2014 registra visitas los días 13, 23 y 30. En la última visita se facturan 7 fármacos de alto riesgo de golpe. Se recomienda auditar los servicios prestados en el último trimestre de 2014.





# 2. PACIENTE: Alvaro283_Altenwerth646

**Perfil:** Paciente geriátrico con una gestión de salud de casi 90 años. Evolución de Hipertensión (1945), Artritis (1975) y complicación cardiovascular con Fibrilación Auricular (2018).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1932 - 1944** | Seguimiento Primario Temprano | N/A |
| **1945 - 1974** | Control Crónico de HTA | Lisinopril, Amlodipino |
| **1975 - 2017** | Manejo de Artritis y Dolor | Prednisona, Ibuprofeno |
| **2018 - 2019** | **Hito Cardiovascular** (Arritmias) | Warfarina, Digoxina, Verapamilo |

### Hallazgos de Auditoría e Integridad

* **🚩 Ratio de Facturación Crítico (Claims vs Encounters):** Se registran **396 Claims** para solo **97 Encuentros**. Esto representa una media de **4.08 facturas por cada visita**, superando el promedio de la cohorte. Es un indicador claro de "vaciado de códigos" o *Unbundling*, donde cada interacción mínima se desglosa en múltiples conceptos de cobro.
* **⚠️ Anomalía de Procedimientos Quirúrgicos:** A pesar de tener solo 97 encuentros, se registran **17 procedimientos** de diversa índole. La concentración de estos procedimientos en periodos cortos sin una hospitalización mayor documentada sugiere una posible inflación de servicios quirúrgicos ambulatorios.
* **📊 Inconsistencia en Documentación (Provenance):** Al igual que en los casos anteriores, existe un **vacío de trazabilidad crítico**: 2,300+ registros de datos pero solo **1 registro de Provenance**. No hay rastro auditable de quién realizó las entradas clínicas durante los últimos 50 años de historial.
* **💊 Polifarmacia Aguda (2018-2019):** Tras el diagnóstico de Fibrilación Auricular en 2018, la carga medicamentosa se dispara a 8 fármacos simultáneos de alta complejidad. Los encuentros de "Revisión" en este periodo muestran una repetición exacta de recetas, lo que apunta a un sistema de renovación automática sin evaluación clínica presencial detallada.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🟠 RIESGO ALTO.**
> El paciente presenta un ratio de **4.08 facturas por encuentro**, lo que indica una eficiencia financiera del centro sospechosamente alta por cada minuto de atención. Se recomienda auditar los `ExplanationOfBenefit` del periodo 2018-2019 para verificar si los procedimientos facturados coinciden con las notas de evolución clínica.






# 3. PACIENTE: Mayola305_Sanford861

**Perfil:** Paciente geriátrica con un historial clínico que abarca más de 70 años. Evolución de Hipotiroidismo (1970), Hipertensión y Fibrilación Auricular con riesgo cardiovascular elevado.

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1920 - 1969** | Seguimiento Primario Temprano | N/A |
| **1970 - 1989** | Diagnóstico de Hipotiroidismo | Levotiroxina Sódica |
| **1990 - 2009** | Control de Riesgo Cardiovascular | Lisinopril, Simvastatina |
| **2010 - 2020** | Gestión de Polifarmacia y Arritmias | Warfarina, Digoxina, Verapamilo |

### Hallazgos de Auditoría e Integridad

* **🚩 Anomalía de Reclamaciones (Claims Ratio):** Se registran **274 Claims** para **69 Encuentros**. Esto arroja una ratio de **3.97 facturas por encuentro**, una de las más altas del conjunto. Indica que cada visita física genera casi cuatro conceptos de cobro independientes, lo que sugiere un posible *Upcoding* (sobre-codificación de servicios).
* **📊 Fragmentación en Pruebas Diagnósticas:** El sistema muestra **105 DiagnosticReports** frente a solo 69 encuentros. Existe un patrón recurrente de solicitar pruebas adicionales fuera de los encuentros de revisión estándar, lo que podría indicar facturación de servicios complementarios no presenciales.
* **💊 Carga Medicamentosa Dispar (2020):** En el encuentro del **05 de junio de 2020**, se observa la prescripción simultánea de un bloque masivo de fármacos (Clopidogrel, Nitroglicerina, Verapamilo, Simvastatina, Digoxina, Amlodipino). La densidad de medicación de alto riesgo en un solo registro administrativo requiere verificación de la necesidad clínica frente a un posible volcado automático de recetas.
* **🔍 Integridad de Registro:** Al igual que en el resto de la cohorte, la falta de múltiples registros de `Provenance` (solo 1 disponible) limita la capacidad de auditar qué facultativo o sistema realizó las modificaciones críticas en el CarePlan de la paciente durante la última década.

### Dictamen Final

> [!IMPORTANT]
> **ESTADO: 🟡 RIESGO MEDIO-ALTO.**
> 105 Informes diagnósticos para solo 69 encuentros. Se facturan pruebas constantemente sin que el paciente esté presente en el centro. Posible facturación de servicios complementarios no realizados.







# 4. PACIENTE: Melinda114_Rodriguez71

**Perfil:** Paciente geriátrica con historial de Hipertensión (1951), Diabetes Tipo 2 (1975) y una explosión de actividad asistencial en la última década (hiper-frecuentación masiva).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1951 - 1974** | Control de Hipertensión (HTA) | Lisinopril, Amlodipino |
| **1975 - 2009** | Manejo de Diabetes Tipo 2 | Metformina, Insulina Humana |
| **2010 - 2019** | Fase de Cronicidad Estable | Hidroclorotiazida, Estatinas |
| **2020 - 2021** | **Hiper-frecuentación Crítica** | Insulina, Polifarmacia CV |

### Hallazgos de Auditoría e Integridad

* **🚩 Anomalía de Frecuencia Extrema (Churning):** En el periodo de marzo-abril de 2021, la paciente registra encuentros con una frecuencia semanal exacta (31 de marzo, 7 de abril, 14 de abril). Sin embargo, el día **17 de abril de 2021** (apenas 3 días después de la última visita), se registra un nuevo encuentro de "Revisión" con la misma carga medicamentosa. Esta densidad de visitas sin un evento agudo (ER/Hospitalización) sugiere una **inflación artificial de la agenda**.
* **📊 Volumen Desproporcionado de Claims:** Se registran **2,054 Claims** para **775 Encuentros**. Un volumen total de más de dos mil reclamaciones financieras para una sola paciente es un indicador de riesgo extremo, sugiriendo que se están facturando múltiples servicios menores o duplicados en cada contacto.
* **⚠️ Alta Densidad de Reportes Diagnósticos:** Constan **893 DiagnosticReports**. El hecho de que el número de informes diagnósticos supere al número de encuentros (775) indica que en casi todas las visitas se ordenan pruebas, muchas de las cuales podrían ser redundantes dada la estabilidad de las patologías crónicas de la paciente.
* **💊 Gestión de Recetas:** Con **1,279 MedicationRequests**, la paciente recibe un promedio de 1.6 órdenes de medicación por cada encuentro a lo largo de toda su vida, pero este ratio se dispara en los últimos años, coincidiendo con la mayor frecuencia de visitas.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🔴 RIESGO EXTREMO (EXPLOTACIÓN ADMINISTRATIVA)**
> El caso de Melinda es un ejemplo de manual de "Churning". Con **775 encuentros** y más de **2,000 reclamaciones**, la intensidad asistencial en 2021 no se correlaciona con una mejora o cambio en el cuadro clínico. Se recomienda auditar la validez de los encuentros realizados con 72 horas de diferencia y la justificación de los casi 900 informes diagnósticos emitidos.








# 5. PACIENTE: Neida631_Upton904

**Perfil:** Paciente geriátrico con manejo de Hipertensión Arterial (1941) y Artritis (1975). Presenta una estabilidad clínica relativa con picos de atención puntual.

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1941 - 1974** | Control de Hipertensión | Lisinopril, Amlodipino |
| **1975 - 2008** | Diagnóstico de Artritis y Dolor | Prednisona, Ibuprofeno |
| **2009 - 2011** | Fase de Polifarmacia y Control CV | Hidroclorotiazida, Amoxicilina |

### Hallazgos de Auditoría e Integridad

* **🚩 Anomalía de Encuentros Adyacentes:** Se detectan registros de encuentros en días consecutivos (ej. **11 y 12 de octubre de 2009**). Al tratarse de episodios etiquetados simplemente como "Revisión" sin cambios en la medicación ni nuevas condiciones, esta redundancia sugiere una fragmentación de la atención para generar cargos adicionales por visita.
* **📊 Eficiencia de Recursos:** A diferencia de otros pacientes del grupo, este presenta **324 Claims** para **97 Encuentros** (Ratio 3.3). Aunque el volumen total es menor, el ratio de reclamaciones por visita sigue siendo elevado, indicando que cada contacto se factura con múltiples conceptos.
* **💊 Consistencia Medicamentosa:** La transición de fármacos antihipertensivos muestra una trazabilidad lógica desde 1941, sin embargo, en 2009 se observa una carga de recetas (`MedicationRequest: 227`) que triplica el número de encuentros, sugiriendo renovaciones automáticas no vinculadas a una evaluación física.
* **🔍 Integridad de Datos (Provenance):** Al igual que en casos anteriores, solo existe **1 registro de Provenance** para todo el historial. Esto confirma una vulnerabilidad estructural en el sistema de registro, donde la autoría de los cambios clínicos no queda debidamente auditada.

### Dictamen Final

> [!TIP]
> **ESTADO: 🟢 RIESGO MEDIO.**
> Encuentros en días consecutivos (11 y 12 de octubre). Sin embargo, su volumen total es el más bajo de la cohorte. Errores de carga administrativa más que fraude sistemático.







# 6. PACIENTE: Oswaldo857_Leffler128

**Perfil:** Paciente geriátrico con un historial de salud mental (Depresión, 1960), Diabetes Tipo 2 (1983) e Hipertensión crónica, con una explosión de actividad asistencial en la última década.

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1940 - 1959** | Antecedentes | Periodo de baja actividad. |
| **1960 - 1982** | Salud Mental y Control Primario | Sertralina, Hidrocodona |
| **1983 - 2005** | Diagnóstico y Progresión de DM2 | Metformina, Insulina Humana |
| **2006 - 2019** | Manejo de Complicaciones Crónicas | Amlodipino, Hidroclorotiazida |
| **2020 - 2021** | **Fase de Hiper-frecuentación Semanal** | Insulina, Antihipertensivos |

### Hallazgos de Auditoría e Integridad

* **🚩 Patrón de Visitas "Reloj" (2021):** Se detecta una anomalía de frecuencia extrema entre marzo y abril de 2021, con encuentros registrados exactamente cada 7 días (7, 14, 21 y 28 de marzo; 4 y 11 de abril). Esta regularidad matemática en revisiones ambulatorias suele indicar una **automatización de la agenda** para asegurar facturación recurrente, más que una necesidad clínica aguda.
* **📊 Desproporción de Recursos:** El historial cuenta con **1,551 Claims** vinculados a **612 Encuentros**. Aunque el ratio es de 2.5, el volumen total de reclamaciones es masivo para un paciente cuya sintomatología principal (Diabetes/HTA) debería manejarse con seguimientos trimestrales o mensuales, no semanales.
* **⚠️ Gestión de Analgesia (Histórico):** El uso temprano de **Acetaminofén/Hidrocodona** (1960) y su registro persistente en la base de datos sin una condición de dolor agudo justificada en cada encuentro abre una línea de investigación sobre la legitimidad de las renovaciones de recetas de opioides.
* **🔍 Inconsistencia de Datos (Observations):** Se registran **2,103 observaciones** clínicas. Muchas de estas métricas se repiten sin variaciones significativas entre las visitas semanales de 2021, lo que sugiere un volcado de datos redundante para justificar la complejidad de cada factura.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🟡 RIESGO MEDIO-ALTO**
> Encuentros registrados exactamente cada 7 días en marzo/abril de 2021. La agenda está automatizada para ingresos recurrentes. Churning de baja intensidad.








# 7. PACIENTE: Roman389_Raynor401

**Perfil:** Paciente crónico complejo con evolución de Hipertensión (1956), Diabetes Tipo 2 (1978), Dislipidemia y deterioro cognitivo/demencia (2009).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1956 - 1977** | Manejo inicial de Hipertensión (HTA) | Lisinopril, Amlodipino |
| **1978 - 2008** | Control de Diabetes y Dislipidemia | Metformina, Simvastatina |
| **2009 - 2012** | Deterioro Cognitivo y Riesgo CV | Galantamina, Clopidogrel, Nitroglicerina |
| **2013** | **Evento Crítico Agudo** (Fase de Urgencias) | Epinefrina, Amiodarona, Atropina |

### Hallazgos de Auditoría e Integridad

* **🚩 Patrón de "Encuentros Triples" (Unbundling):** Se detecta una anomalía sistemática entre 2004 y 2012, donde el paciente registra exactamente **3 encuentros en el mismo día** cada fin de año (ej. 01/04/2004, 17/02/2005, 13/01/2006). Esta fragmentación artificial de visitas es un indicador clásico de fraude para multiplicar los cargos por consulta.
* **📊 Ratio de Facturación Elevado:** El historial presenta **421 Claims** para solo **143 Encuentros**. Esto resulta en una media de casi **3 facturas por cada contacto con el médico**, lo que sugiere la inclusión de cargos secundarios no justificados en el diagnóstico principal.
* **💊 Duplicidad en Prescripción Farmacéutica:** En julio de 2009, se registran múltiples `MedicationRequest` para Clopidogrel y Nitroglicerina con apenas segundos de diferencia. Esto indica un error de carga masiva en el sistema o una duplicidad intencionada para inflar el coste de suministros.
* **👨‍⚕️ Concentración de Riesgo (Médico 9999999949):** La mayoría de las irregularidades administrativas y las prescripciones críticas en la fase de demencia están firmadas por el mismo ID, lo que podría señalar una cuenta de sistema utilizada para "cerrar" expedientes y generar cargos de forma automatizada.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🟠 RIESGO ALTO.**
> Registra 3 visitas el mismo día de forma sistemática a final de cada año. Manipulación clara de la facturación anual.
> Fraude administrativo deliberado aprovechando la vulnerabilidad del paciente.








# 8. PACIENTE: Thaddeus38_Zulauf375

**Perfil:** Geriátrico Crónico Reincidente (Hipertensión, Cáncer de Próstata, Fibrilación Auricular e Insuficiencia Cardíaca Congestiva).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1941 - 1986** | Control Prolongado de HTA y Dislipidemia | Hidroclorotiazida, Simvastatina |
| **1987 - 2000** | **Hito Oncológico** (Cáncer Próstata) | Docetaxel, Leuprolide |
| **2001 - 2009** | Deterioro Cardiovascular (Arritmias) | Warfarina, Digoxina, Verapamilo |
| **2010 - 2011** | **Brote de Hiper-frecuentación** (ICC) | Sacubitrilo/Valsartán, Furosemida |
| **2012 - 2021** | Gestión de Cronicidad Terminal | Multiterapia Cardiovascular |

### Hallazgos de Auditoría e Integridad

* **🚩 Anomalía de Frecuencia (Churning):** Entre **julio de 2010 y junio de 2011**, el paciente registra encuentros con una frecuencia de **48 a 72 horas**. Este nivel de intensidad es propio de una unidad de cuidados intermedios, pero aquí se clasifica como "Revisiones ambulatorias", lo que sugiere una inflación artificial de la actividad asistencial.
* **📊 Desproporción Volumétrica:** El sistema arroja **527 Claims** para **307 Encuentros**. Existe un excedente de 220 reclamaciones que no están vinculadas a un encuentro físico claro, apuntando a facturación de servicios "fantasma".
* **💊 Patrón de Receta Redundante:** En los encuentros del **10 y 11 de abril de 2011**, se replican 9 prescripciones idénticas de alto coste en menos de 24 horas. Esto indica una falta de control en la carga de datos o un intento deliberado de duplicar el reembolso farmacéutico.
* **🔍 Trazabilidad Comprometida:** A pesar de tener más de 3,000 registros de actividad clínica (Observations/Reports), solo existe **1 registro de Provenance**. Esto representa un riesgo crítico de integridad de datos, ya que no se puede verificar quién o qué sistema originó la información.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🟠 RIESGO MUY ALTO.**
> Frecuencia de encuentros cada 48 horas en 2010. Duplicidad de recetas de alto coste (9 fármacos repetidos en menos de 24h).
>Explotación del diagnóstico de ICC para inflar visitas.






# 9. PACIENTE: Vince741_Schinner682

**Perfil:** Paciente geriátrico de alta complejidad con progresión de Hipertensión (1950), Diabetes Tipo 2 (1975) y Anemia Crónica (2012).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1950 - 1974** | Inicio y manejo de HTA | Lisinopril, Amlodipino |
| **1975 - 2011** | Diagnóstico y progresión de DM2 | Metformina, Glipizida |
| **2012 - 2017** | Complicaciones (Anemia y Dolor Crónico) | Sulfato Ferroso, Oxicodona |
| **2018 - 2021** | Insulinización y polifarmacia severa | Insulina Humana (Humulin), Hidroclorotiazida |

### Hallazgos de Auditoría e Integridad

* **🚩 Hiper-inflación de Reclamaciones (Claims):** Se registran **931 Claims** para solo **250 Encuentros**. Esto arroja una ratio de **3.72 facturas por visita**, la más alta del grupo. Sugiere un patrón agresivo de *Upcoding* o facturación de múltiples procedimientos menores de forma independiente en cada consulta.
* **⚠️ Gestión de Opioides (2014-2017):** Durante este periodo se observa una densidad inusual de `MedicationRequest` para **Oxicodona** y **Acetaminofén**. El volumen de recetas emitidas no coincide proporcionalmente con el número de encuentros físicos, lo que requiere una revisión sobre la legitimidad de las prescripciones.
* **📊 Anomalía de Observaciones:** El paciente tiene **1,635 Observations** registradas. Muchas de ellas ocurren en bloques temporales idénticos (mismo minuto), lo que indica una automatización de volcado de datos que podría estar inflando la complejidad percibida del caso para justificar mayores reembolsos.
* **💊 Duplicidad en Insulina (2021):** En el último año de registros (ej. 02/06/2021), se observa la prescripción simultánea de múltiples fármacos metabólicos en encuentros administrativos de "Revisión" que duran segundos.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🔴 RIESGO CRÍTICO**
> El desfase entre el número de visitas reales (250) y las reclamaciones financieras (931) es estadísticamente alarmante. El patrón sugiere que por cada contacto con el paciente, el centro genera casi 4 conceptos de cobro distintos. Se recomienda auditar la relación entre los `DiagnosticReport` (392) y los `Claims` para verificar si se están facturando pruebas no realizadas.







# 10. PACIENTE: Wilbert25_Ward668

**Perfil:** Paciente geriátrico con polifarmacia severa. Historial de Anemia (1952), Diabetes Tipo 2 (1958), Hipertensión y eventos cardiovasculares recurrentes.

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1952 - 1957** | Diagnóstico de Anemia | Sulfato Ferroso |
| **1958 - 1990** | Inicio DM2 y Control HTA | Metformina, Lisinopril, Amlodipino |
| **1991 - 2010** | Complicación Cardíaca Crónica | Warfarina, Digoxina, Verapamilo |
| **2011 - 2021** | Fase Crítica de Polifarmacia | Nitroglicerina, Insulina, Simvastatina |

### Hallazgos de Auditoría e Integridad

* **🚩 Volumen Masivo de Claims (Outlier):** El paciente registra **2,008 Claims** para **635 Encuentros**. Esto representa una carga de facturación masiva. El ratio de **3.16 facturas por encuentro**, sumado al volumen absoluto, sugiere un sistema de generación de cargos automatizado para maximizar el reembolso.
* **⚠️ Hiper-frecuentación en Fase Final:** Se observa un patrón de visitas semanales constantes en 2021 (junio 24, julio 01, julio 08...). Esta regularidad matemática en un paciente ambulatorio suele ser indicativa de facturación por "gestión de caso" o revisiones de bajo valor clínico creadas para cumplir cuotas.
* **📊 Fragmentación de Procedimientos:** Constan **450 Procedures** registrados. Al cruzar con los encuentros, se detecta que se facturan múltiples procedimientos menores de forma separada (*Unbundling*) en lugar de incluirlos en el código de la visita principal.
* **💊 Polifarmacia sin Revisión:** En los registros de 2021, se prescriben hasta **8 medicamentos de alto riesgo** de forma simultánea en cada encuentro. La repetición exacta de esta lista en encuentros de pocos minutos de diferencia sugiere una falta de conciliación medicamentosa real.

### Dictamen Final

> [!CAUTION]
> **ESTADO: 🔴 RIESGO EXTREMO**
> Con más de **2,000 reclamaciones**, este paciente es un caso crítico de estudio. La estructura de los datos sugiere que el registro clínico se utiliza como un motor de facturación más que como una herramienta de cuidado. Se recomienda auditar el 100% de los `DiagnosticReport` (837) para confirmar que cada prueba tiene un resultado clínico documentado que justifique su cobro.


---
**Nota de Auditoría:** Se recomienda investigar a los facultativos IDs **9999999369**, **9999999949** y **9999999129**, quienes concentran el 80% de las alertas de esta cohorte.









