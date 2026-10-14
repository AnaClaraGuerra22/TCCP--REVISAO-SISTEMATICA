#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import hashlib
import json
import os
import random
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path

EXPECTED_PROMPT_SHA256 = "cfac438781c32ec3672dcfb1191149629a4cb23b133646c482d5165696ad19c4"
EXPECTED_BATCHES = {1: 180, 2: 180, 3: 179}
MODEL = "qwen3:4b"
MODEL_ID_PREFIX = "359d7dd4bcda"
PROMPT_VERSION = "v1.2-operational"
CRITERIA = ("primary_study", "operational_rag", "environmental_domain", "empirical_evaluation")
EVIDENCE = tuple(f"{c}_evidence" for c in CRITERIA)
ALLOWED = {"yes", "no", "unclear"}
RAG_ROLES = {"central", "baseline_or_comparator", "unclear", "not_applicable"}
MATCH_FIELDS = ("record_id", "title", "abstract", "author_keywords", "index_keywords", "document_type", "document_identifier")
PILOT_QUOTA = {"include": 10, "maybe": 10}
EXCLUDE_QUOTA = {"CE1": 1, "CE2": 5, "CE3": 3, "CE4": 1}
PILOT_SEED = 42


def root_dir():
    # .../<repo>/screening/llm/day7/prepare_day7_audit_pilot.py
    return Path(__file__).resolve().parents[3]


def read_csv(path):
    if not path.is_file():
        raise RuntimeError(f"Arquivo ausente: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as fp:
        rdr = csv.DictReader(fp)
        headers = rdr.fieldnames or []
        rows = list(rdr)
    return headers, rows


def read_json(path):
    if not path.is_file():
        raise RuntimeError(f"Configuracao ausente: {path}")
    with path.open("r", encoding="utf-8-sig") as fp:
        return json.load(fp)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def unique_index(rows, context):
    index = {}
    for row in rows:
        rid = row.get("record_id", "").strip()
        check(bool(rid), f"ID vazio em {context}")
        check(rid not in index, f"ID duplicado em {context}: {rid}")
        index[rid] = row
    return index


def derive(r):
    # MESMA regra do run_day7_qwen3_4b.py; nao altera resultados existentes.
    if r["primary_study"] == "no":
        return "exclude", "CE3"
    if r["operational_rag"] == "no":
        return "exclude", "CE1"
    if r["environmental_domain"] == "no":
        return "exclude", "CE2"
    if r["empirical_evaluation"] == "no":
        return "exclude", "CE4"
    if any(r[k] == "unclear" for k in CRITERIA):
        return "maybe", ""
    if r["rag_role"] in ("baseline_or_comparator", "unclear"):
        return "maybe", ""
    return "include", ""


def safe_excel(value):
    """Impede que texto bibliografico seja interpretado como formula em Excel."""
    s = str(value or "")
    if s.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + s
    return s


def export_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: safe_excel(row.get(k, "")) for k in fieldnames})


def fmt_counter(counter):
    return ", ".join(f"{name}={counter.get(name, 0)}" for name in ("include", "exclude", "maybe"))


