import os

def generar_sample():
    src = os.path.join('data', 'medication_request_dataset_full.jsonl')
    out = os.path.join('data', 'sample.jsonl')

    if not os.path.exists(src):
        print(f"❌ Error: No se encuentra el archivo principal en {src}")
        return

    print("⏳ Leyendo las primeras 10 líneas del dataset completo...")
    with open(src, 'rb') as f_in:
        primeras_10 = [f_in.readline() for _ in range(10)]

    with open(out, 'wb') as f_out:
        f_out.writelines(primeras_10)

    print(f"✅ ¡Sample generado con éxito en: {out}")

if __name__ == '__main__':
    generar_sample()