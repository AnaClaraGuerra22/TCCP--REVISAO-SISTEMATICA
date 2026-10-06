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

---

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