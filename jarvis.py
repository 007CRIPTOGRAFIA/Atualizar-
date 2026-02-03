import ollama
import pyautogui
import speech_recognition as sr
import pyttsx3
import datetime
import os
import subprocess
import webbrowser
import logging
import sys
import psutil
from scapy.all import conf, sniff

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("jarvis.log")
    ]
)
logger = logging.getLogger(__name__)

class Jarvis:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
        logger.info(f"Initializing Jarvis with model: {self.model}")
        try:
            self.engine = pyttsx3.init()
            logger.info("TTS engine initialized.")
        except Exception as e:
            logger.warning(f"Failed to initialize TTS engine: {e}. Audio output will be disabled.")
            self.engine = None

        self.recognizer = sr.Recognizer()
        self.check_ollama_status()

    def check_ollama_status(self):
        try:
            # Check if ollama server is responsive
            ollama.list()
            logger.info("Ollama server is reachable.")
            return True
        except Exception as e:
            logger.warning(f"Ollama server is not responding: {e}. LLM features will be unavailable.")
            return False

    def speak(self, text):
        logger.info(f"Jarvis says: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS error: {e}")
        else:
            print(f"JARVIS: {text}")

    def listen(self):
        # In a headless environment, this will fail.
        # For testing, we might want to mock this or use text input.
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language="pt-BR")
                logger.info(f"User said: {text}")
                return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            logger.debug(f"Speech recognition error/Microphone not found: {e}")
            return ""

    def ask_llm(self, question):
        try:
            logger.info(f"Querying Ollama with: {question}")
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': 'Você é Jarvis, um assistente avançado estilo Homem de Ferro. Responda em português de forma prestativa e elegante.'},
                {'role': 'user', 'content': question}
            ])
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "Desculpe, senhor. Tive um problema ao processar sua solicitação com o modelo local. Verifique se o Ollama está rodando."

    def get_network_info(self):
        try:
            # Using scapy's conf.iface to get the default interface
            iface = conf.iface
            logger.info(f"Default network interface detected: {iface}")
            return str(iface)
        except Exception as e:
            logger.error(f"Error detecting network interface: {e}")
            return "Unknown"

    def run_network_diagnostics(self):
        self.speak("Iniciando diagnósticos de rede, senhor.")
        iface = self.get_network_info()
        self.speak(f"Interface padrão detectada: {iface}")

        try:
            logger.info("Sniffing packets for diagnostics...")
            # Capture a few packets to show network activity
            packets = sniff(count=5, timeout=5)
            packet_summary = f"Capturados {len(packets)} pacotes na rede."
            logger.info(packet_summary)
            self.speak(packet_summary)
            if len(packets) > 0:
                self.speak("A rede parece estar ativa e processando tráfego.")
        except Exception as e:
            logger.error(f"Explicit error during packet processing: {e}")
            self.speak("Houve uma falha ao tentar processar pacotes de rede. Pode ser necessário permissão de administrador.")

    def check_hardware(self):
        self.speak("Verificando integridade do hardware...")
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            report = f"Uso de CPU em {cpu_usage}%, Memória RAM em {ram_usage}%, e Disco em {disk_usage}%."
            logger.info(f"Hardware report: {report}")
            self.speak(report)

            if cpu_usage > 80 or ram_usage > 80:
                self.speak("Aviso: Alguns recursos estão com uso elevado, senhor.")
        except Exception as e:
            logger.error(f"Error checking hardware: {e}")
            self.speak("Não consegui obter todos os dados de hardware.")

    def execute_command(self, command):
        if not command:
            return

        logger.info(f"Executing command: {command}")

        if "horas" in command:
            hora = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"São exatamente {hora}, senhor.")

        elif "abrir" in command:
            app = command.replace("abrir", "").strip()
            self.speak(f"Abrindo {app}, senhor.")
            try:
                if "chrome" in app:
                    if os.name == 'nt':
                        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
                    else:
                        subprocess.Popen(["google-chrome"])
                elif "notepad" in app or "bloco de notas" in app:
                    if os.name == 'nt':
                        subprocess.Popen(["notepad.exe"])
                    else:
                        subprocess.Popen(["gedit"])
                else:
                    webbrowser.open(f"https://www.google.com/search?q={app}")
            except Exception as e:
                logger.error(f"Error opening app: {e}")
                self.speak(f"Desculpe, não consegui abrir {app}.")

        elif "escrever" in command:
            texto = command.replace("escrever", "").strip()
            try:
                pyautogui.write(texto)
                self.speak("Texto inserido conforme solicitado.")
            except Exception as e:
                logger.error(f"PyAutoGUI error: {e}")
                self.speak("Houve um erro ao tentar escrever no teclado.")

        elif "clicar" in command or "mouse" in command:
            try:
                pyautogui.click()
                self.speak("Clique executado.")
            except Exception as e:
                logger.error(f"PyAutoGUI error: {e}")
                self.speak("Não consegui controlar o mouse.")

        elif "hardware" in command or "sistema" in command:
            self.check_hardware()

        elif "rede" in command or "internet" in command or "wifi" in command:
            self.run_network_diagnostics()

        else:
            resposta = self.ask_llm(command)
            self.speak(resposta)

    def run(self):
        self.speak("Sistemas inicializados e online, senhor. Como posso ajudar?")
        while True:
            comando = self.listen()
            if "jarvis" in comando or "ei jarvis" in comando:
                self.speak("Sim, senhor?")
                comando_real = self.listen()
                if "desativar" in comando_real or "sair" in comando_real:
                    self.speak("Desligando sistemas. Tenha um bom dia, senhor.")
                    break
                self.execute_command(comando_real)

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
