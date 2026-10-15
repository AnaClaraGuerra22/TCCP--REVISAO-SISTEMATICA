# Resolução de divergências — Dia 9

**Projeto:** Revisão Sistemática sobre Retrieval-Augmented Generation (RAG) em Domínios Ambientais e de Sustentabilidade  
**Data:** 2026-10-15  
**Etapa:** Triagem por título e resumo (`title_abstract`)  
**Protocolo congelado:** `protocol/protocol_v1.0.md` (sem alterações)  
**Responsável:** Ana Clara Guerra (revisora única; triagem com apoio de IA)

## 1. Objetivo e procedimento

Registrar, em um único documento, a resolução de **12 divergências**: **uma** identificada na calibração (R0141) e **11** na comparação do piloto com o Qwen (10 divergências de decisão e uma divergência apenas no código de exclusão, R0280).

As decisões foram reavaliadas a partir dos títulos e resumos e dos critérios congelados na versão v1.0. O Qwen e o ChatGPT atuaram como ferramentas de apoio, **não como revisores humanos independentes**. A documentação histórica da calibração, as decisões originais do piloto e as saídas do Qwen devem permanecer inalteradas. Uma decisão `maybe` nesta etapa significa encaminhamento ao texto completo, não inclusão definitiva.

## 2. Divergência resolvida — R0141

**Identificador:** R0141  
**Título:** Bridging the Infrastructure Gap: An AI-Driven Framework for Automated Grant Matching in Environmentally Threatened Rural Communities  
**Autor:** Desai A.  
**Ano:** 2026  
**Fonte:** Scopus  
**DOI:** 10.1109/CAI68641.2026.11536366  
**Identificador na calibração:** C13

### 2.1. Histórico da divergência

Durante a calibração, foram registradas duas classificações distintas:

| Avaliação | Decisão | Critério |
|---|---|---|
| Rodada A | `maybe` | Necessidade de verificação adicional |
| Rodada B | `exclude` | CE4 |

A divergência decorreu da interpretação das evidências disponíveis sobre a implementação e, principalmente, a avaliação empírica da arquitetura proposta.

### 2.2. Reavaliação do resumo

O estudo apresenta uma arquitetura híbrida que combina recuperação por palavras-chave e Retrieval-Augmented Generation (RAG) para associar necessidades de infraestrutura de comunidades rurais ambientalmente vulneráveis a oportunidades de financiamento federal.

A arquitetura utiliza documentos de planejamento comunitário, relatórios de mitigação de riscos, embeddings e informações recuperadas por meio da API Grants.gov.

Embora a aplicação apresente potencial relevância ambiental, o resumo não relata experimentos, métricas quantitativas ou resultados de avaliação empírica do sistema RAG.

Além disso, os autores indicam explicitamente que o trabalho fornece uma base para avaliação e implantação futuras:

> "provides a foundation for future evaluation and deployment."

Portanto, considerando as evidências apresentadas no resumo, não foi possível identificar uma avaliação empírica concluída que atendesse aos requisitos do protocolo.

### 2.3. Decisão final

**Decisão:** `exclude`  
**Critério principal:** `CE4` — Ausência de avaliação empírica demonstrada  
**Status:** Divergência resolvida  
**Data da resolução:** 2026-10-15  
**Responsável:** Ana Clara Guerra (revisora única)

**Justificativa final:**

Estudo que propõe uma arquitetura híbrida de recuperação por palavras-chave e RAG para identificar oportunidades de financiamento de infraestrutura em comunidades rurais ambientalmente vulneráveis. Embora apresente potencial relevância para adaptação climática e descreva componentes técnicos da arquitetura, o resumo não relata avaliação empírica, métricas ou resultados experimentais do sistema. Os autores indicam explicitamente a avaliação e a implantação como trabalhos futuros. Portanto, o estudo é excluído pelo critério CE4, conforme o protocolo v1.0.

### 2.4. Registro e rastreabilidade

A decisão final foi estabelecida após reavaliação do resumo e aplicação dos critérios previamente definidos.

- **Registro oficial:** `screening/decision_log.csv`
- **Registro afetado:** R0141
- **Decisão registrada:** `exclude`
- **Código de exclusão:** `CE4`
- **Protocolo utilizado:** v1.0
- **Alteração nos critérios do protocolo:** Nenhuma
- **Alteração nos resultados históricos da calibração:** Nenhuma

A classificação final não substitui nem modifica os registros originais das rodadas A e B, preservando o histórico da divergência para auditoria e reprodução da triagem.

## 3. Resolução das divergências do piloto — 11 registros

**Método:** reanálise das 11 divergências entre as decisões registradas no piloto e as sugestões do Qwen, considerando o protocolo v1.0 e preservando as classificações originais.

**Resultado:** 9 `exclude` e 2 `maybe`. As decisões finais coincidem com as decisões originalmente registradas no piloto; o que foi complementado são as justificativas e o registro de confirmação.

### 3.1. Comparação das classificações

