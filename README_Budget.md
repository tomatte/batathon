# Orçamento e previsão de custos do projeto

#### 📄 Leia também:

- 👉 [📊 Trampolim Overview](./README.md)
- 👉 [📊 Estimativas Realistas para Funil de Marketing](./README_Estimativas_funil_marketing.md)

--- 

## 🧾 Necessidades técnicas
| Item | Descrição |
| - | - |
| Coolify | Painel PaaS self-hosted (grátis) |
| Hospedagem cloud | Infraestrutura para  rodar Coolify e containers |
| PostgreSQL | Banco relacional |
| FastAPI | Backend Python |
| Frontend | HTML/CSS/JS |
| Containerização | Docker (Coolify já suporta) |
| Redis | Cache e sessões |

## 🔧 Premissas técnicas:
- 900 mil usuários não únicos
- Site e API otimizados com média de 200 KB por requisição
- Infra com auto scaling manual, para economizar
- Utilização de Coolify para deploy via Docker Compose
- Uso de instâncias reservadas ou spot quando possível
- Custo mensal estimado para **pico de uso** (escala conforme necessário)

## 📊 Parâmetros da estimativa
1. Volume total de usuários
- 900 mil de interações
- Cada usuário faz em média 6 interações com o chatbot

2. Modelo utilizado
Assumindo o uso de agentes com o fastagent com OpenAI por trás, o modelo escolhido foi

| Modelo | Preço (jun/2025) | Prompt | Completion |
|-----|-------|------|-------|
| gpt-3.5-turbo	| $0.50 / milhão tokens |	$0.50 | $1.50 |


3. Consumo médio por interação

Uso estimado de tokens:

**Prompt** (sistema + mensagem anterior + input do usuário): ~800 tokens
**Completion** (resposta do modelo): ~300 tokens
**Total por interação:** ~1100 tokens (média)

```text
Prompt tokens:     5.4M × 800 = 4.320.000.000 tokens (4.32B)
Completion tokens: 5.4M × 300 = 1.620.000.000 tokens (1.62B)
Total tokens:                 = 5.940.000.000 tokens (5.94B)
```

### 📉 Custo total estimado Com GPT-3.5-turbo
```
Prompt:     4.32M × $0.50 = $2.16
Completion: 1.62M × $1.50 = $2.43
```


Total: ≈ $2.16 + $2.43 = $4.59

Total em reais: ≈ R$4.59 × 5.5 = R$25,25

### 🏠 Infraestrutura Principal (Máquinas virtuais para Coolify, backend, frontend)

| Item (AWS) | Custo |
|-|-|
| 1x VM para Coolify + backend (2vCPU, 4GB RAM, Linux) | R$90–120 (EC2 t3a.medium com RI/spot) |
| 1x disco SSD 50GB | R$20 |
| 1x Load Balancer (ALB ou App Gateway) | R$45 |

### 🗃️ Banco de Dados

| Item (AWS) | Custo |
|-|-|
|RDS PostgreSQL (db.t3.micro, 20GB)|R$80|

### ⚡ Redis

| Item (AWS) | Custo |
|-|-|
| ElastiCache (cache.t4g.micro)	| R$75 |

### 🧪 Tráfego / Transferência de Dados

| Item  | Custo |
|-|-|
| Egres 900 mil acessos x 200KB = 180GB/mês | R$25 |


## 🧮 Resumo geral do projeto (por mês)
| Item | Valor |
| - | - |
| Infra cloud (VMs, LB) | R$185 |
| Redis/Postgres | R$155 |
| Tráfego 180GB/mês	| R$25 |
| OpenAI API (GPT-3.5-turbo) | R$25,25 |
| **Total mensal** | **R$390,25** |

## Custo humano básico
| Cargo | Salário |
|-|-|
| Sócio (pró-labore) | R$ 1.518,00 x 6|
| **Total mensal** | **R$9.108,00** |

## Marketing (reforçado)

Considera-se um teto de R$95.000 para ser utilizado em marketing no primeiro ano.


## Custo total no primeiro ano

| Item | Valor |
|-|-|
|Infraestrutura|R$4.683,00|
|Custo Humano|R$109.296,00|
|Marketing|R$95.000,00|
|**Total**|**R$208.979,00**|


### Fontes:
- Salário utilizando valor base consultando o [GlassDoor](https://www.glassdoor.com.br/Sal%C3%A1rios/index.htm) para o ano de 2025.
- Infraestrutura calculada utilizando a [AWS Pricing Calculator](https://calculator.aws/) e [OpenAI Docs](https://platform.openai.com/docs/pricing)

