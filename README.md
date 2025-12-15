# O2Events

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,html,css,bootstrap,git,github,sqlite" />
</p>

## 🌟 Visão Geral

O O2Events é uma aplicação web construída com Flask e SQLAlchemy, desenvolvida para ajudar na organização e contabilização de despesas relacionadas a eventos, encontros ou atividades em grupo. Ele permite o cadastro de eventos, o registro de notas fiscais com valores e responsáveis pelo pagamento, e o resumo total dos gastos.



## ✨ Funcionalidades Principais

- **Cadastro de Eventos**  
  Crie e gerencie eventos como *Retiro de Jovens*, *Jantar de Páscoa*, entre outros.

- **Registro de Notas Fiscais**  
  Associe despesas a eventos específicos, informando valor, descrição, data e responsável pelo pagamento.

- **Upload de Notas**  
  Anexe arquivos (PDFs ou imagens) das notas fiscais para fácil acesso e auditoria.

- **Dashboard de Resumo**  
  Visualize o total gasto por evento e um resumo de quanto cada participante pagou.



## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask  
- **Banco de Dados:** SQLite (SQLAlchemy ORM)  
- **Frontend:** HTML, CSS (Bootstrap)  
- **Gerenciamento de Dependências:** pip  
- **Versionamento:** Git e GitHub

## 🚀 Como Configurar e Executar

Siga estas instruções passo a passo para configurar o ambiente e rodar o projeto localmente, partindo do princípio que o código já foi clonado.

## Pré-requisitos

Você precisa ter instalado em sua máquina:

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,git" />
</p>

### 1. Navegar até o Diretório do Projeto

Abra o terminal ou PowerShell e acesse a pasta principal do projeto O2Events:

```text
cd O2Events
```

### 2. Criar e Ativar o Ambiente Virtual

É uma boa prática isolar as dependências do projeto. Este passo garante que as bibliotecas necessárias não interfiram em outros projetos Python.

No Windows (PowerShell):

```text
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux/macOS:


```text
python3 -m venv venv
source venv/bin/activate
```

(Após a ativação, você verá (venv) no início da linha de comando.)

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Flask e SQLAlchemy (e outras dependências) listadas em requirements.txt.
```text
pip install -r requirements.txt
```

### 4. Inicializar e Executar a Aplicação

A aplicação irá utilizar as configurações em config.py. Na primeira execução, o banco de dados (o2events.db) e todas as tabelas necessárias serão criados automaticamente.

```text
python main.py
```


Você verá no terminal uma mensagem indicando que o servidor Flask está rodando.

### 5. Acessar no Navegador

Abra seu navegador e acesse o endereço fornecido pelo Flask (servidor de desenvolvimento):
```text
http://127.0.0.1:5000
```


## Estrutura do Projeto

```text
O2Events/
├── venv/                   # Ambiente Virtual
├── static/                 # Arquivos estáticos (CSS, JS, uploads)
│   ├── files/              # Pasta para upload das notas fiscais
│   └── (outros arquivos estáticos)
├── templates/              # Templates HTML do Flask
│   ├── base.html
│   ├── index.html
│   ├── cadastro_evento.html
│   └── cadastro_nota.html
├── .gitignore              # Arquivos a serem ignorados pelo Git
├── config.py               # Arquivo de configurações do Flask
├── main.py                 # Ponto de entrada da aplicação e inicialização do Flask/DB
├── models.py               # Definição dos modelos do SQLAlchemy (Evento e NotaFiscal)
├── routes.py               # Definição de todas as rotas (URLs) da aplicação
└── requirements.txt        # Lista de dependências do Python

