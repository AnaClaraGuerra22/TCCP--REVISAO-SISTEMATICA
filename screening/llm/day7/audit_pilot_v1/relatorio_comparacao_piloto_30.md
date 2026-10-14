# Relatório comparativo — piloto de triagem, 30 registros

Data de elaboração: 14/10/2026. Fontes: `pilot_30_google_planilhas(1).xlsx` e `pilot_30_gabarito_qwen_nao_abrir_antes.csv`.

## Estatísticas descritivas

| Indicador | Resultado |
|---|---:|
| Artigos conferidos por ID | 30/30 |
| Decisões concordantes | 20 |
| Decisões discordantes | 10 |
| Concordância bruta | 66,7% |
| Kappa de Cohen (nominal, descritivo) | 0,50 |
| Divergência de código com mesma decisão | 1 (R0280) |
| Códigos CE inválidos no preenchimento | 0 |
| Justificativas ausentes | 0 |
| Tempos de triagem preenchidos | 0 |

## Matriz de comparação (linhas = planilha; colunas = Qwen)

| Registrada \ Qwen | include | exclude | maybe | Total |
|---|---:|---:|---:|---:|
| include | 6 | 0 | 0 | 6 |
| exclude | 2 | 10 | 6 | 18 |
| maybe | 2 | 0 | 4 | 6 |
| Total | 10 | 10 | 10 | 30 |

## Casos que exigem conferência

| ID | Decisão registrada | Qwen | Código registrado | Código Qwen |
|---|---|---|---|---|
| R0403 | exclude | include | CE2 | — |
| R0144 | exclude | maybe | CE2 | — |
| R0316 | exclude | maybe | CE2 | — |
| R0085 | maybe | include | — | — |
| R0360 | exclude | maybe | CE2 | — |
| R0280 | exclude | exclude | CE1 | CE4 |
| R0263 | exclude | maybe | CE2 | — |
| R0225 | exclude | include | CE2 | — |
| R0105 | maybe | include | — | — |
| R0069 | exclude | maybe | CE2 | — |
| R0037 | exclude | maybe | CE2 | — |

## Cuidados metodológicos

- O Qwen excluiu 10 artigos do piloto e os dez foram marcados `exclude` na planilha. Esse resultado não permite estimar com segurança o risco de falsos negativos nos demais 241 sugeridos para exclusão.
- A amostra foi construída com 10 registros de cada sugestão do Qwen, logo as taxas não representam a distribuição natural dos 539 artigos.
- As classificações da planilha foram produzidas com auxílio direto do ChatGPT nesta conversa, e portanto **não representam revisão humana independente/cega**. A concordância e o kappa são comparações descritivas, não validação independente.
- No R0280, ambos marcaram `exclude`, mas o código foi CE1 (planilha) e CE4 (Qwen); conferir aplicação da prioridade de critérios do protocolo.
- A coluna `TEMPO (s)` está vazia, impossibilitando estimar o tempo médio da triagem.
- Nenhum dos arquivos originais do projeto nem `screening/decision_log.csv` foi alterado durante esta comparação.
