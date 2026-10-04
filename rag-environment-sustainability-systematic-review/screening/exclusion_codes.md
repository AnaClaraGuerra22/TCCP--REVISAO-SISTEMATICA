# Códigos de Exclusão - versão v0.1

- Versão: `v0.1`
- Status: **PRELIMINAR - sujeito à calibração intra-revisora**

Os códigos abaixo correspondem aos critérios de exclusão definidos no protocolo. Devem ser utilizados no `decision_log.csv`, especialmente na etapa de leitura de texto completo.

| Código | Definição operacional |
|---|---|
| CE1 | **LLM sem mecanismo de recuperação.** Excluir estudos em que o sistema utilize apenas um LLM ou modelo gerador sem recuperar informação de uma fonte externa como parte do processo de geração. |
| CE2 | **Outro domínio sem componente ambiental substancial.** Excluir estudos de RAG aplicados a domínios sem componente ambiental ou de sustentabilidade ambiental explícito, substancial e separável. |
| CE3 | **Estudo secundário ou não empírico.** Excluir surveys, revisões de literatura, editoriais, tutoriais e artigos de opinião. |
| CE4 | **Proposta sem avaliação empírica.** Excluir arquiteturas ou frameworks apenas conceituais quando não houver experimento, avaliação ou evidência empírica do sistema. |
| CE5 | **Duplicata ou versão redundante.** Excluir registros duplicados ou versões redundantes do mesmo estudo. Quando houver múltiplas versões, preservar a versão definida como principal segundo a política de deduplicação adotada posteriormente. |
| CE6 | **Texto integral indisponível.** Excluir registros cujo texto completo não possa ser acessado para avaliação de elegibilidade e extração. |
| CE7 | **Informação técnica insuficiente.** Excluir estudos que, mesmo após leitura integral, não apresentem informações suficientes para responder a nenhuma das RQs da revisão. |

## Uso no screening

- `title_abstract`: o campo `reason_code` pode permanecer vazio quando a decisão ainda for `maybe` ou quando a exclusão não exigir um motivo definitivo nessa fase.
- `fulltext`: toda decisão `exclude` deve possuir exatamente um código principal CE1-CE7. Observações adicionais podem ser registradas em `notes`.
- Casos ambíguos identificados durante a calibração devem ser documentados antes de alterar a redação dos critérios.
