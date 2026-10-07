# Calibração intra-revisora dos critérios de elegibilidade

**Projeto:** Revisão Sistemática — RAG em Domínios Ambientais e de Sustentabilidade  
**Etapa:** Dia 3 — calibração dos critérios de inclusão e exclusão  
**Status:** concluída  
**Versão dos critérios testados:** v0.1  
**Revisora:** única revisora

---

## 1. Objetivo

A calibração teve como objetivo avaliar a consistência de aplicação dos
critérios preliminares de inclusão e exclusão antes do início da triagem
formal da revisão sistemática.

Esta etapa não corresponde à seleção formal dos estudos.

O objetivo foi identificar:

- critérios suficientemente claros;
- situações de fronteira;
- ambiguidades recorrentes;
- necessidade de refinamento das regras operacionais antes do
  congelamento do protocolo v1.0.

---

## 2. Conjunto de calibração

Foram utilizados 18 registros provenientes das amostras diagnósticas
das buscas piloto realizadas na Scopus e no IEEE Xplore.

A amostra foi deliberadamente heterogênea e incluiu:

- estudos claramente aderentes ao escopo;
- estudos claramente não aderentes;
- casos de fronteira.

A finalidade desta amostra não foi estimar a prevalência de estudos
relevantes na literatura, mas testar a aplicabilidade dos critérios de
elegibilidade.

Os registros e todas as decisões estão documentados em:

`screening/calibration_day3.csv`

---

## 3. Procedimento

Cada um dos 18 registros foi avaliado em duas passagens independentes.

### Passagem A

A decisão foi realizada utilizando título e resumo e os critérios
CI1-CI6 e CE1-CE7 da versão v0.1 do protocolo.

As decisões possíveis foram:

- `include`
- `exclude`
- `maybe`

Também foram registrados:

- critério principal;
- confiança da decisão;
- necessidade de texto completo;
- justificativa.

### Passagem B

Os mesmos 18 registros foram avaliados novamente em ordem diferente.

As decisões da Passagem A não foram utilizadas durante a
reclassificação.

Após a conclusão das duas passagens, as decisões foram comparadas.

---

## 4. Resultado da Passagem A

Distribuição das decisões:

| Decisão | n |
|---|---:|
| Include | 6 |
| Exclude | 7 |
| Maybe | 5 |
| Total | 18 |

---

## 5. Comparação entre Passagem A e Passagem B

Dos 18 registros avaliados:

- 17 receberam a mesma decisão nas duas passagens;
- 1 apresentou mudança de decisão.

Concordância bruta intra-revisora:

**17/18 = 94,4%**

Proporção de decisões alteradas:

**1/18 = 5,6%**

Não foi calculado coeficiente de concordância inter-revisor, pois a
revisão é conduzida por uma única revisora.

A concordância bruta foi utilizada apenas como indicador interno de
estabilidade dos critérios.

Como a proporção de mudanças foi inferior ao limite operacional de 20%
estabelecido para a calibração, não foi considerada necessária uma
terceira passagem.

---

## 6. Desacordo identificado

### C13 — IEEEP05

**Título:**  
*Bridging the Infrastructure Gap: An AI-Driven Framework for Automated
Grant Matching in Environmentally Threatened Rural Communities*

**Passagem A:** `maybe`

A dúvida inicial estava relacionada à centralidade da dimensão
ambiental na aplicação.

**Passagem B:** `exclude — CE4`

Durante a segunda avaliação foi observado que o resumo apresenta uma
arquitetura proposta, mas não relata experimento, métricas ou avaliação
empírica e descreve avaliação e implantação como trabalho futuro.

### Resolução

O registro é excluído por:

**CE4 — Proposta sem avaliação empírica.**

O caso mostrou que a ausência explícita de avaliação empírica pode ser
suficiente para decisão de exclusão mesmo quando a aderência temática
ao domínio permanece parcialmente ambígua.

---

## 7. Casos que permaneceram como `maybe`

Quatro registros permaneceram como `maybe` nas duas passagens:

### C04 — DraftNEPABench

RAG é utilizado como baseline comparativo.

Questão de fronteira:

> Um estudo em que RAG não é a abordagem principal deve ser incluído?

A decisão dependerá da quantidade de informação disponível sobre a
configuração e os resultados do baseline RAG.

---

### C07 — Microgrid Battery Dispatch Under Extreme Heat

O estudo envolve microgrids, baterias e calor extremo, mas o resumo
enfatiza custo, degradação e operação.

Questão de fronteira:

> Energia e condições climáticas são suficientes para caracterizar uma
> aplicação como ambiental/sustentável?

Será necessário verificar se clima, sustentabilidade ambiental,
descarbonização ou gestão sustentável de recursos são objetivos
substantivos da aplicação.

---

### C10 — Sustainability Reports / ESG

O estudo utiliza RAG sobre relatórios de sustentabilidade, mas aborda
ESG de maneira ampla.

Questão de fronteira:

> A presença de ESG é suficiente para inclusão?

Será necessário verificar se a dimensão Environmental é explícita,
substancial e separável das dimensões Social e Governance.

---

### C16 — SMTRec

O sistema possui LLMs e semantic retrieval, além de avaliação de
impacto ambiental.

Questão de fronteira:

> Semantic retrieval integrado a um sistema generativo caracteriza RAG?

Será necessário verificar se a informação recuperada é efetivamente
incorporada ao contexto utilizado pelo modelo generativo.

---

## 8. Ambiguidades identificadas durante a calibração

A calibração mostrou necessidade de regras operacionais explícitas para:

1. RAG utilizado apenas como baseline;
2. aplicações em energia, microgrids e baterias;
3. ESG e relatórios de sustentabilidade;
4. semantic retrieval versus Retrieval-Augmented Generation;
5. uso de `environment` e `environmental` em sentido operacional;
6. agricultura sem componente ambiental explícito;
7. estudos que apresentam arquitetura mas deixam avaliação para
   trabalhos futuros;
8. usos da sigla RAG com significado diferente de
   Retrieval-Augmented Generation.

Esses pontos deverão ser incorporados às regras de fronteira da
versão v1.0 do protocolo.

---

## 9. Conclusão da calibração

A calibração indicou alta estabilidade na aplicação dos critérios
preliminares:

**94,4% de concordância entre as duas passagens.**

Os critérios gerais mostraram-se suficientemente estáveis para avanço
do protocolo, mas foram identificadas situações de fronteira que
necessitam de redação operacional mais explícita.

A próxima etapa é:

1. resolver formalmente as regras de fronteira;
2. revisar CI1-CI6 e CE1-CE7;
3. registrar as alterações em `protocol/amendments.md`;
4. criar e congelar `protocol/protocol_v1.0.md`;
5. atualizar `screening/exclusion_codes.md`;
6. confirmar as strings de busca como versão final;
7. somente então executar a busca definitiva.