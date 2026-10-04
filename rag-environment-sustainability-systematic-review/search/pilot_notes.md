# Notas da busca piloto

## Objetivo

Este arquivo registra as execuções piloto da estratégia de busca, os testes controlados realizados para refinamento das strings e os principais padrões de ruído observados.

As classificações `R`, `I` e `D` utilizadas nas amostras possuem finalidade exclusivamente diagnóstica:

- `R` = aparentemente relevante;
- `I` = claramente irrelevante;
- `D` = duvidoso.

Essas classificações não correspondem à triagem formal dos estudos e não devem ser utilizadas para estimar precisão ou recall da revisão.

---

# 1. Scopus

## 1.1 Execução inicial — v0.1

- Data: 2026-10-04
- Base: Scopus
- Versão da string: `v0.1`
- Período: 2020-presente
- Resultados retornados: 2.154
- Ordenação utilizada durante a inspeção: `Date (newest)`
- Status: busca piloto
- Busca definitiva: não executada

### String executada

```text
TITLE-ABS-KEY(
  (
    "retrieval augmented generation"
    OR "retrieval-augmented generation"
    OR "retrieval enhanced generation"
    OR "retrieval-enhanced generation"
    OR "GraphRAG"
    OR "graph RAG"
    OR "agentic RAG"
    OR "multimodal RAG"
    OR ("RAG" AND ("large language model*" OR LLM*))
  )
  AND
  (
    environment*
    OR sustainab*
    OR climat*
    OR ecolog*
  )
)
AND PUBYEAR > 2019
```

## 1.2 Validação pelos estudos-semente — v0.1

- Estudos-semente avaliados: 12
- Estudos-semente confirmadamente indexados na Scopus: 11
- Estudos-semente recuperados pela string: 11
- Estudos-semente não indexados: 1
- Estudo não indexado: S04 — `ClimateGPT: Towards AI Synthesizing Interdisciplinary Research on Climate Change`
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

A taxa-semente é utilizada apenas como indicador interno de calibração e não representa recall formal da literatura.

## 1.3 Diagnóstico de ruído — v0.1

Foi utilizada uma amostra diagnóstica de 17 registros distribuídos ao longo da listagem ordenada por `Date (newest)`.

- Claramente relevantes (`R`): 0
- Claramente irrelevantes (`I`): 13
- Duvidosos (`D`): 4

Distribuição:

- `R`: 0,0%
- `I`: 76,5%
- `D`: 23,5%

A amostra possui finalidade exclusivamente diagnóstica e não deve ser extrapolada para os 2.154 registros retornados.

### Principais padrões de ruído

O termo `environment*` recuperou usos não ambientais de `environment`, como:

- `computing environments`;
- `edge computing environments`;
- `digital environment`;
- `metaverse environments`;
- `training environments`;
- `dynamic environments`;
- `high-risk environments`.

Também foram observados:

- usos genéricos de `sustainab*`;
- estudos em medicina, saúde mental, aplicações militares, robótica e segurança computacional;
- registros agregadores de proceedings;
- estudos secundários;
- registros em que os termos de RAG e os termos ambientais apareciam em contextos distintos.

## 1.4 Interpretação da v0.1

A string v0.1 demonstrou boa capacidade de recuperar os estudos-semente indexados, mas apresentou baixo poder de discriminação do domínio ambiental e de sustentabilidade.

O principal problema identificado foi `environment*`. Por isso, foi realizado o Teste T1.

---

# 2. Scopus — Teste T1

## 2.1 `v0.1-T1` — `environment*` → `environmental`

### Configuração

- Data: 2026-10-04
- Base: Scopus
- Identificador: `v0.1-T1`
- Período: 2020-presente
- Única alteração: `environment*` → `environmental`
- Resultados retornados: 767
- Resultados da v0.1: 2.154
- Redução aproximada: 64,4%

### String executada

