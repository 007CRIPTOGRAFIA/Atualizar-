# JARVIS AI Assistant with n8n, DeepSeek, and Grok

Este projeto fornece uma base para configurar um assistente de IA estilo JARVIS usando n8n, integrando modelos locais (Ollama) e modelos na nuvem (DeepSeek, Grok).

This project provides a base to set up a JARVIS-style AI assistant using n8n, integrating local models (Ollama) and cloud models (DeepSeek, Grok).

## 🚀 Como começar / How to start

### 1. Pré-requisitos / Prerequisites
- Docker e Docker Compose instalados.

### 2. Configuração / Configuration
1. Clone este repositório (ou copie os arquivos).
2. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edite o arquivo `.env` e defina uma `N8N_ENCRYPTION_KEY` segura.

### 3. Iniciar os serviços / Start services
Execute o comando abaixo:
```bash
docker compose up -d
```

- **n8n:** Acesse em [http://localhost:5678](http://localhost:5678)
- **Ollama:** Rodando em [http://localhost:11434](http://localhost:11434)
- **Qdrant:** Banco de dados vetorial em [http://localhost:6333](http://localhost:6333)

---

## 📊 Banco de Dados e Relatórios Offline

Este setup inclui **PostgreSQL** e **Qdrant** para armazenamento de informações e memória de longo prazo.

### Relatórios de Diagnóstico
O workflow `workflows/offline_diagnostic_report.json` exemplifica como:
1. Coletar dados do sistema (simulado).
2. Salvar logs estruturados no **PostgreSQL**.
3. Gerar um relatório técnico em Markdown usando o **Ollama** (100% offline).

Para usar:
- Importe o JSON no n8n.
- Configure as credenciais do Postgres e Ollama (Host: `postgres` e `ollama`).

### Offline Persistence
Todos os dados são armazenados localmente nos volumes Docker:
- `postgres_storage`: Dados estruturados do n8n e diagnósticos.
- `qdrant_storage`: Memória vetorial para a IA.
- `ollama_storage`: Modelos de IA baixados.

---

## 🤖 Integrando DeepSeek e Grok no n8n

Para usar o DeepSeek ou o Grok no n8n, você deve usar o nó **OpenAI Chat Model**, pois ambos possuem APIs compatíveis com a OpenAI.

### Passos:
1. No n8n, crie um novo Workflow.
2. Adicione um nó **AI Agent**.
3. Conecte um nó **OpenAI Chat Model** ao AI Agent.
4. Nas configurações do nó OpenAI:
   - **Credential:** Crie uma nova credencial OpenAI e insira sua API Key do DeepSeek ou Grok.
   - **Model:** Digite manualmente o nome do modelo (ex: `deepseek-chat` ou `grok-beta`).
   - **Base URL (em Options):**
     - Para **DeepSeek**: `https://api.deepseek.com`
     - Para **Grok (X.AI)**: `https://api.x.ai/v1`

---

## 🏠 Usando IA Local (Ollama)

1. Certifique-se de que o container Ollama está rodando.
2. Baixe um modelo (ex: llama3.2):
   ```bash
   docker exec -it ollama ollama pull llama3.2
   ```
3. No n8n, use o nó **Ollama Chat Model**.
4. Configure o "Ollama Host" como `http://ollama:11434`.

---

## 📂 Estrutura do Projeto

- `docker-compose.yml`: Configuração dos containers.
- `workflows/`: Exemplos de workflows para importar no n8n.
- `shared/`: Pasta compartilhada para arquivos entre o host e os containers.
