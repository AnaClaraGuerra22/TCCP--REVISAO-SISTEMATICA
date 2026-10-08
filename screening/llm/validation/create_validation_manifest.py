from pathlib import Path
import hashlib
from datetime import datetime

BASE = Path(__file__).resolve().parent
LLM_DIR = BASE.parent

FILES = [
    BASE / "validation_blind_v1.csv",
    BASE / "validation_human_v1.xlsm",
    BASE / "validation_human_reference_v1.csv",
    BASE / "validation_human_metadata_v1.txt",
    BASE / "validation_gate_v1.txt",
    BASE / "validation_llm_qwen3_4b_v1.csv",
    BASE / "validation_run_metadata_qwen3_4b_v1.txt",
    BASE / "validation_comparison_v1.csv",
    BASE / "validation_mismatches_v1.csv",
    BASE / "validation_confusion_matrix_v1.csv",
    BASE / "validation_comparison_summary_v1.txt",
    BASE / "validation_summary_v1.md",
    LLM_DIR / "llm_screening_prompt_v1_2_candidate.txt",
    LLM_DIR / "llm_screening_prompt_v1_2_operational.txt",
]


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()


missing = [
    path for path in FILES
    if not path.exists()
]

if missing:
    print("ARQUIVOS AUSENTES:")

    for path in missing:
        print(path)

    raise SystemExit(
        "Manifesto nao criado."
    )


lines = [
    "LLM VALIDATION MANIFEST - v1",
    "",
    f"Created: {datetime.now().astimezone().isoformat()}",
    "",
    "FINAL STATUS: PASS",
    "",
]

for path in FILES:
    lines.append(
        f"{path.name}\t{sha256(path)}"
    )

output = (
    BASE
    / "validation_manifest_v1.txt"
)

output.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print(
    output.read_text(
        encoding="utf-8"
    )
)