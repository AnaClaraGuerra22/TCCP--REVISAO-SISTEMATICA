import hashlib
from datetime import datetime
from pathlib import Path

import pandas as pd


N_VALIDATION = 30
RANDOM_SEED = 20261008



BASE_DIR = Path(__file__).resolve().parents[3]

ALL_RECORDS_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "records_deduplicated.csv"
)

CALIBRATION_FILE = (
    BASE_DIR
    / "screening"
    / "llm"
    / "calibration"
    / "calibration_blind_v1.csv"
)

VALIDATION_DIR = (
    BASE_DIR
    / "screening"
    / "llm"
    / "validation"
)

OUTPUT_FILE = (
    VALIDATION_DIR
    / "validation_blind_v1.csv"
)

METADATA_FILE = (
    VALIDATION_DIR
    / "validation_selection_metadata_v1.txt"
)


def file_sha256(path):
    sha = hashlib.sha256()

    with open(path, "rb") as file:
        for block in iter(
            lambda: file.read(65536),
            b""
        ):
            sha.update(block)

    return sha.hexdigest()



if not ALL_RECORDS_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {ALL_RECORDS_FILE}"
    )

if not CALIBRATION_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {CALIBRATION_FILE}"
    )



df_all = pd.read_csv(
    ALL_RECORDS_FILE,
    dtype=str,
    keep_default_na=False
)

df_calibration = pd.read_csv(
    CALIBRATION_FILE,
    dtype=str,
    keep_default_na=False
)


if len(df_all) != 587:
    raise ValueError(
        f"Esperados 587 registros deduplicados, "
        f"mas foram encontrados {len(df_all)}."
    )

if len(df_calibration) != 18:
    raise ValueError(
        f"Esperados 18 registros de calibração, "
        f"mas foram encontrados {len(df_calibration)}."
    )

if df_all["record_id"].duplicated().any():
    raise ValueError(
        "Existem record_id duplicados no conjunto de 587 registros."
    )

if df_calibration["record_id"].duplicated().any():
    raise ValueError(
        "Existem record_id duplicados no conjunto de calibração."
    )



calibration_ids = set(
    df_calibration["record_id"]
)

df_candidates = df_all[
    ~df_all["record_id"].isin(calibration_ids)
].copy()


if len(df_candidates) != 569:
    raise ValueError(
        f"Esperados 569 registros elegíveis para validação, "
        f"mas foram encontrados {len(df_candidates)}."
    )



df_validation = (
    df_candidates
    .sample(
        n=N_VALIDATION,
        random_state=RANDOM_SEED
    )
    .reset_index(drop=True)
)




df_validation.insert(
    0,
    "validation_id",
    [
        f"V{i:02d}"
        for i in range(
            1,
            N_VALIDATION + 1
        )
    ]
)



columns = [
    "validation_id",
    "record_id",
    "title",
    "abstract",
    "author_keywords",
    "index_keywords",
    "document_type",
    "document_identifier",
]

df_validation = df_validation[
    columns
].copy()




overlap = set(
    df_validation["record_id"]
).intersection(
    calibration_ids
)

if overlap:
    raise ValueError(
        f"ERRO: registros da calibração apareceram "
        f"na validação: {sorted(overlap)}"
    )


for forbidden_column in [
    "decision",
    "reason_code",
    "confidence",
    "rationale",
    "human_decision",
    "llm_decision",
]:
    if forbidden_column in df_validation.columns:
        raise ValueError(
            f"Coluna proibida encontrada: {forbidden_column}"
        )



VALIDATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

df_validation.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


all_records_sha256 = file_sha256(
    ALL_RECORDS_FILE
)

calibration_sha256 = file_sha256(
    CALIBRATION_FILE
)

validation_sha256 = file_sha256(
    OUTPUT_FILE
)

created_at = (
    datetime.now()
    .astimezone()
    .isoformat()
)


metadata = f"""INDEPENDENT VALIDATION SAMPLE — v1

Created at: {created_at}

SOURCE DATA

All records file: {ALL_RECORDS_FILE.name}
All records SHA256: {all_records_sha256}
Total deduplicated records: {len(df_all)}

DEVELOPMENT/CALIBRATION SET

Calibration file: {CALIBRATION_FILE.name}
Calibration SHA256: {calibration_sha256}
Calibration records excluded: {len(df_calibration)}

VALIDATION SAMPLING

Candidate pool after calibration exclusion: {len(df_candidates)}
Validation sample size: {N_VALIDATION}
Random seed: {RANDOM_SEED}
Sampling method: pandas.DataFrame.sample
Replacement: no

OUTPUT

Validation file: {OUTPUT_FILE.name}
Validation SHA256: {validation_sha256}
Validation records: {len(df_validation)}

BLINDING

Human decisions included: NO
LLM outputs included: NO
Calibration records included: NO

IMPORTANT

This sample is reserved for independent validation of the
LLM-assisted title/abstract screening procedure.

The 18 development/calibration records were excluded before sampling.
"""


with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:
    file.write(metadata)

print()
print("AMOSTRA INDEPENDENTE DE VALIDAÇÃO PREPARADA")
print("--------------------------------------------")
print(f"Registros totais: {len(df_all)}")
print(f"Registros de calibração excluídos: {len(df_calibration)}")
print(f"Pool disponível: {len(df_candidates)}")
print(f"Registros sorteados: {len(df_validation)}")
print(f"Seed: {RANDOM_SEED}")
print()
print(f"Sobreposição com calibração: {len(overlap)}")
print(
    f"Abstracts ausentes: "
    f"{(df_validation['abstract'].str.strip() == '').sum()}"
)
print()
print("Decisões humanas incluídas: NÃO")
print("Saídas do LLM incluídas: NÃO")
print()
print(f"Arquivo: {OUTPUT_FILE}")
print(f"Metadados: {METADATA_FILE}")