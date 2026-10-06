# Códigos de Exclusão — versão v1.0

- Versão: `v1.0`
- Data de congelamento: `2026-10-06`
- Status: **CONGELADO**
- Protocolo associado: `protocol/protocol_v1.0.md`

Os códigos abaixo correspondem aos critérios oficiais de exclusão da
versão `v1.0` do protocolo.

Devem ser utilizados no `screening/decision_log.csv`, especialmente na
etapa de leitura de texto completo.

---

## 1. Códigos de exclusão

| Código | Definição operacional |
|---|---|
| CE1 | **Não atende à definição operacional de Retrieval-Augmented Generation.** Excluir estudos com LLM sem recuperação externa, recuperação sem geração, semantic retrieval sem integração com a etapa generativa ou uso da sigla `RAG` com outro significado. |
| CE2 | **Domínio fora do escopo ambiental ou de sustentabilidade ambiental.** Excluir aplicações RAG em que questões ambientais, ecológicas, climáticas ou de sustentabilidade ambiental não sejam explícitas e substantivas. |
| CE3 | **Estudo secundário ou publicação não primária.** Excluir surveys, revisões de literatura, revisões narrativas, tutoriais, editoriais e artigos de opinião. |
| CE4 | **Proposta sem avaliação empírica.** Excluir arquiteturas, frameworks ou sistemas apresentados sem experimento, validação ou outra evidência empírica. Inclui estudos em que avaliação ou implantação são apresentadas apenas como trabalho futuro. |
| CE5 | **Duplicata ou versão redundante.** Excluir registros duplicados ou versões redundantes do mesmo estudo. Quando existirem múltiplas versões, preservar a versão definida como principal segundo a política de deduplicação adotada. |
| CE6 | **Texto integral indisponível.** Excluir registros cujo texto completo não possa ser acessado para avaliação final de elegibilidade e extração. |
| CE7 | **Informação técnica insuficiente.** Excluir estudos que, mesmo após leitura integral, não apresentem informações suficientes sobre o sistema RAG ou seus resultados para responder a pelo menos uma das RQs da revisão. |

---

## 2. Uso dos códigos durante o screening

### 2.1 Triagem por título e resumo

As decisões possíveis são:

- `include`
- `exclude`
- `maybe`

Na etapa `title_abstract`:

- casos claramente inelegíveis podem receber um código `CE1–CE4`;
- registros claramente elegíveis avançam para a próxima etapa;
- quando título e resumo não fornecerem informação suficiente para uma
  decisão segura, utilizar `maybe`;
- para registros `maybe`, o campo `reason_code` pode permanecer vazio.

O princípio geral será:

> **Na dúvida, não excluir apenas por inferência.**

Os códigos `CE6` e `CE7` normalmente dependem da etapa de texto completo.

O código `CE5` é utilizado principalmente durante a deduplicação.

---

### 2.2 Leitura de texto completo

Na etapa `fulltext`:

- toda decisão `exclude` deve possuir exatamente um código principal
  `CE1–CE7`;
- quando mais de um código puder ser aplicado, registrar aquele que
  representa o motivo principal da exclusão;
- justificativas adicionais podem ser registradas em `notes`.

---

## 3. Regras operacionais associadas aos códigos

### CE1 — definição operacional de RAG

Para ser considerado Retrieval-Augmented Generation, o sistema deve possuir:

1. uma fonte externa ou base recuperável de conhecimento;
2. um mecanismo de recuperação;
3. uma etapa generativa;
4. utilização da informação recuperada como contexto, evidência ou
   conhecimento pela etapa generativa.

Excluir por `CE1` quando ocorrer qualquer uma das seguintes situações:

- LLM ou modelo generativo sem recuperação externa;
- mecanismo de recuperação sem etapa generativa;
- semantic retrieval utilizado de forma independente da geração;
- informação recuperada não é utilizada no processo generativo;
- `RAG` possui outro significado.

Exemplo de uso alternativo da sigla:

`RAG = Relation-Aware Graph`

Se título e resumo mencionarem recuperação e geração, mas não permitirem
confirmar a integração entre ambas, utilizar `maybe` e verificar o texto
completo.

---

### CE2 — domínio ambiental ou de sustentabilidade

A presença isolada de palavras como:

- `environment`;
- `environmental`;
- `sustainable`;
- `sustainability`;
- `ESG`;
- `SDG`;

não caracteriza automaticamente um domínio ambiental.

A dimensão ambiental deve ser explícita e substantiva no problema,
nos dados, na aplicação ou na avaliação.

#### Environment/environmental em sentido operacional

Excluir por `CE2` quando `environment` ou `environmental` significar apenas:

- ambiente computacional;
- ambiente virtual;
- ambiente robótico;
- ambiente industrial;
- cenário operacional;
- contexto de navegação;
- condições operacionais.

Esses usos não representam meio ambiente no sentido adotado pela revisão.

#### Agricultura

Agricultura, por si só, não caracteriza domínio ambiental.

Incluir somente quando houver componente substantivo relacionado, por exemplo, a:

- clima;
- adaptação climática;
- conservação;
- biodiversidade;
- emissões;
- uso sustentável de água;
- irrigação sustentável;
- eficiência de recursos com objetivo ambiental;
- outras práticas ambientalmente sustentáveis.

Controle operacional de cultivo, produtividade ou diagnóstico de plantas
isoladamente não são suficientes.

#### Energia, microgrids e baterias

A presença de:

