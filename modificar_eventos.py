import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from time import sleep

service = webdriver.ChromeService(executable_path=".\\utils\\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\danielsson\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(service=service, options=options)
actions = ActionChains(driver)

def criar_janela():
    janela = tk.Tk()
    janela.title("Modificar paradas com mais de duas horas")

    label_data_inicio = ttk.Label(janela, text="Data de Início:")
    label_data_inicio.grid(row=0, column=0, padx=2, pady=5)

    entry_data_inicio = ttk.Entry(janela)
    entry_data_inicio.grid(row=0, column=1, padx=2, pady=5)

    label_data_fim = ttk.Label(janela, text="Data Final:")
    label_data_fim.grid(row=1, column=0, padx=10, pady=5)

    entry_data_fim = ttk.Entry(janela)
    entry_data_fim.grid(row=1, column=1, padx=10, pady=5)

    botao_data_hoje = ttk.Button(janela, text="Hoje", command=lambda: pegar_data_hoje(entry_data_fim))
    botao_data_hoje.grid(row=1, column=2, padx=3, pady=5)

    botao_iniciar = ttk.Button(janela, text="Iniciar", command=lambda: iniciar(entry_data_inicio.get(), entry_data_fim.get()))
    botao_iniciar.grid(row=2, column=0, columnspan=1, pady=5)

    botao_loop_tabela = ttk.Button(janela, text="Verificar eventos", command=lambda: loop_tabela())
    botao_loop_tabela.grid(row=3, column=0, columnspan=1, pady=5)
    
    janela.mainloop()

def pegar_data_hoje(entry_data_fim):
    data_hoje = datetime.now()
    formato_data = data_hoje.strftime("%d/%m/%Y")
    entry_data_fim.delete(0, "end")
    entry_data_fim.insert(0, formato_data)

manutencao = "//div[@id='ext-element-365']"
eventos = "//div[@id='container-1027-innerCt']"
input_data_inicial = "//input[@id='dateStarteventProgramContainer-1019FilterPanel-inputEl']"
input_data_fim = "//input[@id='dateFinisheventProgramContainer-1019FilterPanel-inputEl']"
input_evento = "//input[@id='eventOperationalComboboxeventProgramContainer-1019FilterPanel-inputEl']"
botao_busca = "//span[@id='button-1022-btnInnerEl']"
ordem_duracao = "//div[@id='gridcolumn-1033-textContainerEl']"
evento = "PARADA NÃO JUSTIFICADA"

def iniciar(data_inicio, data_fim):
    
    driver.get("https://sfm.weg.net/#event-program")

    # ESCREVER EVENTO PARADA NÃO JUSTIFICADA
    driver.find_element(By.XPATH, input_evento).click()
    actions.send_keys(evento); actions.perform(); sleep(0.5)
    actions.send_keys(Keys.ENTER); actions.perform()

    driver.find_element(By.XPATH, input_evento).clear()
    driver.find_element(By.XPATH, input_evento).send_keys(evento)
    driver.find_element(By.XPATH, input_evento).send_keys(Keys.ENTER)

    data_inicio = "28/01/2024"
    data_fim = "01/02/2024"

    driver.find_element(By.XPATH, input_data_inicial).clear()
    driver.find_element(By.XPATH, input_data_inicial).send_keys(data_inicio, " 00:00:00")
    driver.find_element(By.XPATH, input_data_fim).clear()
    driver.find_element(By.XPATH, input_data_fim).send_keys(data_fim, " 00:00:00")

    driver.find_element(By.XPATH, botao_busca).click()
    driver.find_element(By.XPATH, ordem_duracao).click(); sleep(0.5)
    driver.find_element(By.XPATH, ordem_duracao).click()

row = "//table[@data-recordindex='0']"
celula = "//td[@data-columnid='gridcolumn-1033']"

def loop_tabela():
    sleep(1)
    rows = "//table[@data-boundview='tableview-1035']"
    driver.find_element(By.XPATH, rows)
    
    for row in range(20):
        elemento_pai = driver.find_element(By.XPATH, f"//table[@data-recordindex='{row}'][@role='presentation']")
        elemento_filho = elemento_pai.find_element(By.XPATH, ".//td[@data-columnid='gridcolumn-1033']")
        tempo = elemento_filho.text
        tempo_timedelta = datetime.strptime(tempo, "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")
        limite_2_horas = timedelta(hours=2)

        if tempo_timedelta > limite_2_horas:
            modificar_evento(elemento_pai, driver)
            print(tempo, " - Vai ser modificado (maior que 2 horas)")
            
        else:
            print(tempo, " - Não vai ser modificado (menor que 2 horas)")
            pass


def modificar_evento(elemento_pai, driver):
    input_evento_ = elemento_pai.find_element(By.XPATH, ".//td[@data-columnid='combocolumn-1028']")
    click_element = elemento_pai.find_element(By.XPATH, ".//div[@class='x-grid-cell-inner ']")

    actions.double_click(click_element).perform()

    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys(Keys.DELETE)
    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys("FALTA DE PROGRAMAÇÃO")
    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys(Keys.SPACE)
    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys(Keys.BACK_SPACE)
    driver.find_element(By.XPATH, "//input[@name='EventOperationalId']").send_keys(Keys.ENTER)

    driver.find_element(By.XPATH, "//span[@class='x-btn-inner x-btn-inner-default-small'][text()='Salvar']").click()
    
criar_janela()
