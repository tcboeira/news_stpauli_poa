import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import feedparser

from deep_translator import GoogleTranslator

# =========================================
# TELEGRAM
# =========================================

TOKEN = "MEU TOKEN"
CHAT_ID = "ID BOT"

# =========================================
# SQLITE
# =========================================

conn = sqlite3.connect("noticias.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS noticias (
    link TEXT PRIMARY KEY,
    titulo TEXT,
    fonte TEXT,
    categoria TEXT,
    data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================================
# HEADERS
# =========================================

headers = {
    "User-Agent": "Mozilla/5.0"
}

# =========================================
# EMOJIS
# =========================================

emoji_categoria = {
    "noticia": "📰",
    "opiniao": "🎙️",
    "cultura": "🏴",
    "podcast": "📻",
    "fanzine": "✊"
}

# =========================================
# SOURCES
# =========================================

sources = [

    # =====================================
    # SITE OFICIAL
    # =====================================

    {
        "name": "Official",
        "category": "noticia",
        "type": "scraping",
        "url": "https://www.fcstpauli.com/news/",
        "match": "/news/"
    },

    # =====================================
    # MILLERNTON
    # =====================================

    {
        "name": "MillernTon",
        "category": "opiniao",
        "type": "rss",
        "url": "https://millernton.de/feed/"
    },

    # =====================================
    # ST. PAULI POP
    # =====================================

    {
        "name": "St. Pauli POP",
        "category": "cultura",
        "type": "rss",
        "url": "https://blog.stpauli.social/feed/"
    },

    # =====================================
    # ÜBERSTEIGER
    # =====================================

    {
        "name": "Übersteiger",
        "category": "fanzine",
        "type": "rss",
        "url": "https://blog.uebersteiger.de/feed/"
    },

    # =====================================
    # PODCASTS
    # =====================================

    {
        "name": "MillernTon Podcast",
        "category": "podcast",
        "type": "rss",
        "url": "https://millernton.de/feed/podcast/"
    }

]

# =========================================
# PREFIXOS
# =========================================

prefixos = [
    "Profis",
    "Verein",
    "Business",
    "Rabauken",
    "Millerntor",
    "Genossenschaft",
    "1. Frauen"
]

# =========================================
# TELEGRAM
# =========================================

def enviar_telegram(mensagem):

    telegram_url = (
        f"https://api.telegram.org/"
        f"bot{TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    response = requests.post(
        telegram_url,
        data=payload,
        timeout=15
    )

    return response.status_code

# =========================================
# RSS
# =========================================

def coletar_rss(source):

    noticias = []

    print("\nLENDO RSS:")
    print(source["name"])
    print(source["url"])

    feed = feedparser.parse(
        source["url"]
    )

    print(
        "TOTAL ENTRADAS:",
        len(feed.entries)
    )

    for entry in feed.entries:

        try:

            titulo = entry.title.strip()

            noticias.append({

                "fonte": source["name"],

                "categoria": source["category"],

                "titulo": titulo,

                "link": entry.link

            })

        except Exception as e:

            print("ERRO RSS:", e)

    return noticias


# =========================================
# SCRAPING HTML
# =========================================

def coletar_scraping(source):

    print("\nLENDO SCRAPING:")
    print(source["name"])
    print(source["url"])

    noticias = []

    response = requests.get(
        source["url"],
        headers=headers,
        timeout=15
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    links = soup.find_all("a")

    for link in links:

        texto = link.get_text(
            " ",
            strip=True
        )

        href = link.get("href")

        if texto and href:

            # =================================
            # FILTRO POR FONTE
            # =================================

            if "match" in source:

                if source["match"] not in href:
                    continue

            # =================================
            # URL RELATIVA
            # =================================

            if href.startswith("/"):

                href = (
                    source["url"].rstrip("/")
                    + href
                )

            # =================================
            # REMOVE DATAS
            # =================================

            texto = re.sub(
                r"\d{1,2}\.\s+\w+\s+\d{4}",
                "",
                texto
            )

            # =================================
            # REMOVE PREFIXOS
            # =================================

            for prefixo in prefixos:

                texto = re.sub(
                    rf"^{re.escape(prefixo)}\s*",
                    "",
                    texto
                )

            # =================================
            # LIMPA ESPAÇOS
            # =================================

            texto = " ".join(
                texto.split()
            )

            # =================================
            # FILTRA TÍTULOS PEQUENOS
            # =================================

            if len(texto) > 25:

                noticias.append({

                    "fonte": source["name"],

                    "categoria": source["category"],

                    "titulo": texto,

                    "link": href

                })

    print(
        "TOTAL ENTRADAS:",
        len(noticias)
    )

    return noticias


# =========================================
# COLETOR GERAL
# =========================================

def coletar_noticias(source):

    if source["type"] == "rss":

        return coletar_rss(source)

    elif source["type"] == "scraping":

        return coletar_scraping(source)

    return []

# =========================================
# PROCESSAMENTO
# =========================================

vistos = set()

for source in sources:

    print("\n==========")
    print(f"FONTE: {source['name']}")
    print("==========")

    try:

        noticias = coletar_noticias(
            source
        )

    except Exception as e:

        print("ERRO:", e)

        continue

    for noticia in noticias:

        titulo = noticia["titulo"]

        link = noticia["link"]

        fonte = noticia["fonte"]

        categoria = noticia["categoria"]

        emoji = emoji_categoria.get(
            categoria,
            "📰"
        )

        # =================================
        # EVITA DUPLICIDADE EM MEMÓRIA
        # =================================

        if link in vistos:
            continue

        vistos.add(link)

        # =================================
        # VERIFICA BANCO
        # =================================

        cursor.execute(
            "SELECT link FROM noticias WHERE link = ?",
            (link,)
        )

        resultado = cursor.fetchone()


        # =================================
        # NOVA NOTÍCIA
        # =================================

        if not resultado:

            print("\n🆕 NOVA NOTÍCIA!\n")

            try:

                traducao = GoogleTranslator(
                    source='auto',
                    target='pt'
                ).translate(titulo)

            except:

                traducao = titulo

            print("🇧🇷", traducao)

            mensagem = f"""
{emoji} {categoria.upper()}

📰 Fonte: {fonte}

🇧🇷 {traducao}

🔗 {link}
"""

            status = enviar_telegram(
                mensagem
            )

            print(
                "TELEGRAM:",
                status
            )

            # =============================
            # SALVA NO BANCO
            # =============================

            cursor.execute("""
            INSERT INTO noticias (

                link,
                titulo,
                fonte,
                categoria

            )
            VALUES (?, ?, ?, ?)
            """, (

                link,
                titulo,
                fonte,
                categoria

            ))

            conn.commit()

        # =================================
        # JÁ EXISTE
        # =================================

        else:

            print("✅ JÁ POSTADO:")
            print(titulo)
