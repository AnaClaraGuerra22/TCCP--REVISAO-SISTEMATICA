# Estratégias de busca

## Revisão sistemática

**Tema:** Retrieval-Augmented Generation em domínios ambientais e de sustentabilidade

- Versão documental: `v1.0`
- Data de congelamento das strings: `2026-10-06`
- Status: **STRINGS FINAIS / CONGELADAS**
- Busca definitiva: **ainda não executada**

Este arquivo registra as estratégias de busca utilizadas durante a fase piloto e as strings finais congeladas para a execução definitiva da revisão sistemática.

As consultas são versionadas para preservar a rastreabilidade das alterações realizadas durante o piloto.

---

# 1. Estrutura conceitual da busca

A estratégia de busca é composta por dois blocos principais:

1. termos relacionados a Retrieval-Augmented Generation (RAG);
2. termos relacionados ao domínio ambiental e de sustentabilidade.

Estrutura geral:

```text
(RAG)
AND
(domínio ambiental/sustentabilidade)
```

A construção e o refinamento das strings foram realizados inicialmente na Scopus.

As alterações entre versões foram feitas de forma controlada, modificando preferencialmente um componente por vez.

---

# 2. Bloco conceitual de RAG

O bloco de RAG utilizado durante a calibração foi:

```text
"retrieval augmented generation"
OR "retrieval-augmented generation"
OR "retrieval enhanced generation"
OR "retrieval-enhanced generation"
OR "GraphRAG"
OR "graph RAG"
OR "agentic RAG"
OR "multimodal RAG"
OR ("RAG" AND ("large language model*" OR LLM*))
```

Esse bloco foi mantido inalterado durante os testes `v0.1`, `v0.1-T1` e `v0.1-T2`.

---

# 3. Scopus

## 3.1 String v0.1 — consulta piloto inicial

**Identificador:** `v0.1`  
**Data da execução:** `2026-10-04`  
**Período:** `2020-presente`  
**Resultados:** `2.154 registros`

### String

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

### Observação

A consulta apresentou elevada recuperação dos estudos-semente, porém retornou grande volume de registros não relacionados ao domínio ambiental.

A inspeção diagnóstica mostrou que `environment*` recuperava usos da palavra `environment` relacionados, por exemplo, a:

```text
computing environments
digital environments
virtual environments
dynamic environments
training environments
high-risk environments
```

Por esse motivo, foi realizado o Teste T1.

---

# 4. Scopus — Teste T1

## 4.1 v0.1-T1 — `environment*` → `environmental`

**Identificador:** `v0.1-T1`  
**Data da execução:** `2026-10-04`  
**Período:** `2020-presente`  
**Resultados:** `767 registros`

### Alteração

A única alteração em relação à `v0.1` foi:

```text
environment*
```

substituído por:

```text
environmental
```

### String

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

### Resultado da calibração

- Resultados: 767
- Estudos-semente indexados na Scopus: 11
- Estudos-semente recuperados: 11
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

A alteração reduziu substancialmente falsos positivos relacionados a usos não ambientais de `environment*`.

Entretanto, a análise diagnóstica mostrou que `sustainab*` continuava recuperando usos genéricos de sustentabilidade sem componente ambiental central.

Por esse motivo, foi realizado o Teste T2.

---

# 5. Scopus — Teste T2

## 5.1 v0.1-T2 — remoção de `sustainab*`

**Identificador:** `v0.1-T2`  
**Data da execução:** `2026-10-04`  
**Período:** `2020-presente`  
**Resultados:** `472 registros`

### Alteração

A única alteração em relação ao T1 foi a remoção de:

```text
sustainab*
```

O bloco de domínio passou de:

```text
environmental
OR sustainab*
OR climat*
OR ecolog*
```

para:

```text
environmental
OR climat*
OR ecolog*
```

### String

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

### Resultado da calibração

- Resultados: 472
- Estudos-semente avaliados: 12
- Estudos-semente indexados na Scopus: 11
- Estudos-semente recuperados: 11
- Estudos-semente não indexados: 1 (`S04`)
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

A consulta apresentou redução aproximada de:

```text
38,5% em relação ao T1
```

e:

```text
78,1% em relação à v0.1
```

sem perda de nenhum estudo-semente confirmadamente indexado na Scopus.

---

# 6. String final — Scopus v1.0

Após os testes `v0.1`, `v0.1-T1` e `v0.1-T2` e após a calibração intra-revisora dos critérios de elegibilidade, a estratégia `v0.1-T2` foi aprovada como base da **string final v1.0 da Scopus**.

**Status:** FINAL / CONGELADA  
**Origem:** `v0.1-T2`  
**Busca definitiva:** ainda não executada.

## 6.1 String final v1.0

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

