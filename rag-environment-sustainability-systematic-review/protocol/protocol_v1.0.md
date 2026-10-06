# Protocolo v1.0 — Revisão Sistemática sobre RAG em Domínios Ambientais e de Sustentabilidade

- Versão: `v1.0`
- Data de congelamento: `2026-10-06`
- Status: **CONGELADO**
- Revisora: `[NOME DA AUTORA]`

> Esta versão incorpora os resultados da busca piloto realizada na Scopus e no IEEE Xplore e da calibração intra-revisora dos critérios de elegibilidade.
>
> A partir desta versão, alterações metodológicas deverão ser registradas em `protocol/amendments.md`.

---

## 1. Título provisório

**Estratégias e Arquiteturas de Retrieval-Augmented Generation em Domínios Ambientais e de Sustentabilidade: uma Revisão Sistemática da Literatura**

O título poderá ser refinado na redação final do artigo, desde que permaneça consistente com o objeto principal da revisão — Retrieval-Augmented Generation (RAG) — e com o contexto de aplicação — domínios ambientais e de sustentabilidade ambiental.

---

## 2. Objetivo geral

Identificar e analisar as estratégias arquiteturais, técnicas de recuperação e métodos de avaliação empregados em sistemas Retrieval-Augmented Generation desenvolvidos para domínios ambientais e de sustentabilidade, investigando as evidências disponíveis sobre o impacto dessas escolhas no desempenho dos sistemas.

---

## 3. Definições operacionais

### 3.1 Retrieval-Augmented Generation (RAG)

Para fins desta revisão, considera-se Retrieval-Augmented Generation uma arquitetura ou pipeline em que informações provenientes de uma fonte externa de conhecimento são recuperadas e incorporadas ao contexto utilizado por um modelo generativo para produzir a saída final.

A definição exige, portanto, a presença conjunta de:

1. uma fonte externa ou base recuperável de conhecimento;
2. um mecanismo de recuperação;
3. uso da informação recuperada como contexto, evidência ou conhecimento para uma etapa generativa.

Não serão considerados RAG:

- LLMs utilizados sem recuperação externa;
- sistemas exclusivamente de Information Retrieval sem etapa generativa;
- semantic retrieval utilizado apenas como mecanismo independente, sem integração com a geração;
- sistemas em que a sigla `RAG` possui outro significado, como `Relation-Aware Graph`;
- sistemas em que não seja possível confirmar que a informação recuperada participa do processo generativo.

Quando essa integração não puder ser determinada pelo título e resumo, o registro deverá ser classificado como `maybe` e encaminhado para leitura de texto completo.

### 3.2 Domínios ambientais e de sustentabilidade

Neste estudo, são considerados domínios ambientais e de sustentabilidade aqueles em que questões ambientais, ecológicas, climáticas ou relacionadas à gestão sustentável de recursos naturais constituem parte central do problema investigado, dos dados utilizados ou da aplicação computacional desenvolvida.

A presença isolada de termos como `environment`, `environmental`, `sustainable`, `ESG` ou `SDG` não caracteriza automaticamente aderência ao domínio da revisão.

A dimensão ambiental deverá ser explícita e substantiva no problema, nos dados, na aplicação ou na avaliação do sistema.

---

## 4. Questões de pesquisa

### RQ1

**Quais arquiteturas e estratégias de RAG têm sido utilizadas em aplicações computacionais em domínios ambientais e de sustentabilidade?**

Dados esperados:

- tipo de RAG;
- organização do pipeline;
- GraphRAG;
- multimodalidade;
- componentes agênticos;
- modalidade dos dados;
- fontes externas de conhecimento;
- integração entre recuperação e geração.

### RQ2

**Quais técnicas são empregadas nas etapas de indexação, recuperação, pós-recuperação e geração desses sistemas?**

Dados esperados:

- preparação dos documentos;
- chunking;
- embeddings;
- sparse retrieval;
- dense retrieval;
- hybrid retrieval;
- top-k;
- filtros;
- query transformation;
- reranking;
- knowledge graphs;
- modelo generativo;
- prompting;
- estratégias de grounding.

