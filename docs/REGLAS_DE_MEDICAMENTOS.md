
---

# 🛡️ Guía Explicativa de Seguridad Clínica: Las 20 Reglas de Oro en la Prescripción de Medicamentos

---

Aquí tenemos las **20 reglas de negocio** adaptadas a lo que hemos visto en el EDA de **MIMIC-IV 2.2** (`MedicationRequest` FHIR, Train 2008 vs. Eval 2009 Q1).

---


## 📅 Bloque 1: Errores Posológicos y Duplicidades Críticas (Verificables por Coexistencia)

### Regla 1: Metotrexato Oral Diario

* **Medicamento Objetivo:** Metotrexato tomado en pastillas (para enfermedades como artritis o psoriasis, no para cáncer).
* **El Peligro:** Que se paute en el sistema para tomarse **todos los días** en lugar de **una sola vez a la semana**.
* **¿Qué es y para qué sirve?:** Es un medicamento muy potente que frena el sistema de defensa (inmunosupresor) para que no ataque a los tejidos del propio cuerpo.
* **¿Por qué está prohibido hacerlo diario?:** Este fármaco es tan agresivo que el cuerpo necesita descansar 6 días enteros para recuperarse. Si un médico se confunde y lo pauta a diario, el paciente sufre una **intoxicación masiva**: destruye la médula ósea (que fabrica la sangre), provoca llagas mortales en todo el tubo digestivo y causa un fallo multiorgánico letal.
* **Matiz según el EDA:** Si el fármaco aparece en la cola larga con pocas órdenes en 2008, no dependerá de un perfil estadístico fino sino de una regla clínica explícita sobre la pauta/frecuencia.

### Regla 2: Duplicidad de Anticoagulantes (Orales + Parenterales)

* **Medicamento Objetivo:** Mezclar una pastilla para la sangre (como Acenocumarol, Warfarina o un ACOD) con una inyección de anticoagulante (como Heparina).
* **El Peligro:** Recetar ambos tratamientos al mismo tiempo dentro del mismo encuentro clínico sin un protocolo de transición.
* **¿Por qué es crítico?:** Ambos fluidifican la sangre al máximo para que no se formen trombos.
* **El resultado:** La sangre pierde por completo su capacidad de coagular. Cualquier pequeño golpe interno o úlcera se convierte en una **hemorragia masiva e internalizada** (sangrado estomacal o cerebral) que puede costar la vida.
* **Matiz según el EDA:** En fármacos de alto volumen como *heparin* (donde en la gráfica 6 se ve una dosis muy dominante y en la gráfica 5 múltiples unidades/presentaciones), hay que comprobar qué unidad y presentación se usa en cada orden antes de comparar.

### Regla 3: Duplicidad de Opioides Mayores

* **Medicamento Objetivo:** Recetar dos analgésicos narcóticos potentes diferentes al mismo tiempo (ej. Morfina + Fentanilo).
* **El Peligro:** Administrarlos juntos en el mismo episodio asistencial sin una pauta de rescate justificada.
* **El riesgo:** Al duplicar la potencia para calmar el dolor, se saturan los receptores del cerebro, provocando una **sobredosis accidental con pérdida de consciencia y fallo respiratorio**.
* **Matiz según el EDA:** En el EDA vimos que *morphine sulfate* tiene un **31,2 %** de repeticiones del mismo fármaco dentro de la última hora (por ajustes/rescates) y un peso relevante en dosis no vigilables numéricamente; además, en la gráfica 6 vimos que *hydromorphone* tiene dos etiquetas en MIMIC (*hydromorphone* residual vs. *hydromorphone (dilaudid)* mayoritario), por lo que conviene normalizar nombres de fármacos para no pasar por alto duplicidades entre variantes.

### Regla 4: Duplicidad de Insulinas de Acción Rápida

