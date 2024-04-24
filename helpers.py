import base64
import io
import json
import re
from PIL import Image

def obter_produto_tipo(s):
    match = re.search(r'Tipo produto: (.*?),', s)
    if match:
        return match.group(1)
    else:
        return None
    
def obter_produto_design(s):
    match = re.search(r'Design: (.*?),', s)
    if match:
        return match.group(1)
    else:
        return None
    
def obter_produto_cor(s):
    match = re.search(r'Cor: (\w+)', s)
    if match:
        return match.group(1)
    else:
        return None

def selecionar_imagem_associada(caminho_imagem):
    try:
        with open(caminho_imagem, "r", encoding="utf-8") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def obter_descricao_json(caminho_produto_descricao_json):
    try:
        with open(caminho_produto_descricao_json, 'r') as f:
            produto_descricao_json = json.load(f)
            return produto_descricao_json
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def ler_descricao_json(caminho_descricao_json):
    with open(caminho_descricao_json, 'r') as arquivo:
        dados = json.load(arquivo)
    return dados

def obter_imagem(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        buffered = io.BytesIO()
        imagem.save(buffered, format=imagem.format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except IOError as e:
        print(f"Erro no carregamento de imagem: {e}")
