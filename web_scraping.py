import requests
from bs4 import BeautifulSoup
import json
import csv
import time

def scrape_and_save(categoria, total_paginas=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    todos_produtos = []

    for page in range(1, total_paginas + 1):
        url = f"https://www.loja-exemplo/{categoria}?page={page}"
        print(f"Coletando página {page}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            
            for script in scripts:
                data = json.loads(script.string)
                if data.get('@type') == 'ItemList':
                    items = data.get('itemListElement', [])
                    for element in items:
                        item = element.get('item', {})
                        offers = item.get('offers', {})
                        
                        todos_produtos.append({
                            "Nome": item.get('name'),
                            "Marca": item.get('brand', {}).get('name'),
                            "Preco": offers.get('lowPrice'),
                            "Moeda": offers.get('priceCurrency'),
                            "Link": item.get('@id')
                        })
            
            # Pausa curta para não ser bloqueado pelo servidor
            time.sleep(1) 

        except Exception as e:
            print(f"Erro na página {page}: {e}")

    #  salvando arquivo
    nome_arquivo = f"produtos_{categoria}.csv"
    
    if todos_produtos:
        
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8-sig') as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=todos_produtos[0].keys())
            escritor.writeheader() # Escreve o cabeçalho (Nome, Marca, etc)
            escritor.writerows(todos_produtos) # Escreve os dados
        
        print(f"\nSucesso! {len(todos_produtos)} produtos salvos em: {nome_arquivo}")
    else:
        print("Nenhum dado foi capturado para salvar.")

# Execução
scrape_and_save("categoria", total_paginas=3)