def main():
    base = root_dir()
    day7 = base / "screening" / "llm" / "day7"
    dest = day7 / "audit_pilot_v1"
    raw_base_file = base / "search" / "exports" / "processed" / "records_deduplicated.csv"
    human_log_file = base / "screening" / "decision_log.csv"
    prompt = base / "screening" / "llm" / "llm_screening_prompt_v1_2_operational.txt"
    check(day7.is_dir(), f"Diretorio do Dia 7 nao existe: {day7}")
    check(not dest.exists(), f"A pasta {dest} ja existe. Nao sobrescreveremos um piloto humano existente.")

    bcols, raw_base = read_csv(raw_base_file)
    lcols, human_log = read_csv(human_log_file)
    check(len(raw_base) == len(human_log) == 587, "A base e o log humano devem ter 587 artigos cada.")
    check(set(MATCH_FIELDS).issubset(bcols), "Base deduplicada com colunas insuficientes.")
    check(set(("record_id", "decision", "reason_code")).issubset(lcols), "Log humano com colunas insuficientes.")
    base_idx = unique_index(raw_base, "base deduplicada")
    log_idx = unique_index(human_log, "decision_log.csv")
    check(set(base_idx) == set(log_idx), "IDs da base nao coincidem com decision_log.csv")
    decided = {rid for rid, row in log_idx.items() if row["decision"].strip() in {"include", "exclude", "maybe"}}
    check(len(decided) == 47, f"Esperadas 47 decisoes humanas, encontradas {len(decided)}")
    check(not {rid for rid, row in log_idx.items() if row["decision"].strip() and rid not in decided}, "Log humano com decisao desconhecida")
    check("R0141" in log_idx and not log_idx["R0141"]["decision"].strip(), "R0141 nao esta pendente")
    check(sha256(prompt) == EXPECTED_PROMPT_SHA256, "Prompt do Qwen diverge do hash operacional congelado")

    result_rows = []
    audit_sources = [(raw_base_file, sha256(raw_base_file)), (human_log_file, sha256(human_log_file)), (prompt, sha256(prompt))]
    batch_counts = {}
    digest_set = set()
    multi_no = []
    missing_evidence = []
    total_suggestions = Counter()
    code_counts = Counter()

    for batch_no, expected in EXPECTED_BATCHES.items():
        key = f"{batch_no:02}"
        input_path = day7 / "batches" / f"batch_{key}.csv"
        result_path = day7 / "results" / f"batch_{key}_qwen3_4b_results.csv"
        config_path = day7 / "results" / f"batch_{key}_qwen3_4b_run_config.json"
        config = read_json(config_path)
        icol, inputs = read_csv(input_path)
        rcol, results = read_csv(result_path)
        audit_sources.extend([(input_path, sha256(input_path)), (result_path, sha256(result_path)), (config_path, sha256(config_path))])
        check(len(inputs) == len(results) == expected, f"Lote {key}: nao possui {expected} registros em ambos os CSVs")
        check(set(MATCH_FIELDS).issubset(icol), f"Lote {key}: colunas bibliograficas ausentes")
        check(not (set(icol) & {"human_decision", "human_reason_code", "human_notes", "decision", "reason_code"}), f"Lote {key} contem colunas humanas")
        for k in ("record_id", "status", "derived_decision", "derived_reason_code", "rag_role", *CRITERIA, *EVIDENCE):
            check(k in rcol, f"Lote {key}: falta coluna de resultado {k}")
        input_idx = unique_index(inputs, f"entrada lote {key}")
        result_idx = unique_index(results, f"saida lote {key}")
        check(set(input_idx) == set(result_idx), f"Lote {key}: IDs entrada e saida nao coincidem")
        check(int(config.get("batch", -1)) == batch_no, f"Lote {key}: numero de batch errado no JSON")
        check(int(config.get("expected_records", -1)) == expected, f"Lote {key}: total esperado errado no JSON")
        check(config.get("input_sha256", "").lower() == sha256(input_path), f"Lote {key}: hash da entrada diferente do JSON")
        check(config.get("prompt_sha256", "").lower() == EXPECTED_PROMPT_SHA256, f"Lote {key}: hash do prompt diferente do JSON")
        check(config.get("model_name") == MODEL, f"Lote {key}: nome de modelo inesperado")
        check(str(config.get("model_digest", "")).removeprefix("sha256:").startswith(MODEL_ID_PREFIX), f"Lote {key}: digest diferente do Dia 6")
        check(config.get("prompt_version") == PROMPT_VERSION, f"Lote {key}: versao de prompt incorreta")
        check(config.get("temperature") == 0 and config.get("seed") == 42 and config.get("think") is False and config.get("format") == "json", f"Lote {key}: configuracao de inferencia alterada")
        digest_set.add(config["model_digest"])
        current = Counter()
        for rid, inp in input_idx.items():
            check(rid in base_idx, f"Lote {key}: {rid} nao pertence a base principal")
            check(rid not in decided and rid != "R0141", f"Lote {key}: {rid} possui decisao humana anterior ou esta em consenso")
            for field in MATCH_FIELDS:
                check(inp.get(field, "") == base_idx[rid].get(field, ""), f"Lote {key} {rid}: metadado bibliografico alterado: {field}")
            check(inp["title"].strip() and inp["abstract"].strip(), f"Lote {key} {rid}: sem titulo ou resumo")
            r = result_idx[rid]
            check(r["status"] == "ok" and not r.get("validation_errors", ""), f"Lote {key} {rid}: status/erros invalidos")
            check(r.get("model_name") == MODEL and r.get("model_id") == MODEL_ID_PREFIX, f"Lote {key} {rid}: modelo inesperado")
            check(r.get("prompt_version") == PROMPT_VERSION, f"Lote {key} {rid}: versao inesperada")
            check(r.get("batch", "").zfill(2) == key, f"Lote {key} {rid}: identificador do lote no resultado incorreto")
            for c in CRITERIA:
                check(r[c] in ALLOWED, f"Lote {key} {rid}: criterio invalido {c}={r[c]}")
            check(r["rag_role"] in RAG_ROLES, f"Lote {key} {rid}: rag_role invalido")
            for e in EVIDENCE:
                if not r[e].strip():
                    missing_evidence.append((rid, e))
            decision, code = derive(r)
            check(r["derived_decision"] == decision and r["derived_reason_code"] == code, f"Lote {key} {rid}: derivacao da decisao inconsistente")
            # Pode ocorrer mais de um criterio 'no'; a prioridade do script e diferente da ordem recomendada no protocolo.
            negatives = [x for x in CRITERIA if r[x] == "no"]
            if len(negatives) >= 2:
                multi_no.append((rid, negatives, code))
            result_rows.append({**r, "batch": key})
            current[decision] += 1
            total_suggestions[decision] += 1
            if code:
                code_counts[code] += 1
        batch_counts[key] = current

    check(len(digest_set) == 1, "O digest do modelo nao foi identico nos tres lotes")
    check(not missing_evidence, f"Evidencias vazias em {len(missing_evidence)} registros; exemplo: {missing_evidence[:3]}")
    result_idx = unique_index(result_rows, "539 saidas consolidadas")
    check(len(result_idx) == 539, f"Total de resultados unico inesperado: {len(result_idx)}")
    check(set(result_idx) == (set(base_idx) - decided - {"R0141"}), "Cobertura 539/587 invalida; IDs faltantes ou extras")
    check(total_suggestions == Counter({"include": 175, "exclude": 251, "maybe": 113}), f"Contagens gerais inesperadas: {total_suggestions}")
    check(sum(code_counts.values()) == 251, "Codigos de exclusao nao somam 251")

    rng = random.Random(PILOT_SEED)
    selected = []
    sampled_counts = Counter()
    for dec, quantity in PILOT_QUOTA.items():
        group = sorted([r for r in result_rows if r["derived_decision"] == dec], key=lambda x: x["record_id"])
        check(len(group) >= quantity, f"Nao ha {quantity} casos {dec}")
        choice = rng.sample(group, quantity)
        selected.extend(choice)
        sampled_counts[dec] += len(choice)
    for code, quantity in EXCLUDE_QUOTA.items():
        group = sorted([r for r in result_rows if r["derived_decision"] == "exclude" and r["derived_reason_code"] == code], key=lambda x: x["record_id"])
        check(len(group) >= quantity, f"Nao ha {quantity} registros exclude {code} para o piloto")
        choice = rng.sample(group, quantity)
        selected.extend(choice)
        sampled_counts[f"exclude_{code}"] += len(choice)
    check(len({r["record_id"] for r in selected}) == 30, "A amostra do piloto deve conter 30 IDs distintos")
    rng.shuffle(selected)
    sample_by_batch = Counter(r["batch"] for r in selected)

    blind_fields = [
        "review_order", "record_id", "title", "abstract", "author_keywords",
        "index_keywords", "document_type", "human_decision", "human_reason_code",
        "human_notes", "review_seconds",
    ]
    reference_fields = ["review_order", "batch", "record_id", "derived_decision", "derived_reason_code", *CRITERIA, *EVIDENCE, "rag_role"]
    blind_rows, reference_rows = [], []
    for i, r in enumerate(selected, 1):
        inp = base_idx[r["record_id"]]
        blind_rows.append({
            "review_order": i, "record_id": r["record_id"],
            "title": inp["title"], "abstract": inp["abstract"],
            "author_keywords": inp["author_keywords"], "index_keywords": inp["index_keywords"],
            "document_type": inp["document_type"],
            "human_decision": "", "human_reason_code": "", "human_notes": "", "review_seconds": "",
        })
        reference_rows.append({"review_order": i, **r})

    combined_fields = ["batch", "record_id", "derived_decision", "derived_reason_code", "status", *CRITERIA, *EVIDENCE, "rag_role", "processed_at"]
    total = 539
    pct = lambda v: f"{100*v/total:.1f}%"
    md = [
        "# Dia 7 — Auditoria dos resultados automatizados",
        "",
        "> Auditoria de integridade; NAO constitui verificacao de acuracia, sensibilidade ou elegibilidade humana.",
        "",
        "## Integridade", "",
        "- Base deduplicada: **587** IDs unicos.",
        "- Decisoes humanas ja registradas e preservadas: **47**.",
        "- Consenso pendente: **R0141**.",
        "- Resultados Qwen: **539/539** IDs unicos, completos, sem sobreposicao com os registros humanos.",
        "- Saidas validas e derivacao reavaliada: **539/539**.",
        "- Hash do prompt conferido; digest de modelo e configuracao consistentes nos tres lotes.",
        "- A auditoria nao alterou decision_log.csv nem os resultados originais.",
        "",
        "## Sugestoes do modelo (nao sao decisoes finais)", "",
        "| Lote | Include | Exclude | Maybe | Total |", "|---|---:|---:|---:|---:|",
    ]
    for key, expected in EXPECTED_BATCHES.items():
        b = batch_counts[f"{key:02}"]
        md.append(f"| {key:02} | {b['include']} | {b['exclude']} | {b['maybe']} | {expected} |")
    md.extend([
        f"| **Total** | **175 ({pct(175)})** | **251 ({pct(251)})** | **113 ({pct(113)})** | **539** |",
        "", "## Codigos sugeridos para exclusao", "",
        "| Codigo | Frequencia |", "|---|---:|",
    ])
    for code in ("CE1", "CE2", "CE3", "CE4"):
        md.append(f"| {code} | {code_counts[code]} |")
    md.extend([
        "| **Total** | **251** |", "",
        "## Atencao metodologica", "",
        f"- **{len(multi_no)}** registros possuem dois ou mais criterios com valor 'no'. A prioridade de justificativas do script (CE3 antes de CE1/CE2/CE4) difere da ordem pratica CE1–CE4 documentada no protocolo. Nesses casos, conferir o codigo humano antes de registrar uma exclusao; nenhuma saida foi modificada.",
        "- Saidas tecnicamente validas **nao** comprovam que os criterios foram julgados corretamente pelo LLM.",
        "- Um piloto com 30 estudos nao prova sensibilidade suficiente para exclusao automatica de outros 251 registros.",
        "", "## Piloto humano — desenho exploratorio", "",
        "- Amostra aleatoria reprodutivel, **estratificada intencionalmente**: 10 include, 10 maybe e 10 exclude (1 CE1, 5 CE2, 3 CE3, 1 CE4).",
        "- Seed: **42**. O desenho nao e proporcional a distribuicao dos 539 registros; **nao estimar acuracia populacional diretamente** desta amostra.",
        f"- Registros sorteados por lote: {', '.join(f'{k}={v}' for k, v in sorted(sample_by_batch.items()))}.",
        "- Primeiro preencher o arquivo **pilot_30_humano_cego.csv** sem consultar as sugestoes do Qwen. Depois usar **pilot_30_gabarito_qwen_nao_abrir_antes.csv** para comparar.",
        "- Um segundo revisor humano independente e reconciliacao de discordancias sao recomendaveis para maior rigor da publicacao.",
        "- Manter o protocolo v1.0 congelado; eventuais mudancas no processo de triagem devem ser aprovadas e registradas em amendments.md ANTES de aplicar novos criterios.",
        "", "## Rastros SHA-256 dos arquivos auditados", "",
        "| Caminho relativo ao repositorio | SHA-256 |", "|---|---|",
    ])
    for path, hashv in audit_sources:
        md.append(f"| `{path.relative_to(base).as_posix()}` | `{hashv}` |")
    md.extend(["", "## Artigos com multiplos criterios negativos", ""])
    if multi_no:
        md.append("| Record ID | Criterios 'no' | Codigo sugerido |")
        md.append("|---|---|---|")
        for rid, negatives, code in multi_no:
            md.append(f"| {rid} | {', '.join(negatives)} | {code} |")
    else:
        md.append("Nenhum registro identificado.")
    md.append("")

    guide = """# Como realizar o piloto humano de 30 registros

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
"""

    # Nenhum arquivo anterior e sobrescrito; montagem em pasta temporaria com nome atomico.
    workdir = Path(tempfile.mkdtemp(prefix=".audit_pilot_build_", dir=day7))
    try:
        export_csv(workdir / "qwen_539_audited_summary.csv", combined_fields, sorted(result_rows, key=lambda r: r["record_id"]))
        export_csv(workdir / "pilot_30_humano_cego.csv", blind_fields, blind_rows)
        export_csv(workdir / "pilot_30_gabarito_qwen_nao_abrir_antes.csv", reference_fields, reference_rows)
        (workdir / "audit_report.md").write_text("\n".join(md), encoding="utf-8")
        (workdir / "pilot_instructions.md").write_text(guide, encoding="utf-8")
        check(not dest.exists(), "Destino ja existe; arquivo anterior preservado")
        workdir.rename(dest)
    finally:
        if workdir.exists():
            shutil.rmtree(workdir)

    print("\nAUDITORIA DIA 7: PASS")
    print("Base: 587 | decisoes humanas preservadas: 47 | R0141 pendente: 1")
    print("Resultados Qwen verificados: 539/539 (unicos, sem sobreposicao)")
    print("Sugestoes:", fmt_counter(total_suggestions))
    print("Codigos:", ", ".join(f"{c}={code_counts[c]}" for c in ("CE1", "CE2", "CE3", "CE4")))
    print(f"Registros com multiplos criterios negativos: {len(multi_no)}")
    print(f"Piloto cego: 30 registros | por lote: {dict(sorted(sample_by_batch.items()))}")
    print("Relatorio e CSVs em:", dest)
    print("Nenhum arquivo do Ollama, protocolo ou decision_log.csv foi alterado.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nAUDITORIA INTERROMPIDA: {exc}", file=sys.stderr)
        sys.exit(1)