```text
TITLE-ABS-KEY(
  (
    "retrieval augmented generation"
    OR "retrieval-augmented generation"
    OR "retrieval enhanced generation"
    OR "retrieval-enhanced generation"
    OR "GraphRAG"
    OR "graph RAG"
    OR "agentic RAG"
    OR "multimodal RAG"
    OR ("RAG" AND ("large language model*" OR LLM*))
  )
  AND
  (
    environmental
    OR sustainab*
    OR climat*
    OR ecolog*
  )
)
AND PUBYEAR > 2019
```

## 2.2 Validação dos estudos-semente — T1

- Estudos-semente avaliados: 12
- Estudos-semente indexados na Scopus: 11
- Estudos-semente recuperados: 11
- Estudos-semente não indexados: 1 (S04)
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

## 2.3 Diagnóstico de ruído — T1

Amostra diagnóstica: 17 registros.

- `R`: 4
- `I`: 6
- `D`: 7

Distribuição:

- `R`: 23,5%
- `I`: 35,3%
- `D`: 41,2%

A consulta passou a recuperar estudos claramente aderentes em políticas ambientais, biodiversidade, regulação ambiental e gestão de resíduos, mas `sustainab*` permaneceu como fonte de ruído.

## 2.4 Decisão sobre o T1

O T1 foi considerado aprovado para continuidade da calibração. A alteração reduziu substancialmente o volume sem perda de estudos-semente, mas a string ainda não foi considerada definitiva.

---

# 3. Scopus — Teste T2

## 3.1 `v0.1-T2` — remoção de `sustainab*`

### Configuração

- Data: 2026-10-04
- Base: Scopus
- Identificador: `v0.1-T2`
- Período: 2020-presente
- Alteração em relação ao T1: remoção de `sustainab*`
- Termos de domínio mantidos: `environmental`, `climat*`, `ecolog*`
- Bloco RAG: inalterado
- Resultados retornados: 472
- Resultados do T1: 767
- Resultados da v0.1: 2.154

### String executada

```text
TITLE-ABS-KEY(
  (
    "retrieval augmented generation"
    OR "retrieval-augmented generation"
    OR "retrieval enhanced generation"
    OR "retrieval-enhanced generation"
    OR "GraphRAG"
    OR "graph RAG"
    OR "agentic RAG"
    OR "multimodal RAG"
    OR ("RAG" AND ("large language model*" OR LLM*))
  )
  AND
  (
    environmental
    OR climat*
    OR ecolog*
  )
)
AND PUBYEAR > 2019
```

## 3.2 Validação dos estudos-semente — T2

- Estudos-semente avaliados: 12
- Estudos-semente indexados na Scopus: 11
- Estudos-semente recuperados: 11
- Estudos-semente não indexados: 1 (S04)
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

## 3.3 Impacto sobre o volume

- Redução em relação ao T1: aproximadamente 38,5%
- Redução em relação à v0.1: aproximadamente 78,1%

## 3.4 Diagnóstico de ruído — T2

Amostra diagnóstica: 17 registros.

- `R`: 8
- `I`: 6
- `D`: 3

Distribuição:

- `R`: 47,1%
- `I`: 35,3%
- `D`: 17,6%

A amostra trouxe aplicações claramente relevantes em relato de carbono, impacto ambiental de materiais, biodiversidade, árvores urbanas, materiais sustentáveis, monitoramento ambiental, adaptação climática e robustez de Graph-RAG ecológico.

Os falsos positivos restantes ocorreram principalmente quando `environmental` era usado em sentido operacional.

## 3.5 Decisão sobre o T2

O T2 foi considerado aprovado como estratégia candidata para a Scopus. A remoção de `sustainab*` reduziu o volume sem perda de nenhum estudo-semente indexado.

Novas restrições não foram introduzidas neste momento para evitar sobreajuste da estratégia aos exemplos do piloto.

A busca definitiva ainda não foi executada.

---

# 4. Comparação das versões — Scopus

| Indicador | v0.1 | v0.1-T1 | v0.1-T2 |
|---|---:|---:|---:|
| Resultados | 2.154 | 767 | 472 |
| Seeds indexados | 11 | 11 | 11 |
| Seeds recuperados | 11 | 11 | 11 |
| Query misses | 0 | 0 | 0 |
| Taxa-semente interna | 100% | 100% | 100% |
| Registros na amostra | 17 | 17 | 17 |
| R | 0 | 4 | 8 |
| I | 13 | 6 | 6 |
| D | 4 | 7 | 3 |