* **Medicamento Objetivo:** Insulinas rápidas para el control de la glucosa.
* **El Peligro:** Prescribir dos tipos distintos de insulina rápida de forma concurrente en un mismo ingreso.
* **El riesgo:** El nivel de azúcar en sangre desciende de forma tan violenta y descontrolada que el cerebro se queda sin glucosa, induciendo un **coma hipoglucémico** irreversible si no se trata al instante.
* **Matiz según el EDA:** En el EDA *insulin* presenta un **42,4 %** de repeticiones en 1 hora y una distribución de dosis continua y variable (gráfica 6), además de aparecer entre los fármacos con órdenes sin dosis numérica válida (gráfica 4). La regla debe distinguir entre ajuste/repetición de una pauta y coexistencia de dos insulinas rápidas distintas, sin exigir siempre dosis numérica en las órdenes que no la traen.

---

## 👵 Bloque 2: Criterios por Edad y Población Geriátrica

### Regla 5: Benzodiazepinas de Acción Larga en Mayores de 65 años

* **Medicamento Objetivo:** Tranquilizantes o pastillas para dormir potentes y duraderas (como el *Diazepam*).
* **El Peligro:** Recetarlas a personas mayores de 65 años en el sistema.
* **¿Por qué es un problema?:** Con la edad, el cuerpo elimina los medicamentos mucho más despacio. Este tipo de fármacos se quedan "retenidos" en el organismo del anciano durante días.
* **¿Qué le pasa al paciente?:** Acumula tanta somnolencia que se queda permanentemente mareado, confundido (como si tuviera demencia repentina), pierde los reflejos y sufre **caídas graves con fracturas de cadera**.

### Regla 6: Antipsicóticos en Pacientes con Demencia (Sin Psicosis)

* **Medicamento Objetivo:** Fármacos fuertes para trastornos psiquiátricos graves (como el *Haloperidol* o la *Risperidona*).
* **El Peligro:** Dárselos a ancianos cuyos diagnósticos en el encuentro muestran demencia o Alzheimer sin una enfermedad psicótica real que lo justifique.
* **¿Por qué está desaconsejado?:** Aunque a veces se usaban para "calmar" al paciente, en personas con demencia estos medicamentos tienen efectos secundarios devastadores.
* **El daño en el cuerpo:** Disparan drásticamente el riesgo de sufrir un **ictus (derrame cerebral)** y multiplican la mortalidad prematura.

### Regla 7: Antidiabéticos Orales Antiguos (Sulfonilureas) en Ancianos

* **Medicamento Objetivo:** Pastillas para bajar el azúcar en sangre de acción prolongada (como la *Glibenclamida*).
* **El Peligro:** Usarlas en personas mayores de 65 años.
* **¿Qué ocurre?:** Estas pastillas fuerzan al páncreas a liberar insulina de forma prolongada. Como el metabolismo del anciano es más lento, el fármaco sigue actuando sin parar.
* **El resultado:** Provoca **hipoglucemias severas y prolongadas** (el azúcar cae a mínimos mortales), pudiendo dejar al paciente en coma.

### Regla 8: Mezclar Opioides y Benzodiazepinas en Mayores de 65 años

* **Medicamento Objetivo:** Juntar un analgésico potente (morfina) con un tranquilizante (lorazepam, diazepam) en mayores.
* **El Peligro:** Registrar ambos fármacos de forma simultánea en pacientes mayores de 65 años.
* **¿Por qué es una bomba de relojería?:** Los dos medicamentos actúan deprimiendo el sistema nervioso central.
* **El resultado:** Se potencian de forma exponencial. El cerebro se relaja tanto que **se olvida de mandar la orden de respirar**, provocando una parada respiratoria fulminante.
* **Matiz según el EDA:** Tanto *morphine sulfate* como *lorazepam* figuran entre los fármacos con mayor peso de órdenes sin dosis numérica vigilable (gráfica 4) y en *lorazepam* (gráfica 6) se ven picos claros de dosis habituales; la alerta de interacción debe basarse en la presencia/coexistencia del fármaco y no depender solo de que tenga dosis numérica.

