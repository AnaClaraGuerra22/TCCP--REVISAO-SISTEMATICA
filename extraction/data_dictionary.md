# Data Dictionary — versão v1.0

- Versão: `v1.0`
- Data de congelamento: `2026-10-06`
- Status: **CONGELADO ANTES DA EXTRAÇÃO**
- Protocolo associado: `protocol/protocol_v1.0.md`

Este arquivo define os campos utilizados na extração de dados dos estudos
incluídos na revisão sistemática.

Os campos foram definidos de forma alinhada às questões de pesquisa RQ1–RQ4.

---

## 1. Regras globais

### 1.1 Dados ausentes

Utilizar:

`NR` — `Not Reported`

sempre que o artigo não informar explicitamente um dado necessário.

Não inferir:

- modelos;
- versões;
- parâmetros;
- tamanhos de chunk;
- valores de `top_k`;
- mecanismos de recuperação;
- configurações experimentais;
- resultados.

Utilizar:

`NA` — `Not Applicable`

somente quando o campo realmente não se aplicar à arquitetura estudada.

`NR` e `NA` não são equivalentes.

---

### 1.2 Preservação do valor original

Sempre registrar primeiro a informação tal como reportada pelo artigo.

Quando houver necessidade de normalização, o valor original deve ser
preservado.

Não substituir silenciosamente terminologia utilizada pelos autores por
categorias da revisão.

---

### 1.3 Múltiplas configurações

Quando um estudo utilizar múltiplas configurações:

- registrar todas as configurações relevantes;
- não selecionar apenas a configuração de melhor desempenho;
- preservar diferenças entre variantes quando forem relevantes para as RQs.

Quando necessário, múltiplos valores poderão ser separados por `;`.

---

## 2. Identificação do estudo

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `study_id` | Identificador único atribuído pela revisão. | Todas | `S001`, `S002`, ... | Nunca usar `NR`. |
| `title` | Título do estudo. | Metadado | Texto original. | Nunca usar `NR`. |
| `year` | Ano efetivo da publicação utilizada. | Metadado | `YYYY` | `NR` apenas se realmente indisponível. |
| `venue` | Periódico ou conferência. | Metadado | Nome original. | `NR` se não informado. |
| `doi` | DOI do estudo. | Metadado | DOI normalizado. | `NR` se inexistente ou não informado. |

Os campos bibliográficos são mantidos para rastreabilidade e não constituem
variáveis analíticas das RQs.

---

## 3. Domínio e aplicação

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `environmental_sustainability_domain` | Subdomínio ambiental ou de sustentabilidade no qual a aplicação está situada. | RQ1 | Texto curto controlado. Exemplos: `climate`; `biodiversity`; `wildfire`; `environmental monitoring`; `sustainable agriculture`; `built environment`; `waste`; `environmental policy`; `other`. | `NR` se não for possível identificar claramente o subdomínio. |
| `application_objective` | Problema ou tarefa principal realizada pelo sistema RAG. | RQ1 | Texto curto. | `NR` se não estiver explícito. |
| `data_modality` | Modalidades de dados utilizadas pela aplicação. | RQ1 | `text`; `image`; `tabular`; `geospatial`; `sensor`; `multimodal`; `other`; combinações permitidas. | `NR` se não reportado. |

---

## 4. Arquitetura RAG

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `rag_architecture` | Estratégia arquitetural explicitamente utilizada pelo estudo. | RQ1 | `standard`; `graph`; `agentic`; `multi-agent`; `multimodal`; `hybrid/combined`; `other`; múltiplos valores permitidos. | `NR` quando não for possível classificar. |
| `architecture_description` | Resumo curto da organização do pipeline RAG. | RQ1 | Texto estruturado e factual. | `NR` se não descrito. |
| `knowledge_source` | Fonte externa de conhecimento recuperada pelo sistema. | RQ1 / RQ2 | Ex.: artigos científicos, EPDs, documentos regulatórios, knowledge graph, base institucional, web, dados históricos. | `NR` se não especificada. |
| `knowledge_source_type` | Tipo estrutural da fonte de conhecimento. | RQ1 / RQ2 | `documents`; `database`; `knowledge_graph`; `web`; `API`; `multimodal`; `combination`; `other`; `NR`. | `NR` se não determinável. |
| `agentic_component` | Uso de agentes no pipeline RAG. | RQ1 | `yes`; `no`; `NR` + descrição quando `yes`. | `NR` quando não for possível distinguir ausência de falta de relato. |
| `multimodal_component` | Uso de mais de uma modalidade na arquitetura RAG. | RQ1 | `yes`; `no`; `NR` + modalidades quando aplicável. | `NR` se não reportado. |
| `graph_component` | Uso de knowledge graph ou estrutura de grafo como parte do RAG. | RQ1 | `yes`; `no`; `NR` + tecnologia quando reportada. | `NR` se não reportado. |

