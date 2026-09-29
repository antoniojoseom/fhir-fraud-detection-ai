import json
import os

ruta_data = 'data/'
ruta_output = 'docs/analisis_pacientes/'  # Nueva subcarpeta para orden

# Creamos la carpeta si no existe
if not os.path.exists(ruta_output):
    os.makedirs(ruta_output)

archivos = [f for f in os.listdir(ruta_data) if f.endswith('.json')]

print(f"Procesando {len(archivos)} pacientes individualmente...")

for nombre_archivo in archivos:
    with open(os.path.join(ruta_data, nombre_archivo), 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    entradas = bundle.get('entry', [])
    
    # Obtener nombre del paciente para el nombre del archivo
    p_res = next((e['resource'] for e in entradas if e['resource']['resourceType'] == 'Patient'), None)
    nombre_p = f"{p_res['name'][0]['given'][0]}_{p_res['name'][0]['family']}" if p_res else "Desconocido"
    
    # Nombre del TXT de salida
    nombre_salida = f"informe_{nombre_p}.txt"
    ruta_final = os.path.join(ruta_output, nombre_salida)

    with open(ruta_final, 'w', encoding='utf-8') as f_out:
        f_out.write(f"INFORME MÉDICO DETALLADO: {nombre_p}\n")
        f_out.write("="*50 + "\n")
        
        # 1. Recuento
        f_out.write("1. RECUENTO DE RECURSOS\n")
        tipos = {}
        for e in entradas:
            t = e['resource']['resourceType']
            tipos[t] = tipos.get(t, 0) + 1
        for t, cant in sorted(tipos.items()):
            f_out.write(f"   - {t}: {cant}\n")

        # 2. Cronología
        f_out.write("\n2. CRONOLOGÍA ASISTENCIAL\n")
        encuentros = [e['resource'] for e in entradas if e['resource']['resourceType'] == 'Encounter']
        encuentros.sort(key=lambda x: x.get('period', {}).get('start', '0000'))

        for enc in encuentros:
            fecha = enc.get('period', {}).get('start', '????')[:10]
            id_enc = enc.get('id')
            motivo = enc.get('reasonCode', [{}])[0].get('text', 'Revisión')
            
            f_out.write(f"\n[{fecha}] Episodio: {motivo}\n")
            
            # Buscar sus recetas
            for e in entradas:
                res = e['resource']
                if res['resourceType'] == 'MedicationRequest':
                    if id_enc in res.get('encounter', {}).get('reference', ''):
                        med = res.get('medicationCodeableConcept', {}).get('text', 'N/A')
                        medico = res.get('requester', {}).get('reference', '').split('|')[-1]
                        dosis = res.get('dosageInstruction', [{}])[0].get('text', 'N/A')
                        f_out.write(f"   > MED: {med} | MÉDICO: {medico} | DOSIS: {dosis}\n")

    print(f"   - Generado: {nombre_salida}")

print(f"\n¡Hecho! Revisa la carpeta: {ruta_output}")