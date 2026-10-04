# Revisão Sistemática - RAG em Domínios Ambientais e de Sustentabilidade

## Objetivo do repositório

Este repositório organiza, versiona e documenta todos os artefatos metodológicos da revisão sistemática sobre estratégias e arquiteturas de Retrieval-Augmented Generation (RAG) em domínios ambientais e de sustentabilidade.

O objetivo é garantir rastreabilidade, auditabilidade e reprodutibilidade desde a definição do protocolo até a seleção, extração, avaliação e síntese dos estudos.

## Estado atual

- Fase: Dia 1 - definição do protocolo
- Versão atual do protocolo: `v0.1`
- Status: preliminar; ainda sujeito à busca piloto e à calibração intra-revisora
- Busca definitiva executada: não
- Corpus final definido: não

## Escopo resumido

- Objeto de estudo: Retrieval-Augmented Generation (RAG)
- Perspectiva: Ciência da Computação, com foco técnico em arquiteturas e componentes
- Contexto de aplicação: domínios ambientais e de sustentabilidade
- Foco analítico: arquitetura, retrieval, pós-retrieval, geração, avaliação e evidência experimental
- Revisora: uma única autora
- Prazo operacional: 30 dias

## Convenção de nomes

1. Arquivos metodológicos versionados usam o padrão `nome_vX.Y.ext`.
2. Versões `v0.x` são preliminares e podem ser alteradas durante a calibração.
3. A versão `v1.0` será congelada após a busca piloto e a calibração dos critérios.
4. Arquivos brutos exportados das bases nunca devem ser sobrescritos.
5. Estudos recebem identificadores estáveis no formato `S001`, `S002`, `S003`, ...
6. Dados ausentes ou não informados pelos estudos devem ser registrados como `NR` (`Not Reported`), nunca inferidos.
7. Datas devem ser registradas no formato ISO `AAAA-MM-DD`; quando necessário, usar `AAAA-MM-DD HH:MM`.

## Responsável

- Responsável pela revisão: Ana Clara Guerra 

## Estrutura do repositório

```text
rag-environment-sustainability-systematic-review/
├── README.md
├── protocol/
│   ├── protocol_v0.1.md
│   └── amendments.md
├── search/
│   ├── search_strings.md
│   ├── search_log.csv
│   └── exports/
├── screening/
│   ├── decision_log.csv
│   └── exclusion_codes.md
├── extraction/
│   └── data_dictionary.md
├── quality/
└── figures/
```

## Regra central de rastreabilidade

Nenhuma alteração metodológica posterior ao congelamento do protocolo `v1.0` poderá ser feita silenciosamente. Toda mudança deverá ser registrada em `protocol/amendments.md`, com data, versão, justificativa e impacto esperado.
