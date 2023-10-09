import firebase_admin
import requests
from firebase_admin import credentials, db, storage
import os
import time
from datetime import datetime
import json
from multiprocessing import Pool

today = datetime.now().strftime('%d-%m-%Y')

app_instances = {}
bucket = None


def initialize_firebase(path_SAK, refDB, refST):
    global app_instances
    global bucket

    cred = credentials.Certificate(path_SAK)
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': refDB,
        'storageBucket': refST
    })
    app_instances = app
    bucket = storage.bucket(app=app)


def create_files():
    entregas_data = ref.child('entregas').get()
    entregasOco_data = ref.child('Entregas_oco').get()
    romaneioEnt_data = ref.child('Romaneio_ent').get()
    romaneioIte_data = ref.child('Romaneio_ite').get()

    folder_export = 'dados-export'
    os.makedirs(folder_export, exist_ok=True)

    with open(os.path.join(folder_export, 'entregas.json'), 'w') as file:
        json.dump(entregas_data, file, indent=4)
    with open(os.path.join(folder_export, 'Entregas_oco.json'), 'w') as file:
        json.dump(entregasOco_data, file, indent=4)
    with open(os.path.join(folder_export, 'Romaneio_ent.json'), 'w') as file:
        json.dump(romaneioEnt_data, file, indent=4)
    with open(os.path.join(folder_export, 'Romaneio_ite.json'), 'w') as file:
        json.dump(romaneioIte_data, file, indent=4)

    #create_sub_files(folder_export, romaneioEnt_data)
    download_all_imgs(folder_export)


def download_all_imgs(folder_export):
    print('iniciando download...')
    with open(f'{folder_export}/Romaneio_ite.json', 'r') as json_file:
        data = json.load(json_file)
    organize_all_img(folder_export, data)
    with open(f'{folder_export}/Entregas_oco.json', 'r') as json_file:
        data = json.load(json_file)
    download_img_ent_oco(folder_export, data)


def download_img_ent_oco(dir_name, data):
    for key, snapshot in data.items():
        prefix_ent_oco = f'entregas_oco/{key}'
        download_imgs(dir_name, prefix_ent_oco)


def organize_all_img(dir_name, data):
    for key, snapshot in data.items():
        prefix_photos = f'imagens/{key}/fotos'
        prefix_signature = f'imagens/{key}/assinatura'
        download_imgs(dir_name, prefix_photos)
        download_imgs(dir_name, prefix_signature)


def download_imgs(dir_name, prefix):
    print(prefix)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        if blob.name.endswith('.jpeg'):
            local_file_path = f'{dir_name}/{os.path.basename(blob.name)}'
            blob.download_to_filename(local_file_path)


# Main

start_time = time.time()

refDB = open('config/database.txt').read()
refST = open('config/storage.txt').read()
# SAK = open('config/permissao.json').read()
path_SAK = 'config/permissao.json'

initialize_firebase(path_SAK, refDB, refST)

app = app_instances
ref = db.reference(app=app)

create_files()

end_time = time.time()
execution_time = end_time - start_time
print(f'tempo de execução:{execution_time}')
print('final do download...')
time.sleep(2)
