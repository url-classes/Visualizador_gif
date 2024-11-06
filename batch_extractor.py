import os
from gif_extractor import extract_gif_data


def find_gif_files(directory_path):
    gif_data_list = []
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.lower().endswith('.gif'):
                file_path = os.path.join(root, file_name)
                gif_data = extract_gif_data(file_path)
                gif_data['file_path'] = file_path
                gif_data_list.append(gif_data)
    return gif_data_list
