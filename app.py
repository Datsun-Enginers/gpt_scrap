import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from frikiapps.colores import azul, gris, amarillo, magenta, azul2, blanco
from frikiapps.cursor_arriba import cursor_arriba
from frikiapps.iniciar_webdriver_uc import iniciar_webdriver

class ChatGpt:
    def __init__(self):
        print(f'{azul}Iniciando Webdriver{gris}')
        self.driver = iniciar_webdriver(headless=False, pos="maximizada")
        self.wait = WebDriverWait(self.driver, 30)

        # Abre la página de ChatGPT directamente
        self.driver.get("https://chat.openai.com/")
        print(f'{azul}Cargando CHATGPT{gris}')

    def chatear(self, prompt):
        # Envía el mensaje al campo de texto
        e = self.driver.find_element(By.CSS_SELECTOR, "textarea[tabindex='0']")
        e.send_keys(prompt)

        # Espera un momento para asegurarse de que el botón de envío sea visible y clickeable
        time.sleep(3)

        # Encuentra y hace clic en el botón de enviar
        e = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="send-button"]')))
        e.click()

        respuesta = ""
        inicio = time.time()

        while True: 
            try:
                e = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="stop-button"]')))
            except:
                try:
                    e = self.driver.find_elements(By.XPATH,"//div[@class='markdown prose w-full break-words dark:prose-invert light']")[-1]
                    respuesta = e.text
                except:
                    pass
                try:
                    e = self.driver.find_elements(By.XPATH,"//div[@class='markdown prose w-full break-words dark:prose-invert dark']")[-1]
                    respuesta = e.text
                except:
                    pass
                if respuesta:
                    break
                
            segundos = int(time.time() - inicio)
            print(f'\33[K{azul2}Generando respuesta...{gris}{segundos} segundos ({len(respuesta)} caracteres){gris}')
            time.sleep(1)
            cursor_arriba()

        print(f'\33[K{magenta}Respuesta generada en: {blanco}{segundos} {magenta}segundos{gris}')
        return respuesta

    def cerrar(self):
        print(f'{azul}Saliendo...{gris}')
        self.driver.quit()

#________________MAIN_____________________#
if __name__ == "__main__":
    chatgpt = ChatGpt()

    while True:
        prompt = input(f'{azul}Prompt (S=Salir): {gris}')

        if prompt.lower() == "s":
            chatgpt.cerrar()
            sys.exit()
        else:
            respuesta = chatgpt.chatear(prompt)
            print(f'{amarillo}{respuesta}{gris}')
            print()
