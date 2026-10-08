# Registro de Alterações do Protocolo

Este arquivo registra alterações metodológicas realizadas após a criação
do protocolo inicial.

Alterações realizadas antes do congelamento da versão `v1.0` também são
registradas quando modificam decisões previamente documentadas na versão
preliminar `v0.1`.

As alterações registradas abaixo preservam a rastreabilidade entre o
protocolo preliminar e a versão congelada.

| Data | Versão de origem | Versão resultante | Alteração | Justificativa | Impacto |
|---|---|---|---|---|---|
| 2026-10-04 | v0.1 | v1.0 | Bases de busca alteradas de Scopus + IEEE Xplore + ACM Digital Library para Scopus + IEEE Xplore. | A estratégia final foi definida com Scopus para cobertura multidisciplinar e IEEE Xplore para cobertura especializada em computação e engenharia. A cobertura será complementada por uma rodada de backward e forward snowballing. | A ACM Digital Library deixa de integrar a busca sistemática. As buscas definitivas serão executadas apenas na Scopus e no IEEE Xplore. |
| 2026-10-04 | v0.1 | v1.0 | Refinamento do bloco ambiental da estratégia de busca da Scopus: `environment*` foi substituído por `environmental` e `sustainab*` foi removido da string candidata final. | A busca piloto mostrou ruído recorrente associado a usos não ambientais de `environment*` e a usos amplos de sustentabilidade. Os refinamentos reduziram substancialmente o volume de falsos positivos sem perda dos estudos-semente confirmadamente indexados. | Altera a estratégia de busca definitiva. A string `v0.1-T2` da Scopus passa a constituir a base da string final `v1.0`. |
| 2026-10-04 | v0.1 | v1.0 | A string piloto `v0.1-IEEE` foi aprovada como base da estratégia final do IEEE Xplore. | Todos os estudos-semente confirmadamente indexados no IEEE Xplore foram recuperados e não foram observados `query_misses`. O ruído residual foi considerado tratável pelos critérios de elegibilidade. | A estratégia `v0.1-IEEE` passa a constituir a string final `v1.0` do IEEE Xplore. |
| 2026-10-06 | v0.1 | v1.0 | Realização da calibração intra-revisora dos critérios de elegibilidade em 18 registros, com duas passagens independentes. | A calibração resultou em concordância bruta de 17/18 registros (94,4%) e uma proporção de mudança de 5,6%, inferior ao limite operacional de 20% definido para nova calibração. | Os critérios foram considerados suficientemente estáveis para congelamento, não sendo necessária uma terceira passagem. |
| 2026-10-06 | v0.1 | v1.0 | CE1 foi ampliado de `LLM sem mecanismo de recuperação` para uma definição geral de não atendimento à definição operacional de Retrieval-Augmented Generation. | A calibração identificou casos em que `RAG` possuía outro significado, como `Relation-Aware Graph`, e casos em que recuperação poderia ocorrer sem integração efetiva com a geração. | CE1 passa a contemplar LLM sem recuperação externa, recuperação sem geração, semantic retrieval sem integração com geração e usos alternativos da sigla RAG. |
| 2026-10-06 | v0.1 | v1.0 | CE4 foi operacionalizado para incluir propostas em que avaliação, validação ou implantação aparecem apenas como trabalho futuro. | O caso C13 mudou de `maybe` na Passagem A para `exclude — CE4` na Passagem B após identificação explícita da ausência de avaliação empírica. | Torna mais objetiva a exclusão de frameworks ou arquiteturas não avaliados empiricamente. |
| 2026-10-06 | v0.1 | v1.0 | Adição de regras operacionais de fronteira para RAG como baseline, energia/microgrids/baterias, ESG, semantic retrieval, usos não ambientais de `environment/environmental`, agricultura, ambiente construído, sensoriamento remoto, ODS/SDGs e usos alternativos da sigla RAG. | A calibração revelou casos em que os critérios gerais eram adequados, mas título e resumo não permitiam decisões seguras sem regras adicionais de interpretação. | Maior consistência e rastreabilidade na aplicação dos critérios CI/CE durante o screening. |
| 2026-10-06 | v0.1 | v1.0 | Formalização da regra de encaminhamento de casos ambíguos para texto completo. | Quatro registros permaneceram como `maybe` nas duas passagens de calibração, mostrando que algumas decisões não podem ser tomadas com segurança somente por título e resumo. | Casos ambíguos não serão excluídos por inferência na triagem inicial; deverão avançar para avaliação em texto completo quando necessário. |

