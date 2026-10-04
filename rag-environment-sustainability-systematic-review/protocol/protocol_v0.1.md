# Protocolo v0.1 - Revisão Sistemática sobre RAG em Domínios Ambientais e de Sustentabilidade

- Versão: `v0.1`
- Data de criação: `2026-10-04`
- Status: **PRELIMINAR - NÃO CONGELADO**
- Revisora: `[NOME DA AUTORA]`

> Este protocolo corresponde à versão inicial do Dia 1. A string de busca e os critérios de elegibilidade ainda serão submetidos à busca piloto e à calibração intra-revisora antes do congelamento da versão `v1.0`.

## 1. Título provisório

**Estratégias e Arquiteturas de Retrieval-Augmented Generation em Domínios Ambientais e de Sustentabilidade: uma Revisão Sistemática da Literatura**

O título poderá ser refinado após a análise dos resultados, desde que permaneça consistente com o objeto principal da revisão - RAG - e com o contexto de aplicação - domínios ambientais e de sustentabilidade.

## 2. Objetivo geral

Identificar e analisar as estratégias arquiteturais, técnicas de recuperação e métodos de avaliação empregados em sistemas RAG desenvolvidos para domínios ambientais e de sustentabilidade, investigando as evidências disponíveis sobre o impacto dessas escolhas no desempenho dos sistemas.

## 3. Definições operacionais

### 3.1 Retrieval-Augmented Generation (RAG)

Para fins desta revisão, considera-se RAG uma arquitetura ou pipeline em que informações provenientes de uma fonte externa de conhecimento são recuperadas e incorporadas ao contexto utilizado por um modelo gerador para produzir a saída final.

Não serão considerados RAG, para fins de elegibilidade, estudos que utilizem apenas LLMs sem mecanismo de recuperação externa ou apenas recuperação de informação sem integração com uma etapa de geração.

### 3.2 Domínios ambientais e de sustentabilidade

Neste estudo, são considerados domínios ambientais e de sustentabilidade aqueles em que questões ambientais, ecológicas, climáticas ou relacionadas à gestão sustentável de recursos naturais constituem parte central do problema investigado, dos dados utilizados ou da aplicação computacional desenvolvida.

**Regra de fronteira:** estudos de agricultura, geociências, sensoriamento remoto, gestão de desastres, políticas públicas, energia ou setor corporativo serão incluídos apenas quando apresentarem relação explícita e substancial com questões ambientais ou de sustentabilidade ambiental. Menções genéricas a sustentabilidade, ESG ou ODS, sem componente ambiental relevante para a aplicação RAG, não serão suficientes para inclusão.

## 4. Questões de pesquisa

### RQ1

**Quais arquiteturas e estratégias de RAG têm sido utilizadas em aplicações computacionais em domínios ambientais e de sustentabilidade?**

Dados esperados: tipo de RAG, organização do pipeline, presença de GraphRAG, multimodalidade, componentes agênticos e modalidade dos dados.

### RQ2

**Quais técnicas são empregadas nas etapas de indexação, recuperação, pós-recuperação e geração desses sistemas?**

Dados esperados: chunking, embeddings, sparse/dense/hybrid retrieval, top-k, filtros, query transformation, reranking e LLM gerador.

### RQ3

**Como os sistemas RAG em domínios ambientais e de sustentabilidade são avaliados, considerando datasets, baselines e métricas?**

Dados esperados: corpus/dataset, baseline, métricas de retrieval, métricas de geração, métricas específicas de RAG, avaliação humana e LLM-as-a-Judge.

### RQ4

**Quais evidências experimentais existem sobre os efeitos das diferentes configurações de RAG no desempenho dos sistemas?**

Dados esperados: RAG vs. não-RAG, ablation, comparação entre configurações e registro de ganhos, perdas ou trade-offs.

### 4.1 Regra de alinhamento RQ-dados

Todo campo de extração deverá contribuir para pelo menos uma RQ. Se um campo não contribuir para nenhuma questão de pesquisa, sua necessidade deverá ser justificada antes de ser incorporado ao formulário de extração.

## 5. Fontes de informação

### 5.1 Bases iniciais

A revisão iniciará com as seguintes bases:

- Scopus
- IEEE Xplore
- ACM Digital Library

A Web of Science não será incluída automaticamente. Sua inclusão somente será considerada se a busca piloto indicar cobertura insuficiente das três bases iniciais. Qualquer inclusão deverá ser registrada em `amendments.md`.

## 6. Período de publicação

Intervalo inicial: **2020 até a data da busca final**.

O ano de 2020 foi adotado como ponto de partida por corresponder ao marco moderno do paradigma RAG. O intervalo permanece classificado como definido em princípio até a calibração do protocolo.

## 7. Tipos de publicação e corpus principal

O corpus principal será composto por **estudos peer-reviewed**, publicados em periódicos ou anais de conferências.

