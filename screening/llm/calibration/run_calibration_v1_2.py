import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import ollama


# ============================================================
# CONFIGURAÇÃO
# ============================================================

MODEL = "qwen3:8b"
MODEL_ID = "500a1f067a9f"

PROMPT_VERSION = "v1.2-candidate"

TEMPERATURE = 0
SEED = 42


# ============================================================
# VALORES PERMITIDOS
# ============================================================

ALLOWED_CRITERION_VALUES = {
    "yes",
    "no",
    "unclear",
}

ALLOWED_RAG_ROLES = {
    "central",
    "baseline_or_comparator",
    "unclear",
    "not_applicable",
}


# ============================================================
# CAMINHOS
# ============================================================

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
    / "llm_screening_prompt_v1_2_candidate.txt"
)

OUTPUT_FILE = (
    CALIBRATION_DIR
    / "llm_prescreen_calibration_v1_2.csv"
)

RUN_METADATA_FILE = (
    CALIBRATION_DIR
    / "calibration_run_metadata_v1_2.txt"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

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


# ============================================================
# NORMALIZAR SAÍDA DO QWEN
# ============================================================

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


# ============================================================
# VALIDAR SAÍDA DO QWEN
# ============================================================

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


# ============================================================
# DECISÃO DETERMINÍSTICA
# ============================================================

def derive_decision(result):

    # CE3 — estudo não primário
    if result["primary_study"] == "no":
        return "exclude", "CE3"

    # CE1 — não é RAG operacional
    if result["operational_rag"] == "no":
        return "exclude", "CE1"

    # CE2 — fora do domínio ambiental
    if result["environmental_domain"] == "no":
        return "exclude", "CE2"

    # CE4 — ausência clara de avaliação empírica
    if result["empirical_evaluation"] == "no":
        return "exclude", "CE4"

    criteria = [
        result["primary_study"],
        result["operational_rag"],
        result["environmental_domain"],
        result["empirical_evaluation"],
    ]

    # Qualquer incerteza nos critérios
    # leva para maybe.
    if "unclear" in criteria:
        return "maybe", ""

    # RAG apenas como baseline/comparador
    # permanece para avaliação humana.
    if result["rag_role"] in {
        "baseline_or_comparator",
        "unclear",
    }:
        return "maybe", ""

    # Todos os critérios satisfeitos.
    return "include", ""


# ============================================================
# CARREGAR ARQUIVOS
# ============================================================

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


# ============================================================
# HASHES
# ============================================================

prompt_sha256 = file_sha256(
    PROMPT_FILE
)

input_sha256 = file_sha256(
    INPUT_FILE
)


# ============================================================
# EXECUÇÃO
# ============================================================

results = []

run_started = datetime.now().astimezone()

start_total = time.time()


print()
print("CALIBRAÇÃO CRITERIAL DO LLM")
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

    derived_decision = ""

    derived_reason_code = ""

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

        else:

            (
                derived_decision,
                derived_reason_code
            ) = derive_decision(
                normalized
            )

    except Exception as exc:

        status = "execution_error"

        validation_errors = (
            f"{type(exc).__name__}: {exc}"
        )

        normalized = {
            "primary_study": "",
            "primary_study_evidence": "",
            "operational_rag": "",
            "operational_rag_evidence": "",
            "environmental_domain": "",
            "environmental_domain_evidence": "",
            "empirical_evaluation": "",
            "empirical_evaluation_evidence": "",
            "rag_role": "",
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

        # -----------------------------
        # Avaliações feitas pelo Qwen
        # -----------------------------

        "primary_study":
            normalized[
                "primary_study"
            ],

        "primary_study_evidence":
            normalized[
                "primary_study_evidence"
            ],

        "operational_rag":
            normalized[
                "operational_rag"
            ],

        "operational_rag_evidence":
            normalized[
                "operational_rag_evidence"
            ],

        "environmental_domain":
            normalized[
                "environmental_domain"
            ],

        "environmental_domain_evidence":
            normalized[
                "environmental_domain_evidence"
            ],

        "empirical_evaluation":
            normalized[
                "empirical_evaluation"
            ],

        "empirical_evaluation_evidence":
            normalized[
                "empirical_evaluation_evidence"
            ],

        "rag_role":
            normalized[
                "rag_role"
            ],

        # -----------------------------
        # Decisão feita pelo Python
        # -----------------------------

        "derived_decision":
            derived_decision,

        "derived_reason_code":
            derived_reason_code,

        # -----------------------------
        # Auditoria
        # -----------------------------

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

        reason_display = (
            f" / {derived_reason_code}"
            if derived_reason_code
            else ""
        )

        print(
            f"{derived_decision}"
            f"{reason_display}"
        )

    else:

        print(
            f"ERRO: {validation_errors}"
        )


# ============================================================
# SALVAR RESULTADOS
# ============================================================

results_df = pd.DataFrame(
    results
)


results_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# RESUMO
# ============================================================

total = len(
    results_df
)

successful = (
    results_df["status"] == "ok"
).sum()

errors_count = (
    total - successful
)


decision_counts = (
    results_df[
        "derived_decision"
    ]
    .value_counts()
    .to_dict()
)


reason_counts = (
    results_df[
        "derived_reason_code"
    ]
    .value_counts()
    .to_dict()
)


# ============================================================
# METADADOS DA EXECUÇÃO
# ============================================================

run_finished = (
    datetime.now()
    .astimezone()
)

total_seconds = (
    time.time()
    - start_total
)


metadata = f"""LLM CALIBRATION RUN — v1.2

Run type: blind criterion-based calibration

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

DECISION ARCHITECTURE

LLM role:
criterion-level semantic assessment only.

Software role:
deterministic derivation of include/exclude/maybe
from criterion-level outputs.

Human role:
all official screening decisions remain human.

RESULT

Successful outputs: {successful}
Outputs with error: {errors_count}

include: {decision_counts.get("include", 0)}
exclude: {decision_counts.get("exclude", 0)}
maybe: {decision_counts.get("maybe", 0)}

CE1: {reason_counts.get("CE1", 0)}
CE2: {reason_counts.get("CE2", 0)}
CE3: {reason_counts.get("CE3", 0)}
CE4: {reason_counts.get("CE4", 0)}

Total execution seconds: {total_seconds:.2f}

IMPORTANT

Human reference decisions were not provided to the model.

The LLM did not directly generate the final screening
classification.

The derived decision was generated deterministically
by Python from the LLM criterion assessments.

All outputs remain decision-support suggestions.
Official eligibility decisions remain human.
"""


with open(
    RUN_METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(metadata)


# ============================================================
# SAÍDA DO TERMINAL
# ============================================================

print()
print("CALIBRAÇÃO CRITERIAL EXECUTADA")
print("--------------------------------------")
print(f"Registros processados: {total}")
print(f"Saídas válidas: {successful}")
print(f"Saídas com erro: {errors_count}")
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

print()
print("Códigos de exclusão derivados:")

print(
    f"CE1: "
    f"{reason_counts.get('CE1', 0)}"
)

print(
    f"CE2: "
    f"{reason_counts.get('CE2', 0)}"
)

print(
    f"CE3: "
    f"{reason_counts.get('CE3', 0)}"
)

print(
    f"CE4: "
    f"{reason_counts.get('CE4', 0)}"
)

print("--------------------------------------")
print()

print(
    f"Resultados: "
    f"{OUTPUT_FILE}"
)

print(
    f"Metadados: "
    f"{RUN_METADATA_FILE}"
)

print()

print(
    "IMPORTANTE: nenhuma decisão humana "
    "foi fornecida ao modelo."
)