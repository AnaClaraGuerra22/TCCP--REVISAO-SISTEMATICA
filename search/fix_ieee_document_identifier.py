import pandas as pd
from pathlib import Path
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
)

RAW_IEEE_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "raw"
    / "ieee"
    / "ieee_v1.0_2026-10-06.csv"
)

ALL_RECORDS_FILE = (
    PROCESSED_DIR
    / "all_records_before_dedup.csv"
)

DEDUP_FILE = (
    PROCESSED_DIR
    / "records_deduplicated.csv"
)




ALL_RECORDS_BACKUP = (
    PROCESSED_DIR
    / "all_records_before_dedup_before_metadata_fix.csv"
)

DEDUP_BACKUP = (
    PROCESSED_DIR
    / "records_deduplicated_before_metadata_fix.csv"
)



def normalize_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()



all_records = pd.read_csv(
    ALL_RECORDS_FILE,
    dtype=str,
    keep_default_na=False
)

dedup = pd.read_csv(
    DEDUP_FILE,
    dtype=str,
    keep_default_na=False
)

ieee_raw = pd.read_csv(
    RAW_IEEE_FILE,
    dtype=str,
    keep_default_na=False
)



if len(all_records) != 704:
    raise ValueError(
        f"Esperados 704 registros em all_records_before_dedup.csv, "
        f"mas foram encontrados {len(all_records)}."
    )

if len(dedup) != 587:
    raise ValueError(
        f"Esperados 587 registros em records_deduplicated.csv, "
        f"mas foram encontrados {len(dedup)}."
    )

if len(ieee_raw) != 230:
    raise ValueError(
        f"Esperados 230 registros no CSV bruto do IEEE, "
        f"mas foram encontrados {len(ieee_raw)}."
    )

required_ieee_columns = [
    "Document Title",
    "Document Identifier",
]

for col in required_ieee_columns:
    if col not in ieee_raw.columns:
        raise ValueError(
            f"Coluna obrigatória ausente no IEEE bruto: {col}"
        )




if not ALL_RECORDS_BACKUP.exists():
    shutil.copy2(
        ALL_RECORDS_FILE,
        ALL_RECORDS_BACKUP
    )

if not DEDUP_BACKUP.exists():
    shutil.copy2(
        DEDUP_FILE,
        DEDUP_BACKUP
    )


ieee_mapping = {}

for i, row in ieee_raw.iterrows():

    source_record_id = f"IEEE_{i + 1:04d}"

    ieee_mapping[source_record_id] = {
        "document_identifier":
            normalize_text(
                row.get("Document Identifier", "")
            ),
        "raw_title":
            normalize_text(
                row.get("Document Title", "")
            ),
    }




def fix_dataframe(df, name):

    original_columns = list(df.columns)

    original_ids = None

    if "record_id" in df.columns:
        original_ids = df["record_id"].tolist()

    original_source_ids = (
        df["source_record_id"].tolist()
    )

    if "document_identifier" not in df.columns:

        insert_position = (
            df.columns.get_loc("document_type") + 1
        )

        df.insert(
            insert_position,
            "document_identifier",
            ""
        )

    ieee_mask = (
        df["source_database"]
        == "IEEE Xplore"
    )

    scopus_mask = (
        df["source_database"]
        == "Scopus"
    )

    ieee_count = ieee_mask.sum()

    print()
    print(f"{name}")
    print("-" * len(name))
    print(
        f"Registros Scopus: {scopus_mask.sum()}"
    )
    print(
        f"Registros IEEE: {ieee_count}"
    )

    missing_mapping = []
    title_mismatches = []


    for idx in df[ieee_mask].index:

        source_id = df.at[
            idx,
            "source_record_id"
        ]

        if source_id not in ieee_mapping:
            missing_mapping.append(
                source_id
            )
            continue

        mapping = ieee_mapping[source_id]

        current_title = normalize_text(
            df.at[idx, "title"]
        )

        raw_title = mapping[
            "raw_title"
        ]

        if (
            current_title
            and raw_title
            and current_title != raw_title
        ):
            title_mismatches.append({
                "source_record_id":
                    source_id,
                "processed_title":
                    current_title,
                "raw_title":
                    raw_title,
            })

        df.at[
            idx,
            "document_identifier"
        ] = mapping[
            "document_identifier"
        ]

        df.at[
            idx,
            "document_type"
        ] = ""


    df.loc[
        scopus_mask,
        "document_identifier"
    ] = ""


    if missing_mapping:
        raise ValueError(
            "Registros IEEE sem correspondência no CSV bruto: "
            + ", ".join(missing_mapping)
        )

    if title_mismatches:

        print()
        print(
            "ATENÇÃO: foram encontrados títulos diferentes "
            "entre o consolidado e o bruto do IEEE."
        )

        for item in title_mismatches[:10]:

            print()
            print(
                item["source_record_id"]
            )
            print(
                "Processado:",
                item["processed_title"]
            )
            print(
                "Bruto:",
                item["raw_title"]
            )

        raise ValueError(
            f"Foram encontrados "
            f"{len(title_mismatches)} "
            f"títulos divergentes."
        )

    if (
        df["source_record_id"].tolist()
        != original_source_ids
    ):
        raise ValueError(
            "A sequência de source_record_id foi alterada."
        )

    if original_ids is not None:

        if df["record_id"].tolist() != original_ids:
            raise ValueError(
                "A sequência de record_id foi alterada."
            )

    print(
        "Mapeamento IEEE verificado: OK"
    )

    return df



