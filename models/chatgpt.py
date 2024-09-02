import time
import pyttsx3
import speech_recognition as sr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from frikiapps.iniciar_webdriver_uc import iniciar_webdriver

class ChatGpt:
    def __init__(self):
        print('Iniciando Webdriver')
        self.driver = iniciar_webdriver(headless=False, pos="maximizada")
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://chat.openai.com/")
        print('Cargando CHATGPT')

        # Configuración de texto a voz
        self.engine = pyttsx3.init()

        # Configuración de reconocimiento de voz
        self.recognizer = sr.Recognizer()

        # Leer preferencia del archivo
        self.preference_file = 'preference.txt'
        self.preference = self._load_preference()

    def _load_preference(self):
        try:
            with open(self.preference_file, 'r') as file:
                preference = file.read().strip().lower()
                if preference in ['h', 'e']:
                    return preference
        except FileNotFoundError:
            return None

    def _save_preference(self, preference):
        with open(self.preference_file, 'w') as file:
            file.write(preference)

    def chatear(self, prompt):
        e = self.driver.find_element(By.CSS_SELECTOR, "textarea[tabindex='0']")
        e.send_keys(prompt)
        time.sleep(3)

        e = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="send-button"]')))
        e.click()

        respuesta = ""
        inicio = time.time()
        segundos = 0

        while True:
            try:
                e = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="stop-button"]')))
            except:
                try:
                    e = self.driver.find_elements(By.XPATH, "//div[@class='markdown prose w-full break-words dark:prose-invert light']")[-1]
                    respuesta = e.text
                except:
                    pass
                try:
                    e = self.driver.find_elements(By.XPATH, "//div[@class='markdown prose w-full break-words dark:prose-invert dark']")[-1]
                    respuesta = e.text
                except:
                    pass
                if respuesta:
                    break

            segundos = int(time.time() - inicio)
            print(f'Generando respuesta... {segundos} segundos ({len(respuesta)} caracteres)')
            time.sleep(1)

        print(f'Respuesta generada en: {segundos} segundos')
        self._speak(respuesta)
        return respuesta

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def escuchar(self):
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Texto reconocido: {text}")
                return text
            except sr.UnknownValueError:
                print("No se pudo entender el audio")
                return None
            except sr.RequestError:
                print("Error al conectar con el servicio de reconocimiento de voz")
                return None

    def cambiar_preferencia(self):
        print("¿Deseas hablar o escribir? (H/E):")
        choice = input().strip().lower()
        if choice in ['h', 'e']:
            self.preference = choice
            self._save_preference(choice)
        else:
            print("Opción no válida. No se cambió la preferencia.")

    def cerrar(self):
        print('Saliendo...')
        self.driver.quit()
