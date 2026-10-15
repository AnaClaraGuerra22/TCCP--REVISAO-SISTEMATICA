# Resolução de Divergências — Dia 9

**Projeto:** Revisão Sistemática sobre Retrieval-Augmented Generation (RAG) em Domínios Ambientais e de Sustentabilidade  
**Data:** 2026-10-15  
**Protocolo de referência:** `protocol_v1.0.md`  
**Etapa:** Triagem por título e resumo (*Title/Abstract Screening*)

---

## 1. Objetivo

Este documento registra a resolução de divergências identificadas durante a calibração da triagem de títulos e resumos, garantindo rastreabilidade, consistência metodológica e reprodutibilidade das decisões.

As divergências são resolvidas mediante reavaliação das evidências disponíveis e aplicação dos critérios de inclusão e exclusão previamente definidos no protocolo v1.0.

Os resultados originais da calibração são preservados, sem alterações retroativas.

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
**Responsável:** Revisora humana responsável pela triagem

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

## 3. Resultado da resolução

A divergência referente ao R0141 foi encerrada com a decisão final `exclude`, fundamentada no critério CE4.

A resolução foi realizada sem modificar os critérios de elegibilidade previamente estabelecidos e sem necessidade de alteração do protocolo v1.0.

**Observação metodológica:** A decisão foi tomada na etapa de triagem por título e resumo, com base nas evidências disponíveis nessa etapa. Não representa uma avaliação independente do texto completo.

---

**Status da divergência R0141:** RESOLVIDA