all_records_fixed = fix_dataframe(
    all_records.copy(),
    "all_records_before_dedup.csv"
)

dedup_fixed = fix_dataframe(
    dedup.copy(),
    "records_deduplicated.csv"
)




if len(all_records_fixed) != 704:
    raise ValueError(
        "Número de registros alterado em "
        "all_records_before_dedup.csv."
    )

if len(dedup_fixed) != 587:
    raise ValueError(
        "Número de registros alterado em "
        "records_deduplicated.csv."
    )

ieee_dedup = (
    dedup_fixed["source_database"]
    == "IEEE Xplore"
).sum()

scopus_dedup = (
    dedup_fixed["source_database"]
    == "Scopus"
).sum()

if ieee_dedup != 113:
    raise ValueError(
        f"Esperados 113 registros IEEE após deduplicação, "
        f"mas foram encontrados {ieee_dedup}."
    )

if scopus_dedup != 474:
    raise ValueError(
        f"Esperados 474 registros Scopus após deduplicação, "
        f"mas foram encontrados {scopus_dedup}."
    )


ieee_document_type_nonempty = (
    dedup_fixed.loc[
        dedup_fixed["source_database"]
        == "IEEE Xplore",
        "document_type"
    ]
    .astype(str)
    .str.strip()
    .ne("")
    .sum()
)

if ieee_document_type_nonempty != 0:
    raise ValueError(
        "Ainda existem registros IEEE com document_type preenchido."
    )


ieee_identifier_filled = (
    dedup_fixed.loc[
        dedup_fixed["source_database"]
        == "IEEE Xplore",
        "document_identifier"
    ]
    .astype(str)
    .str.strip()
    .ne("")
    .sum()
)




all_records_fixed.to_csv(
    ALL_RECORDS_FILE,
    index=False,
    encoding="utf-8-sig"
)

dedup_fixed.to_csv(
    DEDUP_FILE,
    index=False,
    encoding="utf-8-sig"
)


print()
print("CORREÇÃO DE METADADOS CONCLUÍDA")
print("--------------------------------")
print(
    "all_records_before_dedup.csv: 704 registros"
)
print(
    "records_deduplicated.csv: 587 registros"
)
print(
    f"Scopus após deduplicação: {scopus_dedup}"
)
print(
    f"IEEE após deduplicação: {ieee_dedup}"
)
print(
    "IEEE com document_type preenchido: 0"
)
print(
    f"IEEE com document_identifier preenchido: "
    f"{ieee_identifier_filled}"
)
print("--------------------------------")
print()
print("IDs R0001-R0587 preservados: yes")
print("source_record_id preservados: yes")
print()
print("Backups criados:")
print(ALL_RECORDS_BACKUP)
print(DEDUP_BACKUP)
print()
print("Arquivos corrigidos:")
print(ALL_RECORDS_FILE)
print(DEDUP_FILE)