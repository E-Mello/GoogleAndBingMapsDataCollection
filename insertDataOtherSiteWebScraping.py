from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém os valores das variáveis do arquivo .env
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")
link_do_site = os.getenv("LINK_DO_SITE")
url_address = os.getenv("URL_ADDRESS")


def login(driver):

    # Espera até que o elemento de e-mail seja visível na página
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    # Espera até que o elemento de senha seja visível na página
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    # Preencha o campo de email e senha
    email_input.send_keys(email)
    password_input.send_keys(senha)

    # Localize o elemento com base no texto da pergunta de soma
    sum_question = driver.find_element(
        By.XPATH, "//div[contains(text(), 'Qual a soma de')]")

    # Extrai o texto e processa para obter os valores de x e y
    question_text = sum_question.text
    split_text = question_text.split(" ")
    x_str, y_str = split_text[4], split_text[6]

    # Remove qualquer caractere não numérico dos valores de x e y
    x_str = ''.join(filter(str.isdigit, x_str))
    y_str = ''.join(filter(str.isdigit, y_str))

    # Converte os valores para inteiros
    x, y = int(x_str), int(y_str)
    result = x + y

    # Preenche o campo de resposta
    result_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@id='result-sum']"))
    )
    result_input.clear()
    result_input.send_keys(result)

    # Clica no botão "Verificar"
    verify_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "btn-sum"))
    )
    verify_button.click()

    # Tempo para aguardar a verificação
    time.sleep(2)

    # Espera o botão de login ficar visível
    login_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@value='ENTRAR']"))
    )
    # Clica no botão de login após ele ficar visível
    login_button.click()

    # Tempo para a página carregar
    time.sleep(5)


def cadastrar_endereco(driver, nome, latitude, longitude):
    try:
        # Esperar o botão "Cadastrar Endereço" ficar visível
        add_address_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.btn.btn-primary[data-toggle="modal"][data-target="#addAddressModal"]'))
        )

        # Clica no botão "Cadastrar Endereço"
        add_address_button.click()

        # Teste de funcionamento
        print("Botão 'Cadastrar Endereço' clicado com sucesso.")

        # Espera até que os campos de entrada sejam visíveis
        nameLocal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@id='nameLocal']"))
        )
        latitude_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@id='latitudeLocal']"))
        )
        longitude_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@id='longitudeLocal']"))
        )

        # Limpa os campos
        nameLocal.clear()
        latitude_input.clear()
        longitude_input.clear()

        # Preenche os campos
        nameLocal.send_keys(nome)
        latitude_input.send_keys(latitude)
        longitude_input.send_keys(longitude)

        # Clica em salvar
        save_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@id='btnSaveAddress']"))
        )
        save_button.click()

        # Espera o modal abrir para fechar
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'button.swal-button--confirm'))
        ).click()
        print("Modal fechado com sucesso.")
    # Tratamento de exceções
    except TimeoutException as e:
        print(f"TimeoutException ao clicar em 'Cadastrar Endereço': {str(e)}")
    except Exception as e:
        print(f"Erro desconhecido ao cadastrar endereço: {str(e)}")

        print(f"Erro desconhecido ao cadastrar endereço: {str(e)}")


def main():
    driver = webdriver.Chrome()
    driver.get(link_do_site)
    time.sleep(5)

    # Realiza o login
    login(driver)

    # Acessa a página de cadastro de locais
    driver.get(url_address)

    # Lê os dados do arquivo resultado.csv e preenche o formulário
    with open("resultados_brusque.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nome_endereco = row["Nome"] + " - " + row["Endereço"]
            latitude = row["Latitude"]
            longitude = row["Longitude"]

            # Cadastra endereço
            cadastrar_endereco(driver, nome_endereco, latitude, longitude)

    driver.quit()


if __name__ == "__main__":
    main()
