from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time

# Defina a cidade e a lista de categorias
cidade = "Brusque"
categorias = ["Restaurantes", "Hoteis", "Supermercados", "Comércios", "Escolas",
              "Hospitais", "Clinicas", "Farmácias", "Postos de gasolina", "Coisas para fazer", "Bares"]

# Conjunto para lugares únicos
lugares_unicos = set()


def pesquisar_categorias(driver):
    for categoria in categorias:
        # Navegar para a página de pesquisa do Bing Maps
        driver.get("https://www.bing.com/maps")

        # Encontrar o campo de pesquisa e inserir a categoria desejada
        search_box = driver.find_element(By.ID, "maps_sb")
        pesquisa = f"{categoria} em {cidade}"
        search_box.send_keys(pesquisa)
        search_box.send_keys(Keys.RETURN)

        # Esperar por alguns segundos para os resultados carregarem
        time.sleep(5)

        # Função para coletar informações dos resultados
        coletar_resultados(driver, categoria)


def coletar_resultados(driver, categoria):
    # Encontrar a lista de pontos encontrados na barra lateral esquerda
    lista_pontos = driver.find_elements(
        By.CSS_SELECTOR, "ul.b_vList.b_divsec > li")

    for ponto in lista_pontos:
        # Extrair informações relevantes do ponto encontrado
        dados_ponto = ponto.find_element(
            By.CSS_SELECTOR, "a.listings-item").get_attribute("data-entity")

        nome = dados_ponto.split('"title":"')[1].split('"')[0]
        endereco = dados_ponto.split('"address":"')[1].split('"')[0]

        # Latitude e longitude
        latitude = float(dados_ponto.split('"y":')[1].split(',')[0])
        longitude = float(dados_ponto.split('"x":')[1].split(',')[0])

        # Verificar se este lugar já foi adicionado aos lugares únicos
        if (nome, endereco, latitude, longitude) not in lugares_unicos:
            lugares_unicos.add((nome, endereco, latitude, longitude))

    # Chamar a função para salvar os dados em um arquivo CSV no final da lista de categorias
    if categoria == categorias[-1]:
        salvar_csv(list(lugares_unicos))


def salvar_csv(dados):
    with open('resultados_brusque.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)

        # Escrever o cabeçalho do CSV
        writer.writerow(["Nome", "Endereço", "Latitude", "Longitude"])

        # Escrever os dados dos resultados
        writer.writerows(dados)


def main():
    driver = webdriver.Chrome()

    # Função para pesquisar as categorias
    pesquisar_categorias(driver)

    # Fechar o navegador no final
    driver.quit()


if __name__ == "__main__":
    main()
