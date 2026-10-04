# Notas da busca piloto

## Objetivo

Este arquivo registra as execuções piloto da estratégia de busca, os testes controlados realizados para refinamento da string e os principais padrões de ruído observados.

As classificações `R`, `I` e `D` utilizadas nas amostras possuem finalidade exclusivamente diagnóstica:

- `R` = aparentemente relevante;
- `I` = claramente irrelevante;
- `D` = duvidoso.

Essas classificações não correspondem à triagem formal dos estudos e não devem ser utilizadas para estimar precisão ou recall da revisão.

---

# Scopus

## Execução inicial — v0.1

- Data: 2026-10-04
- Base: Scopus
- Versão da string: v0.1
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

## Validação pelos estudos-semente — v0.1

Foram utilizados 12 estudos-semente previamente conhecidos como potencialmente relevantes para o escopo da revisão.

- Estudos-semente avaliados: 12
- Estudos-semente confirmadamente indexados na Scopus: 11
- Estudos-semente recuperados pela string: 11
- Estudos-semente não indexados: 1
- Estudo não indexado: S04 — `ClimateGPT: Towards AI Synthesizing Interdisciplinary Research on Climate Change`
- Query misses: 0

### Taxa-semente interna

```text
11 / 11 = 100%
```

A taxa-semente é utilizada apenas como indicador interno de calibração da estratégia de busca.

Ela não representa recall formal da literatura, pois o conjunto-semente não constitui uma amostra completa de todos os estudos relevantes existentes.

---

## Diagnóstico de ruído — v0.1

Devido ao volume elevado de 2.154 registros, não foi realizada triagem dos resultados.

Foi utilizada uma amostra diagnóstica de 17 registros distribuídos ao longo da listagem ordenada por `Date (newest)`.

### Características da amostra

- Tamanho: 17 registros
- Finalidade: diagnóstico qualitativo de ruído
- Ordenação da Scopus: `Date (newest)`
- Método: amostra diagnóstica de conveniência distribuída entre diferentes posições da listagem
- Não utilizada para estimativa formal de precisão da estratégia

### Resultado

Dos 17 registros inspecionados:

- Claramente relevantes (`R`): 0
- Claramente irrelevantes (`I`): 13
- Duvidosos (`D`): 4

Distribuição na amostra:

- `R`: 0,0%
- `I`: 76,5%
- `D`: 23,5%

Essas proporções são exclusivamente descritivas da amostra diagnóstica e não devem ser extrapoladas para os 2.154 registros retornados.

---

## Principais padrões de ruído identificados na v0.1

### 1. Ambiguidade de `environment*`

O termo `environment*` apresentou forte ambiguidade semântica.

Foram recuperados trabalhos nos quais `environment` significava ambiente computacional, virtual, educacional ou operacional, e não meio ambiente.

Exemplos observados:

- `computing environments`;
- `edge computing environments`;
- `digital environment`;
- `metaverse environments`;
- `training environments`;
- `dynamic environments`;
- `high-risk environments`.

Esse padrão foi identificado como uma das principais fontes de ruído da v0.1.

### 2. Ambiguidade de `sustainab*`

O termo `sustainab*` também recuperou ocorrências nas quais sustentabilidade não constituía parte central do problema ambiental investigado.

Exemplo:

- `sustainable smart cities`, utilizado como contexto geral de infraestrutura ferroviária.

Esse resultado indica que a presença lexical de `sustainability` ou `sustainable` não é suficiente, por si só, para garantir aderência ao escopo.

### 3. Domínios tecnicamente relacionados a RAG, mas fora do escopo

Foram observados estudos tecnicamente relevantes para RAG, porém aplicados a áreas não ambientais, incluindo:

- medicina;
- intervenção psicológica;
- aplicações militares;
- metaverso;
- robótica;
- segurança computacional;
- aprendizagem federada;
- sistemas regulatórios não ambientais.

### 4. Registros agregadores

Registros de proceedings podem conter diversos trabalhos no mesmo resumo.

Nesses casos, termos associados a RAG e termos associados a `environment*` podem aparecer em trabalhos diferentes e, ainda assim, satisfazer a string de busca.

### 5. Estudos secundários ou outros tipos documentais

Foram encontrados registros correspondentes a:

- reviews;
- tutorials;
- proceedings completos;
- contribuições conceituais.

Esses registros podem ser tematicamente relacionados, mas não atendem necessariamente ao desenho de estudo primário definido para o corpus principal.

---

## Interpretação da v0.1

A string v0.1 demonstrou boa capacidade de recuperar o conjunto conhecido de estudos relevantes:

```text
11/11 estudos-semente indexados recuperados.
```

Entretanto, o volume total de 2.154 resultados e a inspeção diagnóstica indicaram baixo poder de discriminação do domínio ambiental e de sustentabilidade.

