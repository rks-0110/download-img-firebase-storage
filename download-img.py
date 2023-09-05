import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import requests
import json
import os
from datetime import datetime

# *******************************************************
# CONTA QUANTIDADE DE IMAGENS NO BUCKET
# *******************************************************

def conta_img_no_bucket(bucket, prefixo):
    blobs = bucket.list_blobs(prefix=prefixo)
    image_count = 0

    for blob in blobs:
        if blob.name.endswith('.jpeg'):
            image_count += 1

    return image_count

# *******************************************************
# CRIA DIRETORIOS PARA SALVAR IMAGENS BAIXADAS
# *******************************************************

# Carrega dados do Json importado
with open('romaneio_ent-export.json', 'r') as json_file:
    dados = json.load(json_file)

# Dia de hoje formato dd-MM-yyyy
hoje = datetime.now().strftime('%d-%m-%Y')

# Cria diretorio para guardar dados
output_directory = hoje
os.makedirs(output_directory, exist_ok=True)


def organiza_fotos():
    for key, snapshot in dados.items():
        if hoje in key:
            dir_key = os.path.join(output_directory, key)
            os.makedirs(dir_key, exist_ok=True)

            for childSnapshot in snapshot:
                if childSnapshot and "num_doc" in childSnapshot:
                    num_doc_value = childSnapshot["num_doc"]
                    dir_num_doc = os.path.join(dir_key, str(num_doc_value))
                    os.makedirs(dir_num_doc, exist_ok=True)

                    print(f"Key: {key}, num_doc: {num_doc_value}")

                    baixa_fotos(dir_key, num_doc_value)
                    baixa_assinatura(dir_key, num_doc_value)


# *******************************************************
# INICIALIZA FIREBASE
# *******************************************************

# Ler URL do bucket do Firebase Storage
caminho_arquivo = 'bucket-url.txt'
try:
    with open(caminho_arquivo, 'r') as arquivo_bucket:
        bucket_url = arquivo_bucket.read()
        print(bucket_url)
except FileNotFoundError:
    print(f'Arquivo {caminho_arquivo} não encontrado.')
except Exception as e:
    print(f'Exception: {str(e)}')


# Inicia Firebase Admin SDK
cred = credentials.Certificate('./credentials.json')  # Arquivo de chave de acesso (credentials.json)
firebase_admin.initialize_app(cred, {
    'storageBucket': bucket_url  # Arquivo contendo URL do bucket do Firebase Storage
})
# Reference to the default Firebase Storage bucket
bucket = storage.bucket()


# *******************************************************
# BAIXA IMAGENS DE HOJE
# *******************************************************
def baixa_fotos(key_directory, num_doc_value):
    # Especifica caminho para arquivos no firebase storage
    prefix = f'imagens/{num_doc_value}/fotos/imagem'

    # Determina número de fotos no bucket
    num_img = conta_img_no_bucket(bucket, prefix)

    for i in range(num_img):
        # Caminho foto (Firebase Storage)
        caminho_arquivo = f'{prefix}{i}.jpeg'
        # Cria uma URL de download para o arquivo
        blob = bucket.blob(caminho_arquivo)
        download_url = blob.generate_signed_url(expiration=6000000000)  # Obrigatorio (?) validade do link

        print("Photo Download URL:", download_url)

        local_file_path = os.path.join(key_directory, str(num_doc_value), f'imagem{i}.jpeg')
        response = requests.get(download_url)

        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, 'wb') as file:
                file.write(response.content)
                print(f'Foto salva em {local_file_path}')
        else:
            print((f'Falha ao fazer download da foto. http status code: {response.status_code}'))


def baixa_assinatura(key_directory, num_doc_value):
    file_path = f'imagens/{num_doc_value}/assinatura/assinatura-{num_doc_value}.jpeg'
    blob = bucket.blob(file_path)
    download_url = blob.generate_signed_url(expiration=6000000000)

    print("Signature Download URL:", download_url)

    local_file_path = os.path.join(key_directory, str(num_doc_value), f'assinatura{num_doc_value}.jpeg')
    response = requests.get(download_url)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
            print(f'Assinatura salva em {local_file_path}')
    else:
        print((f'Falha ao fazer download da assinatura. http status code: {response.status_code}'))


organiza_fotos()