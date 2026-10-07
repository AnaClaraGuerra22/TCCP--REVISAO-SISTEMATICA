import csv
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "all_records_before_dedup.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "deduplication_candidates.csv"
)


def title_similarity(title1, title2):
    """
    Similaridade entre títulos já normalizados.
    Retorna valor entre 0 e 1.
    """
    if not title1 or not title2:
        return 0.0

    return SequenceMatcher(
        None,
        title1,
        title2
    ).ratio()


def same_year(record1, record2):
    """
    Verifica se os registros possuem o mesmo ano.
    """
    year1 = record1.get("year", "").strip()
    year2 = record2.get("year", "").strip()

    return bool(year1 and year2 and year1 == year2)



def read_records():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))



def main():

    records = read_records()

    print(f"Registros carregados: {len(records)}")

    if len(records) != 704:
        raise ValueError(
            f"Esperados 704 registros, "
            f"mas foram encontrados {len(records)}."
        )

    candidates = []

    seen_pairs = set()

    doi_matches = 0
    exact_title_matches = 0
    fuzzy_title_matches = 0



    for i in range(len(records)):

        r1 = records[i]

        for j in range(i + 1, len(records)):

            r2 = records[j]

            id1 = r1["source_record_id"]
            id2 = r2["source_record_id"]

            pair = tuple(sorted([id1, id2]))

            doi1 = r1.get(
                "doi_normalized", ""
            ).strip()

            doi2 = r2.get(
                "doi_normalized", ""
            ).strip()

            title1 = r1.get(
                "title_normalized", ""
            ).strip()

            title2 = r2.get(
                "title_normalized", ""
            ).strip()

            match_basis = None
            similarity = ""

            if (
                doi1
                and doi2
                and doi1 == doi2
            ):
                match_basis = "exact_doi"
                similarity = "1.0000"
                doi_matches += 1


            elif (
                title1
                and title2
                and title1 == title2
            ):
                match_basis = "exact_title"
                similarity = "1.0000"
                exact_title_matches += 1
            elif (
                title1
                and title2
                and len(title1) >= 25
                and len(title2) >= 25
                and same_year(r1, r2)
            ):

                sim = title_similarity(
                    title1,
                    title2
                )

                if sim >= 0.94:
                    match_basis = "fuzzy_title_same_year"
                    similarity = f"{sim:.4f}"
                    fuzzy_title_matches += 1


            if match_basis and pair not in seen_pairs:

                seen_pairs.add(pair)

                candidates.append({
                    "candidate_id":
                        f"DUP_{len(candidates) + 1:04d}",

                    "record_id_1":
                        id1,

                    "database_1":
                        r1.get("source_database", ""),

                    "title_1":
                        r1.get("title", ""),

                    "year_1":
                        r1.get("year", ""),

                    "doi_1":
                        r1.get("doi", ""),

                    "record_id_2":
                        id2,

                    "database_2":
                        r2.get("source_database", ""),

                    "title_2":
                        r2.get("title", ""),

                    "year_2":
                        r2.get("year", ""),

                    "doi_2":
                        r2.get("doi", ""),

                    "match_basis":
                        match_basis,

                    "title_similarity":
                        similarity,

                    "review_decision":
                        "",

                    "kept_record_id":
                        "",

                    "removed_record_id":
                        "",

                    "notes":
                        "",
                })


    fieldnames = [
        "candidate_id",
        "record_id_1",
        "database_1",
        "title_1",
        "year_1",
        "doi_1",
        "record_id_2",
        "database_2",
        "title_2",
        "year_2",
        "doi_2",
        "match_basis",
        "title_similarity",
        "review_decision",
        "kept_record_id",
        "removed_record_id",
        "notes",
    ]

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
        writer.writerows(candidates)


    print()
    print("DETECÇÃO DE DUPLICATAS CONCLUÍDA")
    print("--------------------------------")
    print(f"DOI exato: {doi_matches}")
    print(
        f"Título normalizado exato: "
        f"{exact_title_matches}"
    )
    print(
        f"Título semelhante + mesmo ano: "
        f"{fuzzy_title_matches}"
    )
    print("--------------------------------")
    print(
        f"Total de pares candidatos: "
        f"{len(candidates)}"
    )
    print()
    print(f"Arquivo: {OUTPUT_FILE}")
    print()
    print(
        "IMPORTANTE: nenhum registro foi removido."
    )


if __name__ == "__main__":
    main()