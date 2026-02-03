# JARVIS - Local Virtual Assistant

Este é um assistente virtual avançado inspirado no JARVIS do Homem de Ferro, projetado para rodar localmente no seu PC de forma gratuita.

## Funcionalidades / Features

- **Conversação por Voz/Texto**: Integrado com Ollama (Llama 3.2).
- **Controle do Sistema**: Abrir aplicativos, escrever textos, controlar o mouse.
- **Diagnóstico de Hardware**: Verificação de CPU, RAM e Disco.
- **Diagnóstico de Rede**: Detecção dinâmica de interface e monitoramento de pacotes (Packet Processing).
- **Logs Abrangentes**: Registro de todas as atividades para depuração.

## Requisitos / Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) instalado e rodando.
- Bibliotecas do sistema para áudio (PortAudio) e interface gráfica (X11 no Linux).

## Instalação / Installation

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Certifique-se de que o Ollama está rodando e o modelo desejado foi baixado:
   ```bash
   ollama pull llama3.2:3b
   ```

3. Execute o assistente:
   ```bash
   python jarvis.py
   ```

## Comandos Exemplos / Example Commands

- "Jarvis, que horas são?"
- "Jarvis, abrir notepad."
- "Jarvis, escrever Olá Mundo!"
- "Jarvis, como está o sistema?" (Verifica hardware)
- "Jarvis, verifique a rede." (Inicia diagnósticos de rede)

## Abordagem Avançada (n8n + Docker)

Para uma experiência ainda mais potente, você pode utilizar o **n8n** com Docker para criar workflows visuais.
Recomendamos o [Self-hosted AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) oficial.

---

# English Description

This is an advanced virtual assistant inspired by Iron Man's JARVIS, designed to run locally on your PC for free.

## How it works

The assistant uses **Ollama** for local LLM processing, **SpeechRecognition** for voice-to-text, and **PyAutoGUI** for system automation. It also includes advanced networking tools using **Scapy** for traffic monitoring and **psutil** for hardware health checks.

## Setup

Refer to the Installation section above. Ensure you have the necessary system headers for `pyaudio` and `scapy` (which may require administrator privileges for network sniffing).
