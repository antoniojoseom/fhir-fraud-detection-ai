import pandas as pd
import os

# Ajusta el nombre según el archivo que tengas en la carpeta 'data/'
# (por ejemplo, 'prescriptions.csv.gz' o el nombre exacto que le hayas puesto)
nombre_archivo = "prescriptions.csv.gz" # Cámbialo si tiene otro nombre
ruta_archivo = os.path.join('data', nombre_archivo)

print(f"🔍 Leyendo las primeras filas de {nombre_archivo}...")

try:
    # Pandas detecta la compresión automáticamente si termina en .gz o .zip
    df = pd.read_csv(ruta_archivo, nrows=5)
    
    print("\n📋 Columnas encontradas en el CSV original:")
    print(list(df.columns))
    
    print("\n👀 Primeras filas (muestra):")
    print(df.head())

except Exception as e:
    print(f"❌ Error al leer el archivo: {e}")