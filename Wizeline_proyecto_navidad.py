#No olvides instalar el pip de openai
#pip install openai

import csv
import re
import openai
import os

# Pedir al usuario información relevante
nombre_archivo = input("Ingresa el nombre del archivo CSV (incluyendo la extensión .csv): ")
nombre_persona = input("Ingresa el nombre de la persona a la que le vas a dar el regalo: ")
genero_persona = input("Ingresa el genero de la persona: ")
edad_persona = input("Ingresa la edad aproximada de la persona: ")
datos_persona = "La persona tiene"+ edad_persona + " años y su genero es "+ genero_persona


# Pedir al usuario que ingrese la clave API
openai_api_key = input("Ingresa tu clave API de OpenAI: ")
os.environ["OPENAI_API_KEY"] = openai_api_key

#Lee el archivo csv, lo limita a 1000 usuarios como maximo y limpia los datos para que sean faciles de leer para la IA
def leer_y_limpiar_csv(nombre_archivo, limite=1000):
    seguidos = []
    with open(nombre_archivo, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and len(seguidos) < limite:  # Verifica si la fila no está vacía y si no se ha alcanzado el límite
                usuario = row[4]  # Asumiendo que los nombres de usuario están en la quinta columna (índice 4)
                usuario_limpio = re.sub(r'[0-9]', '', usuario)  # Eliminar números
                usuario_limpio = usuario_limpio.replace('_', ' ').replace('.', ' ')  # Reemplazar '_' y '.' con espacios
                seguidos.append(usuario_limpio)
            else:
                break  # Romper el bucle si se alcanza el límite
    return seguidos


def generar_recomendaciones_de_regalos(seguidos, openai_api_key):
    openai.api_key = openai_api_key

    # Crear un prompt que incluya los seguidos y pida recomendaciones de regalos
    prompt = "Basado en los siguientes intereses y personas seguidas: {}\n".format(", ".join(seguidos))
    prompt += "Por favor, sugiere 3 regalos baratos y fáciles de encontrar para Navidad."
    prompt += "Por favor ten encuenta también los siguientes factores de genero y edad aproximada: {}\n".format(", ".join(datos_persona))

    try:
        response = openai.Completion.create(
            model="gpt-4",  # modelo de ChatGPT-4
            prompt=prompt,
            max_tokens=3000 #Aproximadamente 0.05 dolares
        )
        return response.choices[0].text.strip().split('\n')
    except Exception as e:
        print(f"Error al generar recomendaciones: {e}")
        return []

# Guardar las recomendaciones de regalos
regalos = generar_recomendaciones_de_regalos(seguidos, openai_api_key)

#Generar los links de busqueda de amazon México
def generar_enlace_amazon(busqueda):
    palabras = busqueda.split()
    url_amazon = "https://www.amazon.com.mx/s?k=" + '+'.join(palabras)
    return url_amazon

# Guardar los enlaces
enlaces_amazon = [generar_enlace_amazon(regalo) for regalo in regalos]

#Texto introductorio para la lista de regalos
print(f"Dada la lista de seguidos que me diste de {nombre_persona}, pienso que estos regalos pueden gusarle: " )

for regalo, enlace in zip(regalos, enlaces_amazon):
    print(f"Regalo: {regalo}, Enlace de Amazon: {enlace}")
    
def generar_explicaciones(seguidos, regalos, nombre_persona):
    # Crear un prompt para explicar los regalos
    prompt = f"Explica por qué los siguientes regalos son adecuados para {nombre_persona}, quien sigue a estas personas y temas: {', '.join(seguidos)}.\n"
    for regalo in regalos:
        prompt += f"- {regalo}\n"
    prompt += "Explicación:"

    try:
        response = openai.Completion.create(
            model="gpt-4",  #modelo de ChatGPT-4
            prompt=prompt,
            max_tokens=500 #Aproximadamente 0.00833 dolares
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error al generar explicaciones: {e}")
        return ""

# Imprimir la explicación
explicaciones = generar_explicaciones(seguidos, regalos, nombre_persona)
print("La explicación para estos regalos es:", explicaciones)


#Generar la imagen con Dalle3
def generar_imagen_dalle(descripcion, openai_api_key):
    openai.api_key = openai_api_key

    try:
        response = openai.Image.create(
            model="dall-e-3",  #modelo de DALL·E 3
            prompt=descripcion,
            n=1,  # Número de imágenes a generar
            size="1024x1024"  # Tamaño de la imagen
        )
        return response.data[0]['url']  # URL de la imagen generada
    except Exception as e:
        print(f"Error al generar la imagen: {e}")
        return ""

# Imprimir la imagen
descripcion = f"Una escena navideña con un árbol decorado y los tres regalos sugeridos. Que son: {regalos}"
url_imagen = generar_imagen_dalle(descripcion, openai_api_key)
print("URL de la imagen generada:", url_imagen)


# Ejemplo de cálculo de costo considerando la longitud de las respuestas de ChatGPT y una imagen de DALL-E

# Tarifas estimadas
PRECIO_CHATGPT_POR_TOKEN = 0.00002  # Precio estimado por token para ChatGPT
PRECIO_DALLE_POR_IMAGEN = 0.02      # Precio por imagen generada por DALL·E

# Estimación de tokens: Asumiendo que cada token tiene aproximadamente 4 caracteres 
num_tokens_regalos = sum(len(regalo) for regalo in regalos) / 4
num_tokens_amazon = sum(len(enlace) for enlace in enlaces_amazon) / 4
num_tokens_explicacion = len("La explicación para estos regalos es: " + explicaciones) / 4

# Calcular el costo total de los tokens
costo_tokens = (num_tokens_regalos + num_tokens_amazon + num_tokens_explicacion) * PRECIO_CHATGPT_POR_TOKEN

# Calcular el costo total incluyendo una imagen de DALL·E
costo_total = costo_tokens + PRECIO_DALLE_POR_IMAGEN

print(f"El costo total en dolares americanos de esta ejecución fue de: ${costo_total:.5f}")


