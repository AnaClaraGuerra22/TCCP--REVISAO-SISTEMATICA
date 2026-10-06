**# Estratégias de busca**



**## Revisão sistemática**



**\*\*Tema:\*\*** Retrieval-Augmented Generation em domínios ambientais e de sustentabilidade



Este arquivo registra as estratégias de busca utilizadas durante a calibração e, posteriormente, durante a execução definitiva da revisão sistemática.



As consultas são versionadas para permitir rastreabilidade das alterações realizadas durante o piloto.



\---



**# 1. Estrutura conceitual da busca**



A estratégia de busca é composta por dois blocos principais:



1\. termos relacionados a Retrieval-Augmented Generation (RAG);

2\. termos relacionados ao domínio ambiental e de sustentabilidade.



Estrutura geral:



\`\`\`text

(RAG)

AND

(domínio ambiental/sustentabilidade)

\`\`\`



A construção e o refinamento das strings foram realizados inicialmente na Scopus.



As alterações entre versões foram feitas de forma controlada, modificando preferencialmente um componente por vez.



\---



**# 2. Bloco conceitual de RAG**



O bloco de RAG utilizado durante a calibração foi:



\`\`\`text

"retrieval augmented generation"

OR "retrieval-augmented generation"

OR "retrieval enhanced generation"

OR "retrieval-enhanced generation"

OR "GraphRAG"

OR "graph RAG"

OR "agentic RAG"

OR "multimodal RAG"

OR ("RAG" AND ("large language model\*" OR LLM\*))

\`\`\`



Esse bloco foi mantido inalterado durante os testes v0.1, T1 e T2.



\---



**# 3. Scopus**



**## 3.1 String v0.1 — consulta piloto inicial**



**\*\*Identificador:\*\*** \`v0.1\`



**\*\*Data da execução:\*\*** 2026-10-04



**\*\*Período:\*\*** 2020-presente



**\*\*Resultados:\*\*** 2.154 registros



**### String**



\`\`\`text

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

    OR ("RAG" AND ("large language model\*" OR LLM\*))

  )

  AND

  (

    environment\*

    OR sustainab\*

    OR climat\*

    OR ecolog\*

  )

)

AND PUBYEAR > 2019

\`\`\`



**### Observação**



A consulta apresentou elevada recuperação dos estudos-semente, porém retornou grande volume de registros não relacionados ao domínio ambiental.



A inspeção diagnóstica mostrou que \`environment\*\` recuperava usos da palavra \`environment\` relacionados, por exemplo, a:



\`\`\`text

computing environments

digital environments

virtual environments

dynamic environments

training environments

high-risk environments

\`\`\`



Por esse motivo, foi realizado o Teste T1.



\---



**# 4. Scopus — Teste T1**



**## 4.1 v0.1-T1 — \`environment\*\` → \`environmental\`**



**\*\*Identificador:\*\*** \`v0.1-T1\`



**\*\*Data da execução:\*\*** 2026-10-04



**\*\*Período:\*\*** 2020-presente



**\*\*Resultados:\*\*** 767 registros



**### Alteração**



A única alteração em relação à v0.1 foi:



\`\`\`text

environment\*

\`\`\`



substituído por:



\`\`\`text

environmental

\`\`\`



**### String**



\`\`\`text

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

    OR ("RAG" AND ("large language model\*" OR LLM\*))

  )

  AND

  (

    environmental

    OR sustainab\*

    OR climat\*

    OR ecolog\*

  )

)

AND PUBYEAR > 2019

\`\`\`



**### Resultado da calibração**



\- Resultados: 767

\- Estudos-semente indexados na Scopus: 11

\- Estudos-semente recuperados: 11

\- Query misses: 0

\- Taxa-semente interna: 11/11 = 100%



A alteração reduziu substancialmente falsos positivos relacionados a usos não ambientais de \`environment\`.



Entretanto, a análise diagnóstica mostrou que \`sustainab\*\` continuava recuperando usos genéricos de sustentabilidade sem componente ambiental central.



Por esse motivo, foi realizado o Teste T2.



\---



**# 5. Scopus — Teste T2**



**## 5.1 v0.1-T2 — remoção de \`sustainab\*\`**



**\*\*Identificador:\*\*** \`v0.1-T2\`



**\*\*Data da execução:\*\*** 2026-10-04



**\*\*Período:\*\*** 2020-presente



**\*\*Resultados:\*\*** 472 registros



**### Alteração**



A única alteração em relação ao T1 foi a remoção de:



\`\`\`text

sustainab\*

\`\`\`



O bloco de domínio passou de:



\`\`\`text

environmental

OR sustainab\*

OR climat\*

OR ecolog\*

\`\`\`



para:



\`\`\`text

environmental

OR climat\*

OR ecolog\*

\`\`\`



**### String**



\`\`\`text

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

    OR ("RAG" AND ("large language model\*" OR LLM\*))

  )

  AND

  (

    environmental

    OR climat\*

    OR ecolog\*

  )

)

AND PUBYEAR > 2019

\`\`\`



**### Resultado da calibração**



\- Resultados: 472

\- Estudos-semente avaliados: 12

\- Estudos-semente indexados na Scopus: 11

\- Estudos-semente recuperados: 11

\- Estudos-semente não indexados: 1 (S04)

\- Query misses: 0

\- Taxa-semente interna: 11/11 = 100%



A consulta apresentou redução de aproximadamente:



\`\`\`text

38,5% em relação ao T1

\`\`\`



e:



\`\`\`text

78,1% em relação à v0.1

\`\`\`



sem perda de nenhum estudo-semente confirmadamente indexado na Scopus.



\---



**# 6. String candidata — Scopus**



Após os testes v0.1, T1 e T2, a estratégia \`v0.1-T2\` foi selecionada como **\*\*string candidata da Scopus para continuidade da calibração entre bases\*\***.



A string candidata é:



\`\`\`text

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

    OR ("RAG" AND ("large language model\*" OR LLM\*))

  )

  AND

  (

    environmental

    OR climat\*

    OR ecolog\*

  )

)

AND PUBYEAR > 2019

\`\`\`



**### Justificativa**



A v0.1-T2 foi mantida porque:



\- preservou todos os estudos-semente indexados recuperados pelas versões anteriores;

\- apresentou 11/11 estudos-semente recuperados;

\- reduziu significativamente o volume de resultados;

\- eliminou grande parte do ruído relacionado a \`environment\*\`;

\- reduziu usos genéricos associados a \`sustainab\*\`;

\- continuou recuperando estudos em diferentes aplicações ambientais, ecológicas e climáticas;

\- evitou a introdução de termos excessivamente específicos de aplicações particulares.



A consulta ainda apresenta alguns falsos positivos, especialmente quando \`environmental\` é utilizado em sentido operacional.



Esses registros serão tratados durante a triagem pelos critérios de inclusão e exclusão, em vez de aumentar excessivamente a especificidade da string.



A v0.1-T2 ainda não representa a busca definitiva da revisão.



\---



**# 7. Comparação das versões — Scopus**



\| Versão | Alteração principal | Resultados | Seeds recuperados |

\|---|---|---:|---:|

\| v0.1 | String inicial | 2.154 | 11/11 |

\| v0.1-T1 | \`environment\*\` → \`environmental\` | 767 | 11/11 |

\| v0.1-T2 | remoção de \`sustainab\*\` | 472 | 11/11 |



O estudo S04 não foi localizado na Scopus por busca direta pelo título e, portanto, não integra o denominador da taxa-semente.



\---

---

# 8. IEEE Xplore

## 8.1 String piloto — v0.1-IEEE

**Identificador:** `v0.1-IEEE`

**Data da execução:** 2026-10-04

**Período:** 2020-presente

**Resultados:** 230 registros

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

### Decisão

A estratégia `v0.1-IEEE` foi mantida como **string candidata do IEEE Xplore** para a próxima etapa de calibração.

A decisão foi baseada em:

- recuperação de 4/4 estudos-semente confirmadamente indexados;
- ausência de `query_misses`;
- recuperação de estudos claramente relevantes em diferentes subdomínios ambientais;
- possibilidade de tratar falsos positivos pelos critérios de inclusão e exclusão;
- risco de perda de sensibilidade caso a consulta seja restringida excessivamente.

A `v0.1-IEEE` ainda não representa a busca definitiva da revisão.

---

# 9. Bases selecionadas para a revisão

Após a fase piloto, foram selecionadas duas bases bibliográficas para a revisão sistemática:

- **Scopus**
- **IEEE Xplore**

A ACM Digital Library **não integra a estratégia de busca da revisão**.

A decisão de trabalhar com duas bases busca manter a revisão executável por uma única pesquisadora dentro do prazo definido, combinando:

- uma base multidisciplinar de ampla cobertura, a Scopus;
- uma base especializada em computação, engenharia e tecnologias relacionadas, o IEEE Xplore.

A cobertura bibliográfica será posteriormente complementada por **uma rodada de backward e forward snowballing** aplicada ao corpus elegível.

A seleção das bases deverá constar de forma consistente no protocolo `v1.0` e no texto metodológico do artigo.

---

# 10. Regras de versionamento

As estratégias de busca são identificadas por versão.

Exemplos:

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

As strings definitivas somente serão congeladas após a calibração dos critérios de inclusão e exclusão no Dia 3.

---

# 11. Situação atual

Em 2026-10-04:

```text
Scopus

v0.1    → 2.154 registros → 11/11 seeds
v0.1-T1 →   767 registros → 11/11 seeds
v0.1-T2 →   472 registros → 11/11 seeds

IEEE Xplore

v0.1-IEEE → 230 registros → 4/4 seeds indexados
```

**String candidata atual para Scopus:** `v0.1-T2`

**String candidata atual para IEEE Xplore:** `v0.1-IEEE`

**Bases selecionadas:** Scopus e IEEE Xplore.

**ACM Digital Library:** não incluída na metodologia.

- Busca definitiva: **executada em 2026-10-06**

**Próxima etapa:** calibração intra-revisora dos critérios CI/CE e congelamento do protocolo `v1.0`.
