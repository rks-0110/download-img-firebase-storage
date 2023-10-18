# export-firebase-json-rtdb / exporta-json
Exportar arquivos JSON com base nos nomes de tabelas especificado

## Manual de Uso
O executável do programa é o arquivo `exporta-json.exe`, as tabelas que serão exportadas, devem ser especificados no arquivo `config/tabelas-json.txt`.  

## Sobre o Código:
-Desenvolvido em [Python](https://www.python.org/)

### `Main` código fora da função

### Função `initialize_firebase():`
Função definida para iniciar o firebase, já é melhor explicada no arquivo `import-README.md`

### Função `export_json(tabela):`
Recupera o conteúdo da chave filha do firebase com base no nome da tabela, e então cria o arquivo .json usando estes dados.
