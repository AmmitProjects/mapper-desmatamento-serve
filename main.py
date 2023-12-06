from flask import Flask, jsonify
from flask_cors import CORS  # Importe a extensão CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # Adicione essa linha para habilitar o CORS

def calcular_desmatamento():
    try:
        # Definindo manualmente os caminhos das imagens
        foto_ano_anterior = r'C:\Users\eduar\Documents\Projetos\trabalho-marcos\mapper-desmatamento-serve\imgs\2022.jpg'
        foto_ano_atual = r'C:\Users\eduar\Documents\Projetos\trabalho-marcos\mapper-desmatamento-serve\imgs\2021.jpg'

        # Lendo as imagens
        img_ano_anterior = cv2.imread(foto_ano_anterior)
        img_ano_atual = cv2.imread(foto_ano_atual)

        # Convertendo as imagens para escala de cinza
        gray_ano_anterior = cv2.cvtColor(img_ano_anterior, cv2.COLOR_BGR2GRAY)
        gray_ano_atual = cv2.cvtColor(img_ano_atual, cv2.COLOR_BGR2GRAY)

        # Calculando a diferença entre as imagens
        diff = cv2.absdiff(gray_ano_anterior, gray_ano_atual)

        # Aplicando um limiar para destacar as diferenças
        _, threshold_diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Calculando a porcentagem de desmatamento
        porcentagem_desmatamento = (np.count_nonzero(threshold_diff) / threshold_diff.size) * 100

        return porcentagem_desmatamento

    except Exception as e:
        return str(e)

@app.route('/comparar_desmatamento/', methods=['GET'])
def comparar_desmatamento_endpoint():
    porcentagem_desmatamento = calcular_desmatamento()

    if isinstance(porcentagem_desmatamento, str):
        return jsonify({'erro': porcentagem_desmatamento}), 500
    else:
        return jsonify({'porcentagem_desmatamento': porcentagem_desmatamento}), 200

if __name__ == '__main__':
    app.run(debug=True)
