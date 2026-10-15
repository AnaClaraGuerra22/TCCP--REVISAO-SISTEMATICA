# Dia 8 — Procedimento operacional de triagem (RASCUNHO)

> Este documento descreve a organizacao proposta; nao altera o protocolo v1.0 congelado. Confirmar com a orientacao antes de formalizar mudancas metodologicas.

## Proveniencia e escopo

- Base: 587 estudos apos deduplicacao.
- 47 decisoes humanas preexistentes: manter no `screening/decision_log.csv`.
- 539 sugestoes do Qwen ja auditadas; nenhuma e decisao oficial.
- 30 artigos de piloto assistido por ChatGPT, identificados em `screening/llm/day7/audit_pilot_v1/`; nao equivalem a revisao humana cega/independente.
- 509 restantes: fila desta planilha, em 21 blocos (20 de 25 e 1 de 9).
- R0141: divergencia de calibracao pendente, fora da fila.

## Procedimento proposto

1. Revisor humano examina titulo + resumo (e metadados se preciso).
2. Usar `include` para elegibilidade aparente; `exclude` SOMENTE se houver evidencia clara de CE1–CE4; `maybe` para incerteza.
3. Em caso `exclude`, registrar o codigo principal e uma justificativa curta, baseada no resumo.
4. Registrar identificador, revisor e data. Nao classificar sugestoes de Qwen como julgamento humano.
5. Preferir revisores humanos independentes e procedimento de consenso; se nao houver, explicitar limitacao e considerar revisao independente do texto completo.
6. Separar os 30 do piloto para auditoria adicional, as 10 divergencias, o codigo R0280 e R0141 para resolucao.
7. Antes de copiar decisoes para o log oficial, auditar IDs, justificativas e eventuais mudancas no procedimento.

## Regras metodologicas

- Usar `screening/exclusion_codes.md` e `protocol/protocol_v1.0.md`, versao congelada.
- CE2: dimensao ambiental precisa ser explicita e substantiva. Agricultura/energia/edificios/ESG nao bastam por si.
- CE4: ausencia de experimentos descritos no abstract nao e automaticamente evidencia de ausencia de avaliacao; na duvida usar maybe.
- Os 37 registros com multiplos criterios negativos no Qwen serao auditados antes de eventual exclusao formal.
- Nenhum registro pode ser excluido automaticamente pelo Qwen com base neste piloto assistido.
- Alteracoes metodologicas substantivas devem ser aprovadas e documentadas em `protocol/amendments.md`.

## Tarefa imediata

Abrir `triagem_dia8_509_google_planilhas.xlsx` no Google Planilhas.
Filtrar BLOCO = 1 e preencher 25 artigos. Exportar em XLSX antes de fechar a sessao.

## Resultado do primeiro bloco

- Inicio: [preencher]
- Termino: [preencher]
- Revisor(es): [preencher]
- Include: [preencher]
- Exclude: [preencher]
- Maybe: [preencher]
- Pendencias: [preencher]
