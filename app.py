'''
request
No contexto do Flask, request é um objeto importado do módulo Flask que contém todos os dados que o cliente enviou para o servidor como parte de uma solicitação HTTP. O objeto request encapsula informações como cabeçalhos HTTP, dados de formulário, parâmetros de consulta, etc. É normalmente usado em rotas Flask para obter dados enviados pelo cliente.

requests
O requests é uma biblioteca Python para enviar solicitações HTTP. E frequentemente usado para interagir com APIs web ou para ir buscar conteúdo de websites. Esta biblioteca não faz parte do Flask mas pode ser usada em conjunto com o Flask para obter dados de outras APIs.
'''

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Endpoint da API do IPMA
API_ENDPOINT = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cidade_id = request.form.get('cidade')
        response = requests.get(f"{API_ENDPOINT}{cidade_id}.json", verify=False)
        dados_clima = response.json()

        if response.status_code == 200:
            clima = {
                # 'cidade': dados_clima['owner'],
                'temperatura_max': dados_clima['data'][0]['tMax'],
                'temperatura_min': dados_clima['data'][0]['tMin'],
                'probabilidade_prec': dados_clima['data'][0]['precipitaProb'],
                'data_consulta': dados_clima['data'][0]['forecastDate']
            }
        else:
            clima = None

        return render_template('index.html', clima=clima)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)

# python -m pip freeze > requirements