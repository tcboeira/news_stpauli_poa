# FC St. Pauli Brasil News
Trata-se de um script/Bot, desenvolvido em Python que agrega notícias, cultura, podcasts, fanzines e conteúdo comunitário relacionados ao FC St. Pauli, traduzindo automaticamente para português e publicando no Telegram.

O projeto busca criar um hub brasileiro da cultura St. Pauli, indo além do futebol tradicional e trazendo conteúdos ligados à torcida, antifascismo, identidade cultural e comunidade.

---

# Funcionalidades
* Coleta automática de notícias e conteúdos
* Suporte a múltiplas fontes
* RSS + Web Scraping
* Tradução automática para português
* Publicação automática no Telegram
* Sistema anti-duplicidade com SQLite
* Categorias com emojis
* Logs de monitoramento
* Estrutura extensível

---

# Categorias
| Categoria | Emoji |
| --------- | ----- |
| Notícia   | 📰    |
| Opinião   | 🎙️   |
| Cultura   | 🏴    |
| Podcast   | 📻    |
| Fanzine   | ✊     |

---

# Fontes atuais
## Oficial
- Conteúdo oficial do FC St. Pauli.

## MillernTon
- Principal mídia independente ligada ao clube.

## St. Pauli POP
- Conteúdo cultural, político e comunitário.

## Übersteiger
- Fanzine histórico da torcida.

## MillernTon Podcast
- Podcasts da comunidade St. Pauli.

---

# Tecnologias utilizadas
* Python
* SQLite, quem "vem embutido" no Python
* Requests (Biblioteca para Python)
* BeautifulSoup4 (Biblioteca para Python)
* Feedparser (Biblioteca para Python)
* Deep Translator (Biblioteca para Python)
* Telegram (API para BOT)

---

# Instalação

## 1. Instalar Python
Baixe em:
https://www.python.org/downloads/

---

## 2. Criar diretório do projeto

Exemplo:

```powershell
mkdir C:\projeto
cd C:\projeto
```

---

## 3. Instalar bibliotecas

```powershell
pip install feedparser requests beautifulsoup4 deep-translator
```

ou:

```powershell
python -m pip install feedparser requests beautifulsoup4 deep-translator
```

---

# Estrutura do projeto

```text
C:\projeto
│
├── main.py
├── noticias.db
├── requirements.txt
└── README.md
```

---

# Configuração do Telegram

## Criar bot

No Telegram, procure por:

* BotFather

Depois execute:

```text
/newbot
```

O BotFather fornecerá:

* TOKEN do bot
* Username do bot

---

# Variáveis de ambiente

Por segurança, não coloque o token diretamente no código.

## PowerShell

```powershell
$env:TELEGRAM_TOKEN="SEU_TOKEN"
$env:TELEGRAM_CHAT_ID="SEU_CHAT_ID"
```

---

# Banco SQLite

O sistema utiliza SQLite para:

* evitar repostagens;
* armazenar histórico;
* registrar fontes e categorias.

---

# Leitura do banco

Recomendado:

DB Browser for SQLite

https://sqlitebrowser.org/

---

# Execução

```powershell
python main.py
```

---

# Funcionamento

O sistema:

```text
Nova notícia?
        ↓
SIM → traduz → publica → salva
NÃO → ignora
```

---

# Objetivo do projeto

Este projeto não busca apenas replicar notícias esportivas.

A ideia é construir uma comunidade brasileira em torno da cultura do FC St. Pauli, reunindo:

* futebol;
* política;
* antifascismo;
* música;
* bairro;
* torcida;
* identidade cultural;
* podcasts;
* fanzines;
* opinião.

---

# Roadmap futuro

* Integração com WhatsApp
* Bluesky / Mastodon
* Resumos automáticos
* Cards visuais
* Dashboard Web
* Ranking de assuntos
* Integração com Reddit
* Podcasts automáticos
* Sistema de tags
* Busca histórica

---

# Licença

Projeto comunitário e sem fins lucrativos.