As diferenças entre `R`, `I` e `D` são apenas diagnósticas, pois as amostras não são probabilísticas.

---

# 5. IEEE Xplore

## 5.1 Execução piloto — `v0.1-IEEE`

- Data: 2026-10-04
- Base: IEEE Xplore
- Identificador: `v0.1-IEEE`
- Período: 2020-presente
- Resultados retornados: 230
- Estratégia: adaptação da string candidata `v0.1-T2` da Scopus à sintaxe do IEEE Xplore
- Status: busca piloto
- Busca definitiva: não executada

### String executada

```text
(
  "retrieval augmented generation"
  OR "retrieval-augmented generation"
  OR "retrieval enhanced generation"
  OR "retrieval-enhanced generation"
  OR "GraphRAG"
  OR "graph RAG"
  OR "agentic RAG"
  OR "multimodal RAG"
  OR ("RAG" AND ("large language model*" OR LLM*))
)
AND
(
  environmental
  OR climat*
  OR ecolog*
)
```

O período foi aplicado pela interface da base.

## 5.2 Validação dos estudos-semente — IEEE Xplore

Quando um seed não apareceu na consulta, foi realizada busca direta pelo título para distinguir ausência de indexação de falha da string.

- Estudos-semente avaliados: 12
- Estudos-semente indexados no IEEE Xplore: 4
- Estudos-semente recuperados pela `v0.1-IEEE`: 4
- Estudos-semente não indexados: 8
- Query misses: 0
- Taxa-semente interna: 4/4 = 100%

### Seeds recuperados

- S02 — `A LLM-Based Platform For Flood Risk Education and Weather Alerts in SIDS`
- S09 — `AI-Driven Wildfire Reasoning Utilizing Multimodal Retrieval-Augmented Generation`
- S10 — `SeaSense: An AI-Powered Conversational Interface for Oceanographic Data Analysis Using Retrieval Augmented Generation Architecture`
- S11 — `Multimodal Urban Heat Island Mitigation via Knowledge Reasoning and Geospatial Optimisation`

Os demais seeds não foram localizados por busca direta pelo título e foram classificados como `not_indexed`.

## 5.3 Diagnóstico de ruído — IEEE Xplore

Foi realizada uma amostra diagnóstica de 17 registros.

Como a interface do IEEE Xplore não apresentou uma posição global estável dos resultados durante a inspeção, os registros foram identificados sequencialmente como `IEEEP01` a `IEEEP17`.

- `R`: 5
- `I`: 9
- `D`: 3
- Total: 17

Distribuição:

- `R`: 29,4%
- `I`: 52,9%
- `D`: 17,6%

A amostra possui finalidade exclusivamente diagnóstica.

## 5.4 Exemplos de estudos aparentemente relevantes — IEEE

Foram recuperados estudos em:

- monitoramento ambiental em tempo real;
- dados do sistema terrestre e clima;
- previsão de incêndios florestais;
- agricultura sustentável;
- robustez e integridade de dados em Graph-RAG ecológico.

Exemplos:

- `Real-Time Environment Monitoring and Response Through IoT and Retrieval-Augmented Generation`
- `ESGF-Assistant: A Domain-Specific Large Language Model for Navigating Earth System Data`
- `FlameRAG-SHO: A Hybrid RAG and Bio-Inspired Optimisation Framework for Intelligent Wildfire Prediction Using Multi-Source Satellite Data`
- `Vayazh - Leveraging AI and NLP to Empower Farmers with Real-Time Agricultural Insights`
- `Decoupling Error Attribution in Cloud-Native Graph-RAG: A Data Integrity Diagnostic Framework`

## 5.5 Casos de fronteira — IEEE

Foram observados três casos duvidosos:

- grant matching para comunidades ambientalmente ameaçadas;
- damp, confiabilidade de sensores e manutenção predial;
- despacho de baterias em microgrids sob calor extremo.

