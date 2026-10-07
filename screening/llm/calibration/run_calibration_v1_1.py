import csv
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import ollama


MODEL = "qwen3:8b"
MODEL_ID = "500a1f067a9f"
PROMPT_VERSION = "v1.1-candidate"

TEMPERATURE = 0
SEED = 42

ALLOWED_DECISIONS = {
    "include",
    "exclude",
    "maybe",
}

ALLOWED_REASON_CODES = {
    "",
    "CE1",
    "CE2",
    "CE3",
    "CE4",
}

ALLOWED_CONFIDENCE = {
    "high",
    "medium",
    "low",
}



BASE_DIR = Path(__file__).resolve().parents[3]

LLM_DIR = (
    BASE_DIR
    / "screening"
    / "llm"
)

CALIBRATION_DIR = (
    LLM_DIR
    / "calibration"
)

INPUT_FILE = (
    CALIBRATION_DIR
    / "calibration_blind_v1.csv"
)


PROMPT_FILE = (
    LLM_DIR
    / "llm_screening_prompt_v1_1_candidate.txt"
)


OUTPUT_FILE = (
    CALIBRATION_DIR
    / "llm_prescreen_calibration_v1_1.csv"
)


RUN_METADATA_FILE = (
    CALIBRATION_DIR
    / "calibration_run_metadata_v1_1.txt"
)



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
    """
    Substitui somente os placeholders destinados ao registro.
    """

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
    """
    Normaliza apenas espaços/capitalização.
    Não altera semanticamente a decisão.
    """

    decision = clean(
        data.get("decision", "")
    ).lower()

    reason_code = clean(
        data.get("reason_code", "")
    ).upper()

    confidence = clean(
        data.get("confidence", "")
    ).lower()

    rationale = clean(
        data.get("rationale", "")
    )

    return {
        "decision": decision,
        "reason_code": reason_code,
        "confidence": confidence,
        "rationale": rationale,
    }


def validate_output(data):
    """
    Verifica se a saída respeita o protocolo.
    """

    errors = []

    if data["decision"] not in ALLOWED_DECISIONS:
        errors.append(
            "invalid_decision"
        )

    if data["reason_code"] not in ALLOWED_REASON_CODES:
        errors.append(
            "invalid_reason_code"
        )

    if data["confidence"] not in ALLOWED_CONFIDENCE:
        errors.append(
            "invalid_confidence"
        )

    if not data["rationale"]:
        errors.append(
            "missing_rationale"
        )

    # Exclude precisa ter exatamente um CE.
    if (
        data["decision"] == "exclude"
        and data["reason_code"]
        not in {"CE1", "CE2", "CE3", "CE4"}
    ):
        errors.append(
            "exclude_without_valid_reason"
        )

    # Include e maybe não podem receber CE.
    if (
        data["decision"]
        in {"include", "maybe"}
        and data["reason_code"] != ""
    ):
        errors.append(
            "reason_code_not_empty_for_non_exclude"
        )

    return errors



if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {INPUT_FILE}"
    )

if not PROMPT_FILE.exists():
    raise FileNotFoundError(
        f"Prompt não encontrado: {PROMPT_FILE}"
    )


df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False
)

if len(df) != 18:
    raise ValueError(
        f"Esperados 18 registros de calibração, "
        f"mas foram encontrados {len(df)}."
    )


with open(
    PROMPT_FILE,
    "r",
    encoding="utf-8"
) as file:

    prompt_template = file.read()




prompt_sha256 = file_sha256(
    PROMPT_FILE
)

input_sha256 = file_sha256(
    INPUT_FILE
)




results = []

run_started = datetime.now().astimezone()
start_total = time.time()


print()
print("CALIBRAÇÃO CEGA DO LLM")
print("--------------------------------------")
print(f"Modelo: {MODEL}")
print(f"Model ID: {MODEL_ID}")
print(f"Prompt: {PROMPT_VERSION}")
print(f"Temperature: {TEMPERATURE}")
print(f"Seed: {SEED}")
print("Thinking: false")
print(f"Registros: {len(df)}")
print("--------------------------------------")
print()


