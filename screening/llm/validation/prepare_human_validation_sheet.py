from pathlib import Path
import pandas as pd

VALIDATION_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    VALIDATION_DIR
    / "validation_blind_v1.csv"
)

OUTPUT_FILE = (
    VALIDATION_DIR
    / "validation_human_v1.csv"
)


df = pd.read_csv(
    INPUT_FILE,
    dtype=str,
    keep_default_na=False
)


if len(df) != 30:
    raise ValueError(
        f"Esperados 30 registros, "
        f"mas foram encontrados {len(df)}."
    )

if df["record_id"].duplicated().any():
    raise ValueError(
        "Existem record_id duplicados."
    )



df["human_decision"] = ""
df["human_reason_code"] = ""
df["human_notes"] = ""




df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)



print()
print("PLANILHA HUMANA DE VALIDAÇÃO CRIADA")
print("-----------------------------------")
print(f"Registros: {len(df)}")
print()
print("Campos adicionados:")
print("- human_decision")
print("- human_reason_code")
print("- human_notes")
print()
print("Decisões do LLM presentes: NÃO")
print()
print(f"Arquivo: {OUTPUT_FILE}")