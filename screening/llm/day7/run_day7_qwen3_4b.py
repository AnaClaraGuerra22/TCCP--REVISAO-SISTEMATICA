import argparse
import csv
import hashlib
import json
import os
import tempfile
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import ollama
import pandas as pd

MODEL = "qwen3:4b"
MODEL_ID = "359d7dd4bcda"
PROMPT_VERSION = "v1.2-operational"
TEMPERATURE = 0
SEED = 42
EXPECTED_PROMPT_SHA256 = (
    "cfac438781c32ec3672dcfb119114962"
    "9a4cb23b133646c482d5165696ad19c4"
)
EXPECTED_BATCH_SIZE = {1: 180, 2: 180, 3: 179}
SCRIPT_VERSION = "day7-resumable-v1"

ALLOWED_CRITERION_VALUES = {"yes", "no", "unclear"}
ALLOWED_RAG_ROLES = {
    "central", "baseline_or_comparator", "unclear", "not_applicable"
}

BASE_DIR = Path(__file__).resolve().parents[3]
LLM_DIR = BASE_DIR / "screening" / "llm"
DAY7_DIR = LLM_DIR / "day7"
PROMPT_FILE = LLM_DIR / "llm_screening_prompt_v1_2_operational.txt"

CRITERION_FIELDS = [
    "primary_study", "primary_study_evidence",
    "operational_rag", "operational_rag_evidence",
    "environmental_domain", "environmental_domain_evidence",
    "empirical_evaluation", "empirical_evaluation_evidence",
    "rag_role",
]
RESULT_FIELDS = [
    "batch", "record_id", "model_name", "model_id", "prompt_version",
    *CRITERION_FIELDS,
    "derived_decision", "derived_reason_code", "status", "validation_errors",
    "elapsed_seconds", "processed_at", "raw_response",
]
REQUIRED_INPUT = [
    "record_id", "title", "abstract", "author_keywords", "index_keywords",
    "document_type", "document_identifier",
]

def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def file_sha256(path):
    sha = hashlib.sha256()

    with open(path, "rb") as file:
        for block in iter(
            lambda: file.read(65536),
            b""
        ):
            sha.update(block)

    return sha.hexdigest()


def build_prompt(template, row):

    replacements = {
        "{{record_id}}":
            clean(row["record_id"]),

        "{{title}}":
            clean(row["title"]),

        "{{abstract}}":
            clean(row["abstract"]),

        "{{author_keywords}}":
            clean(row["author_keywords"]),

        "{{index_keywords}}":
            clean(row["index_keywords"]),

        "{{document_type}}":
            clean(row["document_type"]),

        "{{document_identifier}}":
            clean(row["document_identifier"]),
    }

    prompt = template

    for placeholder, value in replacements.items():
        prompt = prompt.replace(
            placeholder,
            value
        )

    return prompt


def normalize_output(data):

    return {
        "primary_study":
            clean(
                data.get(
                    "primary_study",
                    ""
                )
            ).lower(),

        "primary_study_evidence":
            clean(
                data.get(
                    "primary_study_evidence",
                    ""
                )
            ),

        "operational_rag":
            clean(
                data.get(
                    "operational_rag",
                    ""
                )
            ).lower(),

        "operational_rag_evidence":
            clean(
                data.get(
                    "operational_rag_evidence",
                    ""
                )
            ),

        "environmental_domain":
            clean(
                data.get(
                    "environmental_domain",
                    ""
                )
            ).lower(),

        "environmental_domain_evidence":
            clean(
                data.get(
                    "environmental_domain_evidence",
                    ""
                )
            ),

        "empirical_evaluation":
            clean(
                data.get(
                    "empirical_evaluation",
                    ""
                )
            ).lower(),

        "empirical_evaluation_evidence":
            clean(
                data.get(
                    "empirical_evaluation_evidence",
                    ""
                )
            ),

        "rag_role":
            clean(
                data.get(
                    "rag_role",
                    ""
                )
            ).lower(),
    }


def validate_output(result):

    errors = []

    for field in [
        "primary_study",
        "operational_rag",
        "environmental_domain",
        "empirical_evaluation",
    ]:

        if (
            result[field]
            not in ALLOWED_CRITERION_VALUES
        ):
            errors.append(
                f"invalid_{field}"
            )

    if (
        result["rag_role"]
        not in ALLOWED_RAG_ROLES
    ):
        errors.append(
            "invalid_rag_role"
        )

    evidence_fields = [
        "primary_study_evidence",
        "operational_rag_evidence",
        "environmental_domain_evidence",
        "empirical_evaluation_evidence",
    ]

    for field in evidence_fields:

        if not result[field]:
            errors.append(
                f"missing_{field}"
            )

    return errors


