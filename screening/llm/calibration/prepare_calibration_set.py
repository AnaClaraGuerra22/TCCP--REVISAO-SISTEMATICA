import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "records_deduplicated.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "screening"
    / "llm"
    / "calibration"
    / "calibration_blind_v1.csv"
)



CALIBRATION_RECORDS = [
    ("C01", "R0051"),
    ("C02", "R0028"),
    ("C03", "R0133"),
    ("C04", "R0216"),
    ("C05", "R0277"),
    ("C06", "R0465"),
    ("C07", "R0559"),
    ("C08", "R0394"),
    ("C09", "R0169"),
    ("C10", "R0404"),
    ("C11", "R0583"),
    ("C12", "R0455"),
    ("C13", "R0141"),
    ("C14", "R0073"),
    ("C15", "R0486"),
    ("C16", "R0143"),
    ("C17", "R0196"),
    ("C18", "R0255"),
]


df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False
)


if len(df) != 587:
    raise ValueError(
        f"Esperados 587 registros deduplicados, "
        f"mas foram encontrados {len(df)}."
    )



rows = []

for calibration_id, record_id in CALIBRATION_RECORDS:

    match = df[
        df["record_id"] == record_id
    ]

    if len(match) != 1:
        raise ValueError(
            f"{record_id}: esperado exatamente 1 registro, "
            f"encontrados {len(match)}."
        )

    r = match.iloc[0]

    rows.append({
        "calibration_id": calibration_id,
        "record_id": record_id,
        "title": r["title"],
        "abstract": r["abstract"],
        "author_keywords": r["author_keywords"],
        "index_keywords": r["index_keywords"],
        "document_type": r["document_type"],
        "document_identifier": r["document_identifier"],
    })


calibration = pd.DataFrame(rows)


if len(calibration) != 18:
    raise ValueError(
        f"Esperados 18 registros de calibração, "
        f"mas foram encontrados {len(calibration)}."
    )

if calibration["record_id"].duplicated().any():
    raise ValueError(
        "Há record_id duplicado no conjunto de calibração."
    )

if calibration["calibration_id"].duplicated().any():
    raise ValueError(
        "Há calibration_id duplicado."
    )


missing_title = (
    calibration["title"]
    .str.strip()
    .eq("")
    .sum()
)

missing_abstract = (
    calibration["abstract"]
    .str.strip()
    .eq("")
    .sum()
)


calibration.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)




print()
print("CONJUNTO CEGO DE CALIBRAÇÃO PREPARADO")
print("--------------------------------------")
print(f"Registros: {len(calibration)}")
print(f"Títulos ausentes: {missing_title}")
print(f"Abstracts ausentes: {missing_abstract}")
print()
print("Campos enviados ao futuro LLM:")
print("- calibration_id")
print("- record_id")
print("- title")
print("- abstract")
print("- author_keywords")
print("- index_keywords")
print("- document_type")
print("- document_identifier")
print()
print("Decisões humanas incluídas: NÃO")
print()
print(f"Arquivo: {OUTPUT_FILE}")