### Regla 9: Fármacos con Alta Carga Anticolinérgica en Ancianos

* **Medicamento Objetivo:** Medicamentos para la alergia antiguos, mareos o algunos antidepresivos tricíclicos.
* **El Peligro:** Prescribirlos de forma continuada a pacientes con más de 65 años.
* **¿Qué hacen en el cuerpo?:** Bloquean la acetilcolina, una sustancia vital para la memoria y para mover los músculos internos.
* **El resultado:** El paciente sufre confusión mental aguda (*delirium*), sequedad extrema, retención urinaria severa y estreñimiento crítico.
* **Matiz según el EDA:** Como la gráfica 9 muestra que el grueso de intervalos entre órdenes consecutivas se concentra en torno a $10^3$ minutos y cerca de `1 día` (`1440 min`), evaluar "continuidad" exige mirar ventanas temporales más amplias (horas/días) que la ventana de 1 hora usada para repeticiones agudas.

---

## 🫘 Bloque 3: Contraindicaciones Orgánicas Cruzadas con Diagnósticos ICD

### Regla 10: AINEs (Ibuprofeno/Diclofenaco) en Insuficiencia Renal Crónica

* **Medicamento Objetivo:** Antiinflamatorios comunes como el ibuprofeno, naproxeno o diclofenaco.
* **El Peligro:** Dárselos a pacientes cuyos diagnósticos en el encuentro muestran fallo renal crónico.
* **¿Por qué es destructivo?:** Los antiinflamatorios bloquean las sustancias naturales que protegen y abren el riego sanguíneo que va hacia los riñones.
* **El resultado:** El riñón se queda sin flujo de sangre y colapsa de golpe (*fallo renal agudo*), provocando que los líquidos se encharquen peligrosamente en el organismo.

### Regla 11: Betabloqueantes no Selectivos en Asma o EPOC Severo

* **Medicamento Objetivo:** Medicamentos para la tensión o el corazón (como el *Propranolol*).
* **El Peligro:** Administrarlos a pacientes que tienen registrado un diagnóstico activo de asma o bronquitis crónica (EPOC).
* **¿Qué hacen?:** Calman el corazón, pero por similitud biológica bloquean también los conductos de aire de los pulmones.
* **El resultado:** Los bronquios del paciente se cierran de golpe, provocando un **ataque de asfixia severo (broncoespasmo mortal)**.

### Regla 12: AINEs Prolongados sin Protector Gástrico en Mayores de 65 años

* **Medicamento Objetivo:** Antiinflamatorios (Ibuprofeno, Naproxeno) en mayores de 65 años.
* **El Peligro:** Prescribir el AINE **sin** que aparezca simultáneamente un protector gástrico (Omeprazol o similar) en el mismo encuentro.
* **¿Qué hacen en el cuerpo?:** Destruyen la capa de moco protector que recubre las paredes del estómago frente a sus ácidos.
* **El resultado:** El ácido digiere la pared estomacal, provocando una **úlcera sangrante o una perforación** que puede pasar desapercibida hasta causar una hemorragia grave.

### Regla 13: Antibióticos Aminoglucósidos (Gentamicina) con Diagnóstico de Fallo Renal

* **Medicamento Objetivo:** Antibióticos potentes para infecciones graves (como Gentamicina o Amikacina).
* **El Peligro:** Prescribirlos a pacientes con problemas renales previos registrados.
* **El daño:** Estos antibióticos son altamente tóxicos para los filtros del riñón y el oído interno.
* **El resultado:** Aceleran un **fallo renal irreversible** y pueden causar sordera permanente.

### Regla 14: Metformina en Pacientes con Acidosis o Fallo Renal Severo

