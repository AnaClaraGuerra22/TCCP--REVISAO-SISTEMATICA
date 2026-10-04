# Data Dictionary - núcleo inicial do Dia 1

- Versão: `v0.1`
- Status: **NÚCLEO INICIAL - será refinado antes da extração definitiva**

## Regra global para dados ausentes

Utilizar `NR` (`Not Reported`) sempre que o artigo não informar explicitamente um dado necessário. Não inferir valores, modelos, parâmetros ou configurações a partir de contexto indireto.

`NA` (`Not Applicable`) só deve ser utilizado quando o campo realmente não se aplicar à arquitetura estudada, e não quando a informação estiver ausente.

| Campo | Definição operacional | RQ associada | Valores permitidos / formato | Regra para NR |
|---|---|---|---|---|
| `study_id` | Identificador estável e único atribuído ao estudo ao entrar na base consolidada. | Todas | `S001`, `S002`, `S003`, ... | Nunca usar NR; o identificador é atribuído pela revisão. |
| `environmental_sustainability_domain` | Subdomínio ambiental ou de sustentabilidade ambiental em que a aplicação RAG está situada. | RQ1 | Texto curto controlado; exemplos de categorias serão refinados após a calibração. | `NR` se o estudo for elegível, mas não permitir identificar claramente o subdomínio. |
| `rag_architecture` | Estratégias arquiteturais de RAG explicitamente reportadas pelo estudo. Permite múltiplos rótulos quando a arquitetura combinar abordagens. | RQ1 | Texto controlado; categorias iniciais podem incluir standard, graph, multimodal, agentic, multi-agent ou combinações. | `NR` se a arquitetura não puder ser determinada a partir do texto. |
| `retrieval_type` | Tipo de recuperação utilizado no pipeline. | RQ2 | `sparse`; `dense`; `hybrid`; `graph`; `multimodal`; `combination`; `NR` | Usar `NR` quando o mecanismo de retrieval não for explicitamente descrito. |
| `chunking` | Estratégia de fragmentação do corpus e tamanho/overlap quando informados. | RQ2 | Texto estruturado, por exemplo `semantic; 1000 chars; overlap NR`. | Registrar `NR` para cada componente não informado; não estimar tamanho ou overlap. |
| `embedding_model` | Modelo de embedding utilizado para representar consultas/documentos. | RQ2 | Nome e versão exatos quando disponíveis. | `NR` se não houver identificação explícita. |
| `top_k` | Número `k` de itens recuperados e encaminhados à etapa seguinte do pipeline. | RQ2 | Inteiro positivo; lista de valores se houver experimento com múltiplos `k`; `NR` | `NR` quando o valor não for explicitamente reportado. |
| `reranking` | Presença e método de reranking aplicado após a recuperação inicial. | RQ2 | `none`; nome do método/modelo; `NR` | `NR` quando não for possível distinguir ausência de reranking de falta de relato. |
| `generator_llm` | Modelo gerador utilizado pelo sistema RAG e sua versão, quando disponível. | RQ2 | Nome do modelo + versão/checkpoint quando reportados. | `NR` se o estudo não identificar o modelo ou sua versão. |
| `evaluation_dataset` | Dataset, corpus ou conjunto de avaliação usado para medir o desempenho do sistema. | RQ3 | Nome oficial e/ou descrição do conjunto. | `NR` se o conjunto de avaliação não for descrito. |
| `baseline` | Sistema, modelo ou configuração utilizada como comparação experimental. | RQ3 / RQ4 | Nome da baseline; múltiplos valores permitidos; `none`; `NR` | `NR` se o artigo não esclarecer se houve baseline. |
| `metrics` | Métricas empregadas na avaliação do sistema ou de seus componentes. | RQ3 | Lista de métricas exatamente como reportadas, posteriormente normalizadas em campo derivado. | `NR` se nenhuma métrica for descrita. |
| `comparative_evidence` | Resultado explicitamente reportado de comparação entre configurações, RAG vs. não-RAG ou experimento de ablation. | RQ4 | Texto estruturado contendo comparação, direção do efeito e métrica associada quando disponível. | `NR` se não houver evidência comparativa explícita. |

## Regras de preenchimento

1. Registrar primeiro o valor tal como reportado pelo estudo; normalizações posteriores devem preservar o valor original.
2. Não converter ausência de relato em ausência do componente.
3. Quando um estudo usar múltiplas configurações, manter todos os valores relevantes no mesmo registro ou em estrutura auxiliar, sem escolher apenas a configuração "melhor".
4. Campos adicionais só devem ser adicionados antes do início da extração definitiva ou mediante alteração metodológica documentada.
