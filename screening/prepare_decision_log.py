import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    / "decision_log.csv"
)

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)
    records = list(reader)


if len(records) != 587:
    raise ValueError(
        f"Esperados 587 registros deduplicados, "
        f"mas foram encontrados {len(records)}."
    )



record_ids = [
    row["record_id"].strip()
    for row in records
]

expected_ids = [
    f"R{i:04d}"
    for i in range(1, 588)
]

if record_ids != expected_ids:
    raise ValueError(
        "Os record_id não correspondem à sequência "
        "R0001 até R0587."
    )


fieldnames = [
    "record_id",
    "stage",
    "decision",
    "reason_code",
    "notes",
    "date",
]


rows = []

for record_id in record_ids:

    rows.append({
        "record_id": record_id,
        "stage": "title_abstract",
        "decision": "",
        "reason_code": "",
        "notes": "",
        "date": "",
    })


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print("DECISION LOG PREPARADO")
print("------------------------------")
print(f"Registros criados: {len(rows)}")
print(f"Primeiro ID: {rows[0]['record_id']}")
print(f"Último ID: {rows[-1]['record_id']}")
print(f"Stage: title_abstract")
print()
print(f"Arquivo: {OUTPUT_FILE}")
print()
print("Nenhuma decisão de screening foi atribuída.")