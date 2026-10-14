# Como realizar o piloto humano de 30 registros

1. Abra `pilot_30_humano_cego.csv` no Excel ou LibreOffice; preserve o CSV original.
2. Leia somente `title`, `abstract`, palavras-chave e tipo documental. NAO abra o gabarito do Qwen antes de preencher as decisoes.
3. Em `human_decision`, use `include`, `exclude` ou `maybe`.
   - `include`: nao ha motivo claro de exclusao; avanca a leitura completa.
   - `exclude`: so quando o titulo/resumo permitem excluir com seguranca.
   - `maybe`: informacao insuficiente; avanca a leitura completa.
4. Em `human_reason_code`, use CE1, CE2, CE3 ou CE4 apenas para `exclude`. Nunca use CE6/CE7 nesta etapa.
5. Registre a justificativa em `human_notes` e o tempo gasto, em segundos, em `review_seconds`.
6. Se o resumo nao comprovar ausencia de avaliacao empirica, NAO conclua CE4 apenas por falta de metricas descritas; use `maybe` quando houver duvida.
7. Quando concluir as 30 linhas, SALVE O CSV e envie as contagens ou o arquivo para avaliarmos concordancia e tempo.
8. NAO copie os resultados do piloto para `decision_log.csv` antes da conferencia e resolucao das divergencias.

Este piloto mede tempo e identifica possiveis falhas. Com amostragem intencional nao proporcional e n=30, NAO valida exclusao automatica dos demais artigos.