* **Medicamento Objetivo:** Metformina (fármaco para la diabetes).
* **El Peligro:** Recetarla a pacientes con registros de fallos metabólicos graves o riñón muy deteriorado.
* **El resultado:** Al no eliminarse correctamente, se acumula en la sangre provocando una complicación metabólica letal llamada *acidosis láctica*.

---

## ⚠️ Bloque 4: Restricciones de Dosis y Posología Estructurada

### Regla 15: Metotrexato Oral con Frecuencia Diaria en la Pauta

* **Medicamento Objetivo:** Metotrexato oral.
* **El Peligro:** Que el campo de texto de la dosis (`dosage_text`) indique una frecuencia diaria en lugar de semanal.
* **El resultado:** Intoxicación masiva que destruye la médula ósea y provoca un fallo multiorgánico letal.

### Regla 16: Omisión de Ácido Fólico junto al Metotrexato

* **Medicamento Objetivo:** Metotrexato oral.
* **El Peligro:** Encontrar la prescripción de metotrexato en el historial del paciente **sin** rastro de la co-prescripción de Ácido Fólico.
* **El resultado:** El fármaco arrasa con las células sanas del estómago e intestino, provocando una toxicidad gastrointestinal grave e innecesaria.

### Regla 17: Digoxina a Dosis Altas en Pacientes Mayores de 65 años

* **Medicamento Objetivo:** Digoxina (para el corazón y arritmias).
* **El Peligro:** Registrar una dosis numérica (`dose_value`) superior a $0.125\text{ mg/día}$ en un paciente con `edad_real > 65`.
* **El resultado:** Como el cuerpo del anciano la elimina peor (corregido el error tipográfico "Peor"), se acumula de inmediato generando una **intoxicación digitálica** (arritmias cardíacas caóticas y parada).
* **Matiz según el EDA:** Al comparar dosis numéricas, debe verificarse primero que la orden tenga dosis numérica válida (`> 0`) y que la unidad sea comparable (ej. `mg`), ya que el 10,8 % de órdenes en 2008 carece de dosis válida y el 60 % de órdenes pertenece a fármacos con múltiples unidades.

---

## 🏥 Bloque 5: Seguridad Estructural y Antecedentes de Paciente

### Regla 18: Antipsicóticos en Pacientes con Antecedentes de Ictus

* **Medicamento Objetivo:** Fármacos antipsicóticos.
* **El Peligro:** Prescribirlos a pacientes cuyos diagnósticos previos incluyan historia de accidente cerebrovascular (ictus).
* **El resultado:** Elevan drásticamente la probabilidad de sufrir nuevos eventos vasculares cerebrales y aumentan la mortalidad.

### Regla 19: Opioides Mayores en Pacientes con Historial de Abuso de Sustancias

* **Medicamento Objetivo:** Opioides potentes (morfina, fentanilo, oxicodona).
* **El Peligro:** Recetarlos a pacientes con diagnósticos previos de dependencia o abuso de sustancias narcóticas.
* **El resultado:** Alto riesgo de recaída, sobredosis intencionada o dependencia severa no controlada.

### Regla 20: Uso de la Abreviatura "U" en lugar de "Unidades"

* **Medicamento Objetivo:** Insulinas y Heparinas.
* **El Peligro:** Que el texto de la prescripción emplee la letra "U" aislada en lugar de la palabra completa "unidades".
* **El desastre:** Al leerse de forma rápida, la "U" se confunde con un cero (`0`) o un cuatro (`4`), provocando que se administren **diez veces más cantidad de fármaco**, lo que genera una sobredosis letal.
* **Matiz según el EDA:** En la gráfica 5 vimos que el 60 % de las órdenes recae en fármacos con varias unidades y en la gráfica 6 que *heparin* e *insulin* se miden en `UNIT` (además de haber otras unidades como `mL`/`ml` en *heparin*), por lo que normalizar y validar la unidad antes de interpretar la magnitud numérica es clave.



