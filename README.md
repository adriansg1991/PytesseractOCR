# ℹ️ Pytesseract: OCR (image to text)
[![Python Version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Pytesseract](https://img.shields.io/pypi/v/pytesseract)](https://pypi.org/project/pytesseract/)
[![Pandas](https://img.shields.io/badge/pandas-1.2.0+-yellow)](https://pandas.pydata.org/)
<div id="header" align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm1tN3Zsdm81cjVjZTJscmExdmV2eTM3YmlkN2hzZHFhbDA2YXRmdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Zebztgv7jmkoLe1DoY/giphy.gif" width="100"/>
</div>

En el mundo de la programación, a menudo nos enfrentamos a desafíos que requieren habilidades de reconocimiento de patrones. Pero, ¿qué pasa cuando esos patrones están atrapados en imágenes? Aquí es donde entra en juego pytesseract, una poderosa herramienta de reconocimiento óptico de caracteres (OCR) en Python. En este artículo, exploraremos qué es pytesseract, cómo funciona y cómo puede revolucionar la forma en que interactuamos con imágenes que contienen texto.

## ¿Qué es pytesseract?
Pytesseract es una interfaz Python para la popular herramienta de OCR llamada Tesseract-OCR. Tesseract es un motor de reconocimiento óptico de caracteres de código abierto desarrollado originalmente por HP y ahora mantenido por Google. Lo que hace pytesseract es permitirnos utilizar la funcionalidad de Tesseract-OCR dentro de nuestros programas Python, lo que facilita enormemente la extracción de texto de imágenes.

### ¿Para qué sirve?
La utilidad principal de pytesseract es convertir texto contenido en imágenes en texto digitalizable. Imagina que tienes una fotografía de un recibo o un ticket de compra. Con pytesseract, puedes extraer automáticamente el texto de esa imagen, convirtiéndolo en una cadena de texto que puedes manipular y utilizar en tus programas o análisis de datos.

### ¿Cómo se utiliza?
El proceso de utilizar pytesseract es sorprendentemente sencillo. Primero, necesitas instalar la librería pytesseract y Tesseract-OCR en tu sistema. Una vez instalado, puedes utilizar pytesseract para cargar una imagen y extraer el texto de ella con solo unas pocas líneas de código Python.

Aquí tienes un ejemplo básico:
```python
import pytesseract
from PIL import Image

# Cargar la imagen
img = Image.open('imagen.jpg')

# Utilizar pytesseract para extraer el texto
texto = pytesseract.image_to_string(img)

# Imprimir el texto extraído
print(texto)
```
## Caso Práctico: Extracción de Información de Tickets de Datafono con Pytesseract
ecientemente, un amigo mío abrió un negocio y me pidió ayuda para extraer información de los tickets del datáfono, específicamente la fecha y el importe. Sin embargo, el importe en los tickets incluía el IVA, por lo que también necesitábamos eliminarlo. Para abordar este desafío, decidí utilizar pytesseract en Python junto con pandas para automatizar el proceso.

Primero, utilicé pytesseract para extraer el texto de las imágenes de los tickets. Esto me permitió obtener los datos en formato de texto, que luego procesé con pandas para estructurarlos en un DataFrame de Python. En este DataFrame, agregué una nueva columna para calcular el importe sin IVA, lo cual fue bastante sencillo gracias a las funciones de pandas.

Una vez que tuve el DataFrame completo y actualizado, exporté los datos a un archivo Excel utilizando las capacidades de exportación de pandas.

Para completar el proceso, automatizamos el análisis de múltiples imágenes de tickets almacenadas en una carpeta específica. Utilizando un bucle en Python, iteramos a través de todas las imágenes en la carpeta, aplicamos el mismo proceso de extracción de información con pytesseract y pandas, y finalmente almacenamos los resultados en un único archivo Excel.

Este enfoque nos permitió manejar eficientemente grandes cantidades de datos de tickets del datáfono, proporcionando una forma rápida y precisa de analizar la información financiera de su negocio.

En resumen, la combinación de pytesseract y pandas en Python facilitó enormemente la extracción y manipulación de datos de tickets del datáfono.

¡Espero que encuentres útil este ejemplo práctico y te anime a explorar las posibilidades de automatización que ofrecen estas herramientas!

A continuación, os comparto el script utilizado para automatizar esta tarea:
```python
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

`````
![Df](https://github.com/adriansg1991/PytesseractOCR/blob/main/Df.png)

![Df_Ticket](https://github.com/adriansg1991/PytesseractOCR/blob/main/df_Ticket.png)


## 📬 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de [mi correo electrónico](mailto:adriansg1991@gmail.com) o en [Linkedin](https://linkedin.com/in/adriansanchez-garcia/).

¡Gracias por visitar el repositorio! 🚀