- energia;
- eficiência energética;
- microgrids;
- baterias;
- degradação;
- calor extremo;

não caracteriza automaticamente domínio ambiental.

Deve existir componente substantivo relacionado, por exemplo, a:

- clima;
- adaptação ou mitigação climática;
- descarbonização;
- impacto ambiental;
- redução de emissões;
- sustentabilidade ambiental;
- gestão sustentável de recursos.

Custo ou eficiência operacional isoladamente não são suficientes.

#### ESG e relatórios de sustentabilidade

ESG, isoladamente, não é suficiente para inclusão.

A dimensão `Environmental` deve ser:

- explícita;
- substantiva;
- separável das dimensões `Social` e `Governance`;
- relevante para a aplicação ou avaliação do sistema RAG.

Quando o resumo não permitir essa decisão, utilizar `maybe` e verificar
o texto completo.

#### Ambiente construído

Estudos de construção ou edifícios podem ser incluídos quando envolverem,
de forma substantiva:

- Environmental Product Declarations (EPDs);
- Life Cycle Assessment (LCA);
- carbono incorporado;
- descarbonização;
- impacto ambiental;
- eficiência de recursos;
- sustentabilidade de materiais.

Manutenção, segurança ou operação predial isoladamente não bastam.

#### Sensoriamento remoto e geoespacial

Sensoriamento remoto ou dados geoespaciais não definem automaticamente o
domínio como ambiental.

A tarefa avaliada precisa possuir finalidade ambiental, climática,
ecológica ou de sustentabilidade.

#### ODS / SDGs

A menção genérica a Sustainable Development Goals não é suficiente.

Deve existir um componente ambiental substantivo na aplicação RAG.

---

### CE3 — estudo secundário ou publicação não primária

Excluir por `CE3`:

- surveys;
- systematic reviews;
- scoping reviews;
- revisões narrativas;
- tutorials;
- editoriais;
- artigos de opinião.

Um estudo pode ser tematicamente ambiental e discutir RAG extensivamente
e ainda assim ser excluído por `CE3` se não constituir estudo primário.

---

### CE4 — ausência de avaliação empírica

Excluir por `CE4` quando o estudo:

- apresenta apenas uma arquitetura ou framework conceitual;
- descreve somente uma proposta;
- não apresenta experimento, validação ou avaliação;
- declara que avaliação, validação ou deployment serão realizados em
  trabalhos futuros.

A presença de uma implementação ou arquitetura descrita não substitui
a necessidade de avaliação empírica exigida por `CI4`.

---

### CE5 — duplicatas e versões redundantes

A identificação de duplicatas deverá considerar, quando disponíveis:

- DOI;
- título;
- autores;
- ano;
- venue;
- outros metadados bibliográficos.

A remoção deve preservar uma versão principal do estudo.

Os arquivos brutos exportados das bases nunca deverão ser modificados
para remover duplicatas.

A deduplicação será realizada somente na base consolidada.

---

### CE6 — texto integral indisponível

Aplicar `CE6` somente quando o texto completo necessário para verificar
a elegibilidade não puder ser obtido.

A ausência de abstract completo, isoladamente, não deve ser registrada
como `CE6`.

---

### CE7 — informação técnica insuficiente

`CE7` somente deverá ser aplicado após avaliação do texto completo.

Utilizar quando o artigo não fornecer informação suficiente para
responder a pelo menos uma das RQs, mesmo sendo tematicamente aderente.

#### RAG utilizado apenas como baseline

Quando RAG aparecer somente como baseline:

- na triagem por título e resumo, utilizar `maybe` quando necessário;
- verificar o texto completo;
- incluir se a configuração RAG e seus resultados forem descritos com
  detalhe suficiente para extração e resposta a pelo menos uma RQ;
- caso contrário, excluir por `CE7`.

---

## 4. Ordem prática de decisão

Durante o screening, utilizar preferencialmente a seguinte sequência:

1. É realmente Retrieval-Augmented Generation?
   - Não → `CE1`.

2. A aplicação pertence ao domínio ambiental ou de sustentabilidade
   ambiental definido no protocolo?
   - Não → `CE2`.

3. É estudo primário?
   - Não → `CE3`.

4. Existe avaliação empírica?
   - Não → `CE4`.

5. É duplicata ou versão redundante?
   - Sim → `CE5`.

6. O texto completo está disponível?
   - Não → `CE6`.

7. Após leitura integral, existe informação técnica suficiente para
   responder a pelo menos uma RQ?
   - Não → `CE7`.

---

## 5. Casos ambíguos

Quando título e resumo não forem suficientes para determinar:

- se há RAG verdadeiro;
- se a dimensão ambiental é substantiva;
- se um baseline RAG possui informação extraível;
- se ESG possui componente ambiental separável;

o registro deverá ser classificado como:

`maybe`

e avançar para texto completo.

Casos ambíguos não devem ser excluídos apenas por ausência de informação
no abstract quando essa informação puder estar disponível no artigo completo.

---

## 6. Rastreabilidade

Os critérios oficiais estão definidos em:

`protocol/protocol_v1.0.md`

Os casos que motivaram o refinamento dos critérios estão documentados em:

`screening/calibration_day3.csv`

e:

`screening/calibration_day3.md`

As mudanças entre `v0.1` e `v1.0` estão registradas em:

`protocol/amendments.md`

Qualquer alteração futura nos códigos `CE1–CE7` deverá ser registrada
em `protocol/amendments.md` antes de sua aplicação.