| 2026-10-06 | v1.0 | v1.0 + amendment | Adição de pré-triagem assistida por LLM no screening de título e resumo. O LLM será utilizado exclusivamente como ferramenta de apoio, fornecendo uma sugestão de classificação (`include`, `exclude` ou `maybe`), código de exclusão quando aplicável, nível de confiança e justificativa curta. A decisão oficial continuará sendo realizada pela revisora. O modelo e o prompt serão congelados somente após calibração prévia utilizando os 18 registros da calibração intra-revisora. Nenhum registro será excluído automaticamente com base apenas na saída do LLM. | Reduzir a carga operacional do screening de título e resumo, considerando a condução da revisão por uma única revisora e o volume de 587 registros deduplicados, preservando controle humano sobre todas as decisões de elegibilidade. | Não altera as perguntas de pesquisa, os critérios `CI1–CI6` e `CE1–CE7`, as regras de fronteira, as bases bibliográficas, as strings de busca ou o corpus recuperado. Introduz apenas uma ferramenta de apoio ao screening, com validação prévia, versionamento e rastreabilidade das saídas. |

| 2026-10-07 | v1.0 + amendment | v1.0 + amendment | Refinamento da pré-triagem assistida por LLM: comparação de Qwen3:8B, Llama 3.2 3B e Qwen3:4B nos 18 registros do conjunto de desenvolvimento/calibração e substituição da classificação direta pelo LLM por uma arquitetura criterial. Na nova arquitetura, o modelo avalia separadamente os critérios de estudo primário, RAG operacional, domínio ambiental, avaliação empírica e papel do RAG; uma regra determinística em Python deriva posteriormente a sugestão `include`, `exclude` ou `maybe` e o código de exclusão aplicável. O Qwen3:4B foi selecionado como candidato operacional para a etapa de validação independente. | A classificação direta apresentou comportamento excessivamente permissivo nas versões iniciais do prompt, enquanto a decomposição por critérios tornou explícita e auditável a origem das sugestões. Entre os modelos locais avaliados, o Qwen3:4B apresentou melhor equilíbrio entre desempenho computacional e preservação de sensibilidade: processou os 18 registros em 722,31 segundos, sem classificar como `exclude` nenhum dos seis registros classificados como `include` pela revisora no conjunto de desenvolvimento. | Altera apenas a implementação da assistência por LLM no screening. Não modifica `CI1–CI6`, `CE1–CE7`, regras de fronteira, estratégia de busca ou autoridade da decisão humana. Os 18 registros passam a ser tratados como conjunto de desenvolvimento/calibração e não serão usados como evidência independente de validação. Antes da aplicação operacional, o procedimento será avaliado em uma nova amostra cega de validação. |
| 2026-10-08 | v1.0 + amendment | v1.0 + amendment | Finalização da amostra de validação da assistência por LLM. As decisões de referência dos 30 registros foram finalizadas pela revisora antes da exposição às saídas do Qwen3:4B. Durante a aplicação dos critérios, casos foram discutidos com ChatGPT como apoio de adjudicação protocolar; portanto, o conjunto é tratado como referência finalizada pela revisora com apoio protocolar, e não como classificação humana totalmente independente de ferramentas de IA. | Preservar transparência sobre a formação das decisões de referência utilizadas para avaliar o Qwen3:4B, sem ocultar o uso de apoio durante casos de fronteira. | Não altera CI1–CI6, CE1–CE7, regras de fronteira, amostra de validação ou decisões finais da revisora. O Qwen3:4B permaneceu cego às decisões de referência durante a inferência de validação. |
| 2026-10-08 | v1.0 + amendment | v1.0 + amendment | Validação cega do procedimento de pré-triagem assistida por LLM em uma nova amostra de 30 registros, não utilizada no desenvolvimento ou calibração do procedimento de screening assistido. O modelo processou os 30 registros sem erros e apresentou concordância exata de 73,3% (22/30), Cohen's kappa de 0,5294 e sensibilidade de retenção de 100% (11/11 registros classificados pela referência como `include` ou `maybe` não foram sugeridos como `exclude`). Não ocorreu nenhum caso `human include -> Qwen exclude` nem `human maybe -> Qwen exclude`. Entre os 17 registros excluídos por ambos, houve concordância do código CE em 15 (88,2%). O gate previamente definido foi atendido em todos os critérios e o Qwen3:4B + arquitetura criterial v1.2 foi aprovado para uso operacional como ferramenta de apoio ao screening. | Verificar em dados não utilizados no desenvolvimento/calibração do procedimento se a assistência por LLM preserva a sensibilidade necessária ao screening e não produz falsas exclusões de estudos potencialmente elegíveis. | Autoriza a aplicação operacional da configuração validada como apoio à revisora. Não autoriza exclusões automáticas e não altera CI1–CI6, CE1–CE7, regras de fronteira ou autoridade da decisão humana. |

