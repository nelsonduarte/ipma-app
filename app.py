
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Endpoint da API do IPMA
API_ENDPOINT = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"


@app.route('/', methods=['GET', 'POST'])
def index():
    nome_cidade = None 
    clima = None # Vamos preencher isto mais tarde
    if request.method == 'POST':
        cidade_id = request.form.get('cidade')
        if cidade_id:  # Verifica se cidade_id não é vazio
            response = requests.get(f"{API_ENDPOINT}{cidade_id}.json", verify=False)
            dados_clima = response.json()

            if response.status_code == 200:
                clima = {
                    'temperatura_max': dados_clima['data'][0]['tMax'],
                    'temperatura_min': dados_clima['data'][0]['tMin'],
                    'probabilidade_prec': dados_clima['data'][0]['precipitaProb'],
                    'data_consulta': dados_clima['data'][0]['forecastDate']
                }
                # Aqui, você deve adicionar um código para mapear o 'cidade_id' para o nome da cidade
                if cidade_id == "1010500":
                    nome_cidade = "Lisboa"
                elif cidade_id == "1030300":
                    nome_cidade = "Porto"
                elif cidade_id == "1141600":
                    nome_cidade = "Santarém"  # Note que deve ser '=', não '=='
            else:
                clima = None
        else:
            clima = None  # Defina clima como None se cidade_id for vazio

    return render_template('index.html', clima=clima, nome_cidade=nome_cidade)

    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

