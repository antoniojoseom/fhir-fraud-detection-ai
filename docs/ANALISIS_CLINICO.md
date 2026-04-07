### 1. PACIENTE: Adolfo777_Yost751
**Perfil:** Crónico Multipatológico (Diabetes Tipo 2, Oncología y Demencia).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1968 - 1969** | Inicio Hipertensión y Tabaquismo | Lisinopril, Parches Nicotina |
| **1970 - 1999** | **Cronicidad Metabólica** (Diabetes T2) | Metformina (Uso continuado) |
| **2000** | **Hito Oncológico** (Cáncer Próstata) | Docetaxel, Leuprolide |
| **2004** | Deterioro Cognitivo Inicial | Galantamina |
| **2005 - 2019** | Gestión de Pluripatología Compleja | Multiterapia Crónica |

#### **Hallazgos de Auditoría e Integridad**
* **Hiper-frecuentación (Volumetría):** Volumen masivo de **1.033 Claims** y **641 MedicationRequests** frente a solo 392 encuentros.
* **Anomalía de Registro (1996-10-07):** Encuentro administrativo con médico 9999999909 donde **no consta medicación** (N/A), rompiendo la serie lógica del tratamiento.
* **Dictamen:** **Riesgo Alto.** Incoherencia crítica en la ratio: **1,6 recetas por cada encuentro**. La desproporción sugiere un escenario de "Upcoding" o automatización de facturación por servicios recurrentes sin justificación clínica presencial.


### 2. PACIENTE: Alvaro283_Altenwerth646
**Perfil:** Crónico Multipatológico (Oncología, Cardiología y Demencia).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1945 - 1993** | Hipertensión y Tabaquismo | Lisinopril, Parches Nicotina |
| **1994 - 1996** | **Hito Oncológico** (Cáncer Próstata) | Docetaxel, Leuprolide |
| **1997 - 2004** | Fibrilación/Insuficiencia Cardíaca | Warfarina, Digoxina |
| **2004** | **Evento Isquémico Agudo** (Infarto) | Nitroglicerina, Clopidogrel |
| **2010 - 2019** | Deterioro Cognitivo (Alzheimer) | Galantamina, Memantina |

#### **Hallazgos de Auditoría e Integridad**
* **Alerta de "Doctor Shopping":** Uso de 3 facultativos distintos para HTA en la etapa temprana.
* **Anomalía de Registro (2004-12-19):** Detectada **duplicidad de recetas** en un mismo encuentro (Clopidogrel y Nitroglicerina). 
* **Dictamen:** **Riesgo Moderado.** Incoherencia volumétrica: **299 recetas vs 97 encuentros**. Esta ratio sugiere un posible inflado de facturación mediante la automatización de prescripciones sin visita presencial vinculada.



### 3. PACIENTE: Mayola305_Sanford861
**Perfil:** Crónico Complejo (Endocrinología, Cardiología y Salud Ósea).

| Periodo | Evolución Clínica | Medicación Clave |
| :--- | :--- | :--- |
| **1970 - 1989** | Seguimiento Endocrino | Levotiroxina |
| **1990 - 1996** | Control de Dislipemia | Simvastatina (10mg) |
| **1997 - 2003** | Registro Cardiovascular | Clopidogrel, Nitroglicerina |
| **2004 - 2007** | Eventos de Falla Cardíaca | Warfarina, Digoxina, Verapamilo |
| **2008 - 2021** | Registro de Polimedicación | Alendronato, Tratamiento Combinado |

#### **Hallazgos de Auditoría e Integridad (Detección de Fraude/Error)**
* **Alerta de Duplicidad en Facturación (Redundancia):** Se detecta la carga de múltiples recetas idénticas de **Clopidogrel y Nitroglicerina** en encuentros únicos (ej. 1997-01-24 y 2013-04-26). Este patrón sugiere una posible **duplicidad de cobros** por el mismo concepto en un solo acto médico.
* **Conflicto de Prescripción Multi-Facultativo:** Registro concurrente de Simvastatina en dos dosis distintas (10mg y 20mg) emitidas por dos IDs médicos diferentes (9999999669 y 9999910659). Esta falta de conciliación es un indicador de **fragmentación administrativa** que facilita la sobre-prescripción y el gasto farmacéutico innecesario.
* **Anomalía de "Upcoding" (2012-11-30):** Registro de **Alteplase** (fármaco trombolítico de alto coste/hospitalario) vinculado a un encuentro de tipo "Revisión" (bajo coste). La discrepancia entre el nivel del servicio y el coste del insumo sugiere un posible inflado de factura o error grave en la codificación del servicio.
* **Dictamen:** **Riesgo Moderado-Alto.** Incoherencia volumétrica: **205 recetas vs 69 encuentros**. Con una ratio de **2,97 recetas por visita**, el volumen de prescripciones automáticas sin respaldo de actividad clínica presencial indica un riesgo elevado de facturación irregular por servicios crónicos.



