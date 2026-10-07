import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
)

RECORDS_FILE = (
    PROCESSED_DIR
    / "all_records_before_dedup.csv"
)

REVIEW_FILE = (
    PROCESSED_DIR
    / "deduplication_review.csv"
)

DEDUP_LOG_FILE = (
    PROCESSED_DIR
    / "deduplication_log.csv"
)

FINAL_FILE = (
    PROCESSED_DIR
    / "records_deduplicated.csv"
)




records = pd.read_csv(
    RECORDS_FILE,
    dtype=str,
    keep_default_na=False
)

review = pd.read_csv(
    REVIEW_FILE,
    dtype=str,
    keep_default_na=False
)



if len(records) != 704:
    raise ValueError(
        f"Esperados 704 registros antes da deduplicação, "
        f"mas foram encontrados {len(records)}."
    )

if len(review) != 121:
    raise ValueError(
        f"Esperados 121 pares candidatos, "
        f"mas foram encontrados {len(review)}."
    )



manual_mask = (
    review["match_basis"] == "exact_title"
)

review.loc[
    manual_mask,
    "review_decision"
] = "not_duplicate"

review.loc[
    manual_mask,
    "kept_record_id"
] = ""

review.loc[
    manual_mask,
    "removed_record_id"
] = ""

review.loc[
    manual_mask,
    "notes"
] = (
    "Manual bibliographic inspection confirmed distinct "
    "conference proceedings volumes. Records have different "
    "volume numbers, ISBNs and EIDs; therefore they were retained."
)

duplicates = review[
    review["review_decision"] == "duplicate"
].copy()

if len(duplicates) != 117:
    raise ValueError(
        f"Esperadas 117 duplicatas confirmadas por DOI, "
        f"mas foram encontradas {len(duplicates)}."
    )


removed_ids = (
    duplicates["removed_record_id"]
    .dropna()
    .astype(str)
    .str.strip()
)

removed_ids = [
    x for x in removed_ids
    if x
]


if len(set(removed_ids)) != 117:
    raise ValueError(
        "Os 117 pares de DOI não correspondem a "
        "117 registros únicos para remoção."
    )


all_ids = set(
    records["source_record_id"]
)

missing_ids = (
    set(removed_ids) - all_ids
)

if missing_ids:
    raise ValueError(
        f"IDs para remoção não encontrados: {missing_ids}"
    )



dedup_log_rows = []

for number, (_, row) in enumerate(
    duplicates.iterrows(),
    start=1
):

    dedup_log_rows.append({
        "duplicate_group_id":
            f"DUP_{number:04d}",

        "kept_record_id":
            row["kept_record_id"],

        "removed_record_id":
            row["removed_record_id"],

        "match_basis":
            "exact_normalized_doi",

        "decision":
            "duplicate_removed",

        "notes":
            (
                "Same normalized DOI in Scopus and IEEE Xplore. "
                "Scopus record retained according to the "
                "predefined source-precedence rule."
            ),
    })


dedup_log = pd.DataFrame(
    dedup_log_rows
)

dedup_log.to_csv(
    DEDUP_LOG_FILE,
    index=False,
    encoding="utf-8-sig"
)


deduplicated = records[
    ~records["source_record_id"].isin(
        removed_ids
    )
].copy()


if len(deduplicated) != 587:
    raise ValueError(
        f"Esperados 587 registros após deduplicação, "
        f"mas foram encontrados {len(deduplicated)}."
    )


deduplicated.insert(
    0,
    "record_id",
    [
        f"R{i:04d}"
        for i in range(
            1,
            len(deduplicated) + 1
        )
    ]
)



deduplicated.to_csv(
    FINAL_FILE,
    index=False,
    encoding="utf-8-sig"
)


review.to_csv(
    REVIEW_FILE,
    index=False,
    encoding="utf-8-sig"
)


scopus_final = (
    deduplicated["source_database"]
    == "Scopus"
).sum()

ieee_final = (
    deduplicated["source_database"]
    == "IEEE Xplore"
).sum()

manual_not_duplicates = (
    review["review_decision"]
    == "not_duplicate"
).sum()


print()
print("DEDUPLICAÇÃO FINALIZADA")
print("------------------------------")
print(f"Registros antes: {len(records)}")
print(
    f"Registros removidos por DOI: "
    f"{len(set(removed_ids))}"
)
print(
    f"Pares de título mantidos após revisão manual: "
    f"{manual_not_duplicates}"
)
print(f"Registros após deduplicação: {len(deduplicated)}")
print("------------------------------")
print()
print(f"Scopus preservados: {scopus_final}")
print(f"IEEE Xplore preservados: {ieee_final}")
print()
print(f"Log: {DEDUP_LOG_FILE}")
print(f"Base deduplicada: {FINAL_FILE}")
print()
print(
    "IDs de screening atribuídos: "
    "R0001 até R0587"
)