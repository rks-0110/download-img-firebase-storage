# export-firebase-json-rtdb / exporta-json
Exportar arquivos JSON com base nos nomes de tabelas especificado

## Manual de Uso
O executável do programa é o arquivo `exporta-json.exe`, as tabelas que serão exportadas, devem ser especificados no arquivo `config/tabelas-json.txt`.  

## Sobre o Código:
-Desenvolvido em [Python](https://www.python.org/)

### "`Main`" código fora da função
É o código executado primariamente, a partir dele são chamadas as funções seguintes, primeiro são definidas as variáveis para os caminhos do banco de dados, e permissão, então é chamado o método `inicialize_firebase()`.
Após isso define a variável para armazenar a referência do firebase, em seguida o arquivo `config/tabelas-json.txt` é lido e separado em linhas, para separar cada nome de tabela solicitada. Finalmente para cada linha é comparada se aquela linha está entre os nomes de todas as tabelas do firebase, finalmente chama a função `export_json(line)`.

### Função `initialize_firebase():`
Função definida para iniciar o firebase, já é melhor explicada no arquivo `import-README.md`

### Função `export_json(tabela):`
Recupera o conteúdo da chave filha do firebase com base no nome da tabela, e então cria o arquivo .json usando estes dados.