---

## 5. Preparação e indexação

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `data_preprocessing` | Processamento realizado antes da indexação. | RQ2 | Texto curto. | `NR` se não descrito. |
| `chunking` | Estratégia de fragmentação e parâmetros associados. | RQ2 | Ex.: `semantic; 1000 chars; overlap 100`. | Registrar `NR` para componentes não informados. |
| `embedding_model` | Modelo utilizado para representação vetorial. | RQ2 | Nome e versão exatos quando disponíveis. | `NR` se não identificado. |
| `index_or_store` | Tecnologia utilizada para armazenar/indexar representações recuperáveis. | RQ2 | Ex.: `FAISS`; `ChromaDB`; `Pinecone`; `Neo4j`; `Elasticsearch`; `custom`; `NR`. | `NR` se não reportado. |
| `indexing_method` | Estratégia de indexação explicitamente reportada. | RQ2 | Texto curto. | `NR` se não descrita. |

---

## 6. Recuperação

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `retrieval_type` | Tipo principal de recuperação utilizado. | RQ2 | `sparse`; `dense`; `hybrid`; `graph`; `multimodal`; `combination`; `other`; `NR`. | `NR` se não descrito. |
| `retrieval_method` | Método ou algoritmo específico utilizado na recuperação. | RQ2 | Nome reportado pelo estudo. | `NR` se não informado. |
| `retrieval_unit` | Unidade recuperada pelo sistema. | RQ2 | Ex.: `chunk`; `document`; `graph node`; `triplet`; `image`; `record`; `NR`. | `NR` se não informado. |
| `top_k` | Número de itens recuperados. | RQ2 | Inteiro ou lista de valores. | `NR` se não reportado. |
| `metadata_filtering` | Uso de filtros ou metadados durante retrieval. | RQ2 | `none`; descrição do filtro; `NR`. | `NR` quando não for possível distinguir ausência de falta de relato. |
| `query_transformation` | Técnica aplicada à consulta antes ou durante retrieval. | RQ2 | `none`; query rewriting; expansion; decomposition; multi-query; HyDE; método reportado; `NR`. | `NR` se não informado. |

---

## 7. Pós-recuperação

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `reranking` | Uso e método de reranking após recuperação inicial. | RQ2 | `none`; modelo/método; `NR`. | `NR` quando não for possível distinguir ausência de falta de relato. |
| `post_retrieval_method` | Outras técnicas aplicadas ao conjunto recuperado antes da geração. | RQ2 | Ex.: filtering; compression; fusion; deduplication; validation; `none`; `NR`. | `NR` se não informado. |

---

## 8. Geração

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `generator_llm` | Modelo gerador utilizado no sistema RAG. | RQ2 | Nome + versão/checkpoint quando disponível. | `NR` se não identificado. |
| `generation_strategy` | Estratégia utilizada na etapa generativa. | RQ2 | Texto curto: prompting, chain-of-thought quando explicitamente reportado, agent orchestration, validation loop etc. | `NR` se não descrita. |
| `prompting_strategy` | Técnica de prompting explicitamente utilizada. | RQ2 | `zero-shot`; `few-shot`; template; structured prompt; other; `NR`. | `NR` se não informado. |
| `citation_or_grounding` | Mecanismo explícito para grounding, provenance ou citação das fontes recuperadas. | RQ2 | `yes`; `no`; `NR` + descrição quando aplicável. | `NR` quando não reportado. |

---

## 9. Avaliação experimental

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `evaluation_dataset` | Dataset, corpus ou conjunto usado para avaliar o sistema. | RQ3 | Nome oficial ou descrição. | `NR` se não descrito. |
| `evaluation_size` | Quantidade de exemplos, consultas, perguntas ou casos utilizados na avaliação. | RQ3 | Número + unidade. | `NR` se não reportado. |
| `baseline` | Sistemas ou configurações utilizados como comparação. | RQ3 / RQ4 | Nomes; múltiplos valores permitidos; `none`; `NR`. | `NR` se não houver informação suficiente. |
| `metrics` | Métricas utilizadas na avaliação. | RQ3 | Lista exatamente como reportada. | `NR` se nenhuma métrica for descrita. |
| `human_evaluation` | Existência de avaliação humana. | RQ3 | `yes`; `no`; `NR` + descrição quando aplicável. | `NR` se não informado. |
| `llm_as_judge` | Uso de LLM como avaliador. | RQ3 | `yes`; `no`; `NR` + modelo quando reportado. | `NR` se não informado. |
| `evaluation_dimensions` | Aspectos avaliados além das métricas numéricas. | RQ3 | Ex.: faithfulness; relevance; hallucination; factuality; latency; usability. | `NR` se não reportado. |

