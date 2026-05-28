# Web Proxy com Controle de Conteúdo 

## Visão Geral

Este projeto foi desenvolvido como parte da disciplina de Sistemas para Internet II, com o objetivo de implementar um Web Proxy para controle e filtragem de conteúdo web. O sistema atua intermediando o acesso às páginas da Internet, analisando as URLs requisitadas e verificando se estão presentes em uma lista de bloqueio.

Caso a URL esteja bloqueada, o proxy retorna ao usuário uma página de erro personalizada. Se o acesso for permitido, o sistema realiza a análise do conteúdo da página, identificando palavras cadastradas como proibidas e substituindo-as automaticamente por seus respectivos termos definidos. Quando não há bloqueios ou palavras proibidas, o conteúdo original da página é retornado normalmente ao usuário.

## Tecnologias Utilizadas

**Linguagem**: Python 3.12.3

**Framework Flask 3.0.2**: utilizado para subir o servidor web local, escutar as requisições na porta `5000` e interceptar os caminhos digitados.
  * **redirect**: utilizada para desviar o fluxo do navegador automaticamente para a rota de erro `/erro` caso o site acessado esteja bloqueado.
  * **render_template**: utilizada para localizar e renderizar arquivos HTML personalizados dentro da pasta `templates`.

**Bibliotecas**: 
* **requests**: utilizada para disparar as requisições HTTP reais para os sites na internet e trazer o conteúdo de volta para o proxy.
* **re (Expressões Regulares)**: aplicada para buscar os palavrões no HTML de forma *case-insensitive* e fazer as substituições inteligentes.
* **json**: utilizada para abrir e ler os arquivos locais de configuração (`blocked.json` e `words.json`).
* **datetime**: utilizada para capturar a data e hora exatas de cada acesso para gerar os logs do sistema.

## Justificativa para a escolha das tecnologias

Para este projeto, optou-se pela utilização da linguagem Python em conjunto com o framework Flask, por serem tecnologias abordadas na disciplina e que despertaram um interesse de aprofundamento prático. A escolha também foi motivada pela simplicidade de desenvolvimento proporcionada, permitindo uma implementação mais rápida, legível e organizada do proxy web.

Uma das principais vantagens encontradas ao usar Flask foi a abstração eficiente sobre o protocolo HTTP e sobre o gerenciamento das conexões TCP. Diferentemente da utilização direta da biblioteca socket, o Flask reduz a complexidade relacionada à manipulação manual de buffers, controle de conexões e interpretação das requisições HTTP, permitindo que o foco do desenvolvimento permanecesse concentrado na lógica principal do projeto, como o bloqueio de URLs, filtragem de conteúdo e geração de logs.
Além disso, a integração do Flask com funções como redirect e render_template facilitou o desenvolvimento do fluxo de navegação e da interface de erro personalizada, contribuindo para uma estrutura mais modular e organizada do sistema.
A biblioteca requests também teve papel fundamental no projeto por simplificar o envio de requisições HTTP e o recebimento do conteúdo das páginas web. Já o uso de expressões regulares com a biblioteca re permitiu implementar filtros de palavras de maneira dinâmica e case-insensitive, possibilitando a substituição dos termos sem depender de comparações simples de texto.

Em contraponto, uma das principais dificuldades encontradas durante o desenvolvimento com Flask foi o tratamento de páginas web modernas, que utilizam múltiplos recursos externos, rotas dinâmicas, carregamento assíncrono e caminhos relativos para arquivos CSS e JavaScript. Como o proxy intercepta e reescreve URLs dinamicamente, alguns desses recursos podem gerar falhas de carregamento ou problemas de resolução de rotas quando acessados através do servidor local.
Outra limitação observada está relacionada ao fato de o Flask não operar em um nível tão baixo quanto sockets puros. Embora isso aumente a produtividade e reduza a complexidade da implementação, também limita o controle detalhado sobre determinados aspectos do tráfego de rede e do comportamento interno das conexões HTTP. Ainda assim, considerando o escopo acadêmico do projeto, a utilização do Flask mostrou-se adequada por equilibrar simplicidade, produtividade e facilidade de manutenção.

## Estrutura do Projeto:
```
webproxy/
├── conf/
│   ├── blocked.json
│   └── words.json
├── templates/
│   └── erro.html
├── logs/
│   └── logs.txt #criado automaticamente caso não exista
├── img/
│   └── personagens.png
├── proxy.py
└── README.md
```

## Pré-requisitos e execução

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

### 6. Acessar no navegador, substituindo <url_requisitada> pela URL que se deseja acessar. Ex: http://localhost:5000/http://urubu-do-pix.org
```bash
http://localhost:5000/<url_requisitada>
```

## Personalização das listas

O controle de conteúdo do proxy é totalmente dinâmico e baseado em arquivos JSON localizados na pasta `conf/`.
Se necessário, esses arquivos podem ser alterados, permitindo a personalização dos sites bloqueados, palavras proibidas e suas respectivas substituições.

### Bloqueio de URLs (`conf/blocked.json`)
Para bloquear novos sites, abra o arquivo `blocked.json` e adicione o domínio ou IP desejado dentro do array `sitesBloqueados`. 
Importante: O proxy faz a checagem de forma limpa, portanto, adicione os endereços **SEM** o protocolo `http://` ou `https://`.

```json
{
  "sitesBloqueados": [
    "www.site1.com.br",
    "www.site2.org",
    "127.0.0.1:8081"
  ]
}
```

### Filtro de Palavras (conf/words.json)
A lista de substituição de palavras funciona como um dicionário de Chave (palavra proibida) e Valor (termo substituto). 
O motor do proxy ignora maiúsculas e minúsculas na busca, mas preserva a formatação original na entrega da página.

```json
{
  "palavraProibida1": "termo substituto",
  "palavra_proibida_2": "substituto2"
}
```

## Uso de Inteligência Artificial
O desenvolvimento deste projeto contou com o auxílio de inteligência artificial para ajudar no aprendizado e explicação de conteúdos, além de algumas questões com lógica e formatação de texto para os relatórios. O uso de IA foi focado nos seguintes pilares:

1. **Refatoração e Tratamento de Exceções:** Auxílio na estruturação de blocos `try/except` robustos no arquivo `proxy.py` para capturar falhas de requisições secundárias e evitar o travamento ou poluição visual do terminal do servidor.
2. **Manipulação Avançada de Strings (Regex):** Apoio na criação da lógica interna da função `verificaPalavroes`, especificamente no desenvolvimento da função de ajuste de caixa textual, garantindo que o proxy preserve maiúsculas e minúsculas originais da página ao aplicar as substituições com `re.sub`.
3. **Desenvolvimento Front-End:** Auxílio na estilização CSS e estrutura HTML da página `templates/erro.html` e páginas de teste.
4. **Análise Arquitetural (Flask vs. Sockets):** Uso da IA para discutir as limitações teóricas do framework Flask em comparação com a biblioteca nativa `socket`, auxiliando no aprendizado sobre cada tecnologia e na escolha de uso para o projeto.
5. **Documentação:** Suporte na revisão gramatical, formatação técnica e organização visual do arquivo `README.md` e relatório.

*Toda a lógica de roteamento do Flask, regras de negócios das listas locais (JSON) e tratamento do fluxo de arquivos de log foram projetados e validados com base nos conceitos ministrados em aula e conhecimentos adquiridos anteriormente, além de consultas em documentações oficiais.*














