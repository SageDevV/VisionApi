from flask import Flask, jsonify, request, render_template
from documento_service import obter_caminho_produto_descricao_diretorio, obter_caminho_produto_imagem_diretorio, obter_produtos_descricoes, obter_produtos_imagens
from helpers import obter_produto_cor, obter_produto_design, obter_produto_tipo, ler_descricao_json, obter_imagem
from vision_service import analisar_imagem
import tiktoken

app = Flask(__name__)

def vision_service(imagem_base64, prompt = None):
    descricao_imagem = analisar_imagem(imagem_base64, prompt)

    if(descricao_imagem is None):
        return "Não foi possível analisar a imagem." 
    
    print(descricao_imagem)
    
    produto_tipo = obter_produto_tipo(descricao_imagem)
    produto_design = obter_produto_design(descricao_imagem)
    produto_cor = obter_produto_cor(descricao_imagem)

    print(f"Não foi possível classificar o produto: tipo: {produto_tipo}, formato: {produto_design}, cor: {produto_cor}.")

    if(produto_tipo is None or produto_design is None or produto_cor is None):
        return f"Não foi possível classificar o produto: tipo: {produto_tipo}, formato: {produto_design}, cor: {produto_cor}."

    caminho_descricao_diretorio = obter_caminho_produto_descricao_diretorio(produto_tipo, produto_design, produto_cor)

    if(caminho_descricao_diretorio is None):
        return "Não foi possível encontrar o diretório de descrição do produto."

    descricoes_json_lista = obter_produtos_descricoes(caminho_descricao_diretorio)

    if(descricoes_json_lista is None):
        return f"Não há desicrições de produtos associados a classificação: tipo: {produto_tipo}, formato: {produto_design}, cor: {produto_cor}."

    produto_descricao_composicao_json_lista = []

    for descricao_json in descricoes_json_lista:
        produto_descricao_composicao_json = ler_descricao_json(f"{caminho_descricao_diretorio}/{descricao_json}")

        if(produto_descricao_composicao_json is None):
            return "Não foi possível carregar a descrição do produto."

        produto_descricao_composicao_json_lista.append(produto_descricao_composicao_json)

    caminho_imagem_diretorio = obter_caminho_produto_imagem_diretorio(produto_tipo, produto_design, produto_cor)

    if(caminho_imagem_diretorio is None):
        return "Não foi possível encontrar o diretório de imagem do produto."

    produtos_imagens_lista = obter_produtos_imagens(caminho_imagem_diretorio)

    if(produtos_imagens_lista is None):
        return f"Não há imagens de produtos associadas a classificação: tipo: {produto_tipo}, formato: {produto_design}, cor: {produto_cor}."

    produto_imagem_composicao_lista = []

    for produto_imagem in produtos_imagens_lista:
        produto_imagem_composicao = obter_imagem(f"{caminho_imagem_diretorio}/{produto_imagem}")

        if(produto_imagem_composicao is None):
            return "Não foi possível carregar a imagem do produto."
        
        produto_imagem_composicao_lista.append(produto_imagem_composicao)

    return jsonify({
        'descricoes': produto_descricao_composicao_json_lista,
        'imagens': produto_imagem_composicao_lista
    })

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def vision_interface():
    try :
        prompt = request.json['prompt']
        imagem_base64 = request.json['image']

        if(imagem_base64 is None):
            return str("é necessário informar a imagem.")
        
        encode = tiktoken.encoding_for_model("gpt-4-vision-preview")
        total_tokens = len(encode.encode(imagem_base64))

        if(total_tokens > 10000):
            return str(f"O numero máximo de tokens suportado é de 10000, numero de tokens informado: {total_tokens}.")
    
        return vision_service(imagem_base64, prompt)
    except Exception as e:
        return str(f"Houve um erro na requisição {e}.")

app.run(host="0.0.0.0", port=80)