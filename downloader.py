import pathlib
import requests
import parsel
import os
import json
from peewee import *
from PIL import Image
from io import BytesIO
from fake_useragent import FakeUserAgent

# Caminho onde as imagens serão salvas
path = pathlib.Path('imgs')
path.mkdir(exist_ok=True)

# Sessão de requests
session = requests.Session()
session.headers['User-Agent'] = FakeUserAgent().random

# Banco de dados
db = SqliteDatabase('history.db')

class Imagem(Model):
    url = CharField(unique=True)
    path = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Imagem])

# Carrega os links
with open('links.json') as f:
    urls = json.load(f)

# Verifica se a imagem já foi baixada
def check_image(url):
    return Imagem.select().where(Imagem.url == url).exists()

# Função para salvar e comprimir a imagem
def save(url):
    response = session.get(url, stream=True)
    response.raise_for_status()

    # Pega o nome original e define novo nome
    original_name = os.path.basename(url)
    base_name, ext = os.path.splitext(original_name)  # sem extensão

    # Carrega a imagem na memória
    img = Image.open(BytesIO(response.content))

    # Define caminho de saída (convertendo para JPEG ou WebP, por exemplo)
    output_path = path / f"{base_name}"

    if 'gif' in ext:
    # Salva comprimido no novo formato (WebP é muito bom para compressão)
        img.save(str(output_path)+'.gif', 'GIF', quality=85, save_all=True)  # quality 85 é um ótimo equilíbrio
    else:
        img.save(str(output_path)+'.webp', 'WEBP', quality=85)

    try:
        Imagem.create(url=url, path=output_path)
        print(f"Imagem salva: {output_path.name}")
    except IntegrityError:
        print(f'Imagem já existe: {output_path.name}')

# Função para extrair imagens do site
def eporner(url):
    response = session.get(url)
    response.raise_for_status()
    
    page = parsel.Selector(response.text)
    data = page.xpath(".//div[@id='container']/.//@src").getall()

    for item in data:
        if check_image(item):
            continue
        save(item)

# Processa todos os links
for url in urls:
    if 'eporner' in url:
        eporner(url)