### RQ3

**Como os sistemas RAG em domínios ambientais e de sustentabilidade são avaliados, considerando datasets, baselines e métricas?**

Dados esperados:

- corpus ou dataset;
- benchmark;
- baselines;
- métricas de retrieval;
- métricas de geração;
- métricas específicas de RAG;
- avaliação humana;
- LLM-as-a-Judge;
- avaliação de factualidade;
- avaliação de alucinação;
- avaliação de eficiência ou latência, quando aplicável.

### RQ4

**Quais evidências experimentais existem sobre os efeitos das diferentes configurações de RAG no desempenho dos sistemas?**

Dados esperados:

- RAG versus não-RAG;
- comparação entre configurações RAG;
- estudos de ablação;
- efeitos de diferentes métodos de recuperação;
- efeitos de diferentes fontes de conhecimento;
- efeitos de reranking, GraphRAG, agentes ou multimodalidade;
- ganhos;
- perdas;
- trade-offs;
- degradações de desempenho.

### 4.1 Regra de alinhamento entre RQs e dados

Todo campo utilizado durante a extração deverá contribuir para responder a pelo menos uma questão de pesquisa.

Campos sem relação direta com alguma RQ somente poderão ser incorporados mediante justificativa metodológica registrada.

---

## 5. Fontes de informação

### 5.1 Bases bibliográficas selecionadas

A busca sistemática será realizada nas seguintes bases:

- **Scopus**
- **IEEE Xplore**

A Scopus foi selecionada por sua cobertura multidisciplinar ampla.

O IEEE Xplore foi selecionado por sua cobertura especializada em computação, engenharia e tecnologias relacionadas ao objeto da revisão.

A cobertura obtida pelas buscas tradicionais será posteriormente complementada por uma rodada de:

- backward snowballing;
- forward snowballing.

A ACM Digital Library não integra a estratégia de busca da versão v1.0.

Qualquer alteração posterior nas bases utilizadas deverá ser registrada em `protocol/amendments.md`.

---

## 6. Período de publicação

Serão considerados estudos publicados entre:

**2020 e a data da execução da busca definitiva.**

O ano de 2020 foi adotado como ponto inicial por corresponder ao período de consolidação do paradigma moderno de Retrieval-Augmented Generation.

Para estudos classificados bibliograficamente com ano futuro, será considerada a data efetiva de publicação online.

Um registro somente poderá atender ao critério temporal se estiver efetivamente publicado e disponível até a data da busca definitiva.

---

## 7. Tipos de publicação e corpus principal

O corpus principal será composto por **estudos primários peer-reviewed**, publicados em:

- periódicos;
- anais de conferências.

Serão excluídos do corpus principal:

- surveys;
- revisões de literatura;
- revisões narrativas;
- tutoriais;
- editoriais;
- artigos de opinião;
- publicações puramente conceituais sem avaliação empírica.

Preprints não integrarão automaticamente a síntese principal.

Caso sejam utilizados posteriormente para análise complementar em razão da rápida evolução da área, deverão ser identificados separadamente e não poderão ser misturados ao corpus principal sem justificativa metodológica registrada.

---

## 8. Critérios de elegibilidade — versão v1.0

Os critérios abaixo foram refinados após busca piloto e calibração intra-revisora e encontram-se congelados nesta versão.

### 8.1 Critérios de inclusão

| Código | Critério de inclusão v1.0 |
|---|---|
| CI1 | Estudo primário que desenvolva, aplique ou avalie uma arquitetura ou configuração de Retrieval-Augmented Generation segundo a definição operacional adotada nesta revisão. |
| CI2 | Aplicação em domínio ambiental ou de sustentabilidade ambiental de forma explícita e substancial. |
| CI3 | O estudo fornece informação mínima sobre a arquitetura ou os componentes do sistema que permita identificar e classificar a configuração RAG utilizada. |
| CI4 | Presença de avaliação empírica do sistema RAG ou de algum de seus componentes. |
| CI5 | Texto completo disponível para avaliação final de elegibilidade e posterior extração de dados. |
| CI6 | Estudo peer-reviewed publicado entre 2020 e a data da busca definitiva, considerando a data efetiva de publicação online quando aplicável. |

