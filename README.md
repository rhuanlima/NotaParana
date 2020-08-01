# NOTA PARANÁ SCRIPT EXPORT

Script python desenvolvido para consulta e exportação dos ultimos 13 meses de notas fiscais do nota Paraná

## How to use
-  Criar arquivo .env com os parametros:
    ```
    user='CPF_SOMENTE_NUMEROS'
    password='SENHA_DO_NOTA_PARANA'
    ```
- Instalar as dependencias
    ```
    pip install -r requirements.txt
    ```
- Instalar o pdfkit:
    https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf

- Executar o script informando quantos meses deseja baixar:
    ```
    python main.py 12
    ```
    
    Para baixar apenas o mes atual basta chamar o script sem nenhum parametro:

    ```
    python main.py
    ```
    
## Results

Após a execução é criado o csv ``` data_nf.csv ``` com a lista de notas com os valores:

    nf_nr : Número da Nota Fiscal
    dt_emissao : Timestamp da emissáo da nota
    place_name : Nome do estabelecimento
    vl_nf : Valor da nota fiscal
    acess_key : Chave de acesso
    qr_code_link : Link para a nota no site da Receita Federal

Além disso o script exporta as páginas da Receita Federal usando o **pdfkit** no caminho **./nf_pdf**

## TODO:
- Formatar a base de exportação que atualmente esta somente como texto
- Aprimorar a exportação de PDF pois em alguns casos o link não é fornecido pelo portal