## 6.2 Justificativa

A estratégia foi congelada porque:

- preservou todos os estudos-semente confirmadamente indexados recuperados pelas versões anteriores;
- recuperou 11/11 estudos-semente indexados na Scopus;
- apresentou 0 `query_miss`;
- reduziu significativamente o volume de resultados em relação à versão inicial;
- reduziu falsos positivos associados a usos não ambientais de `environment*`;
- reduziu ruído associado ao uso genérico de `sustainab*`;
- continuou recuperando estudos em diferentes aplicações ambientais, ecológicas e climáticas;
- evitou introduzir termos excessivamente específicos de aplicações particulares.

A estratégia ainda recupera alguns registros em que `environmental` é utilizado em sentido operacional. Esses casos serão tratados durante o screening mediante os critérios de elegibilidade e as regras de fronteira do `protocol/protocol_v1.0.md`.

## 6.3 Resultado do piloto

Na execução piloto de `2026-10-04`:

- resultados: 472;
- estudos-semente avaliados: 12;
- estudos-semente indexados: 11;
- estudos-semente recuperados: 11;
- estudos-semente não indexados: 1 (`S04`);
- `query_misses`: 0;
- taxa-semente interna: 11/11.

Esses números são exclusivamente diagnósticos.

**Os 472 registros do piloto não serão utilizados automaticamente como resultado da busca definitiva.**

---

# 7. Comparação das versões — Scopus

| Versão | Alteração principal | Resultados | Seeds recuperados |
|---|---|---:|---:|
| `v0.1` | String inicial | 2.154 | 11/11 |
| `v0.1-T1` | `environment*` → `environmental` | 767 | 11/11 |
| `v0.1-T2` | remoção de `sustainab*` | 472 | 11/11 |

O estudo `S04` não foi localizado na Scopus por busca direta pelo título e, portanto, não integra o denominador da taxa-semente.

---

# 8. IEEE Xplore

## 8.1 String piloto — v0.1-IEEE

**Identificador:** `v0.1-IEEE`  
**Data da execução:** `2026-10-04`  
**Período:** `2020-presente`  
**Resultados:** `230 registros`

A estratégia conceitual candidata definida na Scopus foi adaptada ao IEEE Xplore, preservando os dois blocos principais da consulta.

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

### Validação dos estudos-semente

- Estudos-semente avaliados: 12
- Estudos-semente indexados no IEEE Xplore: 4
- Estudos-semente recuperados: 4
- Estudos-semente não indexados: 8
- Query misses: 0
- Taxa-semente interna: 4/4 = 100%

Estudos-semente recuperados:

- S02 — `A LLM-Based Platform For Flood Risk Education and Weather Alerts in SIDS`
- S09 — `AI-Driven Wildfire Reasoning Utilizing Multimodal Retrieval-Augmented Generation`
- S10 — `SeaSense: An AI-Powered Conversational Interface for Oceanographic Data Analysis Using Retrieval Augmented Generation Architecture`
- S11 — `Multimodal Urban Heat Island Mitigation via Knowledge Reasoning and Geospatial Optimisation`

Os demais estudos-semente não foram localizados por busca direta pelo título no IEEE Xplore e, portanto, foram classificados como `not_indexed`.

A taxa-semente é utilizada apenas como indicador interno de calibração e não representa recall formal da literatura.

### Diagnóstico de ruído

Foi utilizada uma amostra diagnóstica de 17 registros.

- `R`: 5
- `I`: 9
- `D`: 3

Distribuição:

- `R`: 29,4%
- `I`: 52,9%
- `D`: 17,6%

Os principais padrões de ruído observados foram:

- `environment` ou `environmental` empregados em sentido operacional;
- estudos de domínios não ambientais;
- estudos secundários;
- colisão da sigla `RAG` com outros significados, como `Relation-Aware Graph`.

A amostra tem finalidade exclusivamente diagnóstica e não constitui uma estimativa formal da precisão da estratégia.

### Decisão final

Após a busca piloto e a calibração intra-revisora dos critérios de elegibilidade, a estratégia `v0.1-IEEE` foi aprovada como base da **string final v1.0 do IEEE Xplore**.

**Status:** FINAL / CONGELADA  
**Origem:** `v0.1-IEEE`  
**Busca definitiva:** ainda não executada.

A decisão foi baseada em:

- recuperação de 4/4 estudos-semente confirmadamente indexados;
- ausência de `query_misses`;
- recuperação de estudos claramente relevantes em diferentes subdomínios ambientais;
- possibilidade de tratar falsos positivos mediante os critérios de elegibilidade e regras de fronteira;
- risco de perda de sensibilidade caso a consulta fosse restringida excessivamente.

