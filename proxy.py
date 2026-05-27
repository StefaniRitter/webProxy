## instalar python3, flask, requests se necessário
from flask import Flask, json, redirect, render_template
from datetime import datetime as dt
import requests, re

app = Flask(__name__)

@app.route("/<path:url_destino>", methods=["GET"])
def proxy(url_destino):
    acao = 'permitido'
    timestamp = (dt.now()).timestamp()
    data_formatada = dt.now().strftime("%d/%m/%Y %H:%M:%S")

    url = verificaURL(url_destino)
    if url[0] == "erro":
        acao = url[1]
        registraLog(url_destino, timestamp, data_formatada, acao)
        return redirect("/erro")
    
    resposta = requests.get(url[0])
    conteudo = resposta.text
    cont = verificaPalavroes(conteudo, acao)
    acao = cont[1]
    cont = cont[0]
    registraLog(url_destino, timestamp, data_formatada, acao)
    return f"{cont}"

@app.route("/erro", methods=["GET"])
def erro():
    return render_template("erro.html")

"""@app.route("/teste", methods=["GET"])
def teste():
    return render_template("index.html")"""

def registraLog(url, timestamp, data, acao):
    with open('log.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"[{timestamp} - {data}]: Url: {url}; Ação: {acao}\n")



def verificaURL(url):
    with open('./conf/blocked.json', 'r', encoding='utf-8') as arquivo:
        ## json.load: converte o texto do json em um dicionário python
        urlsBloqueadas = json.load(arquivo)
        urlsBloqueadas = urlsBloqueadas["sitesBloqueados"]
        if url in urlsBloqueadas:
            return ['erro', 'bloqueado']
        return [url]

def verificaPalavroes(cont, acao):
    with open('./conf/words.json', 'r', encoding='utf-8') as arquivo:
        palavroes = json.load(arquivo)
        contOriginal = cont
        for k, v in palavroes.items():
            #usei ia
            def ajustar(dados):
                palavraOriginal = dados.group(0) #captura a palavra na formatação do site
                if palavraOriginal.isupper():
                    return v.upper()
                elif palavraOriginal[0].isupper():
                    return v.capitalize()
                return v
            cont = re.sub(re.escape(k), ajustar, cont, flags=re.IGNORECASE)
        if cont != contOriginal:
            acao = 'filtrado'
    return [cont, acao]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)