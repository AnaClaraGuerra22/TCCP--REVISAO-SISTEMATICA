import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RECORDS_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "all_records_before_dedup.csv"
)

CANDIDATES_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "deduplication_candidates.csv"
)

REVIEW_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "deduplication_review.csv"
)

MANUAL_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "manual_duplicate_groups.csv"
)


records = pd.read_csv(
    RECORDS_FILE,
    dtype=str,
    keep_default_na=False
)

candidates = pd.read_csv(
    CANDIDATES_FILE,
    dtype=str,
    keep_default_na=False
)



review = candidates.copy()

review["review_decision"] = ""
review["kept_record_id"] = ""
review["removed_record_id"] = ""
review["notes"] = ""


for idx, row in review.iterrows():


    if row["match_basis"] == "exact_doi":

        review.at[idx, "review_decision"] = "duplicate"


        if (
            row["database_1"] == "Scopus"
            and row["database_2"] == "IEEE Xplore"
        ):

            review.at[
                idx, "kept_record_id"
            ] = row["record_id_1"]

            review.at[
                idx, "removed_record_id"
            ] = row["record_id_2"]

        elif (
            row["database_2"] == "Scopus"
            and row["database_1"] == "IEEE Xplore"
        ):

            review.at[
                idx, "kept_record_id"
            ] = row["record_id_2"]

            review.at[
                idx, "removed_record_id"
            ] = row["record_id_1"]

        else:
            raise ValueError(
                "Caso exact_doi inesperado: "
                f"{row['candidate_id']}"
            )

        review.at[
            idx, "notes"
        ] = (
            "Exact normalized DOI match. "
            "Cross-database duplicate. "
            "Scopus record retained according to "
            "the predefined deduplication precedence rule."
        )



    elif row["match_basis"] == "exact_title":

        review.at[
            idx, "review_decision"
        ] = "manual_review"

        review.at[
            idx, "notes"
        ] = (
            "Exact normalized title without matching DOI. "
            "Manual inspection required before deduplication."
        )


review.to_csv(
    REVIEW_FILE,
    index=False,
    encoding="utf-8-sig"
)



manual_candidates = review[
    review["review_decision"] == "manual_review"
].copy()


parent = {}


def find(x):
    parent.setdefault(x, x)

    if parent[x] != x:
        parent[x] = find(parent[x])

    return parent[x]


def union(a, b):
    root_a = find(a)
    root_b = find(b)

    if root_a != root_b:
        parent[root_b] = root_a


for _, row in manual_candidates.iterrows():

    id1 = row["record_id_1"]
    id2 = row["record_id_2"]

    union(id1, id2)


groups = {}

for record_id in parent:
    root = find(record_id)

    groups.setdefault(
        root,
        []
    ).append(record_id)



manual_rows = []

for group_number, ids in enumerate(
    groups.values(),
    start=1
):

    group_id = f"MANUAL_{group_number:02d}"

    for record_id in sorted(ids):

        record = records[
            records["source_record_id"] == record_id
        ]

        if len(record) != 1:
            raise ValueError(
                f"Registro não encontrado ou duplicado: "
                f"{record_id}"
            )

        r = record.iloc[0]

        manual_rows.append({
            "manual_group_id": group_id,
            "source_record_id":
                r["source_record_id"],
            "source_database":
                r["source_database"],
            "title":
                r["title"],
            "authors":
                r["authors"],
            "year":
                r["year"],
            "source_title":
                r["source_title"],
            "doi":
                r["doi"],
            "document_type":
                r["document_type"],
            "native_id":
                r["native_id"],
            "abstract":
                r["abstract"],
            "manual_decision":
                "",
            "notes":
                "",
        })


manual_df = pd.DataFrame(manual_rows)

manual_df.to_csv(
    MANUAL_FILE,
    index=False,
    encoding="utf-8-sig"
)


accepted = (
    review["review_decision"]
    == "duplicate"
).sum()

manual_pairs = (
    review["review_decision"]
    == "manual_review"
).sum()


print()
print("PREPARAÇÃO DA DEDUPLICAÇÃO CONCLUÍDA")
print("------------------------------------")
print(
    f"Duplicatas por DOI aceitas: {accepted}"
)
print(
    f"Pares enviados para revisão manual: "
    f"{manual_pairs}"
)
print(
    f"Grupos manuais únicos: {len(groups)}"
)
print(
    f"Registros nos grupos manuais: "
    f"{len(manual_df)}"
)
print("------------------------------------")
print()
print(f"Arquivo de revisão: {REVIEW_FILE}")
print(f"Casos manuais: {MANUAL_FILE}")
print()
print("Nenhum registro foi removido.")