for position, (_, row) in enumerate(
    df.iterrows(),
    start=1
):

    calibration_id = clean(
        row["calibration_id"]
    )

    record_id = clean(
        row["record_id"]
    )

    full_prompt = build_prompt(
        prompt_template,
        row
    )

    print(
        f"[{position:02d}/18] "
        f"{calibration_id} | "
        f"{record_id} ... ",
        end="",
        flush=True
    )

    item_start = time.time()

    raw_response = ""
    status = "ok"
    validation_errors = ""

    try:

        response = ollama.chat(
            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],

            format="json",

            options={
                "temperature": TEMPERATURE,
                "seed": SEED,
            },

            think=False,
        )

        raw_response = (
            response["message"]["content"]
            .strip()
        )

        parsed = json.loads(
            raw_response
        )

        normalized = normalize_output(
            parsed
        )

        errors = validate_output(
            normalized
        )

        if errors:
            status = "validation_error"
            validation_errors = ";".join(
                errors
            )

    except Exception as exc:

        status = "execution_error"
        validation_errors = (
            f"{type(exc).__name__}: {exc}"
        )

        normalized = {
            "decision": "",
            "reason_code": "",
            "confidence": "",
            "rationale": "",
        }

    elapsed = (
        time.time() - item_start
    )

    results.append({
        "calibration_id":
            calibration_id,

        "record_id":
            record_id,

        "model_name":
            MODEL,

        "model_id":
            MODEL_ID,

        "prompt_version":
            PROMPT_VERSION,

        "decision":
            normalized["decision"],

        "reason_code":
            normalized["reason_code"],

        "confidence":
            normalized["confidence"],

        "rationale":
            normalized["rationale"],

        "status":
            status,

        "validation_errors":
            validation_errors,

        "elapsed_seconds":
            f"{elapsed:.2f}",

        "raw_response":
            raw_response,
    })

    if status == "ok":
        print(
            f"{normalized['decision']} "
            f"({normalized['confidence']})"
        )
    else:
        print(
            f"ERRO: {validation_errors}"
        )


results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)



total = len(results_df)

successful = (
    results_df["status"] == "ok"
).sum()

errors = total - successful


decision_counts = (
    results_df["decision"]
    .value_counts()
    .to_dict()
)



run_finished = datetime.now().astimezone()

total_seconds = (
    time.time() - start_total
)


metadata = f"""LLM CALIBRATION RUN — v1

Run type: blind calibration
Run started: {run_started.isoformat()}
Run finished: {run_finished.isoformat()}

MODEL

Model name: {MODEL}
Model ID: {MODEL_ID}
Runtime: Ollama
Temperature: {TEMPERATURE}
Seed: {SEED}
Thinking: false
Structured output: JSON

PROMPT

Prompt version: {PROMPT_VERSION}
Prompt file: {PROMPT_FILE.name}
Prompt SHA256: {prompt_sha256}

INPUT

Input file: {INPUT_FILE.name}
Input SHA256: {input_sha256}
Expected records: 18
Processed records: {total}

RESULT

Successful outputs: {successful}
Outputs with error: {errors}

include: {decision_counts.get("include", 0)}
exclude: {decision_counts.get("exclude", 0)}
maybe: {decision_counts.get("maybe", 0)}

Total execution seconds: {total_seconds:.2f}

IMPORTANT

Human reference decisions were not provided to the model during inference.

This run is a calibration of the LLM-assisted pre-screening procedure.
The outputs are suggestions and are not official eligibility decisions.
"""


with open(
    RUN_METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(metadata)


print()
print("CALIBRAÇÃO EXECUTADA")
print("--------------------------------------")
print(f"Registros processados: {total}")
print(f"Saídas válidas: {successful}")
print(f"Saídas com erro: {errors}")
print()
print(
    f"include: "
    f"{decision_counts.get('include', 0)}"
)
print(
    f"exclude: "
    f"{decision_counts.get('exclude', 0)}"
)
print(
    f"maybe: "
    f"{decision_counts.get('maybe', 0)}"
)
print("--------------------------------------")
print()
print(f"Resultados: {OUTPUT_FILE}")
print(
    f"Metadados da execução: "
    f"{RUN_METADATA_FILE}"
)
print()
print(
    "IMPORTANTE: as decisões humanas ainda "
    "não foram comparadas."
)