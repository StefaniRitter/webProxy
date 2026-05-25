## instalar python3, flask, requests se necessário
from flask import Flask, json, redirect, url_for, render_template
import requests

app = Flask(__name__)

@app.route("/<path:url_destino>", methods=["GET"])
def proxy(url_destino):
    resposta = requests.get(url_destino)
    conteudo = resposta.text
    cont = verificaPalavroes(conteudo)
    return f"{cont}"

    return verificaURL(url_destino)
    ## Conferir a url no blocked.json
    ## Conferir html e palavras proibidas no words.json


@app.route("/erro", methods=["GET"])
def erro():
    return render_template("erro.html")

"""@app.route("/teste", methods=["GET"])
def teste():
    return render_template("index.html")"""


def verificaURL(url):
    with open('./conf/blocked.json', 'r', encoding='utf-8') as arquivo:
        ## json.load: converte o texto do json em um dicionário python
        urlsBloqueadas = json.load(arquivo)
        urlsBloqueadas = urlsBloqueadas["sitesBloqueados"]
        if url in urlsBloqueadas:
            return redirect(url_for('erro'))
        else: 
            return redirect(url_for(url))

def verificaPalavroes(cont):
    with open('./conf/words.json', 'r', encoding='utf-8') as arquivo:
        palavroes = json.load(arquivo)
        for k, v in palavroes.items():
            if k in cont:
                cont = cont.replace(k, v)
    return cont

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)