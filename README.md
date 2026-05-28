# Web Proxy com Controle de Conteúdo 

## Visão Geral

Este projeto foi desenvolvido como parte da disciplina de Sistemas para Internet II, com o objetivo de implementar um web proxy para o controle de conteúdo das páginas web, bloqueando urls específicas e filtrando palavras proibidas.

## Tecnologias Utilizadas

Linguagem: Python 3.12.3

Framework Flask 3.0.2: utilizado para subir o servidor web local, escutar as requisições na porta `5000` e interceptar os caminhos digitados.
  * redirect: utilizada para desviar o fluxo do navegador automaticamente para a rota de erro `/erro` caso o site acessado esteja bloqueado.
  * render_template: utilizada para localizar e renderizar arquivos HTML personalizados dentro da pasta `templates`.

Bibliotecas: 
* requests: utilizada para disparar as requisições HTTP reais para os sites na internet e trazer o conteúdo de volta para o proxy.
* re (Expressões Regulares): aplicada para buscar os palavrões no HTML de forma *case-insensitive* e fazer as substituições inteligentes.
* json: utilizada para abrir e ler os arquivos locais de configuração (`blocked.json` e `words.json`).
* datetime: utilizada para capturar a data e hora exatas de cada acesso para gerar os logs do sistema.

## Justificativa para a escolha das tecnologias

Para este projeto, optou-se por usar a linguagem Python com Flask, por ser uma tecnologia abordada em aula e pela qual houve um interesse de aprofundamento. Uma das principais vantagens encontradas ao usar Flask foi a abstração na parte de manipulação dos bits brutos do socket, gerenciamento de conexões TCP e buffers de dados, promovendo mais produtividade e segurança no tratamento do protocolo HTTP. 
Em contraponto, uma das principais dificuldades encontradas foi o tratamento de páginas web modernas, que utilizam múltiplos recursos externos e caminhos relativos. Como o proxy intercepta e reescreve URLs dinamicamente, alguns elementos das páginas, como folhas de estilo e scripts, podem apresentar falhas de carregamento ou problemas de resolução de rotas no servidor local.


## Estrutura do Projeto:
```
webproxy/
├── conf/
│    └── blocked.json
|    └── words.json
├── templates/
|    └── erro.html
├── logs/
|    └── logs.txt #criado automaticamente caso não exista
├── img/
|    └── personagens.png
├── proxy.py
└── README.md
```

## Passo a passo e requisitos para execução

### 1. Clonar o repositório
```bash
git clone https://github.com/StefaniRitter/webProxy.git
```

### 2. Acessar o diretório do projeto
```bash
cd webProxy
```

### 3. Instalar o Python (Ambiente WSL / Linux)
```bash
sudo apt update
sudo apt install python3-pip python3-dev -y
```

### 4. Instalar Flask
```bash
pip install flask requests
```

### 5. Executar o proxy
```bash
python3 proxy.py
```

### 6. Acessar no navegador, substituindo <url_requisitada> pela url que se deseja acessar. Ex: http://localhost:5000/http://urubu-do-pix.org
```bash
http://localhost:5000<url_requisitada>
```




















