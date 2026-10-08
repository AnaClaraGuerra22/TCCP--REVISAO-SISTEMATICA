# Validação do apoio por LLM no screening — v1

- Data: 2026-10-08
- Etapa: validação cega da pré-triagem assistida por LLM
- Modelo: `qwen3:4b`
- Model ID: `359d7dd4bcda`
- Runtime: Ollama
- Prompt: `v1.2-candidate`
- Temperature: `0`
- Seed: `42`
- Thinking: `false`
- Structured output: JSON

## 1. Objetivo

Avaliar se o procedimento baseado em Qwen3:4B apresenta sensibilidade
suficiente para ser utilizado como apoio ao screening de título e resumo,
sem conceder ao modelo autoridade para realizar exclusões automáticas.

A prioridade da validação é evitar falsas exclusões de registros
potencialmente elegíveis.

## 2. Arquitetura avaliada

O LLM não produz diretamente a decisão final de screening.

Para cada registro, o modelo avalia separadamente:

- `primary_study`: yes / no / unclear;
- `operational_rag`: yes / no / unclear;
- `environmental_domain`: yes / no / unclear;
- `empirical_evaluation`: yes / no / unclear;
- `rag_role`: central / baseline_or_comparator / unclear / not_applicable.

Uma regra determinística implementada em Python deriva posteriormente:

- `include`;
- `exclude`;
- `maybe`;

e, quando aplicável, o código principal `CE1–CE4`.

As decisões formais da revisão permanecem sob responsabilidade da
revisora.

## 3. Conjunto de desenvolvimento

Os 18 registros anteriormente utilizados para calibrar os critérios
humanos foram empregados como conjunto de desenvolvimento da assistência
por LLM.

Esse conjunto foi utilizado para comparar modelos e arquiteturas de
prompt e, portanto, não foi utilizado como evidência independente de
validação.

O Qwen3:4B foi selecionado como candidato operacional devido ao equilíbrio
entre custo computacional e preservação de sensibilidade.

## 4. Conjunto de validação

Foi selecionada uma nova amostra de 30 registros a partir do conjunto
deduplicado, excluindo os 18 registros de desenvolvimento.

O conjunto foi apresentado ao Qwen sem as colunas de decisão humana.

Arquivo de entrada:

`validation_blind_v1.csv`

SHA-256:

`015679f23a17682408c9c372b4b827ee46286108437ae556c011f17e2e175b74`

A referência foi finalizada pela revisora antes da inspeção das saídas
do Qwen.

Durante a aplicação dos critérios aos registros de validação, casos foram
discutidos com ChatGPT como apoio de adjudicação protocolar. Portanto, o
conjunto deve ser descrito como uma referência finalizada pela revisora
com apoio protocolar, e não como uma classificação humana totalmente
independente de ferramentas de IA.

## 5. Referência

Distribuição das 30 decisões de referência:

- include: 5
- maybe: 6
- exclude: 19

Códigos de exclusão:

- CE1: 3
- CE2: 13
- CE3: 3
- CE4: 0

Arquivo original da revisora:

`validation_human_v1.xlsm`

SHA-256:

`c2fcf7cbb75a8247d9af3784a1830217f787384108f0c4df30f8548c78e7a2c7`

## 6. Execução do Qwen3:4B

A validação foi executada em 2026-10-08.

- Registros processados: 30
- Saídas válidas: 30
- Erros: 0
- Tempo total: 1354.48 segundos

Distribuição das sugestões derivadas:

- include: 11
- maybe: 2
- exclude: 17

Códigos derivados:

- CE1: 1
- CE2: 12
- CE3: 3
- CE4: 1

O modelo recebeu apenas os campos bibliográficos do conjunto cego.
As decisões de referência não foram fornecidas durante a inferência.

## 7. Resultados

### 7.1 Concordância global

- Concordância exata: 22/30
- Concordância exata percentual: 73,3%
- Cohen's kappa: 0,5294

O kappa é apresentado como medida descritiva de concordância e não como
critério principal de aprovação da ferramenta.

### 7.2 Segurança para screening

Registros classificados pela referência como:

- include: 5
- maybe: 6
- include + maybe: 11

Resultados críticos:

- human include -> Qwen exclude: 0
- human maybe -> Qwen exclude: 0
- falsas exclusões entre registros retidos: 0
- registros retidos pelo Qwen: 11/11
- sensibilidade de retenção: 100%

### 7.3 Concordância dos códigos de exclusão

Dos 19 registros excluídos pela referência:

- 17 também foram excluídos pelo Qwen;
- em 15 dos 17 casos houve concordância exata no código CE;
- concordância de código entre exclusões conjuntas: 88,2%.

### 7.4 Matriz de confusão

| Referência \\ Qwen | include | maybe | exclude |
|---|---:|---:|---:|
| include | 4 | 1 | 0 |
| maybe | 5 | 1 | 0 |
| exclude | 2 | 0 | 17 |

## 8. Discordâncias

Foram observadas oito discordâncias de decisão:

| validation_id | record_id | Referência | Qwen |
|---|---|---|---|
| V03 | R0029 | maybe | include |
| V06 | R0268 | exclude — CE1 | include |
| V10 | R0184 | maybe | include |
| V11 | R0072 | maybe | include |
| V15 | R0472 | include | maybe |
| V17 | R0251 | maybe | include |
| V27 | R0052 | exclude — CE1 | include |
| V28 | R0386 | maybe | include |

Nenhuma discordância correspondeu a uma falsa exclusão de registro
retido pela referência.

As divergências observadas foram predominantemente conservadoras,
fazendo o Qwen reter registros adicionais para avaliação humana.

## 9. Gate definido previamente

Antes da inspeção das saídas do modelo foram definidos três critérios:

### G1

Todos os 30 registros devem produzir saídas estruturalmente válidas.

Resultado: **PASS**

### G2

`human include -> Qwen exclude = 0`

Resultado: **PASS**

### G3

Sensibilidade de retenção >= 0,90.

Resultado observado: `11/11 = 1,000`

Resultado: **PASS**

## 10. Decisão

**FINAL GATE: PASS**

O Qwen3:4B com o prompt v1.2 e a arquitetura criterial é aprovado para
uso operacional como ferramenta de apoio ao screening de título e resumo.

A aprovação não autoriza exclusões automáticas.

As saídas do modelo devem ser utilizadas apenas como apoio à revisora,
que continuará responsável pela decisão formal de:

- include;
- exclude;
- maybe;

e pelo código de exclusão registrado no `decision_log.csv`.

O procedimento aprovado permanece congelado para a aplicação operacional.
Alterações posteriores no modelo, prompt, critérios, regra determinística
ou parâmetros de inferência exigem versionamento e nova justificativa
metodológica.