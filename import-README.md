# import-firebase-rtdb / importa-registro
Importar novo registro para firebase realtime database sem apagar os registros existentes.

## Manual de Uso
A pasta do programa contém um programa `importa.exe`, duas pastas `config` e `dados` e um arquivo de texto com a versão do programa.  

### `importa.exe`
É o arquivo executável do programa, caso os arquivos nas pastas estejam corretos deve funcionar corretamente (na versão 1.0 (25/julho/2023), está implementando dados para as tabelas `entregas`, `Romaneio_ent` e `Romaneio_ite`).

### `config`
Nesta pasta estão os arquivos que provavelmente não serão alterados com frequência.  
O conteúdo de `database.txt` deve ser alterado com o devido link do firebase da empresa (não é a URL do navegador mas sim o link do realtime database).
O arquivo `permissao.json` deve ser substituído com a própria chave de autorização para aquele banco de dados. [saiba mais](#chave-de-autorização)

### `dados`
Aqui deverão ficar os arquivos .json de novos registros que serão adicionados ao firebase que foi [configurado](#config).

## Sobre o Código:
-Desenvolvido em [Python](https://www.python.org/)-  
Imports necessários:

- [firebase_admin](https://firebase.google.com/docs/reference/admin/python/firebase_admin) > [credentials](https://firebase.google.com/docs/reference/admin/python/firebase_admin.credentials), [db](https://firebase.google.com/static/docs/reference/admin/python/firebase_admin.db)
- [json](https://docs.python.org/3/library/json.html)  
---
Inicialmente é feita a leitura do arquivo que contém o caminho para o firebase realtime database (não é a URL do navegador) que deve ser alterada no caminho `./config/database.txt`  

##### chave de autorização:
Em seguida, utilizamos `firebase_admin.credentials` para passar como parâmetros o endereço do realtime database que foi recuperado anteriormente, e a chave de autorização que pode ser gerada em `sidebar do firebase > Configurações do projeto > Contas de serviço > SDK Admin do Firebase > Python > Gerar nova chave privada`. O caminho e nome designado para a chave única deve ser `./config/permissao.json`.  

### Função `lerJson(caminhoJson):`
É uma função definida para retornar os conteúdos dos arquivos Json de acordo com o caminho passado, aqui é utilizada a dependência [json](#import-firebase-rtdb)

Logo a baixo são declarados os caminhos para as partes relevantes do firebase:
##### referencias:
```
firebaseRef = db.reference()
entregasRef = firebaseRef.child("entregas")
romaneioEntRef = firebaseRef.child("Romaneio_ent")
romaneioIteRef = firebaseRef.child("Romaneio_ite")
```
e então já são lidos os arquivos .json utilizando a função previamente criada:
##### dados:
```
entregasDados = lerJson("./dados/entregas.json")
romaneioEntDados = lerJson("./dados/Romaneio_ent.json")
romaneioIteDados = lerJson("./dados/Romaneio_ite.json")
``` 

### Função `indiceEntregas():`
Esta função simplesmente tem o objetivo de contar a quantidade de itens abaixo de `Firebase/entregas` (caso o nó esteja vazio retorna 0). Este valor de retorno será utiliizado como chave para o item adicionado a `entregas`.

### Função `importaEntregas():`
Para cada ***entrega*** dentro de `entregasDados` é definida uma chave (`key = f"{indiceEntregas()}"`) e então é feito o mapeamento de dados para entrega, contendo cada campo da tabela `entregas (dat_ent, km_per...)`, por fim foi utiliziado o método `set()` passando a chave declarada usando `indiceEntregas()` para especificar a chave e então o método `.set()` passando como parâmetro o mapeamento feito dentro [desta função](#função-importaentregas).

### Função `importaRomaneioEnt():` & `importaRomaneioIte():`
Estes métodos são mais simples que `importaEntregas()` e bem semelhantes entre eles. O código simplesmente pega a respectiva [referencia](#referencias), então usamos o método `.update()` (para **atualizar** a tabela) e passamos os [dados](#dados) da respectiva função.

## Obs 
A estrutura de `entregas` (o nó raiz sendo uma lista, assim o arquivo é uma lista de itens) é distinta das estruturas de `Romaneio_ent` e `Romaneio_ite` (nó raiz é um item, sendo o arquivo um item de llistas com itens), assim foi necessário uma abordagem diferenet para `importarEntregas()`  
O arquivo `importa.py` presente neste repositório não é o arquivo descrito `importa.exe`, mas sim seu código fonte para fim de análise.