Todos os critérios de inclusão aplicáveis deverão ser satisfeitos para a inclusão final do estudo.

### 8.2 Critérios de exclusão

| Código | Critério de exclusão v1.0 |
|---|---|
| CE1 | O estudo não atende à definição operacional de Retrieval-Augmented Generation. Inclui LLM sem recuperação externa, recuperação sem geração, semantic retrieval sem integração com a geração ou uso da sigla `RAG` com outro significado. |
| CE2 | RAG aplicado a domínio sem componente ambiental ou de sustentabilidade ambiental explícito e substancial. |
| CE3 | Estudo secundário ou publicação não primária, incluindo survey, revisão, tutorial, editorial ou artigo de opinião. |
| CE4 | Arquitetura, framework ou proposta sem avaliação empírica. Inclui estudos em que avaliação ou implantação são apresentadas apenas como trabalho futuro. |
| CE5 | Duplicata ou versão redundante do mesmo estudo. |
| CE6 | Texto integral indisponível para avaliação de elegibilidade. |
| CE7 | Informação técnica insuficiente, mesmo após leitura integral, para responder a pelo menos uma das RQs da revisão. |

---

## 9. Regras de fronteira — versão v1.0

As regras abaixo foram formalizadas a partir das ambiguidades identificadas durante a busca piloto e a calibração intra-revisora.

### 9.1 RAG utilizado apenas como baseline

Durante a triagem por título e resumo, estudos em que RAG aparecer apenas como baseline deverão ser classificados como `maybe` quando não houver informação suficiente para uma decisão segura.

Na leitura de texto completo, o estudo poderá ser incluído somente se:

- a configuração RAG for descrita com detalhe suficiente;
- houver resultados específicos do baseline RAG;
- esses resultados permitirem responder a pelo menos uma das RQs.

Caso contrário, excluir por `CE7`.

### 9.2 Energia, microgrids e baterias

A presença de termos relacionados a:

- energia;
- microgrids;
- baterias;
- eficiência energética;
- degradação de baterias;
- calor extremo;

não caracteriza automaticamente uma aplicação ambiental ou sustentável.

O estudo deverá apresentar como componente substantivo pelo menos uma dimensão como:

- sustentabilidade ambiental;
- clima;
- adaptação climática;
- mitigação climática;
- descarbonização;
- impacto ambiental;
- redução de emissões;
- gestão sustentável de recursos.

Eficiência operacional ou redução de custos isoladamente não são suficientes.

### 9.3 ESG e relatórios de sustentabilidade

A presença de ESG ou de relatórios de sustentabilidade não é suficiente para inclusão automática.

O estudo somente será considerado aderente ao domínio quando a dimensão **Environmental** for:

- explícita;
- substancial;
- separável das dimensões Social e Governance;
- relevante para a aplicação ou avaliação RAG.

Caso o resumo não permita essa determinação, classificar como `maybe` e verificar o texto completo.

### 9.4 Semantic retrieval

Recuperação semântica isolada não caracteriza Retrieval-Augmented Generation.

Para atender à definição operacional de RAG, a informação recuperada deverá ser incorporada como contexto, conhecimento ou evidência utilizada por um modelo generativo.

Se essa relação não puder ser determinada por título e resumo, o registro deverá ser classificado como `maybe` e encaminhado para leitura integral.

### 9.5 Environment e environmental em sentido operacional

O uso de `environment` ou `environmental` em sentidos como:

- ambiente computacional;
- ambiente virtual;
- ambiente robótico;
- ambiente industrial;
- cenário operacional;
- contexto de navegação;
- condições operacionais;

