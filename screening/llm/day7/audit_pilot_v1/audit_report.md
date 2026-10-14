# Dia 7 — Auditoria dos resultados automatizados

> Auditoria de integridade; NAO constitui verificacao de acuracia, sensibilidade ou elegibilidade humana.

## Integridade

- Base deduplicada: **587** IDs unicos.
- Decisoes humanas ja registradas e preservadas: **47**.
- Consenso pendente: **R0141**.
- Resultados Qwen: **539/539** IDs unicos, completos, sem sobreposicao com os registros humanos.
- Saidas validas e derivacao reavaliada: **539/539**.
- Hash do prompt conferido; digest de modelo e configuracao consistentes nos tres lotes.
- A auditoria nao alterou decision_log.csv nem os resultados originais.

## Sugestoes do modelo (nao sao decisoes finais)

| Lote | Include | Exclude | Maybe | Total |
|---|---:|---:|---:|---:|
| 01 | 65 | 77 | 38 | 180 |
| 02 | 70 | 67 | 43 | 180 |
| 03 | 40 | 107 | 32 | 179 |
| **Total** | **175 (32.5%)** | **251 (46.6%)** | **113 (21.0%)** | **539** |

## Codigos sugeridos para exclusao

| Codigo | Frequencia |
|---|---:|
| CE1 | 3 |
| CE2 | 180 |
| CE3 | 66 |
| CE4 | 2 |
| **Total** | **251** |

## Atencao metodologica

- **37** registros possuem dois ou mais criterios com valor 'no'. A prioridade de justificativas do script (CE3 antes de CE1/CE2/CE4) difere da ordem pratica CE1–CE4 documentada no protocolo. Nesses casos, conferir o codigo humano antes de registrar uma exclusao; nenhuma saida foi modificada.
- Saidas tecnicamente validas **nao** comprovam que os criterios foram julgados corretamente pelo LLM.
- Um piloto com 30 estudos nao prova sensibilidade suficiente para exclusao automatica de outros 251 registros.

## Piloto humano — desenho exploratorio

- Amostra aleatoria reprodutivel, **estratificada intencionalmente**: 10 include, 10 maybe e 10 exclude (1 CE1, 5 CE2, 3 CE3, 1 CE4).
- Seed: **42**. O desenho nao e proporcional a distribuicao dos 539 registros; **nao estimar acuracia populacional diretamente** desta amostra.
- Registros sorteados por lote: 01=13, 02=9, 03=8.
- Primeiro preencher o arquivo **pilot_30_humano_cego.csv** sem consultar as sugestoes do Qwen. Depois usar **pilot_30_gabarito_qwen_nao_abrir_antes.csv** para comparar.
- Um segundo revisor humano independente e reconciliacao de discordancias sao recomendaveis para maior rigor da publicacao.
- Manter o protocolo v1.0 congelado; eventuais mudancas no processo de triagem devem ser aprovadas e registradas em amendments.md ANTES de aplicar novos criterios.

## Rastros SHA-256 dos arquivos auditados

