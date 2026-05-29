## instalar python3, flask, requests se necessário
from flask import Flask, redirect, render_template
from datetime import datetime as dt
import requests, re, json

# parâmetros a mais, para carregar a imagem da página de erro
app = Flask(__name__, static_folder='img', static_url_path='/img')

# pega a url informada e coloca na variável url_destino
@app.route("/<path:url_destino>", methods=["GET"])
def proxy(url_destino):

    if url_destino == "favicon.ico":
        return "", 204
    # parâmetros para o arquivo de log
    acao = 'permitido'
    timestamp = (dt.now()).timestamp()
    data_formatada = dt.now().strftime("%d/%m/%Y %H:%M:%S")

    # chama a função para verificar se a url é permitida
    # se a url estiver na lista de bloqueados o retorno é uma lista com a string "erro" e a acao tomada, se a url for permitida retorna uma lista apenas com a url
    url = verificaURL(url_destino)
    if url[0] == "erro": 
        acao = url[1]
        registraLog(url_destino, timestamp, data_formatada, acao)
        return redirect("/erro")
    
    try:
        resposta = requests.get(url[0]) # url[0] retorna a url requisitada
    
        conteudo = resposta.text # usa .text para transformar o conteúdo do site em uma string
        cont = verificaPalavroes(conteudo, acao) # retorna uma lista com conteúdo e ação tomada
        acao = cont[1]
        cont = cont[0]
        registraLog(url_destino, timestamp, data_formatada, acao)
        return f"{cont}"
    except Exception as e:
        print(f"Proxy: Requisição ignorada/falhou")
        return "Recurso indisponível no proxy", 404

@app.route("/erro", methods=["GET"])
def erro():
    return render_template("erro.html")

def registraLog(url, timestamp, data, acao):
    with open('./logs/logs.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"[{timestamp} - {data}]: Url: {url}; Ação: {acao};\n")

def verificaURL(url):
    with open('./conf/blocked.json', 'r', encoding='utf-8') as arquivo:
        url_limpa = url.replace("http://", "") # tratamento para a url
        urlsBloqueadas = json.load(arquivo) # json.load: converte o texto do json em um dicionário
        urlsBloqueadas = urlsBloqueadas["sitesBloqueados"]
        if url_limpa in urlsBloqueadas:
            return ['erro', 'bloqueado']
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url # adiciona http na frente para ficar no padrão

        return [url]

def verificaPalavroes(cont, acao):
    with open('./conf/words.json', 'r', encoding='utf-8') as arquivo:
        palavroes = json.load(arquivo)
        contOriginal = cont # salva conteudo original para verificar alterações depois
        for k, v in palavroes.items(): # percorre o dicionário de palavrões
            
            # tratamento para case-sensitive
            def ajustar(dados):
                palavraOriginal = dados.group(0) #captura a palavra na formatação do site
                if palavraOriginal.isupper():
                    return v.upper()
                elif palavraOriginal[0].isupper():
                    return v.capitalize()
                return v
            
            # re.sub(): busca um padrão no texto e substitui por outra coisa
            # re.escape(k): pega a palavra chave do dicionário e se tiver caracteres especiais ignora eles
            # ajustar: o python chama a função ajustar(dados) automaticamente quando encontra uma palavra proibida
            # flags=re.IGNORECASE faz com que todas as variações da palavra sejam capturadas
            cont = re.sub(re.escape(k), ajustar, cont, flags=re.IGNORECASE)

        if cont != contOriginal:
            acao = 'conteúdo filtrado' # se o conteúdo mudou, é porque alguma palavra foi filtrada

    return [cont, acao]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)