não caracteriza domínio ambiental para fins desta revisão.

Esses estudos deverão ser excluídos por `CE2` quando não existir outro componente ambiental ou de sustentabilidade ambiental substantivo.

### 9.6 Agricultura

Agricultura, por si só, não caracteriza automaticamente domínio ambiental.

Estudos agrícolas serão incluídos quando apresentarem dimensão ambiental substantiva, como:

- adaptação climática;
- conservação;
- uso sustentável de água;
- irrigação sustentável;
- emissões;
- uso sustentável de recursos;
- impacto ambiental;
- biodiversidade;
- práticas agrícolas ambientalmente sustentáveis.

Estudos voltados apenas ao controle operacional, produtividade, diagnóstico de plantas ou automação agrícola sem dimensão ambiental substantiva serão excluídos por `CE2`.

### 9.7 Ambiente construído

Estudos relacionados a edifícios ou construção serão incluídos quando apresentarem componente ambiental substantivo, como:

- impactos ambientais;
- avaliação de ciclo de vida;
- Environmental Product Declarations;
- carbono incorporado;
- descarbonização;
- eficiência de recursos;
- sustentabilidade de materiais;
- qualidade ambiental quando vinculada explicitamente à sustentabilidade.

Manutenção, segurança, navegação ou operação predial isoladas não caracterizam domínio ambiental.

### 9.8 Sensoriamento remoto e aplicações geoespaciais

O uso de sensoriamento remoto, imagens de satélite ou dados geoespaciais não caracteriza automaticamente domínio ambiental.

A tarefa efetivamente avaliada deverá possuir finalidade ambiental, climática, ecológica ou de sustentabilidade.

### 9.9 ODS / SDGs

A simples menção a Sustainable Development Goals não é suficiente para inclusão.

O estudo deverá possuir componente ambiental substantivo na aplicação RAG.

### 9.10 Ausência de avaliação empírica

Quando o artigo apresentar uma arquitetura ou framework e indicar avaliação, validação ou implantação apenas como trabalho futuro, deverá ser excluído por `CE4`.

### 9.11 Sigla RAG com outro significado

Estudos em que `RAG` signifique algo diferente de Retrieval-Augmented Generation deverão ser excluídos por `CE1`.

Exemplo:

`Relation-Aware Graph`.

---

## 10. Estratégia de busca — versão v1.0

As estratégias de busca foram refinadas durante o piloto e congeladas após a preservação dos estudos-semente indexados e a calibração dos critérios de elegibilidade.

A execução definitiva deverá ser realizada novamente após o congelamento deste protocolo.

Os números obtidos durante o piloto não serão considerados automaticamente os números da busca definitiva.

### 10.1 Scopus — string final v1.0

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

Esta string deriva da versão piloto `v0.1-T2`.

No piloto, a consulta recuperou:

- 472 registros;
- 11/11 estudos-semente confirmadamente indexados na Scopus;
- 0 `query_miss`.

Esses números possuem finalidade diagnóstica e não correspondem à busca definitiva.

### 10.2 IEEE Xplore — string final v1.0

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

Esta string deriva da versão piloto `v0.1-IEEE`.

No piloto, a consulta recuperou:

- 230 registros;
- 4/4 estudos-semente confirmadamente indexados no IEEE Xplore;
- 0 `query_miss`.

Os demais estudos-semente avaliados não foram encontrados por busca direta de título no IEEE Xplore e foram classificados como `not_indexed`.

Esses números possuem finalidade diagnóstica e não correspondem à busca definitiva.

### 10.3 Justificativa para remoção de `sustainab*`

Durante o piloto na Scopus, o termo `sustainab*` mostrou elevada capacidade de recuperar registros em que sustentabilidade era utilizada em sentido amplo, institucional, econômico ou operacional, sem componente ambiental substantivo.

A retirada do termo reduziu significativamente o volume de resultados sem causar perda dos estudos-semente confirmadamente indexados.

O conceito de sustentabilidade ambiental permanece contemplado operacionalmente pelos critérios de elegibilidade e pelos termos:

- `environmental`;
- `climat*`;
- `ecolog*`.

A alteração está registrada no histórico da estratégia de busca.

---

## 11. Validação da estratégia de busca

A estratégia foi avaliada utilizando estudos-semente conhecidos previamente.

A validação distinguiu:

- estudo indexado e recuperado;
- estudo indexado mas não recuperado (`query_miss`);
- estudo não indexado na base (`not_indexed`).

A taxa de recuperação dos estudos-semente foi utilizada somente como diagnóstico interno da estratégia.

Ela não é interpretada como estimativa formal de recall da revisão.

Também foram utilizadas amostras diagnósticas de registros recuperados para identificação de padrões de ruído.

Essas amostras foram de conveniência e não probabilísticas, portanto não serão utilizadas para estimativas formais de precisão.

---

## 12. Calibração intra-revisora

A revisão é conduzida por uma única revisora.

Antes da triagem formal, os critérios de elegibilidade v0.1 foram avaliados em um conjunto deliberadamente heterogêneo de 18 registros provenientes das buscas piloto.

Cada registro foi classificado em duas passagens independentes como:

- `include`;
- `exclude`;
- `maybe`.

As passagens foram realizadas em ordens diferentes.

Os registros incluíram:

- casos claramente aderentes;
- casos claramente não aderentes;
- casos de fronteira.

A finalidade da calibração foi avaliar a estabilidade de aplicação dos critérios, e não estimar a proporção de estudos relevantes na literatura.

### 12.1 Resultado da calibração

Dos 18 registros:

- 17 receberam a mesma decisão nas duas passagens;
- 1 apresentou mudança de decisão.

Concordância bruta intra-revisora:

**17/18 = 94,4%**

Proporção de mudança:

**1/18 = 5,6%**

Não foi calculado Cohen's kappa ou outra medida inter-revisor, pois existe apenas uma revisora.

A concordância bruta foi utilizada exclusivamente como indicador interno de estabilidade.

Como a proporção de mudanças foi inferior ao limite operacional de 20% previamente definido, não foi realizada uma terceira passagem.

### 12.2 Desacordo observado

O único desacordo ocorreu no registro:

**C13 — Bridging the Infrastructure Gap: An AI-Driven Framework for Automated Grant Matching in Environmentally Threatened Rural Communities**

- Passagem A: `maybe`
- Passagem B: `exclude — CE4`

Na segunda passagem foi observado que o estudo apresentava a arquitetura proposta, mas não apresentava avaliação empírica, descrevendo avaliação e implantação como trabalho futuro.

O caso foi resolvido como:

**CE4 — Proposta sem avaliação empírica.**

### 12.3 Resultado metodológico da calibração

A calibração indicou estabilidade suficiente dos critérios gerais, mas revelou necessidade de explicitar regras operacionais para:

- RAG utilizado como baseline;
- energia, microgrids e baterias;
- ESG;
- semantic retrieval;
- usos não ambientais de `environment/environmental`;
- agricultura;
- ambiente construído;
- propostas sem avaliação empírica;
- usos alternativos da sigla RAG.

Essas regras foram incorporadas à Seção 9 deste protocolo.

Os dados completos da calibração estão registrados em:

`screening/calibration_day3.csv`

O relatório metodológico da calibração está registrado em:

`screening/calibration_day3.md`

---

## 13. Processo de seleção dos estudos

A seleção será realizada em etapas.

### 13.1 Exportação

Os resultados definitivos serão exportados separadamente de cada base.

Os arquivos brutos deverão ser preservados sem edição.

### 13.2 Deduplicação

Após a consolidação das exportações, serão identificados registros duplicados utilizando, quando disponíveis:

- DOI;
- título;
- autores;
- ano;
- outros metadados bibliográficos.

Quando houver múltiplas versões do mesmo estudo, será preservada a versão considerada principal de acordo com a política de deduplicação adotada.