| Caminho relativo ao repositorio | SHA-256 |
|---|---|
| `search/exports/processed/records_deduplicated.csv` | `53d24a8157670337e7f27b8f5fd9b02c70f5350478d77ec93b451e2fc18b2860` |
| `screening/decision_log.csv` | `30958aa8656bdd6375a669bc5f4a556fbc7a87b87152edec7040a606e89e3c00` |
| `screening/llm/llm_screening_prompt_v1_2_operational.txt` | `cfac438781c32ec3672dcfb1191149629a4cb23b133646c482d5165696ad19c4` |
| `screening/llm/day7/batches/batch_01.csv` | `4c267caa92fc4f64d17b5027d7ce9c3bd49c9a4410880376106b9051017c7c2c` |
| `screening/llm/day7/results/batch_01_qwen3_4b_results.csv` | `b134e50991010eb52be18fd67607c72aa91c275cec1fb915cff81fa0c2663249` |
| `screening/llm/day7/results/batch_01_qwen3_4b_run_config.json` | `8b66a77b86ae83881fda3fb90427cdf3376a5567772abf0242e90e2ba2f8ab88` |
| `screening/llm/day7/batches/batch_02.csv` | `639dc0af65b95f3d8bb1cd42195e51169816da21430ea89271c4c31f10eb18f6` |
| `screening/llm/day7/results/batch_02_qwen3_4b_results.csv` | `acebd2ea983d73f81cc70ea428560861a4a3d49af5b33958f00250b054f08c82` |
| `screening/llm/day7/results/batch_02_qwen3_4b_run_config.json` | `7c92a052d7a25138bde22089c16c2ac812cc8a5ed7a9133469dba3e33496de20` |
| `screening/llm/day7/batches/batch_03.csv` | `bf1839fb5e1cb1d933557498a61e0ef8d9d28052bcc80b76fd0cfc2ec124e4f0` |
| `screening/llm/day7/results/batch_03_qwen3_4b_results.csv` | `bde0e29435d97e98c3340a3efb69c25a6ca54378d1a78efc2e96a960ab6ac75e` |
| `screening/llm/day7/results/batch_03_qwen3_4b_run_config.json` | `0abaa52e85f04352dfeba8c6b4f6cec0872232a26537d65f207dec371242b7f8` |

## Artigos com multiplos criterios negativos

| Record ID | Criterios 'no' | Codigo sugerido |
|---|---|---|
| R0012 | primary_study, environmental_domain | CE3 |
| R0017 | primary_study, environmental_domain | CE3 |
| R0020 | primary_study, environmental_domain | CE3 |
| R0025 | primary_study, environmental_domain | CE3 |
| R0064 | primary_study, environmental_domain | CE3 |
| R0127 | primary_study, environmental_domain | CE3 |
| R0167 | primary_study, environmental_domain | CE3 |
| R0168 | primary_study, environmental_domain, empirical_evaluation | CE3 |
| R0170 | primary_study, environmental_domain | CE3 |
| R0193 | primary_study, environmental_domain | CE3 |
| R0218 | primary_study, environmental_domain | CE3 |
| R0228 | primary_study, environmental_domain | CE3 |
| R0236 | operational_rag, environmental_domain | CE1 |
| R0264 | primary_study, empirical_evaluation | CE3 |
| R0270 | primary_study, empirical_evaluation | CE3 |
| R0286 | primary_study, environmental_domain | CE3 |
| R0304 | primary_study, environmental_domain | CE3 |
| R0311 | primary_study, environmental_domain | CE3 |
| R0321 | primary_study, environmental_domain | CE3 |
| R0332 | primary_study, environmental_domain | CE3 |
| R0342 | primary_study, environmental_domain | CE3 |
| R0346 | primary_study, environmental_domain | CE3 |
| R0376 | primary_study, environmental_domain, empirical_evaluation | CE3 |
| R0387 | primary_study, environmental_domain, empirical_evaluation | CE3 |
| R0388 | primary_study, environmental_domain | CE3 |
| R0416 | primary_study, environmental_domain | CE3 |
| R0437 | primary_study, operational_rag, empirical_evaluation | CE3 |
| R0451 | primary_study, environmental_domain | CE3 |
| R0469 | primary_study, environmental_domain | CE3 |
| R0474 | primary_study, environmental_domain | CE3 |
| R0502 | primary_study, environmental_domain | CE3 |
| R0542 | primary_study, environmental_domain | CE3 |
| R0547 | primary_study, environmental_domain, empirical_evaluation | CE3 |
| R0564 | operational_rag, environmental_domain | CE1 |
| R0576 | primary_study, empirical_evaluation | CE3 |
| R0577 | primary_study, environmental_domain | CE3 |
| R0581 | primary_study, environmental_domain | CE3 |