Na execução piloto de `2026-10-04`, a estratégia retornou 230 registros.

Esse número possui finalidade diagnóstica.

**Os 230 registros do piloto não serão utilizados automaticamente como resultado da busca definitiva.**

---

# 9. Bases selecionadas para a revisão

Após a fase piloto, foram selecionadas duas bases bibliográficas para a revisão sistemática:

- **Scopus**
- **IEEE Xplore**

A ACM Digital Library **não integra a estratégia de busca da revisão**.

A seleção combina:

- uma base multidisciplinar de ampla cobertura, a Scopus;
- uma base especializada em computação, engenharia e tecnologias relacionadas, o IEEE Xplore.

A cobertura bibliográfica será posteriormente complementada por **uma rodada de backward e forward snowballing** aplicada ao corpus elegível.

A decisão sobre as bases é mantida de forma consistente no `protocol/protocol_v1.0.md` e no registro `protocol/amendments.md`.

---

# 10. Regras de versionamento

As estratégias de busca são identificadas por versão.

Versões utilizadas durante o piloto:

```text
v0.1
v0.1-T1
v0.1-T2
v0.1-IEEE
```

Os testes `T1`, `T2`, etc. correspondem a alterações controladas realizadas durante a fase piloto.

Cada execução deve registrar:

```text
base
data
versão
string executada
filtros
número de resultados
resultado da validação pelos estudos-semente
justificativa da alteração
```

## 10.1 Relação entre versões piloto e finais

As versões piloto foram preservadas para rastreabilidade:

```text
Scopus

v0.1
  ↓
v0.1-T1
  ↓
v0.1-T2
  ↓
v1.0 FINAL

IEEE Xplore

v0.1-IEEE
  ↓
v1.0 FINAL
```

A versão `v1.0` não representa uma nova modificação textual das strings.

Ela representa o **congelamento metodológico**, após:

- validação pelos estudos-semente;
- diagnóstico de ruído;
- calibração intra-revisora dos critérios de elegibilidade;
- formalização das regras de fronteira.

Qualquer alteração futura nas strings após este congelamento deverá receber nova versão e ser registrada em `protocol/amendments.md`.

---

# 11. Situação atual

Em `2026-10-06`, a fase de busca piloto e a calibração intra-revisora foram concluídas.

## 11.1 Histórico da Scopus

```text
v0.1    → 2.154 registros → 11/11 seeds
v0.1-T1 →   767 registros → 11/11 seeds
v0.1-T2 →   472 registros → 11/11 seeds
```

`v0.1-T2` foi congelada como base da **Scopus v1.0 FINAL**.

## 11.2 Histórico do IEEE Xplore

```text
v0.1-IEEE → 230 registros → 4/4 seeds confirmadamente indexados
```

`v0.1-IEEE` foi congelada como base do **IEEE Xplore v1.0 FINAL**.

## 11.3 Bases definitivas

- Scopus
- IEEE Xplore

A ACM Digital Library não integra a estratégia metodológica da revisão.

A cobertura será posteriormente complementada por uma rodada de backward e forward snowballing.

## 11.4 Resultado da calibração dos critérios

A calibração intra-revisora utilizou 18 registros avaliados em duas passagens independentes.

Resultado:

- 17/18 decisões concordantes;
- concordância bruta: 94,4%;
- mudança de decisão: 5,6%;
- uma divergência resolvida;
- não foi necessária uma terceira passagem.

As regras de fronteira resultantes foram incorporadas ao `protocol/protocol_v1.0.md`.

## 11.5 Status das estratégias

**Scopus:** `v1.0 — FINAL / CONGELADA`  
**IEEE Xplore:** `v1.0 — FINAL / CONGELADA`  
**Busca definitiva:** ainda não executada.

## 11.6 Próxima etapa

Antes da execução da busca definitiva:

1. revisar `extraction/data_dictionary.md`;
2. criar a ficha `quality/quality_assessment.csv`;
3. verificar o Gate documental do Dia 3.

Após o fechamento do Gate:

1. executar novamente a string final na Scopus;
2. executar novamente a string final no IEEE Xplore;
3. registrar data, filtros e número de resultados em `search/search_log.csv`;
4. exportar e preservar os registros brutos;
5. iniciar consolidação, deduplicação e screening formal.

---

# 12. Observação sobre os resultados piloto

Os números obtidos nas buscas piloto foram utilizados para:

- calibrar as strings;
- avaliar cobertura interna por estudos-semente;
- identificar padrões de ruído;
- apoiar o congelamento da estratégia de busca.

Eles **não constituem os números definitivos da revisão**.

As buscas definitivas serão executadas novamente após o fechamento documental do protocolo `v1.0`, e seus resultados serão registrados separadamente em `search/search_log.csv`.
