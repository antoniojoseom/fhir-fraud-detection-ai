import os
import orjson
from collections import Counter

output_file = os.path.join('data', 'medication_request_dataset_full.jsonl')

print("🔍 Auditoría profunda de 'encounter_procedures'...")

conteo_procs = Counter()
total_lineas = 0

if not os.path.exists(output_file):
    print(f"❌ Error: No se encuentra el archivo en {output_file}")
else:
    with open(output_file, 'rb') as f:
        for line in f:
            total_lineas += 1
            fila = orjson.loads(line)
            
            # Cogemos el valor tal cual viene guardado
            procs = fila.get('encounter_procedures', 'CAMPO_AUSENTE')
            conteo_procs[procs] += 1

    print(f"\n========================================")
    print(f"📊 Resumen de la auditoría (Total líneas: {total_lineas}):")
    print(f"========================================")
    for texto, frecuencia in conteo_procs.most_common(10):
        print(f"[{frecuencia} veces] -> {texto}")
    print(f"========================================")