O principal problema identificado foi o uso de:

```text
environment*
```

que recuperava diversos sentidos não ambientais da palavra `environment`.

Por esse motivo, foi planejado um teste controlado alterando exclusivamente esse termo e mantendo todos os demais componentes da estratégia constantes.

---

# Teste T1 — `environment*` → `environmental`

## Objetivo

Avaliar se a substituição de:

```text
environment*
```

por:

```text
environmental
```

reduziria falsos positivos relacionados a usos não ambientais de `environment`, sem comprometer a recuperação dos estudos-semente.

## Configuração

- Data: 2026-10-04
- Base: Scopus
- Identificador: v0.1-T1
- Período: 2020-presente
- Única alteração realizada: `environment*` → `environmental`
- Demais termos: inalterados
- Resultados retornados: 767
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
    OR sustainab*
    OR climat*
    OR ecolog*
  )
)
AND PUBYEAR > 2019
```

---

## Impacto sobre o volume de resultados

A consulta passou de:

```text
2.154 registros
```

para:

```text
767 registros
```

Redução:

```text
aproximadamente 64,4%
```

A redução foi obtida alterando apenas um componente da string.

---

## Validação dos estudos-semente — T1

- Estudos-semente avaliados: 12
- Estudos-semente confirmadamente indexados na Scopus: 11
- Estudos-semente recuperados pela v0.1-T1: 11
- Estudos-semente não indexados: 1 (S04)
- Query misses: 0

### Taxa-semente interna

```text
11 / 11 = 100%
```

Portanto, a substituição de `environment*` por `environmental` não provocou perda de nenhum estudo-semente confirmadamente indexado na Scopus.

---

# Diagnóstico de ruído — T1

Foi realizada uma segunda amostra diagnóstica com 17 registros da listagem da consulta v0.1-T1.

### Resultado

Dos 17 registros inspecionados:

- Claramente relevantes (`R`): 4
- Claramente irrelevantes (`I`): 6
- Duvidosos (`D`): 7

Distribuição na amostra:

- `R`: 23,5%
- `I`: 35,3%
- `D`: 41,2%

Esses valores não representam estimativas formais de precisão da busca.

A amostra tem apenas finalidade diagnóstica.

---

## Exemplos aparentemente relevantes encontrados na T1

A nova consulta recuperou estudos claramente próximos ao objeto da revisão, incluindo aplicações de RAG em:

### Políticas ambientais

`Graphing the European Green Deal: A Graph Retrieval-Augmented Generation Pipeline for Policy Documents Analysis`

O estudo utiliza GraphRAG para análise de documentos relacionados ao European Green Deal e apresenta avaliação contra outros baselines GraphRAG.

### Biodiversidade

`InvaderDefender: Multimodal recognition of invasive alien species via a large language model with vision-guided targeted RAG`

O estudo utiliza RAG multimodal para identificação de espécies exóticas invasoras e monitoramento da biodiversidade.

### Regulação ambiental

`Use of AI-Powered Technologies for Review of Environmental Regulations`

O estudo utiliza LLMs, RAG e workflow agentic para análise de regulações ambientais.

### Gestão de resíduos

`A Retrieval-Augmented Agent for Context-Aware Waste Classification Across National Systems`

O estudo utiliza arquitetura RAG para classificação de resíduos, reciclagem, economia circular e gestão sustentável de resíduos.

---

# Casos de fronteira encontrados na T1

A nova consulta também revelou estudos cuja elegibilidade não pode ser determinada apenas pelo título e resumo.

Esses registros foram classificados como `D` e deverão ser tratados posteriormente durante a calibração dos critérios de inclusão e exclusão.

## ESG

`ESGRep: Learning Domain-Specific Embeddings for ESG Retrieval-Augmented Question Answering`

RAG é central, mas o estudo aborda ESG de maneira ampla. É necessário verificar se a dimensão ambiental é suficientemente substancial em relação aos componentes social e de governança.

## Eficiência energética

`LEO satellites meet movable antennas: an SEEI entropy driven agentic AI cross-domain optimization framework`

O estudo aborda eficiência energética e sustentabilidade, mas não está claro se sustentabilidade ambiental constitui objetivo central ou apenas atributo de eficiência do sistema.

## Sensoriamento remoto

`GeoGATE: Geo-Sensor-Guided Adaptive Token and Evidence Reasoning for High-Resolution Remote Sensing Image Understanding`

O domínio é próximo ao eixo ambiental, porém environmental monitoring aparece como extensão futura e não necessariamente como aplicação empiricamente validada.

## RAG como baseline

`DraftNEPABench: A Benchmark for Drafting NEPA Document Sections with Coding Agents`

O domínio ambiental é claro, mas RAG aparece como baseline de comparação e não como abordagem principal.

Será necessário decidir se estudos nos quais RAG é apenas baseline serão incluídos quando houver informação suficiente para responder às RQs.

## Gestão sustentável da água

`Sustainable water information systems with LLMs and RAG: Opportunities and challenges`

O domínio e o RAG são aderentes, mas o resumo sugere um estudo conceitual/revisão, e não necessariamente uma avaliação empírica de um sistema RAG.

## Recomendação sustentável

`An Adaptive Cold-Aware Recommendation System for Sparse E-Commerce Data`

O sistema incorpora pontuação de sustentabilidade e impacto ambiental, porém a aplicação principal permanece recomendação em e-commerce.

É necessário verificar a centralidade e a avaliação da dimensão ambiental.

## Sustentabilidade espacial

`Space Debris Intelligence Platform: A Multi-Model Deep Learning Framework with RAG`

O trabalho trata de detritos orbitais e sustentabilidade de operações espaciais.

Esse caso exige uma decisão de fronteira sobre a inclusão ou não de sustentabilidade espacial dentro da definição operacional da revisão.

---

# Padrões de ruído ainda presentes na T1

Embora a substituição de `environment*` por `environmental` tenha reduzido substancialmente o volume de resultados, alguns tipos de ruído permaneceram.

## 1. `sustainab*` continua semanticamente amplo

Foram observados usos de sustentabilidade que não representam necessariamente sustentabilidade ambiental.

Exemplo:

`scalability and sustainability of SSC programs`

Nesse caso, `sustainability` significa continuidade ou viabilidade de um programa de segurança viária.

Também foram observados trabalhos sobre SDGs de forma ampla sem foco ambiental central.

## 2. `environmental` ainda apresenta alguma ambiguidade

Apesar de ser muito menos amplo do que `environment*`, o termo `environmental` ainda pode aparecer no sentido de contexto operacional.

Exemplos observados:

- `environmental context` em planejamento de robôs;
- `environmental context` em geração de ambientes de simulação 3D.

Portanto, a alteração reduziu o problema, mas não o eliminou completamente.

## 3. Tipos documentais não elegíveis continuam presentes

Ainda foram encontrados:

- reviews;
- tutorials;
- artigos conceituais.

O tratamento por tipo documental será avaliado separadamente para evitar combinar múltiplas alterações em um único teste.

---

# Comparação v0.1 × T1

| Indicador | v0.1 | v0.1-T1 |
|---|---:|---:|
| Resultados Scopus | 2.154 | 767 |
| Redução em relação à v0.1 | — | 64,4% |
| Seeds indexados | 11 | 11 |
| Seeds recuperados | 11 | 11 |
| Query misses | 0 | 0 |
| Taxa-semente interna | 100% | 100% |
| Registros da amostra diagnóstica | 17 | 17 |
| R | 0 | 4 |
| I | 13 | 6 |
| D | 4 | 7 |

A comparação entre as amostras é utilizada somente como diagnóstico exploratório.

Como as amostras não constituem amostras probabilísticas equivalentes da população de resultados, as diferenças entre `R`, `I` e `D` não devem ser interpretadas como estimativas formais de ganho de precisão.

---

# Decisão sobre o Teste T1

O Teste T1 foi considerado **aprovado para continuidade da calibração**.

A alteração:

```text
environment* → environmental
```

produziu simultaneamente:

1. redução de aproximadamente 64,4% no volume total de registros;
2. manutenção de 100% da recuperação dos estudos-semente indexados;
3. redução evidente de falsos positivos associados a expressões como `computing environments`, `digital environments` e `dynamic environments`;
4. recuperação de estudos claramente relacionados aos domínios ambientais e de sustentabilidade.

Assim, `environmental` passa a ser o termo preferencial em relação a `environment*` para a próxima iteração da estratégia.

Entretanto, a string v0.1-T1 ainda não é considerada a string definitiva.

---

# Questões metodológicas abertas após T1

Os seguintes pontos deverão ser tratados durante a continuação da calibração:

1. Refinar o uso de `sustainab*`, que ainda recupera usos genéricos ou não ambientais de sustentabilidade.
2. Definir de forma operacional como tratar estudos de ESG.
3. Definir quando aplicações agrícolas são suficientemente ambientais/sustentáveis para inclusão.
4. Definir se estudos de eficiência energética entram somente quando houver objetivo ambiental explícito.
5. Definir como tratar sensoriamento remoto de propósito geral.
6. Definir se RAG utilizado apenas como baseline é suficiente para inclusão.
7. Definir se sustentabilidade espacial/orbital pertence ao escopo.
8. Avaliar posteriormente filtros de tipo documental para reduzir reviews, tutorials e proceedings completos.
9. Definir o tratamento de registros com ano bibliográfico futuro/online-first, como artigos indexados como 2027 durante a busca realizada em 2026.

Esses pontos não serão resolvidos por conveniência para reduzir o corpus. As decisões deverão ser fundamentadas na definição operacional do domínio e registradas no protocolo/amendments quando aplicável.

---

# Próximo passo

O próximo teste controlado será direcionado ao termo:

```text
sustainab*
```

A intenção é reduzir usos genéricos de sustentabilidade sem alterar simultaneamente:

- o bloco de RAG;
- `environmental`;
- `climat*`;
- `ecolog*`;
- período de publicação;
- filtros por tipo documental.

Essa estratégia mantém o princípio de alterar uma variável por vez, permitindo identificar o efeito específico de cada modificação.

A busca definitiva ainda não foi executada.


# Teste T2 — remoção de `sustainab*`

## Objetivo

Avaliar se a remoção de `sustainab*` reduz resultados associados a usos genéricos de sustentabilidade sem comprometer a recuperação dos estudos-semente.

## Configuração

- Data: 2026-10-04
- Base: Scopus
- Identificador: v0.1-T2
- Período: 2020-presente
- Alteração em relação ao T1: remoção de `sustainab*`
- Termos de domínio mantidos: `environmental`, `climat*` e `ecolog*`
- Bloco RAG: inalterado
- Resultados retornados: 472
- Resultados do T1: 767
- Resultados da v0.1: 2.154

## Validação dos estudos-semente

- Estudos-semente avaliados: 12
- Estudos-semente confirmadamente indexados na Scopus: 11
- Estudos-semente recuperados pela v0.1-T2: 11
- Estudos-semente não indexados: 1 (S04)
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

## Impacto sobre o volume de resultados

Comparação:

- v0.1: 2.154 registros
- v0.1-T1: 767 registros
- v0.1-T2: 472 registros

A v0.1-T2 apresentou redução aproximada de 38,5% em relação ao T1 e de 78,1% em relação à consulta inicial v0.1.

A remoção de `sustainab*` não provocou perda de nenhum estudo-semente confirmadamente indexado.

## Interpretação preliminar

O T2 apresenta resultado promissor, pois reduziu novamente o volume de registros retornados mantendo a taxa-semente interna de 100%.

Entretanto, a menor quantidade de resultados não é suficiente para concluir que a estratégia é superior. Antes da decisão sobre a manutenção ou rejeição do T2, será realizada uma nova amostra diagnóstica dos resultados para verificar se a redução de volume corresponde também a uma melhoria qualitativa da aderência ao escopo.

O T2 permanece em avaliação e ainda não constitui a string definitiva.

# Resultado do Teste T2

A consulta v0.1-T2 retornou 472 registros na Scopus.

A validação dos estudos-semente mostrou que todos os 11 estudos
confirmadamente indexados na Scopus continuaram sendo recuperados.
O estudo S04 permaneceu classificado como não indexado e, portanto,
não foi incluído no denominador da taxa-semente.

- Estudos-semente avaliados: 12
- Estudos-semente indexados na Scopus: 11
- Estudos-semente recuperados: 11
- Query misses: 0
- Taxa-semente interna: 11/11 = 100%

## Diagnóstico de ruído — T2

Foi realizada uma amostra diagnóstica de 17 registros da consulta
v0.1-T2.

Resultados:

- Claramente relevantes (R): 8
- Claramente irrelevantes (I): 6
- Duvidosos (D): 3

A amostra possui finalidade exclusivamente diagnóstica e não constitui
estimativa formal da precisão da estratégia de busca.

Os resultados considerados relevantes incluíram aplicações de RAG em
relato de carbono, análise de impacto ambiental de materiais,
biodiversidade, monitoramento de árvores urbanas, seleção sustentável
de materiais de construção, monitoramento ambiental, adaptação
climática e avaliação de robustez de Graph-RAG em conhecimento
ecológico.

Os principais falsos positivos restantes decorreram do uso de termos
como "environmental" em sentido operacional, por exemplo em ambientes
virtuais, direção autônoma e testes de veículos.

Também permaneceram casos de fronteira relacionados a agricultura,
turismo sustentável e ESG, cuja elegibilidade deverá ser resolvida
posteriormente pela aplicação dos critérios de inclusão e exclusão,
e não por novas restrições na string de busca.

## Decisão sobre o T2

O Teste T2 foi considerado aprovado como estratégia candidata para a
Scopus.

A remoção de `sustainab*` reduziu o volume de resultados sem provocar
perda de nenhum estudo-semente confirmadamente indexado.

Embora ainda existam falsos positivos, novas restrições na string
poderiam aumentar o risco de perda de estudos relevantes e produzir
sobreajuste da estratégia aos registros utilizados durante a
calibração.

Por esse motivo, a v0.1-T2 será mantida como string candidata da
Scopus e adaptada às demais bases selecionadas.

A busca definitiva ainda não foi executada.