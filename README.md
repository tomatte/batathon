# 🤖 Trampolim - Chatbot de Conexão de Serviços

#### 📄 Leia também:

- 👉 [💸 Orçamento e Previsão de Custos do Projeto](./README_Budget.md)
- 👉 [📊 Estimativas Realistas para Funil de Marketing](./README_Estimativas_funil_marketing.md)


---
✅ Observações:

Projeto desenvolvido durante o Hackathon de Presidente Prudente (SP), com foco em impacto social baseado nas [ODS da ONU](https://brasil.un.org/pt-br/sdgs) com foco nas:
- ODS 1 - Erradicação da pobreza
- ODS 8 - Trabalho decente e crescimento
- ODS 9 - Indústria, inovação e infraestrutura

## 🌟 Objetivo

O Trampolim conecta pessoas que precisam de serviços com pessoas que oferecem serviços – com foco na base da pirâmide e nos trabalhadores informais.

Nossa plataforma nasceu para ajudar desde quem precisa de um serviço rápido.
Mas o Trampolim vai além da simples conexão:
👉 Queremos dar suporte, visibilidade e oportunidade de geração de renda para quem está na informalidade.
👉 Nosso objetivo é ajudar esses profissionais a conquistarem mais estabilidade, recorrência de trabalho e até capacitação futura.

Tudo isso por meio de uma interface simples, acessível, humanizada e automatizada via WhatsApp.
**Sem precisar baixar aplicativo, sem burocracia**

<!-- Conectar pessoas que **precisam de serviços** com pessoas que **oferecem serviços** (ex: designers, eletricistas, valetes de dança, diaristas etc.) por meio de uma interface simples, acessível e automatizada via **whatsapp**. -->

---

## 📦 Futuras Expansões
- Inteligência para recomendação automática de prestadores com base no perfil do cliente.
- Parcerias com programas públicos de capacitação
- Dashboard para organizações monitorarem impacto em tempo real
- Escalabilidade sem perder a curadoria humana
- Segurança e moderação de vagas
---

## 🧠 Tecnologias Utilizadas

| Camada | Tecnologia | Descrição |
|--------|------------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) | Framework Python assíncrono para APIs Web. Responsável pelo core do chatbot e roteamento das interações. |
| Geração Visual | HTML + [Jinja2](https://jinja.palletsprojects.com/en/stable/) | Templates usados apenas como base visual para gerar um cartão de visitas, sem frontend para o usuário. |
| Headless Browser | [Playwright](https://playwright.dev/python/) | Utilizado para renderizar o HTML gerado e capturar um **screenshot** do cartão de apresentação do prestador. |
| Infraestrutura | [Docker](https://www.docker.com/) | Empacotamento e execução do projeto com ambiente isolado e reproduzível. |
| Dependências | [uv](https://github.com/astral-sh/uv) | Ferramenta rápida para instalação e sincronização de dependências via `pyproject.toml`. |
| Inteligência Artificial | [OpenAI](https://openai.com/api/) | Utilizado para gerar respostas inteligentes no fluxo do chatbot. |

---

## 🚀 Como Rodar Localmente

1. **Pré-requisitos:**
   - Python 3.11+
   - Docker (opcional)
   - [uv](https://github.com/astral-sh/uv) instalado (alternativa ao pip)
   - Playwright instalado (manual)

2. **Rodando com uv (modo local):**
```bash
uv venv
uv sync
uv pip install playwright
playwright install
uvicorn src.main:app --reload
```

3. **Rodando com Docker:**
```bash
docker-compose up --build
```

## 💬 Funcionalidade Principal
1. Prestador de serviço entra em contato com o bot pelo whatsapp

2. 

2. Backend processa os dados e renderiza um cartão HTML com as informações.

3. O HTML é renderizado em um navegador headless (Playwright) e transformado em imagem.

4. A imagem é retornada e pode ser enviada via WhatsApp ou compartilhada.

## 🧑‍💻 Time
Desenvolvido por um time participante do Hackathon de Presidente Prudente com foco em impacto social e soluções acessíveis via tecnologia.

