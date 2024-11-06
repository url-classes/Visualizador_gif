import os
import datetime

def read_bytes(file, num_bytes):
    byte_array = []
    for _ in range(num_bytes):
        byte = file.read(1)
        if byte:
            byte_array.append(ord(byte))
    return byte_array

def extract_gif_data(file_path):
    data = {}
    with open(file_path, 'rb') as file:
        # Firma y versión (primeros 6 bytes)
        header = read_bytes(file, 6)
        data['signature'] = ''.join(chr(b) for b in header[:3])
        data['version'] = ''.join(chr(b) for b in header[3:])

        # Tamaño de imagen
        width_bytes = read_bytes(file, 2)
        height_bytes = read_bytes(file, 2)
        data['width'] = width_bytes[0] + (width_bytes[1] << 8)
        data['height'] = height_bytes[0] + (height_bytes[1] << 8)

        # Color de fondo
        packed_field = read_bytes(file, 1)[0]
        data['global_color_table_flag'] = (packed_field & 0b10000000) >> 7
        data['color_resolution'] = (packed_field & 0b01110000) >> 4
        color_table_size = 2 ** ((packed_field & 0b00000111) + 1)
        data['color_count'] = color_table_size
        data['background_color_index'] = read_bytes(file, 1)[0]

        # Tipo de compresión de imagen
        data['compression_type'] = 'LZW'

        # Formato numérico
        data['numerical_format'] = '8-bit'

        # Leer fecha de creación y modificación del sistema
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        data['creation_date'] = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        data['modification_date'] = datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

        # Comentario en el archivo
        data['comments'] = extract_comments(file)

    return data


def extract_comments(file):
    comments = "No hay comentarios"
    while True:
        byte = file.read(1)
        if byte == b"\x21":
            extension = file.read(1)
            if extension == b"\xfe":
                comments = ""
                block_size = file.read(1)[0]
                while block_size != 0:
                    comment = file.read(block_size).decode("utf-8", "ignore")
                    comments += comment
                    block_size = file.read(1)[0]
            elif extension == b"\xf9":
                file.read(6)
        return comments