| ID | Decisão inicial | Sugestão Qwen | Decisão final | CE final |
|---|---|---|---|---|
| R0403 | `exclude` | `include` | `exclude` | CE2 |
| R0144 | `exclude` | `maybe` | `exclude` | CE2 |
| R0316 | `exclude` | `maybe` | `exclude` | CE2 |
| R0085 | `maybe` | `include` | `maybe` | — |
| R0360 | `exclude` | `maybe` | `exclude` | CE2 |
| R0263 | `exclude` | `maybe` | `exclude` | CE2 |
| R0225 | `exclude` | `include` | `exclude` | CE2 |
| R0105 | `maybe` | `include` | `maybe` | — |
| R0069 | `exclude` | `maybe` | `exclude` | CE2 |
| R0037 | `exclude` | `maybe` | `exclude` | CE2 |
| R0280 | `exclude` | `exclude` | `exclude` | CE1 |

### 3.2. Justificativas finais por registro

#### R0403 — `exclude` / CE2

Estudo primário com implementação explícita de RAG e avaliação empírica em um sistema IoT para monitoramento e controle do cultivo de Sacha Inchi. Embora utilize sensores de umidade do solo e permita controlar irrigação e fertilização, o objetivo principal está na eficiência operacional e produtividade agrícola. O resumo não demonstra finalidade ambiental substantiva, como conservação hídrica, redução do uso de fertilizantes ou mitigação de impactos ecológicos. Portanto, enquadra-se no critério CE2, conforme o protocolo v1.0.

#### R0144 — `exclude` / CE2

Estudo que apresenta a integração de RAG e modelos generativos em uma plataforma de gestão e manutenção de ativos de sistemas elétricos. Embora mencione mudanças climáticas, energias renováveis e políticas de baixo carbono na contextualização, a aplicação concentra-se na confiabilidade dos equipamentos, redução de custos de manutenção e estabilidade da rede. Não demonstra finalidade ambiental substantiva, como mitigação climática, redução de emissões ou gestão sustentável de recursos. Portanto, enquadra-se no critério CE2, conforme o protocolo v1.0.

#### R0316 — `exclude` / CE2

Estudo primário com implementação explícita de RAG, integrado a grafos de conhecimento e modelos de linguagem para tomada de decisão de múltiplos robôs subaquáticos, com avaliação empírica e estudos de ablação. Embora mencione monitoramento ambiental como possível aplicação, o objetivo e os resultados apresentados concentram-se na autonomia robótica, interação humano-robô e confiabilidade das decisões. As condições ambientais descritas referem-se principalmente ao contexto operacional subaquático, sem demonstração de uma aplicação ecológica, climática ou de sustentabilidade ambiental substantiva. Portanto, enquadra-se no critério CE2, conforme o protocolo v1.0.

#### R0085 — `maybe`

Estudo primário que propõe um framework de apoio à decisão agrícola baseado em grafos de conhecimento causais e GraphRAG, incorporando explicitamente riscos ecológicos, variabilidade climática e restrições de recursos. A dimensão ambiental apresenta relevância substantiva, especialmente para adaptação climática e manejo sustentável. Entretanto, embora apresente uma prova de conceito implementada em aplicativo móvel, o resumo não descreve experimentos, métricas ou procedimentos suficientes para confirmar a avaliação empírica do sistema RAG. Recomenda-se verificar o texto completo, principalmente quanto à integração operacional do GraphRAG e à existência de validação empírica, conforme os critérios CE1 e CE4.

#### R0360 — `exclude` / CE2

Estudo primário que combina uma CNN para detecção de doenças vegetais com um chatbot RAG baseado em LLaMA-2 e FAISS para fornecer orientações sobre tratamento e cuidados com plantas. Embora mencione mudanças climáticas como fator associado à ocorrência de doenças, a aplicação concentra-se no diagnóstico e manejo fitossanitário, sem demonstrar finalidade ambiental substantiva, como adaptação climática, redução de agrotóxicos ou conservação de recursos naturais. Os resultados quantitativos apresentados referem-se principalmente ao módulo CNN, sem avaliação específica suficientemente detalhada do RAG. Portanto, recomenda-se a exclusão pelo critério CE2, conforme o protocolo v1.0.

#### R0263 — `exclude` / CE2

Estudo primário com utilização declarada de RAG, modelos de linguagem e Digital Twins para reconstrução de dados de telemetria e detecção de falhas em redes de comunicação veicular V2X, apresentando avaliação empírica. Embora mencione environmental priors, o termo refere-se às condições operacionais utilizadas para orientar a recuperação dos dados, não a questões ecológicas ou climáticas. A aplicação concentra-se na confiabilidade das comunicações e na estabilidade dos sistemas de transporte inteligente, sem demonstrar finalidade ambiental substantiva. Portanto, recomenda-se a exclusão pelo critério CE2, conforme o protocolo v1.0.

#### R0225 — `exclude` / CE2