Preprints não integrarão automaticamente a síntese principal. Caso sejam utilizados para uma análise exploratória complementar devido à rápida evolução da área, deverão ser identificados separadamente e não misturados ao corpus principal sem justificativa metodológica registrada.

## 8. Critérios de elegibilidade - versão v0.1

Os critérios abaixo são preliminares. Eles serão testados na calibração intra-revisora antes de serem congelados na versão `v1.0`.

### 8.1 Critérios de inclusão

| Código | Critério de inclusão v0.1 |
|---|---|
| CI1 | Estudo primário que desenvolva, aplique ou avalie RAG. |
| CI2 | Aplicação em domínio ambiental ou de sustentabilidade conforme a definição operacional deste protocolo. |
| CI3 | Descrição mínima da arquitetura ou dos componentes necessários para classificação. |
| CI4 | Presença de avaliação empírica. |
| CI5 | Texto completo disponível. |
| CI6 | Publicado no período definido pela revisão. |

### 8.2 Critérios de exclusão

| Código | Critério de exclusão v0.1 |
|---|---|
| CE1 | LLM sem mecanismo de recuperação. |
| CE2 | RAG aplicado a outro domínio sem componente ambiental ou de sustentabilidade ambiental substancial e separável. |
| CE3 | Survey, revisão, editorial, tutorial ou artigo de opinião. |
| CE4 | Proposta sem avaliação empírica. |
| CE5 | Duplicata ou versão redundante do mesmo estudo. |
| CE6 | Texto integral indisponível. |
| CE7 | Informação técnica insuficiente para responder às RQs. |

## 9. Estratégia de busca - estado no Dia 1

A estratégia de busca ainda não é definitiva. No Dia 1 será registrada apenas uma versão candidata `v0.1`, disponível em `search/search_strings.md`.

A busca piloto deverá testar se a combinação de termos de RAG com termos ambientais e de sustentabilidade recupera estudos conhecidos e claramente relevantes. Ajustes serão permitidos antes do congelamento do protocolo `v1.0`, desde que registrados.

Nenhuma execução do rascunho `v0.1` deverá ser tratada como busca definitiva.

## 10. Plano de seleção dos estudos

A revisão será conduzida por uma única revisora. O rigor será sustentado por critérios previamente definidos, calibração intra-revisora e registro sistemático das decisões.

### 10.1 Calibração intra-revisora

Antes da triagem definitiva, serão selecionados aproximadamente 15-20 registros para testar os critérios CI/CE v0.1. Cada registro será classificado como `include`, `exclude` ou `maybe`.

Os casos ambíguos serão utilizados para identificar problemas de interpretação e ajustar os critérios antes de congelar a versão `v1.0`.

### 10.2 Etapas de seleção

1. Exportação dos registros brutos de cada base.
2. Deduplicação, preservando os arquivos brutos originais.
3. Triagem por título e resumo.
4. Leitura do texto completo dos candidatos remanescentes.
5. Registro obrigatório do código de exclusão para exclusões na etapa de texto completo.
6. Avaliação de qualidade dos estudos incluídos.
7. Uma rodada de backward e forward snowballing sobre o conjunto final da busca tradicional.
8. Aplicação dos mesmos CI/CE aos estudos provenientes do snowballing.
9. Fechamento do corpus para extração e síntese.

## 11. Rastreabilidade e versionamento

- Nunca sobrescrever silenciosamente uma string de busca; usar `v0.1`, `v0.2`, `v1.0` etc.
- Registrar data e hora das buscas definitivas por base.
- Manter intactos os arquivos brutos exportados por cada base.
- Registrar decisões de triagem em `screening/decision_log.csv`.
- Toda exclusão em texto completo deverá possuir um `reason_code` válido.
- Toda alteração posterior ao protocolo `v1.0` deverá ser documentada em `protocol/amendments.md`.
- Dados não informados nos artigos não serão inferidos; será utilizado `NR` (`Not Reported`).

## 12. Itens ainda provisórios no Dia 1

| Item | Estado atual | Momento de congelamento |
|---|---|---|
| String de busca | Rascunho v0.1 | Após busca piloto em artigos conhecidos |
| CI/CE | Versão preliminar v0.1 | Após calibração em 15-20 registros |
| Taxonomia de tipos de RAG | Categorias iniciais como guia | Após observar como os estudos reportam as arquiteturas |
| Campos de extração | Núcleo vinculado às RQs | Antes do início da extração |
| Web of Science | Não incluída automaticamente | Somente se a busca piloto justificar |

## 13. Gate metodológico do Dia 1

A revisão somente avançará para a busca piloto quando a revisora conseguir explicar e localizar no repositório:

1. o que é considerado RAG nesta revisão;
2. o que conta como domínio ambiental e de sustentabilidade;
3. o que cada RQ pretende medir;
4. onde cada decisão metodológica será registrada.
