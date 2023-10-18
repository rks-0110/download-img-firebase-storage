import firebase_admin
import json
import os
from firebase_admin import credentials, db


app_instances = {}

def initialize_firebase():
    global app_instances

    cred = credentials.Certificate(path_sak)
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': ref_db
    })
    app_instances = app


def export_json(tabela):
    data = firebase_ref.child(tabela).get()

    folder_export = 'dados-export'
    os.makedirs(folder_export, exist_ok=True)

    with open(os.path.join(folder_export, f'{tabela}.json'), 'w') as file:
        json.dump(data, file, indent=4)


ref_db = open('config/database.txt').read()
path_sak = 'config/permissao.json'

initialize_firebase()
app = app_instances
firebase_ref = db.reference(app=app)

with open('config/tabelas-json.txt') as tables:
    lines = tables.read().splitlines()
    for line in lines:
        print(f'Processando: {line}...')

        try:
            line_ref = db.reference(f'{line}')
        except Exception as e:
            print(f'Erro ao encontrar referência {line}, exception: {e}')

        if line in ['Deposito', 'Ite_nota_sai', 'Item', 'Item-cod-bar', 'Nota_sai',
                    'Programas', 'Programas-proc', 'Romaneio_ent', 'Romaneio_ite', 'Usuario',
                    'Versao', 'bi', 'entregas', 'item-dep', 'motivo-nao-entrega']:
            export_json(line)
        else:
            print(f'Nome de tabela {line} inválido, verifique .config-rpteste/tabelas.txt')