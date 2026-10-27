import os
import json

def ver_muestra():
    # Ruta del archivo generado en local
    ruta_archivo = os.path.join('data_procesada', 'medication_request_dataset_full2.jsonl')
    
    if not os.path.exists(ruta_archivo):
        print(f"❌ No se encuentra el archivo en: {ruta_archivo}")
        return
        
    print(f"🔍 Mostrando las primeras 5 líneas de: {ruta_archivo}\n")
    print("-" * 60)
    
    with open(ruta_archivo, 'rt', encoding='utf-8') as f:
        for i in range(5):
            linea = f.readline()
            if not linea:
                break  # Si el archivo tiene menos de 5 líneas
            
            # Parseamos el JSON para verlo ordenado y bonito
            datos = json.loads(linea.strip())
            print(f"Línea {i + 1}:")
            print(json.dumps(datos, indent=4, ensure_ascii=False))
            print("-" * 60)

if __name__ == '__main__':
    ver_muestra()