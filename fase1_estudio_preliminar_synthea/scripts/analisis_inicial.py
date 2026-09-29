import json
import os
from collections import Counter

ruta_data = 'data/'
archivos = [f for f in os.listdir(ruta_data) if f.endswith('.json')]

print(f"--- RESUMEN DE AUDITORÍA ({len(archivos)} PACIENTES) ---\n")

for nombre_archivo in archivos:
    with open(os.path.join(ruta_data, nombre_archivo), 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    entradas = bundle.get('entry', [])
    
    # 1. Identificar al Paciente
    p_res = next((e['resource'] for e in entradas if e['resource']['resourceType'] == 'Patient'), None)
    nombre = f"{p_res['name'][0]['given'][0]} {p_res['name'][0]['family']}" if p_res else "Desconocido"
    
    # 2. Analizar Medicamentos
    recetas = [e['resource'] for e in entradas if e['resource']['resourceType'] == 'MedicationRequest']
    
    # Contamos cuántas veces aparece cada medicina
    conteo_meds = Counter([r.get('medicationCodeableConcept', {}).get('text', 'N/A') for r in recetas])
    
    # Buscamos médicos únicos (usando el ID que vimos antes)
    medicos_unicos = set()
    for r in recetas:
        ref = r.get('requester', {}).get('reference', 'Desconocido')
        id_medico = ref.split('|')[-1] if '|' in ref else ref
        medicos_unicos.add(id_medico)

    print(f"PACIENTE: {nombre}")
    print(f"  - Total recetas: {len(recetas)}")
    print(f"  - Médicos diferentes que han recetado: {len(medicos_unicos)}")
    print(f"  - Top 3 medicamentos más recetados:")
    for med, cant in conteo_meds.most_common(3):
        print(f"    * {med}: {cant} veces")
    print("-" * 40)

print("\n--- ANÁLISIS FINALIZADO ---")