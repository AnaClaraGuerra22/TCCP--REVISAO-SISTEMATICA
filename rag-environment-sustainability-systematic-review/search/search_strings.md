# Estratégia de Busca - Rascunho v0.1

- Versão: `v0.1`
- Data: `2026-10-04`
- Status: **RASCUNHO - NÃO É BUSCA DEFINITIVA**
- Execução definitiva realizada: **não**

## Objetivo da versão v0.1

Construir uma string piloto que combine termos relacionados a Retrieval-Augmented Generation com termos relacionados aos domínios ambientais e de sustentabilidade.

Esta versão deverá ser validada nos Dias 2-3 utilizando estudos conhecidos e claramente relevantes. Se estudos esperados não forem recuperados, os termos poderão ser ajustados antes do congelamento da versão `v1.0`.

## Bloco A - RAG

Termos candidatos:

```text
"retrieval augmented generation"
OR "retrieval-augmented generation"
OR "retrieval enhanced generation"
OR "retrieval-enhanced generation"
OR "GraphRAG"
OR "graph RAG"
OR "agentic RAG"
OR "multimodal RAG"
```

## Bloco B - Domínio ambiental e de sustentabilidade

Termos candidatos iniciais definidos no protocolo:

```text
environment*
OR sustainab*
OR climat*
OR ecolog*
```

## String conceitual v0.1

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
)
AND
(
    environment*
    OR sustainab*
    OR climat*
    OR ecolog*
)
```

## Observações para a busca piloto

- Esta é uma string conceitual; a sintaxe será adaptada separadamente para Scopus, IEEE Xplore e ACM Digital Library.
- Não aplicar filtros definitivos antes de registrar a versão específica da base.
- Não interpretar o número de resultados desta versão como resultado final da revisão.
- Toda alteração deverá gerar uma nova versão (`v0.2`, `v0.3`, ...).
- A versão `v1.0` será congelada somente após validação da recuperação e calibração dos critérios.

## Registro de versões

| Versão | Data | Status | Alteração principal |
|---|---|---|---|
| v0.1 | 2026-10-04 | Rascunho | String conceitual inicial para busca piloto |