Estudo primário com implementação explícita de RAG, integrado a modelos de linguagem, detecção visual de pragas e sensores IoT para geração de recomendações de manejo agrícola. Apresenta avaliação empírica com métricas quantitativas, incluindo 68,7% de F1-score na extração de conhecimento e 77,33% de acurácia na geração de recomendações. Entretanto, o objetivo central é melhorar o controle de pragas e reduzir perdas de produtividade. Embora utilize dados ambientais e práticas de agricultura de precisão, o resumo não demonstra finalidade ambiental substantiva, como redução do uso de pesticidas, conservação da biodiversidade ou mitigação de impactos ecológicos. Portanto, recomenda-se a exclusão pelo critério CE2, conforme o protocolo v1.0.

#### R0105 — `maybe`

Estudo primário que apresenta um sistema multiagente com RAG para análise geoespacial e monitoramento das monções indianas, integrando dados de precipitação, umidade do solo e saúde da vegetação. A aplicação possui relevância ambiental e climática substantiva, especialmente para monitoramento ambiental e planejamento de desastres. Entretanto, embora descreva uma arquitetura com recuperação contextual e modelos de linguagem, o resumo não detalha suficientemente a integração operacional do RAG nem apresenta resultados de avaliação empírica do sistema. Recomenda-se verificar o texto completo pelos critérios CE1 e CE4, conforme o protocolo v1.0.

#### R0069 — `exclude` / CE2

Estudo primário com implementação de Vector-Graph RAG e modelos de linguagem para consultas e controle adaptativo de ambientes internos de edifícios, apresentando avaliação empírica em um escritório operacional. Embora utilize o termo environmental management, a aplicação concentra-se na integração de dados prediais, interpretação das preferências dos ocupantes e melhoria da precisão das consultas. O resumo não demonstra finalidade ambiental substantiva, como eficiência energética com objetivo de conservação de recursos, redução de emissões ou mitigação de impactos ecológicos. Portanto, recomenda-se a exclusão pelo critério CE2, conforme o protocolo v1.0.

#### R0037 — `exclude` / CE2

Estudo primário com implementação de RAG multimodal integrado a modelos de linguagem e mecanismos de raciocínio para apoiar decisões de direção autônoma, apresentando avaliação empírica em múltiplos conjuntos de dados. Embora utilize atributos ambientais, estes correspondem às condições operacionais do cenário de direção e não a questões ecológicas ou climáticas. A aplicação concentra-se na segurança veicular, precisão das decisões e prevenção de comportamentos inadequados, sem demonstrar finalidade ambiental substantiva, como redução de emissões, eficiência energética ou mobilidade sustentável. Portanto, recomenda-se a exclusão pelo critério CE2, conforme o protocolo v1.0.

#### R0280 — `exclude` / CE1

Estudo de caráter predominantemente exploratório, baseado em revisão da literatura sobre a integração de modelos de linguagem e técnicas de otimização combinatória para problemas de roteamento. Embora mencione RAG e o potencial de apoio à mobilidade sustentável, a recuperação aumentada é apresentada apenas como possibilidade de aplicação, sem implementação operacional demonstrada ou avaliação empírica específica. Além disso, o trabalho não apresenta uma aplicação ambiental substantiva efetivamente investigada. Portanto, recomenda-se a exclusão pelo critério principal CE1, conforme a definição operacional de RAG estabelecida no protocolo v1.0.

## 4. Consolidação, rastreabilidade e integridade

- **R0141:** `exclude` / CE4, após divergência de calibração entre `maybe` e `exclude` / CE4.
- **Piloto:** 11 divergências resolvidas (9 `exclude` e 2 `maybe`); R0280 teve divergência somente no código CE.
- **Contagem consolidada de títulos e resumos:** 587 registros únicos — 118 `include`, 118 `maybe`, 351 `exclude`. A resolução não alterou esses totais.
- **Arquivo de decisões do Dia 9:** `screening/day9/decision_log_dia9_APOS_DIVERGENCIAS_587.csv`. Este arquivo foi preparado como cópia consolidada; o registro oficial é `screening/decision_log.csv`, após backup e substituição/conferência.
- **Evidência das decisões do piloto:** `screening/day9/divergencias_piloto_dia9_11_registros.xlsm` (manter os campos originais e as sugestões do Qwen).
- **Documentação da calibração:** preservar arquivos originais em `screening/`, incluindo os registros das rodadas A e B.
- **Datas:** a resolução do R0141 e as 11 resoluções do piloto foram registradas como 2026-10-15; não preencher retrospectivamente datas desconhecidas de outros registros.
- **Protocolo:** nenhuma alteração nos critérios de inclusão ou exclusão da versão v1.0; portanto, não há emenda de protocolo por causa dessas resoluções.
- **Próxima etapa:** os registros `include` e `maybe` avançam para verificação do texto completo, quando se decidirá a elegibilidade definitiva.

**Status das 12 divergências documentadas:** RESOLVIDAS na triagem por título e resumo.