Duplicatas removidas serão registradas como `CE5` quando necessário para rastreabilidade.

### 13.3 Triagem por título e resumo

Cada registro será classificado como:

- `include`;
- `exclude`;
- `maybe`.

Na etapa de título e resumo:

- casos claramente inelegíveis poderão ser excluídos;
- casos claramente elegíveis avançarão;
- casos ambíguos deverão ser classificados como `maybe` e seguir para texto completo.

O princípio adotado será:

**na dúvida, não excluir apenas por inferência.**

O campo `reason_code` poderá permanecer vazio para registros `maybe`.

### 13.4 Leitura de texto completo

Os estudos classificados como `include` ou `maybe` quando necessária confirmação serão avaliados em texto completo.

Na etapa de texto completo:

- toda exclusão deverá possuir exatamente um código principal `CE1–CE7`;
- informações adicionais poderão ser registradas no campo `notes`.

### 13.5 Avaliação de qualidade

Após a seleção por texto completo, os estudos incluídos serão submetidos à avaliação de qualidade definida no diretório:

`quality/`

A avaliação de qualidade não substituirá os critérios de elegibilidade.

### 13.6 Snowballing

Após a definição do conjunto proveniente das buscas tradicionais, será realizada uma rodada de:

- backward snowballing;
- forward snowballing.

Os estudos identificados por snowballing serão submetidos aos mesmos critérios `CI1–CI6` e `CE1–CE7`.

A origem desses registros deverá ser documentada.

---

## 14. Uso dos códigos de exclusão

Os códigos `CE1–CE7` constituem o conjunto oficial de motivos de exclusão da versão v1.0.

Na etapa de título e resumo, o código poderá permanecer vazio para casos `maybe`.

Na leitura de texto completo, toda exclusão deverá possuir exatamente um código principal.

Quando mais de um critério puder ser aplicado, deverá ser registrado o motivo principal responsável pela exclusão.

Os detalhes operacionais são mantidos em:

`screening/exclusion_codes.md`

---

## 15. Rastreabilidade

Os seguintes arquivos constituem parte da trilha de auditoria da revisão:

```text
protocol/
    protocol_v0.1.md
    protocol_v1.0.md
    amendments.md

search/
    search_strings.md
    search_log.csv
    pilot_validation.csv
    pilot_noise_sample.csv
    pilot_notes.md
    exports/

screening/
    calibration_day3.csv
    calibration_day3.md
    decision_log.csv
    exclusion_codes.md

extraction/
    data_dictionary.md

quality/
    quality_assessment.csv
```

As decisões metodológicas não deverão ser sobrescritas silenciosamente.

Alterações após o congelamento da versão v1.0 deverão ser registradas em:

`protocol/amendments.md`

---

## 16. Regras de registro

Durante todas as etapas:

- strings executadas deverão ser preservadas literalmente;
- data da busca deverá ser registrada;
- número de resultados deverá ser registrado;
- arquivos exportados das bases deverão ser mantidos sem alteração;
- registros não deverão ser excluídos silenciosamente;
- exclusões de texto completo deverão possuir código CE;
- dados ausentes nos artigos não deverão ser inferidos;
- quando uma informação não for reportada, deverá ser utilizado `NR` (`Not Reported`);
- decisões metodológicas posteriores deverão ser registradas no histórico de alterações.

---

## 17. Estratégia de extração

Os dados dos estudos incluídos serão extraídos utilizando o dicionário definido em:

`extraction/data_dictionary.md`

Os campos deverão permanecer alinhados às RQs.

A extração deverá contemplar, quando reportado:

- identificação do estudo;
- domínio ambiental;
- objetivo da aplicação;
- tipo de RAG;
- fonte de conhecimento;
- preparação e chunking;
- embeddings;
- armazenamento/indexação;
- estratégia de recuperação;
- top-k;
- reranking;
- query transformation;
- GraphRAG;
- agentes;
- multimodalidade;
- LLM utilizado;
- estratégia de geração;
- dataset/corpus;
- baselines;
- métricas;
- resultados;
- estudos de ablação;
- efeitos experimentais das configurações;
- limitações reportadas.

