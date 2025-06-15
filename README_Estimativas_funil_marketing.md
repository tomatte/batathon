# Estimativas Realistas para Funil de Marketing do Projeto Trampolim


#### 📄 Leia também:

- 👉 [📊 Trampolim Overview](./README.md)
- 👉 [💸 Orçamento e Previsão de Custos do Projeto](./README_Budget.md)

---
Este documento descreve como prever, com maior realismo, as taxas de conversão e retenção do funil de marketing do projeto **Trampolim** (chatbot de impacto social via WhatsApp).

---

## 🔍 Etapas para Tornar os Percentuais Mais Realistas

### 1. Fonte do Tráfego (Canais de Aquisição)

Benchmarks com base nos principais canais de tráfego:

| Canal             | CTR médio (%) | CPC médio (R$) | Observações |
|------------------|----------------|----------------|-------------|
| **Meta Ads**     | 1,0% a 2,5%    | R$0,50 a R$1,20| Ótimo para projetos sociais, fácil segmentação regional |
| **Google Ads**   | 3% a 7% (search) | R$1,00 a R$2,00 | Melhor para quem já tem intenção de busca |
| **Impacto direto** (parcerias, eventos, etc.) | Variável | Custo fixo | Ótimo para reforço de marca e causa social |

**Fontes:**
- [Wordstream - Facebook Ads Benchmarks](https://www.wordstream.com/blog/ws/2017/02/28/facebook-advertising-benchmarks)
- [Wordstream - Google Ads Benchmarks](https://www.wordstream.com/blog/ws/2016/02/29/google-adwords-industry-benchmarks)

---

### 2. Benchmarks de Funil (WhatsApp)

| Etapa                          | Conversão esperada | Fonte |
|-------------------------------|--------------------|-------|
| Clicam no WhatsApp            | 100% (do clique)   | Meta / Google |
| Enviam mensagem               | **20–40%**         | Take Blip, Yalo/McKinsey |
| Completam cadastro simples    | **85–95%**         | Conversational UX benchmarks |
| Retenção no mês seguinte     | **10–35%**         | Reforge, Amplitude |

**Fontes:**
- [Take Blip - Conversão em bots](https://www.take.net/blog/)
- [Amplitude Retention Benchmarks](https://www.amplitude.com/blog/product-benchmarks)

---

### 3. Valores Recomendados para o Projeto Trampolim

Com base na proposta do projeto Trampolim (WhatsApp acessível, cadastro facilitado, causa social):

| Métrica                   | Valor sugerido | Justificativa |
|---------------------------|----------------|---------------|
| % enviam mensagem         | **35%**        | Baixo atrito + abordagem amigável |
| % completam cadastro      | **90%**        | Formulário muito simples |
| % de retenção (M+1)      | **25%**        | Valor percebido é bom, mas parte do público é rotativo |

---

### 4. Previsão Realista de Cliques no WhatsApp

#### 🎯 Objetivo

Estimar quantas pessoas clicarão no link do WhatsApp mês a mês, com base em dados reais de mídia paga e otimização progressiva das campanhas. Essa estimativa serve como base para calcular o restante do funil (mensagens, cadastros, retenção etc.).

---

### 📌 Premissas

#### 💰 1. Orçamento de Marketing
- **R$ 7.900 por mês**

#### 🎯 2. Custo por Clique (CPC)
- Estimativa: **R$0,80 por clique** (conservadora e realista)
- Para campanhas sociais com bom apelo visual em Meta Ads (Facebook e Instagram)
- **Fontes:**
  - [Wordstream – Facebook Benchmarks](https://www.wordstream.com/blog/ws/2017/02/28/facebook-advertising-benchmarks)

#### 📈 3. Crescimento Mensal de Cliques
- Supõe-se um **crescimento de 20% ao mês**
- Justificativas:
  - Aprendizado do algoritmo de anúncios (Meta Ads)
  - Crescimento orgânico e boca a boca
  - Iterações e melhorias nas campanhas

---

### ✅ Como Refinar as Estimativas com Dados Reais

Após lançar o projeto, você pode:

- Usar **UTM tracking** em links (ex: `wa.me/12345?utm_source=meta&utm_campaign=lancamento`)
- Medir eventos com **PostHog, Mixpanel ou Amplitude**
- Atualizar as taxas reais com base em dados históricos por planilha ou dashboard

---

### 📊 Conclusão

Use inicialmente as estimativas abaixo como base para simulações:

- **35%** das pessoas que clicam no WhatsApp enviam mensagem
- **90%** das que mandam mensagem completam o cadastro
- **25%** dos cadastrados voltam no mês seguinte
- **20%** de aumento de clicks por mês

Esses números são realistas para bots de WhatsApp com proposta social e podem ser ajustados à medida que você colete dados reais do seu projeto.

Baseado nos valores mostrados acima, segue estimativa

|Mês|	Cliques no WhatsApp	|Mensagens|	Cadastros|	Retidos do Mês Anterior	|Usuários Ativos no Mês|
|-|-|-|-|-|-|
|1	|9.875	|	3.456|		3.110|		0|	3.110|
|2	|11.850	|	4.147|		3.732|		777|	4.510|
|3	|14.220	|	4.977|		4.479|		1.127|	5.606|
|4	|17.064	|	5.972|		5.375|		1.401|	6.776|
|5	|20.476	|	7.166|		6.450|		1.694	|8.144|
|6	|24.572	|	8.600|		7.740|		2.036	|9.776|
|7	|29.486	|	10.320|		9.288|		2.444	|11.732|
|8	|35.383	|	12.384|		11.145|		2.933	|14.079|
|9	|42.460	|	14.861|		13.375|		3.519	|16.894|
|10|	50.952	|	17.833|		16.050|		4.223|	20.273|
|11|	61.143	|	21.400|		19.260|		5.068|	24.328|
|12|	73.372	|	25.680|		23.112|		6.082|	29.194|
				


