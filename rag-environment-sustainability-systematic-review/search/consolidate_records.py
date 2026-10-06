import csv
import re
import unicodedata
from pathlib import Path


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SCOPUS_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "raw"
    / "scopus"
    / "scopus_v1.0_2026-10-06.csv"
)

IEEE_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "raw"
    / "ieee"
    / "ieee_v1.0_2026-10-06.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "all_records_before_dedup.csv"
)


# ============================================================
# NORMALIZAÇÃO AUXILIAR
# ============================================================

def normalize_doi(doi):
    """
    Normaliza DOI apenas para comparação.
    O DOI original continua preservado na coluna 'doi'.
    """
    if not doi:
        return ""

    doi = doi.strip().lower()

    prefixes = [
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "doi:",
    ]

    for prefix in prefixes:
        if doi.startswith(prefix):
            doi = doi[len(prefix):].strip()

    return doi


def normalize_title(title):
    """
    Normaliza título apenas para identificação de possíveis duplicatas.
    O título original continua preservado.
    """
    if not title:
        return ""

    title = unicodedata.normalize("NFKC", title)
    title = title.casefold()

    # Substitui pontuação por espaço.
    title = re.sub(r"[^\w\s]", " ", title)

    # Colapsa espaços consecutivos.
    title = re.sub(r"\s+", " ", title).strip()

    return title


# ============================================================
# LEITURA SCOPUS
# ============================================================

def read_scopus():
    records = []

    with open(
        SCOPUS_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for i, row in enumerate(reader, start=1):

            record = {
                "source_database": "Scopus",
                "source_record_id": f"SCOPUS_{i:04d}",

                "title": row.get("Title", "").strip(),
                "authors": row.get("Authors", "").strip(),
                "year": row.get("Year", "").strip(),
                "source_title": row.get("Source title", "").strip(),

                "doi": row.get("DOI", "").strip(),
                "abstract": row.get("Abstract", "").strip(),

                "author_keywords": row.get(
                    "Author Keywords", ""
                ).strip(),

                "index_keywords": row.get(
                    "Index Keywords", ""
                ).strip(),

                "document_type": row.get(
                    "Document Type", ""
                ).strip(),

                "language": row.get(
                    "Language of Original Document", ""
                ).strip(),

                "url": row.get("Link", "").strip(),

                # Identificador original da Scopus
                "native_id": row.get("EID", "").strip(),
            }

            record["doi_normalized"] = normalize_doi(
                record["doi"]
            )

            record["title_normalized"] = normalize_title(
                record["title"]
            )

            records.append(record)

    return records


# ============================================================
# LEITURA IEEE
# ============================================================

def read_ieee():
    records = []

    with open(
        IEEE_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for i, row in enumerate(reader, start=1):

            record = {
                "source_database": "IEEE Xplore",
                "source_record_id": f"IEEE_{i:04d}",

                "title": row.get(
                    "Document Title", ""
                ).strip(),

                "authors": row.get("Authors", "").strip(),

                "year": row.get(
                    "Publication Year", ""
                ).strip(),

                "source_title": row.get(
                    "Publication Title", ""
                ).strip(),

                "doi": row.get("DOI", "").strip(),

                "abstract": row.get(
                    "Abstract", ""
                ).strip(),

                "author_keywords": row.get(
                    "Author Keywords", ""
                ).strip(),

                "index_keywords": row.get(
                    "IEEE Terms", ""
                ).strip(),

                # IEEE não fornece aqui um campo equivalente
                # direto ao Document Type da Scopus.
                "document_type": row.get(
                    "Document Identifier", ""
                ).strip(),

                "language": "",

                "url": row.get(
                    "PDF Link", ""
                ).strip(),

                # Não usamos Document Identifier como identificador
                # único, pois ele pode representar a coleção/tipo.
                "native_id": "",
            }

            record["doi_normalized"] = normalize_doi(
                record["doi"]
            )

            record["title_normalized"] = normalize_title(
                record["title"]
            )

            records.append(record)

    return records


# ============================================================
# CONSOLIDAÇÃO
# ============================================================

def main():

    scopus_records = read_scopus()
    ieee_records = read_ieee()

    print(f"Scopus: {len(scopus_records)} registros")
    print(f"IEEE Xplore: {len(ieee_records)} registros")

    if len(scopus_records) != 474:
        raise ValueError(
            f"Esperados 474 registros da Scopus, "
            f"mas foram encontrados {len(scopus_records)}."
        )

    if len(ieee_records) != 230:
        raise ValueError(
            f"Esperados 230 registros do IEEE, "
            f"mas foram encontrados {len(ieee_records)}."
        )

    all_records = scopus_records + ieee_records

    if len(all_records) != 704:
        raise ValueError(
            f"Esperados 704 registros consolidados, "
            f"mas foram encontrados {len(all_records)}."
        )

    fieldnames = [
        "source_database",
        "source_record_id",
        "title",
        "authors",
        "year",
        "source_title",
        "doi",
        "doi_normalized",
        "abstract",
        "author_keywords",
        "index_keywords",
        "document_type",
        "language",
        "url",
        "native_id",
        "title_normalized",
    ]

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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
        writer.writerows(all_records)

    print()
    print("Consolidação concluída.")
    print(f"Total: {len(all_records)} registros")
    print(f"Arquivo: {OUTPUT_FILE}")

    dois_scopus = sum(
        1 for r in scopus_records
        if r["doi_normalized"]
    )

    dois_ieee = sum(
        1 for r in ieee_records
        if r["doi_normalized"]
    )

    print()
    print(f"Scopus com DOI: {dois_scopus}")
    print(f"IEEE com DOI: {dois_ieee}")


if __name__ == "__main__":
    main()