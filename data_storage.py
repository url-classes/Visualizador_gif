import os
import random


def save_data(storage_path, data):
    with open(storage_path, 'w') as file:
        for gif_data in data:
            file.write("Archivo: " + gif_data['file_path'] + "\n")
            file.write("Versión: " + gif_data['version'] + "\n")
            file.write("Tamaño de Imagen: " + str(gif_data['width']) + "x" + str(gif_data['height']) + "\n")
            file.write("Cantidad de Colores: " + str(gif_data['color_count']) + "\n")
            file.write("Tipo de aCompresión: " + gif_data['compression_type'] + "\n")
            file.write("Formato Numérico: " + gif_data['numerical_format'] + "\n")
            file.write("Color de Fondo: " + str(gif_data['background_color_index']) + "\n")
            file.write("Fecha de Creación: " + gif_data['creation_date'] + "\n")
            file.write("Fecha de Modificación: " + gif_data['modification_date'] + "\n")
            file.write("Comentarios: " + gif_data['comments'] + "\n")
            file.write("-" * 40 + "\n")


def information(data):
    file = []
    for gif_data in data:
        file.append(gif_data['version'])
        file.append(str(gif_data['width']) + "x" + str(gif_data['height']))
        file.append(str(gif_data['color_count']))
        file.append(gif_data['file_path'])
        file.append(gif_data['compression_type'])
        file.append(gif_data['numerical_format'])
        file.append(str(gif_data['background_color_index']))
        file.append(str(random.randint(3, 45)))
        file.append(gif_data['creation_date'])
        file.append(gif_data['modification_date'])
        file.append(gif_data['comments'])
    return file


def load_data(storage_path):
    if not os.path.exists(storage_path):
        return []

    data = []
    with open(storage_path, 'r') as file:
        gif_data = {}
        for line in file:
            line = line.strip()
            if line.startswith("Archivo: "):
                gif_data['file_path'] = line.replace("Archivo: ", "")
            elif line.startswith("Versión: "):
                gif_data['version'] = line.replace("Versión: ", "")
            elif line.startswith("Tamaño de Imagen: "):
                size = line.replace("Tamaño de Imagen: ", "").split("x")
                gif_data['width'] = int(size[0])
                gif_data['height'] = int(size[1])
            elif line.startswith("Cantidad de Colores: "):
                gif_data['color_count'] = int(line.replace("Cantidad de Colores: ", ""))
            elif line.startswith("Tipo de Compresión: "):
                gif_data['compression_type'] = line.replace("Tipo de Compresión: ", "")
            elif line.startswith("Formato Numérico: "):
                gif_data['numerical_format'] = line.replace("Formato Numérico: ", "")
            elif line.startswith("Color de Fondo: "):
                gif_data['background_color_index'] = int(line.replace("Color de Fondo: ", ""))
            elif line.startswith("Fecha de Creación: "):
                gif_data['creation_date'] = line.replace("Fecha de Creación: ", "")
            elif line.startswith("Fecha de Modificación: "):
                gif_data['modification_date'] = line.replace("Fecha de Modificación: ", "")
            elif line.startswith("Comentarios: "):
                gif_data['comments'] = line.replace("Comentarios: ", "")
            elif line == "-" * 40:
                data.append(gif_data)
                gif_data = {}
    return data