Esses casos deverão ser resolvidos posteriormente com aplicação dos critérios formais de inclusão e exclusão.

## 5.6 Principais padrões de ruído — IEEE

Foram observados:

- uso de `environment`/`environmental` em sentido operacional;
- estudos secundários;
- domínios fora do escopo, como saúde pública, manutenção industrial, robótica e vigilância;
- colisão do acrônimo `RAG`.

### Colisão do acrônimo RAG

No artigo:

`MBANet: A Multi-Branch Deep Learning Model for Giant Panda Age Estimation`

`RAG` significa `Relation-Aware Graph`, e não `Retrieval-Augmented Generation`.

Apesar de o domínio ser relacionado à biodiversidade, o estudo foi classificado como irrelevante porque não utiliza RAG no sentido definido nesta revisão.

## 5.7 Interpretação do piloto — IEEE

A `v0.1-IEEE` recuperou todos os quatro estudos-semente confirmadamente indexados no IEEE Xplore, sem `query misses`.

A amostra diagnóstica mostrou presença de falsos positivos, mas também recuperou aplicações claramente ambientais e climáticas em diferentes subdomínios.

Os principais falsos positivos podem ser tratados durante a triagem pelos critérios de inclusão e exclusão, sem necessidade imediata de tornar a string mais restritiva.

## 5.8 Decisão sobre a `v0.1-IEEE`

A estratégia `v0.1-IEEE` foi considerada aprovada para continuidade da calibração entre bases.

A decisão foi baseada em:

1. recuperação de 4/4 estudos-semente indexados;
2. ausência de query misses;
3. recuperação de estudos claramente relevantes;
4. possibilidade de tratar o ruído na triagem;
5. risco de perda de sensibilidade com restrições adicionais.

A busca definitiva ainda não foi executada.

---

# 6. Comparação parcial entre bases

| Base / versão | Resultados | Seeds indexados | Seeds recuperados | Query misses | R | I | D |
|---|---:|---:|---:|---:|---:|---:|---:|
| Scopus v0.1 | 2.154 | 11 | 11 | 0 | 0 | 13 | 4 |
| Scopus v0.1-T1 | 767 | 11 | 11 | 0 | 4 | 6 | 7 |
| Scopus v0.1-T2 | 472 | 11 | 11 | 0 | 8 | 6 | 3 |
| IEEE Xplore v0.1-IEEE | 230 | 4 | 4 | 0 | 5 | 9 | 3 |

As contagens `R`, `I` e `D` derivam de amostras diagnósticas não probabilísticas e não devem ser interpretadas como estimativas formais de precisão entre bases.

---

# 7. Questões metodológicas abertas

Permanecem alguns casos de fronteira a serem resolvidos durante a calibração dos critérios de inclusão e exclusão:

1. ESG e sustentabilidade corporativa;
2. aplicações agrícolas em que a dimensão ambiental não é explicitamente central;
3. eficiência energética e sistemas de energia;
4. sensoriamento remoto de propósito geral;
5. RAG utilizado apenas como baseline;
6. sustentabilidade espacial/orbital;
7. ambiente construído, qualidade ambiental interna e manutenção predial;
8. turismo sustentável;
9. políticas públicas e grant matching em contextos ambientalmente ameaçados;
10. registros com ano bibliográfico futuro/online-first.

Esses pontos não devem ser resolvidos apenas por conveniência para reduzir o corpus.

---

# 8. Próximo passo

A próxima etapa do Dia 2 é adaptar a estratégia conceitual candidata para a **ACM Digital Library**.

A adaptação deverá preservar, tanto quanto possível:

```text
RAG
AND
(environmental OR climat* OR ecolog*)
```

Na ACM Digital Library deverão ser registrados:

- string exata executada;
- data;
- período/filtros aplicados;
- número de resultados;
- indexação dos 12 estudos-semente;
- estudos-semente recuperados;
- `query_misses`;
- pequena amostra diagnóstica de ruído.

A busca definitiva ainda não foi executada.
