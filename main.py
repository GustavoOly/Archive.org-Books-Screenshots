import time
import re
from tqdm import tqdm
from selenium import webdriver

#firefox
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

#chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

#edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


try:

     print("\n\033[92mIniciando o programa...\033[0m")

     url_site = input("\nDigite a url do livro que esta presente no site da archive.org \n\033[92m ->\033[0m ")

     navegador = input("\nPor favor, insira o navegador que você esta usando (edge,firefox ou chrome) \n\033[92m ->\033[0m ")

     armazenarImg = input('\nDefina o caminho onde os prints serao salvos(E.g. /computador/Downloads/nome_do_arquivo) \n\033[92m ->\033[0m ')

     tempoParaScreenshots = input('\nDefina o intervalo em segundos no qual os prints serao capturados\n(depende da velocidade da internet, e importante garantir\nque as paginas serão totalmente carregadas para tirar os prints) \n\033[92m ->\033[0m ')

except UnicodeDecodeError:
     print("Ocorreu um erro de decodificação Unicode. Por favor, verifique a entrada.")

if navegador.lower() == 'edge':
   options = webdriver.EdgeOptions()
   options.add_argument('--headless')
   webdriver_service = Service(EdgeChromiumDriverManager().install())
   browser = webdriver.Edge(service=webdriver_service, options=options)
elif navegador.lower() == 'firefox':
   options = webdriver.FirefoxOptions()
   options.add_argument('--headless')
   webdriver_service = Service(GeckoDriverManager().install())
   browser = webdriver.Firefox(service=webdriver_service, options=options)
elif navegador.lower() == 'chrome':
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   webdriver_service = Service(ChromeDriverManager().install())
   browser = webdriver.Chrome(service=webdriver_service, options=options)
else:
   print("Navegador nao suportado")

try:
     print("\n\033[92mCarregando pagina...\033[0m")

except UnicodeDecodeError:
     print("Ocorreu um erro de decodificação Unicode. Por favor, verifique a entrada.")

for i in tqdm(range(1)):
   browser.get(url_site)

time.sleep(3)

browser.fullscreen_window()

browser.set_window_size(1600, 800)

time.sleep(8)

try:
    # click: botão tela cheia.
    browser.find_element('xpath','//*[@id="BookReader"]/div[2]/div/nav/ul[2]/li[11]/button').click()

except NoSuchElementException:

    print("elemento nao encontrado no DOOM")
# -------------------------------------------------------------------------------

time.sleep(3)

try:
    # set: display:none; na barra de anuncios.
    element = browser.find_element('xpath', '//*[@id="IABookReaderMessageWrapper"]')
    browser.execute_script("arguments[0].style.display = 'none';", element)

except NoSuchElementException:

    print("elemento nao encontrado no DOOM")

xpaths = ['//*[@id="frame"]/div/nav', '//*[@id="frame"]/div/nav/div[1]']

for xpath in xpaths:
    try:
        elemento = browser.find_element('xpath', xpath)
        browser.execute_script("arguments[0].style.opacity = '0';", ocultarIcones)
    except NoSuchElementException:
        print(f"Elemento com XPath {xpath} nao encontrado.")
# -------------------------------------------------------------------------------

time.sleep(1)

print("\n\033[92mTirando prints da paǵina, por favor aguarde... :)\033[0m")

time.sleep(2)

element = browser.find_element('xpath', '//*[@id="BookReader"]/div[2]/div/nav/ul[2]/li[1]/p/span')

text = element.text 

match = re.search(r'\((\d+) of (\d+)\)', text)

if match:

    first_number = int(match.group(1)) 
    second_number = int(match.group(2))

try: 
   removeBarra = browser.find_element('xpath', '//*[@id="BookReader"]/div[2]')
   browser.execute_script("arguments[0].style.opacity = '0';", removeBarra)

except NoSuchElementException:

   print("elemento nao encontrado no DOOM")

for i in tqdm(range(second_number)):

   time.sleep(float(tempoParaScreenshots))

   browser.save_screenshot(f'{armazenarImg}_{i}.png')
    
   # click: botão next.
   browser.find_element('xpath', '//*[@id="BookReader"]/div[2]/div/nav/ul[2]/li[3]/button').click()

# -------------------------------------------------------------------------------------------------

print("\n\033[92mPrints concluidos com sucesso!\033[0m")
input('\nPressione ENTER para sair...')