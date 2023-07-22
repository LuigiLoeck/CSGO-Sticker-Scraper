from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import re
import tkinter as tk
from tkinter import ttk

PATH = "chromedriver.exe"

# Opções do ChromeDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")

# Criar o serviço do ChromeDriver
service = Service(PATH)

# Criar a instancia do ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

def login():
    # Abrir a pagina do csgofloat
    driver.get("https://csgofloat.com")
    steam = driver.find_element(By.XPATH, "/html/body/app-root/div/div[1]/app-header/div/mat-toolbar/div[2]/img")
    steam.click()

def start():

    # Abrir a pagina do csgostash
    Pdriver = webdriver.Chrome(service=service,options=options)
    Pdriver.get("https://csgostash.com/")
    Pdriver.set_window_size(1400,1080)
    time.sleep(5)
    # Aceita os cookies para nao bugar o resto
    cookies = Pdriver.find_element(By.XPATH, "//*[@id=\"unic-b\"]/div/div/div/div[3]/div[1]/button[2]")
    cookies.click()

    # Abrir o arquivo .CSV para escrita
    with open('output.csv', 'w', newline='') as file:
        # Criar objeto de escrita
        writer = csv.writer(file)

        # header
        writer.writerow(["Sticker","Applied","Price"])
        # writer.writerow(["Sticker","Price"])
        # writer.writerow(["Sticker","Applied"])

        # Ler os stickers escolhidos no .CSV
        with open('stickers.csv', 'r') as input_file:
            # Criar objeto de leitura
            reader = csv.reader(input_file)

            # Processar cada linha do arquivo
            for row in reader:
                #Vai no Database
                driver.get("https://csgofloat.com/db")

                array_inputs = [5, 10, 15, 20]
                result = 0

                for nmb in array_inputs:

                    #Encontra o input do sticker 
                    stickerSlot = driver.find_element(By.XPATH, f"//*[@id=\"mat-input-{nmb}\"]")

                    #Encontra o botao de pesquisa
                    btn = driver.find_element(By.XPATH, "/html/body/app-root/div/div[2]/app-float-db/div/div/div/div/div/mat-spinner-button/button/span[1]")

                    print(row[0])
                    stickerSlot.send_keys(row[0])
                    btn.click()
                    time.sleep(5)
                    try:
                        #Encontra o resultado da pesquisa
                        applied = driver.find_element(By.XPATH, "/html/body/app-root/div/div[2]/app-float-db/div/div/app-float-dbtable/div/div/mat-card")
                        match = re.search(r'[\d,]+(\.\d+)?', applied.text)
                        if match:
                            #Soma para o resultado final
                            result += int(match.group().replace(',', ''))
                        else:
                            result += 0
                    except NoSuchElementException:
                        result += 0
                    
                    print(result)

                PSearch = Pdriver.find_element(By.ID, "navbar-search-input")

                PSearch.clear()
                PSearch.send_keys(row[0], Keys.ARROW_DOWN)
                PSendSearch = Pdriver.find_element(By.XPATH, "//*[@id=\"navbar-expandable\"]/form/div/div[1]/span[2]/button")
                PSendSearch.click()
                time.sleep(1)
                PStickerClick = Pdriver.find_element(By.XPATH, "//*[@id=\"___gcse_0\"]/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a")
                PStickerClick.click()
                time.sleep(2)
                
                price = Pdriver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div[1]/div/div[2]/div[2]/table/tbody/tr[2]/td/span").text.replace("R$ ","")
                print(price)
                # Write the row to the output CSV file
                # writer.writerow([row[0], result])
                # writer.writerow([row[0], price])
                writer.writerow([row[0], result, price])
            
            # Pdriver.quit()

window = tk.Tk()
window.geometry("300x150")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, relief="solid", borderwidth=2, foreground="black", background="#e0e0e0")

loginbutton = ttk.Button(window, text="Logar na conta", command=login)
startbutton = ttk.Button(window, text="Começar busca", command=start)

loginbutton.pack(pady = 10)
startbutton.pack(pady = 10)

window.mainloop()


