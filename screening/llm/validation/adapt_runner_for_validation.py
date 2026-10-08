from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent
    / "run_validation_qwen3_4b_v1.py"
)

text = SCRIPT.read_text(encoding="utf-8")

replacements = {
    '''CALIBRATION_DIR = (
    LLM_DIR
    / "calibration"
)

INPUT_FILE = (
    CALIBRATION_DIR
    / "calibration_blind_v1.csv"
)''':
    '''VALIDATION_DIR = (
    LLM_DIR
    / "validation"
)

INPUT_FILE = (
    VALIDATION_DIR
    / "validation_blind_v1.csv"
)''',

    '''OUTPUT_FILE = (
    CALIBRATION_DIR
    / "llm_prescreen_calibration_qwen3_4b_full18.csv"
)

RUN_METADATA_FILE = (
    CALIBRATION_DIR
    / "calibration_run_metadata_qwen3_4b_full18.txt"
)''':
    '''OUTPUT_FILE = (
    VALIDATION_DIR
    / "validation_llm_qwen3_4b_v1.csv"
)

RUN_METADATA_FILE = (
    VALIDATION_DIR
    / "validation_run_metadata_qwen3_4b_v1.txt"
)''',

    '''if len(df) != 18:
    raise ValueError(
        f"Esperados 18 registros de calibração, "
        f"mas foram encontrados {len(df)}."
    )''':
    '''if len(df) != 30:
    raise ValueError(
        f"Esperados 30 registros de validacao, "
        f"mas foram encontrados {len(df)}."
    )

forbidden_columns = {
    "human_decision",
    "human_reason_code",
    "human_notes",
}

present_forbidden = forbidden_columns.intersection(df.columns)

if present_forbidden:
    raise ValueError(
        "O arquivo de entrada contem colunas humanas: "
        f"{sorted(present_forbidden)}"
    )''',

    '''calibration_id = clean(
        row["calibration_id"]
    )''':
    '''validation_id = clean(
        row["validation_id"]
    )''',

    '''f"{calibration_id} | "''':
    '''f"{validation_id} | "''',

    '''"calibration_id":
            calibration_id,''':
    '''"validation_id":
            validation_id,''',

    '''print("CALIBRAÇÃO CRITERIAL DO LLM")''':
    '''print("VALIDACAO CEGA CRITERIAL DO LLM")''',

    '''metadata = f"""LLM CALIBRATION RUN — v1.2

Run type: blind criterion-based calibration''':
    '''metadata = f"""LLM VALIDATION RUN - v1

Run type: blind criterion-based validation''',

    '''Expected records: 18''':
    '''Expected records: 30''',

    '''print("CALIBRAÇÃO CRITERIAL EXECUTADA")''':
    '''print("VALIDACAO CEGA CRITERIAL EXECUTADA")''',
}

for old, new in replacements.items():
    if old not in text:
        print("ATENCAO: trecho nao encontrado:")
        print(old[:120])
        print()
    else:
        text = text.replace(old, new)

SCRIPT.write_text(text, encoding="utf-8")

print("Runner adaptado:")
print(SCRIPT)