import firebase_admin
from firebase_admin import credentials, db
import json


def initialize_firebase():
    cred = credentials.Certificate(path_SAK)
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': refDB
    })


def read_json(path_to_json):
    with open(path_to_json, 'r') as file:
        return json.load(file)


def indx_entregas():
    snapshot = line_ref.get()
    if snapshot:
        return len(snapshot)
    return 0


def import_without_key():
    try:
        for spec_line_data in line_data:
            key = f'{indx_entregas()}'
            print(f'Importando: {line}...')
            line_ref.child(key).update(spec_line_data)
    except Exception as e:
        print(f'Erro ao importar dados para {line}, exception: {e}')



def import_with_key():
    try:
        print(f'Importando: {line}...')
        line_ref.update(line_data)
    except Exception as e:
        print(f'Erro ao importar dados para {line}, exception: {e}')


# Main

refDB = open('config-rpteste/database.txt').read()
# SAK = open('config-rpteste/permissao.json').read()
path_SAK = 'config-rpteste/permissao.json'

initialize_firebase()

# Caminho rtdb
firebase_ref = db.reference()

with open('config-rpteste/tabelas.txt') as tables_file:
    lines = tables_file.read().splitlines()
    for line in lines:
        print(f'Processando: {line}...')

        # caminho
        try:
            line_ref = db.reference(f'{line}')
        except Exception as e:
            print(f'Erro ao importar dados para {line}, exception: {e}')
        # dados
        try:
            line_data = read_json(f'dados/{line}.json')
        except Exception as e:
            print(f'Erro ao importar dados para {line}, exception: {e}')

        if line in ['Item', 'Item-cod-bar', 'Programas', 'Programas-proc', 'Romaneio_ent',
                    'Romaneio_ite', 'Usuario', 'item-dep', 'motivo-nao-entrega']:
            import_with_key()
        elif line in ['Deposito', 'bi', 'entregas']:
            import_without_key()
        else:
            print(f'Nome de tabela "{line}" inválido, verifique ./config-rpteste/tabelas.txt')