def derive_decision(result):
    if result["primary_study"] == "no":
        return "exclude", "CE3"

    if result["operational_rag"] == "no":
        return "exclude", "CE1"

    if result["environmental_domain"] == "no":
        return "exclude", "CE2"

    if result["empirical_evaluation"] == "no":
        return "exclude", "CE4"

    criteria = [
        result["primary_study"],
        result["operational_rag"],
        result["environmental_domain"],
        result["empirical_evaluation"],
    ]


    if "unclear" in criteria:
        return "maybe", ""


    if result["rag_role"] in {
        "baseline_or_comparator",
        "unclear",
    }:
        return "maybe", ""

    return "include", ""



def model_digest():
    """Confere se o modelo local e o mesmo usado no Dia 6."""
    try:
        response = ollama.list()
    except Exception as exc:
        raise RuntimeError(
            "Nao foi possivel conectar ao Ollama. Abra o Ollama e tente novamente."
        ) from exc

    items = response.get("models", [])
    for item in items:
        # O cliente ollama pode retornar objetos Pydantic ou dicionarios.
        model = getattr(item, "model", None)
        digest = getattr(item, "digest", None)
        if isinstance(item, dict):
            model = model or item.get("model") or item.get("name")
            digest = digest or item.get("digest")
        if model == MODEL:
            digest = str(digest or "").removeprefix("sha256:")
            if not digest.startswith(MODEL_ID):
                raise RuntimeError(
                    f"O modelo {MODEL} mudou desde o Dia 6: "
                    f"digest local = {digest!r}; esperado com inicio {MODEL_ID}. "
                    "Nao execute sem verificar essa mudanca."
                )
            return digest
    raise RuntimeError(
        f"Modelo {MODEL} nao encontrado no Ollama. Execute 'ollama list'."
    )


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def atomic_write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def atomic_write_csv(path, records, input_order):
    """Substituicao atomica: ate em desligamento, preserva o checkpoint anterior."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
            writer.writeheader()
            for record_id in input_order:
                if record_id in records:
                    writer.writerow(records[record_id])
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_existing_results(path, input_ids):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != RESULT_FIELDS:
            raise RuntimeError("Esquema do checkpoint diferente do esperado.")
        rows = list(reader)
    result = {}
    for row in rows:
        record_id = row["record_id"]
        if record_id not in input_ids:
            raise RuntimeError(f"ID alheio ao lote no checkpoint: {record_id}")
        if record_id in result:
            raise RuntimeError(f"ID duplicado no checkpoint: {record_id}")
        if row["status"] not in {"ok", "validation_error", "execution_error"}:
            raise RuntimeError(f"Status invalido no checkpoint: {record_id}")
        if row["status"] == "ok" and row["derived_decision"] not in {
            "include", "exclude", "maybe"
        }:
            raise RuntimeError(f"Decisao derivada invalida: {record_id}")
        result[record_id] = row
    return result


def preflight(batch):
    input_file = DAY7_DIR / "batches" / f"batch_{batch:02}.csv"
    results_dir = DAY7_DIR / "results"
    output_file = results_dir / f"batch_{batch:02}_qwen3_4b_results.csv"
    config_file = results_dir / f"batch_{batch:02}_qwen3_4b_run_config.json"

    if not input_file.is_file():
        raise FileNotFoundError(f"Lote nao encontrado: {input_file}")
    if not PROMPT_FILE.is_file():
        raise FileNotFoundError(f"Prompt nao encontrado: {PROMPT_FILE}")

    p_hash = file_sha256(PROMPT_FILE)
    if p_hash != EXPECTED_PROMPT_SHA256:
        raise RuntimeError(
            f"Hash do prompt operacional NAO corresponde ao Dia 6.\n"
            f"Esperado: {EXPECTED_PROMPT_SHA256}\nEncontrado: {p_hash}"
        )

    df = pd.read_csv(input_file, dtype=str, keep_default_na=False)
    if len(df) != EXPECTED_BATCH_SIZE[batch]:
        raise RuntimeError(f"Lote {batch} deveria ter {EXPECTED_BATCH_SIZE[batch]} artigos, "
                           f"mas contem {len(df)}")
    missing = sorted(set(REQUIRED_INPUT) - set(df.columns))
    if missing:
        raise RuntimeError(f"Colunas faltando no lote: {missing}")
    forbidden = set(df.columns) & {"human_decision", "human_reason_code", "human_notes", "decision", "reason_code"}
    if forbidden:
        raise RuntimeError(f"Lote contem decisoes humanas: {sorted(forbidden)}")
    ids = [clean(x) for x in df["record_id"]]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise RuntimeError("IDs vazios ou repetidos no lote")
    if "R0141" in ids:
        raise RuntimeError("R0141 pertence a revisao de consenso, nao ao lote")
    if any(not clean(x) for x in df["title"]) or any(not clean(x) for x in df["abstract"]):
        raise RuntimeError("Ha titulo ou resumo vazio no lote")

    # Nao le nem transmite decisoes humanas ao modelo.
    digest = model_digest()
    config = {
        "script_version": SCRIPT_VERSION,
        "batch": batch,
        "input_file": str(input_file.relative_to(BASE_DIR)),
        "input_sha256": file_sha256(input_file),
        "prompt_file": str(PROMPT_FILE.relative_to(BASE_DIR)),
        "prompt_sha256": p_hash,
        "prompt_version": PROMPT_VERSION,
        "model_name": MODEL,
        "model_digest": digest,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "think": False,
        "format": "json",
        "expected_records": len(df),
    }

    if config_file.exists() != output_file.exists():
        raise RuntimeError(
            "Checkpoint/configuracao incompletos. Nao recriar automaticamente; "
            "envie a mensagem de erro para verificar os arquivos."
        )

    if config_file.exists():
        saved = json.loads(config_file.read_text(encoding="utf-8"))
        mismatched = [k for k, v in config.items() if saved.get(k) != v]
        if mismatched:
            raise RuntimeError(
                "Tentativa de retomar com configuracao diferente! "
                f"Campos divergentes: {mismatched}"
            )

    return df, ids, config, config_file, output_file


def run_one(row, batch, template):
    record_id = clean(row["record_id"])
    started = time.monotonic()
    status, errors_text = "ok", ""
    raw_response = ""
    decision, reason = "", ""
    normalized = {k: "" for k in CRITERION_FIELDS}

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": build_prompt(template, row)}],
            format="json",
            options={"temperature": TEMPERATURE, "seed": SEED},
            think=False,
        )
        raw_response = response["message"]["content"].strip()
        parsed = json.loads(raw_response)
        if not isinstance(parsed, dict):
            raise ValueError("JSON retornado nao e um objeto")
        normalized = normalize_output(parsed)
        errs = validate_output(normalized)
        if errs:
            status = "validation_error"
            errors_text = ";".join(errs)
        else:
            decision, reason = derive_decision(normalized)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        status = "validation_error"
        errors_text = f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        status = "execution_error"
        errors_text = f"{type(exc).__name__}: {exc}"

    return {
        "batch": f"{batch:02}",
        "record_id": record_id,
        "model_name": MODEL,
        "model_id": MODEL_ID,
        "prompt_version": PROMPT_VERSION,
        **normalized,
        "derived_decision": decision,
        "derived_reason_code": reason,
        "status": status,
        "validation_errors": errors_text,
        "elapsed_seconds": f"{time.monotonic()-started:.2f}",
        "processed_at": now_iso(),
        "raw_response": raw_response,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--check", action="store_true", help="Somente validar; nao executa o LLM")
    parser.add_argument("--retry-errors", action="store_true", help="Reexecutar erros ja registrados")
    args = parser.parse_args()

    df, ids, config, config_file, output_file = preflight(args.batch)
    results = load_existing_results(output_file, set(ids))
    done_ok = sum(r["status"] == "ok" for r in results.values())
    flagged = sum(r["status"] != "ok" for r in results.values())
    print(f"\nDIA 7 | Qwen3:4B | LOTE {args.batch:02}")
    print(f"Arquivos: {len(ids)} artigos | ok salvos: {done_ok} | erros salvos: {flagged}")
    print(f"Prompt e modelo conferidos. SHA256: {config['prompt_sha256']}")
    print(f"Resultados: {output_file}")
    if args.check:
        print("CHECAGEM: PASS. Nenhum artigo processado, nenhum arquivo alterado.")
        return

    if not config_file.exists():
        atomic_write_json(config_file, {**config, "started_at": now_iso()})
        atomic_write_csv(output_file, results, ids)

    template = PROMPT_FILE.read_text(encoding="utf-8")
    started = time.monotonic()
    try:
        for pos, (_, row) in enumerate(df.iterrows(), start=1):
            record_id = clean(row["record_id"])
            if record_id in results and (
                results[record_id]["status"] != "execution_error"
                and not (args.retry_errors and results[record_id]["status"] == "validation_error")
            ):
                continue

            print(f"[{pos:03}/{len(df)}] {record_id} ... ", end="", flush=True)
            result = run_one(row, args.batch, template)
            results[record_id] = result
            atomic_write_csv(output_file, results, ids)
            label = result["derived_decision"] or "SEM SUGESTAO"
            reason = result["derived_reason_code"]
            print(f"{result['status']} | {label} {reason}".strip())
            if result["status"] == "execution_error":
                print("Falha de execucao: checkpoint salvo. Corrija o Ollama e execute novamente.")
                break
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario. Artigos anteriores ja estao salvos.")
        return

    counts = Counter(row["status"] for row in results.values())
    suggestions = Counter(
        row["derived_decision"] for row in results.values()
        if row["status"] == "ok"
    )
    print("\n===== RESUMO LOTE =====")
    print(f"Processados e salvos: {len(results)}/{len(ids)}")
    print(f"Validos: {counts['ok']} | Falhas de validacao: {counts['validation_error']} "
          f"| Erros de execucao: {counts['execution_error']}")
    print(f"Sugestoes: include={suggestions['include']}, "
          f"exclude={suggestions['exclude']}, maybe={suggestions['maybe']}")
    print(f"Tempo desta sessao: {time.monotonic()-started:.1f}s")
    print("ATENCAO: nenhuma decisao humana foi modificada.")


if __name__ == "__main__":
    main()
