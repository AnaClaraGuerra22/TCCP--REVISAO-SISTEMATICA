from pathlib import Path
from datetime import datetime
import hashlib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

HUMAN_FILE = BASE_DIR / "validation_human_v1.xlsm"
SNAPSHOT_FILE = BASE_DIR / "validation_human_reference_v1.csv"
METADATA_FILE = BASE_DIR / "validation_human_metadata_v1.txt"

EXPECTED_RECORDS = 30

VALID_DECISIONS = {"include", "exclude", "maybe"}
VALID_REASON_CODES = {"CE1", "CE2", "CE3", "CE4"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


print("=" * 70)
print("CONGELAMENTO DA REFERÊNCIA HUMANA")
print("=" * 70)

if not HUMAN_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado:\n{HUMAN_FILE}"
    )



excel = pd.ExcelFile(HUMAN_FILE, engine="openpyxl")

preferred_sheet = "Validação Humana"

if preferred_sheet in excel.sheet_names:
    sheet_name = preferred_sheet
else:
    sheet_name = excel.sheet_names[0]

print(f"Planilha utilizada: {sheet_name}")

df = pd.read_excel(
    HUMAN_FILE,
    sheet_name=sheet_name,
    engine="openpyxl"
)

df = df.dropna(how="all").copy()

required_columns = [
    "validation_id",
    "record_id",
    "human_decision",
    "human_reason_code",
    "human_notes",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Colunas obrigatórias ausentes: {missing_columns}"
    )

df = df[df["validation_id"].notna()].copy()

# Normalização
for col in [
    "validation_id",
    "record_id",
    "human_decision",
    "human_reason_code",
    "human_notes",
]:
    df[col] = df[col].fillna("").astype(str).str.strip()

df["human_decision"] = df["human_decision"].str.lower()
df["human_reason_code"] = df["human_reason_code"].str.upper()



errors = []

if len(df) != EXPECTED_RECORDS:
    errors.append(
        f"Esperados {EXPECTED_RECORDS} registros, encontrados {len(df)}."
    )

if df["validation_id"].duplicated().any():
    duplicated = df.loc[
        df["validation_id"].duplicated(keep=False),
        "validation_id"
    ].tolist()

    errors.append(
        f"validation_id duplicado: {duplicated}"
    )

if df["record_id"].duplicated().any():
    duplicated = df.loc[
        df["record_id"].duplicated(keep=False),
        "record_id"
    ].tolist()

    errors.append(
        f"record_id duplicado: {duplicated}"
    )

invalid_decisions = sorted(
    set(df["human_decision"]) - VALID_DECISIONS
)

if invalid_decisions:
    errors.append(
        f"Decisões inválidas: {invalid_decisions}"
    )

exclude_rows = df["human_decision"] == "exclude"

invalid_exclusion_codes = df.loc[
    exclude_rows
    & ~df["human_reason_code"].isin(VALID_REASON_CODES),
    ["validation_id", "human_reason_code"]
]

if not invalid_exclusion_codes.empty:
    errors.append(
        "Registros exclude sem código CE1-CE4 válido:\n"
        + invalid_exclusion_codes.to_string(index=False)
    )

non_exclude_with_code = df.loc[
    (~exclude_rows)
    & (df["human_reason_code"] != ""),
    ["validation_id", "human_decision", "human_reason_code"]
]

if not non_exclude_with_code.empty:
    errors.append(
        "Registros include/maybe com código de exclusão:\n"
        + non_exclude_with_code.to_string(index=False)
    )

missing_notes = df.loc[
    df["human_notes"] == "",
    "validation_id"
].tolist()

if missing_notes:
    errors.append(
        f"Registros sem human_notes: {missing_notes}"
    )

if errors:
    print("\nERROS ENCONTRADOS:")
    for error in errors:
        print("\n-", error)

    raise SystemExit(
        "\nArquivo NÃO congelado. Corrija os erros primeiro."
    )



df.to_csv(
    SNAPSHOT_FILE,
    index=False,
    encoding="utf-8-sig"
)

human_hash = sha256_file(HUMAN_FILE)
snapshot_hash = sha256_file(SNAPSHOT_FILE)

counts = (
    df["human_decision"]
    .value_counts()
    .reindex(["include", "maybe", "exclude"], fill_value=0)
)

reason_counts = (
    df.loc[df["human_decision"] == "exclude", "human_reason_code"]
    .value_counts()
    .reindex(["CE1", "CE2", "CE3", "CE4"], fill_value=0)
)

now = datetime.now().astimezone().isoformat()

metadata = f"""HUMAN VALIDATION REFERENCE — v1

Created: {now}

SOURCE
File: {HUMAN_FILE.name}
SHA256: {human_hash}
Worksheet: {sheet_name}

REFERENCE SNAPSHOT
File: {SNAPSHOT_FILE.name}
SHA256: {snapshot_hash}

VALIDATION SET
Records: {len(df)}

DECISIONS
include: {counts["include"]}
maybe: {counts["maybe"]}
exclude: {counts["exclude"]}

EXCLUSION CODES
CE1: {reason_counts["CE1"]}
CE2: {reason_counts["CE2"]}
CE3: {reason_counts["CE3"]}
CE4: {reason_counts["CE4"]}

STATUS
Human/reference decisions finalized before inspection of Qwen3:4B
validation outputs.

The XLSM file is preserved as the reviewer-facing source.
The CSV snapshot is used only for deterministic comparison.

IMPORTANT
No Qwen3:4B validation output had been consulted when these
reference decisions were finalized.
"""

METADATA_FILE.write_text(
    metadata,
    encoding="utf-8"
)

print()
print("VALIDAÇÃO CONCLUÍDA.")
print()
print(f"Registros: {len(df)}")
print()
print("Distribuição:")
print(counts.to_string())
print()
print("Códigos de exclusão:")
print(reason_counts.to_string())
print()
print(f"SHA256 XLSM:")
print(human_hash)
print()
print(f"Snapshot criado:")
print(SNAPSHOT_FILE)
print()
print(f"Metadata criado:")
print(METADATA_FILE)