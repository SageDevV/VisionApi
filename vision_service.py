import os
from openai import OpenAI

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_imagem(imagem_base64, prompt = None):
    try :
        prompt = f"""" 
        # Assuma o perfil de transcritor de imagens da loja Havan e analise a imagem abaixo.

        # Ao analisar a imagem você deve somente informar qual categoria que a imagem pertence, independente se a imagem é de um produto ou não, ela deve ser classificada nas categorias abaixo.
        # Não use acentos."
        # palavras devem ser minúsculas.

        # Categorias: 
        # - Tipo produto = fritadeira, liquidificador.
        # - Design = quadrangular, cilindrico, triangular, retangular, circular, oval, hexagonal, octogonal
        # - Cor = vermelho, azul, verde, amarelo, branco, preto, cinza, marrom, rosa, roxo, laranja, bege

        # Formato de saída:
        # Categorias: 1 - Tipo produto: fritadeira, 2 - Design: quadrangular, 3 - Cor: vermelho
            
        # Se o usuário informar um prompt, utilize-o como instrução durante a transcrição da imagem: {prompt}
        """
        resposta = cliente.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{imagem_base64}",
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
            )
        return resposta.choices[0].message.content
    except Exception as e:
        return str(f"Houve um erro na requisição {e}.")