import os

def obter_caminho_produto_descricao_diretorio(produto_tipo, produto_design, produto_cor):
    tipos_produto = ['fritadeira', 'liquidificador']
    tipos_cor = ['vermelho', 'azul', 'verde', 'amarelo', 'branco', 'preto', 'cinza', 'marrom', 'rosa', 'roxo', 'laranja', 'bege']
    tipos_design = ['quadrangular', 'cilindrico', 'triangular', 'retangular', 'circular', 'oval', 'hexagonal', 'octogonal']

    if produto_tipo in tipos_produto and produto_cor in tipos_cor and produto_design in tipos_design:
        print(f"database/descricao/{produto_tipo}/{produto_cor}/{produto_design}")
        return f"database/descricao/{produto_tipo}/{produto_cor}/{produto_design}"
    else:
        return 'Caminho inválido'
    
def obter_caminho_produto_imagem_diretorio(produto_tipo, produto_design, produto_cor):
    tipos_produto = ['fritadeira', 'liquidificador']
    tipos_cor = ['vermelho', 'azul', 'verde', 'amarelo', 'branco', 'preto', 'cinza', 'marrom', 'rosa', 'roxo', 'laranja', 'bege']
    tipos_design = ['quadrangular', 'cilindrico', 'triangular', 'retangular', 'circular', 'oval', 'hexagonal', 'octogonal']

    if produto_tipo in tipos_produto and produto_cor in tipos_cor and produto_design in tipos_design:
        return f"database/imagem/{produto_tipo}/{produto_cor}/{produto_design}"
    else:
        return 'Caminho inválido'
        
def obter_produtos_descricoes(caminho_descricao_diretorio):
    todos_arquivos = os.listdir(caminho_descricao_diretorio)
    descricoes_json_lista = [arquivo for arquivo in todos_arquivos if arquivo.endswith('.json')]
    return descricoes_json_lista

def obter_produtos_imagens(caminho_imagens_diretorio):
    todos_arquivos = os.listdir(caminho_imagens_diretorio)
    imagens_lista = [arquivo for arquivo in todos_arquivos if arquivo.endswith(('.jpg', '.jpeg', '.png'))]
    return imagens_lista