### 4. PACIENTE: Melinda114_Rodriguez71
**Perfil:** Paciente Geriátrico con Hipertensión Crónica y Diabetes Tipo 2.

| Periodo | Evolución Administrativa | Medicación Clave (Patrón de Carga) |
| :--- | :--- | :--- |
| **1951 - 1952** | Inicio de Co-Prescripción | Lisinopril, Amlodipino (Alternancia de IDs médicos) |
| **1953 - 1959** | Estabilización de Combo HTA | Hidroclorotiazida + Lisinopril + Amlodipino |
| **1960 - 1972** | Mantenimiento Crónico | Triple terapia constante (Sin cambios de dosis) |
| **1973 - 1986** | Expansión Metabólica | Inclusión de Metformina (Dosis fija 500mg) |
| **1987 - 1993** | Intensificación de Recursos | Adición de Insulina + Explosión de Revisiones semanales |

#### **Hallazgos de Auditoría e Integridad (Detección de Fraude/Error)**
* **Patrón de "Churning" (Visitas Innecesarias):** Se detecta una frecuencia de encuentros anómala en los años 90 (ej. visitas el 1991-06-12, 1991-06-13 y 1991-06-19). Facturar tres revisiones en una semana para una patología crónica estable es un indicador clásico de generación artificial de actividad para aumentar los ingresos por visita.
* **Inconsistencia de Roles Médicos:** Los médicos **9999933569** y **9999999969** se alternan para emitir exactamente las mismas recetas en días consecutivos. Esta falta de asignación de un "médico responsable" sugiere una gestión administrativa deficiente que permite la **duplicidad de reclamaciones (Claims)** por gestión de medicación.
* **Ratio de Facturación Inflada (Unbundling):** El expediente muestra 2,054 Reclamaciones (Claims) frente a solo 775 Encuentros. Esta ratio de **2.65 reclamaciones por visita** indica que el centro médico podría estar "desglosando" servicios básicos en múltiples códigos de cobro para maximizar el reembolso de las aseguradoras.
* **Automatización de Recetas sin Acto Clínico:** Con 1,279 `MedicationRequest` y solo 775 encuentros, existe un excedente de **504 solicitudes de medicación** que no coinciden con una visita física. Esto supone un riesgo de facturación de fármacos no entregados o prescripciones automáticas sin supervisión.

#### **Dictamen de Auditoría**
**Nivel de Riesgo: MUY ALTO.** La combinación de **Churning** (exceso de visitas) y **Unbundling** (exceso de reclamaciones por visita) sitúa a este paciente como el caso principal para una investigación de fraude por sobreutilización de recursos. La eficiencia administrativa es nula, favoreciendo el inflado de la cuenta de resultados del prestador de salud.




### 5. PACIENTE: Neida631_Upton904
**Perfil:** Paciente Geriátrico con Hipertensión persistente y aparición de deterioro cognitivo (Alzheimer/Demencia).

| Periodo | Evolución Administrativa | Medicación Clave (Patrón de Carga) |
| :--- | :--- | :--- |
| **1941 - 1942** | Fase de Ajuste | Inicio Lisinopril, Amlodipino e Hidroclorotiazida. |
| **1943 - 1981** | Estabilidad de "Reloj" | Triple terapia HTA. Visitas anuales con alta precisión temporal. |
| **1982 - 2000** | Continuidad Crónica | Mantenimiento sin variaciones clínicas en 18 años. |
| **2001 - 2005** | Quiebre Cognitivo | Inicio de **Donepezilo**. Aumento súbito de la frecuencia de encuentros. |
| **2006 - 2012** | Fase de Fragmentación | Visitas con días de diferencia y polifarmacia (AINEs, Antibióticos). |

---

#### **Hallazgos de Auditoría e Integridad (Detección de Fraude/Error)**