Campos não reportados deverão receber `NR`.

---

## 18. Avaliação de qualidade

Os estudos incluídos serão avaliados por uma ficha de qualidade específica.

A avaliação deverá considerar, no mínimo:

- clareza do objetivo;
- descrição suficiente da arquitetura RAG;
- clareza da origem e preparação dos dados;
- adequação da avaliação experimental;
- clareza das métricas e baselines;
- reprodutibilidade ou detalhamento metodológico suficiente.

A ficha operacional deverá ser mantida em:

`quality/quality_assessment.csv`

A avaliação de qualidade será utilizada para contextualizar a força das evidências e não como substituto automático dos critérios de inclusão e exclusão.

---

## 19. Síntese dos resultados

A síntese deverá ser conduzida de forma alinhada às RQs.

Para RQ1 e RQ2 serão priorizadas sínteses descritivas e taxonômicas das arquiteturas e técnicas utilizadas.

Para RQ3 serão sintetizados:

- datasets;
- baselines;
- métricas;
- estratégias de avaliação.

Para RQ4 serão priorizadas evidências comparativas, como:

- RAG versus não-RAG;
- comparações entre arquiteturas;
- estudos de ablação;
- efeitos de diferentes componentes;
- ganhos;
- perdas;
- trade-offs.

Resultados heterogêneos não serão agregados quantitativamente sem justificativa metodológica.

---

## 20. Alterações da versão v0.1 para v1.0

As principais alterações incorporadas nesta versão incluem:

- definição das bases finais como Scopus e IEEE Xplore;
- exclusão da ACM Digital Library da estratégia definitiva;
- refinamento da string ambiental;
- retirada de `sustainab*` da busca candidata da Scopus;
- congelamento das strings finais de busca;
- realização da calibração intra-revisora;
- refinamento de `CI1–CI6` e `CE1–CE7`;
- ampliação de `CE1` para contemplar usos da sigla RAG que não representam Retrieval-Augmented Generation;
- inclusão de regras operacionais de fronteira;
- definição explícita de como tratar RAG utilizado como baseline;
- definição explícita de como tratar ESG, agricultura, energia e usos operacionais de `environment/environmental`;
- formalização da regra de `semantic retrieval`;
- formalização da exclusão de propostas sem avaliação empírica.

O histórico detalhado das alterações deverá ser mantido em:

`protocol/amendments.md`

---

## 21. Gate metodológico da versão v1.0

A versão v1.0 é considerada congelada quando estiverem concluídos:

- [x] definição operacional de RAG;
- [x] definição operacional do domínio ambiental;
- [x] RQ1–RQ4;
- [x] bases finais definidas;
- [x] busca piloto concluída;
- [x] estudos-semente avaliados;
- [x] strings candidatas calibradas;
- [x] calibração intra-revisora concluída;
- [x] critérios CI/CE estabilizados;
- [x] regras de fronteira formalizadas;
- [x] protocolo v1.0 criado;
- [x] `amendments.md` atualizado;
- [x] `exclusion_codes.md` atualizado para v1.0;
- [x] `search_strings.md` marcado com strings finais v1.0;
- [x] `data_dictionary.md` revisado;
- [x] ficha de qualidade criada.

A busca definitiva somente deverá ser executada após a conclusão dos itens documentais restantes deste gate.

---

## 22. Próxima etapa

Após o fechamento documental da versão v1.0:

1. executar novamente a busca definitiva na Scopus;
2. executar novamente a busca definitiva no IEEE Xplore;
3. registrar data, string literal, filtros e quantidade de resultados;
4. exportar os resultados brutos;
5. preservar os arquivos originais;
6. consolidar os registros;
7. realizar deduplicação;
8. iniciar a triagem formal por título e resumo.

Os resultados obtidos durante a fase piloto não deverão ser reutilizados automaticamente como resultados definitivos da revisão.
