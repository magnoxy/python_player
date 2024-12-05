# Funções utilitárias

import os

print(f"Diretório atual: {os.getcwd()}")

def delete_files_from_folder(folder):
    # Verifica se a pasta existe
    if os.path.exists(folder) and os.path.isdir(folder):
        # Itera sobre todos os arquivos dentro da folder
        for arquivo in os.listdir(folder):
            path_file = os.path.join(folder, arquivo)
            # Verifica se é um arquivo e deleta
            if os.path.isfile(path_file):
                os.remove(path_file)
                print(f"Arquivo deletado: {path_file}")
            else:
                print(f"Não é um arquivo: {path_file}")
    else:
        print(f"A pasta '{folder}' não existe ou não é uma pasta.")


