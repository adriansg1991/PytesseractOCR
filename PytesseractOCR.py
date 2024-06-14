import os
import pandas as pd
import re
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd =r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Función para extraer información de una imagen
def extraer_informacion_imagen(ruta_imagen):
    texto = pytesseract.image_to_string(Image.open(ruta_imagen))

    # Expresiones regulares para extraer la fecha y el importe
    fecha_regex = r'(\d{2}) de (\w+) de (\d{4})'
    importe_regex = r'(\d+\.\d{2})'

    # Buscar fecha
    fecha_match = re.search(fecha_regex, texto)
    if fecha_match:
        dia = fecha_match.group(1)
        mes = fecha_match.group(2)
        año = fecha_match.group(3)

        # Convertir mes a número
        meses = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        mes_num = meses.get(mes.lower(), None)

        if mes_num:
            fecha = f"{dia}/{mes_num}/{año}"
    else:
        fecha = None

    # Buscar importe
    importe_match = re.search(importe_regex, texto)
    if importe_match:
        importe = float(importe_match.group(1))
    else:
        importe = None

    # Calcular el importe descontado
    importe_descontado = importe / 1.21
    
    # Calcular el 21% del importe
    impuesto = importe - importe_descontado

    return fecha, importe, impuesto, importe_descontado

# Carpeta donde se encuentran las imágenes
carpeta_imagenes = r"C:\Users\adria\Downloads\Tickets_sommelier"

# Lista para almacenar los resultados de cada imagen
resultados = []

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta_imagenes):
    if archivo.endswith(".png") or archivo.endswith(".jpg"):
        ruta_imagen = os.path.join(carpeta_imagenes, archivo)
        fecha, importe, impuesto, importe_descontado = extraer_informacion_imagen(ruta_imagen)
        resultados.append((archivo, fecha, importe, importe_descontado, impuesto))

# Crear DataFrame con los resultados
df = pd.DataFrame(resultados, columns=["Archivo", "Fecha", "Importe",  "Importe Sin IVA", "IVA(21%)"])

# Mostrar DataFrame
print(df)