---

## 10. Evidência comparativa — RQ4

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `comparison_type` | Tipo de comparação experimental realizada. | RQ4 | `RAG_vs_non_RAG`; `RAG_configuration`; `ablation`; `retriever_comparison`; `LLM_comparison`; `other`; múltiplos permitidos; `none`; `NR`. | `NR` se não descrito. |
| `ablation_study` | Existência de experimento de ablação. | RQ4 | `yes`; `no`; `NR`. | `NR` se não informado. |
| `comparative_evidence` | Resultado explicitamente reportado da comparação. | RQ4 | Texto estruturado contendo configurações comparadas, métrica e resultado. | `NR` se não houver evidência comparativa. |
| `effect_direction` | Direção do efeito observado na comparação. | RQ4 | `improvement`; `degradation`; `mixed`; `no_difference`; `NR`. | Derivar somente quando a direção estiver inequivocamente sustentada pelos resultados reportados. |
| `trade_offs` | Trade-offs explicitamente observados ou discutidos com base nos experimentos. | RQ4 | Texto curto. | `NR` se não reportado. |

---

## 11. Informação complementar para interpretação

| Campo | Definição operacional | RQ associada | Valores / formato | Regra para NR |
|---|---|---|---|---|
| `reported_limitations` | Limitações explicitamente reconhecidas pelos autores que afetem a interpretação das evidências da revisão. | RQ3 / RQ4 | Texto resumido fiel ao artigo. | `NR` se não reportadas. |

---

## 12. Regras de preenchimento

1. Registrar primeiro o valor explicitamente reportado pelo estudo.

2. Não converter ausência de relato em ausência do componente.

   Exemplo:

   Se o artigo não mencionar reranking:

   `reranking = NR`

   e não:

   `reranking = none`

3. Utilizar `none` apenas quando o artigo permitir afirmar explicitamente
   que o componente não foi utilizado.

4. Utilizar `NA` apenas quando o campo não fizer sentido para aquela
   arquitetura.

5. Quando houver múltiplas configurações, preservar todas as configurações
   relevantes.

6. Resultados quantitativos não deverão ser recalculados ou inferidos durante
   a extração, salvo quando uma transformação metodológica for posteriormente
   definida e documentada.

7. Nomes de modelos, datasets, métricas e ferramentas devem ser registrados
   inicialmente exatamente como aparecem no estudo.

8. Normalizações utilizadas na síntese deverão ser realizadas posteriormente,
   preservando os valores originais.

9. Campos adicionais somente poderão ser adicionados após o início da
   extração mediante alteração documentada em `protocol/amendments.md`.

---

## 13. Alinhamento com as questões de pesquisa

| Questão | Principais campos |
|---|---|
| RQ1 — arquiteturas e estratégias | `environmental_sustainability_domain`, `application_objective`, `data_modality`, `rag_architecture`, `architecture_description`, `knowledge_source`, `knowledge_source_type`, `agentic_component`, `multimodal_component`, `graph_component` |
| RQ2 — indexação, recuperação, pós-recuperação e geração | `data_preprocessing`, `chunking`, `embedding_model`, `index_or_store`, `indexing_method`, `retrieval_type`, `retrieval_method`, `retrieval_unit`, `top_k`, `metadata_filtering`, `query_transformation`, `reranking`, `post_retrieval_method`, `generator_llm`, `generation_strategy`, `prompting_strategy`, `citation_or_grounding` |
| RQ3 — datasets, baselines e métricas | `evaluation_dataset`, `evaluation_size`, `baseline`, `metrics`, `human_evaluation`, `llm_as_judge`, `evaluation_dimensions` |
| RQ4 — efeitos das configurações | `comparison_type`, `ablation_study`, `comparative_evidence`, `effect_direction`, `trade_offs` |

---

## 14. Status do dicionário

O presente dicionário foi refinado antes do início da extração definitiva,
em conformidade com o Gate metodológico da versão `v1.0`.

Após o início da extração, novos campos não deverão ser adicionados
silenciosamente.

Qualquer modificação estrutural deverá ser registrada em:

`protocol/amendments.md`