* **Patrón de "Self-Referral" y Visitas en Cascada:** A partir del diagnóstico de deterioro cognitivo en 2001, la frecuencia de encuentros rompe el patrón anual histórico. Se observan grupos de visitas extremadamente cercanos (ej. **2002-08-04, 2002-08-05 y 2002-08-12**). En auditoría forense, esto se clasifica como **generación de encuentros de baja utilidad clínica** con el único fin de facturar el código de visita (`Encounter`).
* **Inconsistencia en la Carga de Reclamaciones (Claims):** El sistema registra **324 Claims** para solo **97 Encuentros**. Esto arroja una ratio de **3.33 reclamaciones por visita**, la métrica más alarmante detectada en el dataset. Sugiere una práctica agresiva de **Unbundling** (desagregación de servicios), donde procedimientos mínimos que deberían ir en un solo paquete se facturan por separado para maximizar el reembolso.
* **Prescripciones "Fantasma" o Huérfanas:** El recuento de **227 MedicationRequests** frente a los 97 encuentros documentados muestra que más del 50% de las recetas se emiten sin un acto médico presencial que las sustente. Esto indica un riesgo elevado de **automatización de recetas** para justificar cobros por gestión de farmacia sin supervisión clínica real.
* **Uso Oportunista de la Fragilidad Cognitiva:** La alternancia entre los médicos **9999956809** y **9999999839** se vuelve errática tras la aparición del Alzheimer. Mientras uno mantiene la cronicidad, el otro aparece brevemente para recetar analgésicos en visitas consecutivas, lo que indica una **fragmentación del cuidado** deliberada para multiplicar los cargos de consulta.

#### **Dictamen de Auditoría**
**Nivel de Riesgo: ALTO (Fraude por Fragmentación y Sobreutilización).** El perfil de este paciente demuestra una transición de "mantenimiento pasivo" a "explotación activa de recursos" coincidiendo con su pérdida de autonomía cognitiva. La ratio de 3.33 claims/visita es el indicador técnico principal para recomendar una auditoría de campo, ya que es altamente probable la existencia de facturación por servicios no prestados o duplicidad de cargos.



### 6. PACIENTE: Oswaldo857_Leffler128
**Perfil:** Paciente con Hipertensión, Diabetes Insulinodependiente y Salud Mental (Depresión).

| Periodo | Evolución Administrativa | Medicación Clave (Patrón de Carga) |
| :--- | :--- | :--- |
| **1940 - 1959** | Antecedentes | Periodo de baja actividad. |
| **1960 - 1961** | Inicio Salud Mental | Introducción de Sertralina y analgésicos opioides. |
| **1962 - 1968** | Gestión HTA | Estabilización con Hidroclorotiazida y Amlodipino. |
| **1969 - 1989** | Escalada Diabética | Introducción de **Insulina Humulin**. Inicio de visitas multifrecuencia. |
| **1990 - 1995** | Explosión de Datos | Hiper-frecuencia de encuentros (mensuales o semanales). |

---

#### **Hallazgos de Auditoría e Integridad (Detección de Fraude/Error)**

* **Volumen Masivo Anomalía (Outlier):** Con **2,103 Observaciones** y **612 Encuentros**, este paciente genera un volumen de datos que triplica la media. En auditoría forense, un número tan alto de `Observation` (constantes, pesos, analíticas) suele utilizarse para justificar la complejidad de un paciente y así aplicar **Upcoding** (facturar niveles de consulta más caros).
* **Patrón de "Doctor Shopping" o Monopolio de ID:** A diferencia de otros casos, aquí el médico **9999999129** firma prácticamente todo. La persistencia de este ID en cientos de registros de Insulina en intervalos de tiempo mínimos (ej. **1992-01-24 y 1992-01-26**) sugiere una **automatización de clics** o un sistema de "copiar y pegar" expedientes para generar facturación por encuentro.
* **Ratio de Claim vs. Encounter:** Presenta **1,551 Claims** para 612 encuentros. Aunque la ratio es de **2.53**, el volumen absoluto es tan alto que cualquier error sistemático en la codificación se traduce en pérdidas (o ganancias ilícitas) de miles de euros/dólares.
* **Inconsistencia de "MedicationRequest":** Registra **939 solicitudes de medicación**. Teniendo en cuenta que muchos son para Insulina, la frecuencia de renovación es excesiva incluso para un paciente mal controlado. Esto podría indicar **reabastecimiento preventivo (Stockpiling)** facturado a la aseguradora pero no necesariamente entregado al paciente.
* **Hiper-fragmentación (Churning Extremo):** Se observan episodios con apenas 48 horas de diferencia (enero de 1992). Clínicamente, no hay cambio en el tratamiento que justifique una revisión presencial tan cercana, lo que apunta a **facturación por visitas de seguimiento innecesarias**.

#### **Dictamen de Auditoría**
**Nivel de Riesgo: CRÍTICO.** Este es un caso de libro para una auditoría de "Eficiencia de Recursos". La cantidad de **DiagnosticReports (789)** y **Observations (2,103)** indica una monitorización que roza el acoso clínico o, más probablemente, una **inflación de la historia clínica** para blindar las reclamaciones de pago ante posibles revisiones de la aseguradora. Se recomienda inspección técnica de los registros de entrada al sistema para verificar si las visitas fueron reales.