---

## Uso de LLM no screening de título e resumo

A partir do conjunto deduplicado da busca definitiva (`n = 587`), será
utilizada uma ferramenta baseada em Large Language Model (LLM) como apoio
à etapa de screening de título e resumo.

A configuração operacional validada utiliza:

- modelo `qwen3:4b`;
- execução local via Ollama;
- prompt `v1.2-operational`, promovido sem alteração de conteúdo a partir de `v1.2-candidate`;
- `temperature = 0`;
- `seed = 42`;
- `thinking = false`;
- saída estruturada em JSON.

O prompt operacional é byte a byte idêntico ao prompt validado, ambos com SHA-256 `cfac438781c32ec3672dcfb1191149629a4cb23b133646c482d5165696ad19c4`.

O LLM não produz diretamente a decisão final de screening.

Para cada registro, recebe apenas informações provenientes dos metadados
bibliográficos recuperados pelas bases da revisão, como título, resumo,
palavras-chave e tipo de documento, quando disponíveis.

O modelo avalia separadamente:

- se o registro representa estudo primário;
- se há Retrieval-Augmented Generation operacional;
- se o domínio ambiental ou de sustentabilidade ambiental é substantivo;
- se existe avaliação empírica;
- qual é o papel do RAG no estudo.

As avaliações são expressas por categorias controladas
(`yes`, `no`, `unclear` e, para o papel do RAG, categorias específicas).

Uma regra determinística implementada em Python transforma essas
avaliações criteriais em uma sugestão de:

- `include`;
- `exclude`; ou
- `maybe`;

e, quando aplicável, em um código de exclusão `CE1–CE4`.

A ferramenta não é considerada um segundo revisor independente e nenhuma
exclusão será realizada automaticamente com base exclusivamente em sua
saída.

Todas as decisões formais de elegibilidade continuarão sob
responsabilidade da revisora e serão registradas em
`screening/decision_log.csv`.

O desenvolvimento da assistência por LLM utilizou 18 registros da
calibração inicial. Esses registros foram tratados exclusivamente como
conjunto de desenvolvimento e não como evidência independente de
validação.

Antes da aplicação operacional, o Qwen3:4B foi avaliado em uma nova
amostra cega de 30 registros. A referência foi finalizada antes da
inspeção das saídas do Qwen. Durante a classificação da referência,
casos foram discutidos com ChatGPT como apoio de adjudicação protocolar;
por esse motivo, essa referência não é caracterizada como uma
classificação humana totalmente independente de ferramentas de IA.

Na validação, foram obtidos:

- 22/30 decisões exatamente concordantes (73,3%);
- Cohen's kappa = 0,5294;
- 0 casos `human include -> Qwen exclude`;
- 0 casos `human maybe -> Qwen exclude`;
- sensibilidade de retenção = 11/11 (100%);
- concordância do código CE em 15/17 exclusões conjuntas (88,2%).

Todos os critérios do gate definido previamente foram atendidos.

Consequentemente, o Qwen3:4B com a arquitetura criterial v1.2 foi
aprovado para uso operacional como ferramenta de apoio ao screening.

Na presença de informação insuficiente ou ambígua, permanece o princípio
do protocolo de favorecer retenção para avaliação humana em vez de
exclusão por inferência.

Nenhuma informação externa, busca na Web ou web scraping será utilizada
pelo modelo durante essa etapa.

## Regras de preenchimento

- **Data:** usar o formato `AAAA-MM-DD`.
- **Versão de origem:** versão em vigor antes da alteração.
- **Versão resultante:** versão na qual a alteração foi incorporada.
- **Alteração:** descrever objetivamente o que mudou.
- **Justificativa:** registrar a evidência, observação ou problema que motivou a alteração.
- **Impacto:** indicar se a alteração afeta busca, elegibilidade, triagem, extração, qualidade, síntese ou outro componente.

Nenhuma alteração metodológica deve ser realizada silenciosamente.

Após o congelamento da versão `v1.0`, qualquer nova alteração deverá ser
registrada neste arquivo antes de sua aplicação.