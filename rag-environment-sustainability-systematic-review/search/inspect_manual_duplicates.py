import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SCOPUS_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "raw"
    / "scopus"
    / "scopus_v1.0_2026-10-06.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "search"
    / "exports"
    / "processed"
    / "manual_duplicate_groups_detail.csv"
)


TARGETS = {
    "SCOPUS_0172": 172,
    "SCOPUS_0211": 211,
    "SCOPUS_0218": 218,
    "SCOPUS_0451": 451,
    "SCOPUS_0474": 474,
}


df = pd.read_csv(
    SCOPUS_FILE,
    dtype=str,
    keep_default_na=False
)

rows = []

for record_id, row_number in TARGETS.items():

    r = df.iloc[row_number - 1]

    rows.append({
        "source_record_id": record_id,
        "Title": r.get("Title", ""),
        "Year": r.get("Year", ""),
        "Source title": r.get("Source title", ""),
        "Volume": r.get("Volume", ""),
        "Issue": r.get("Issue", ""),
        "Art. No.": r.get("Art. No.", ""),
        "Page start": r.get("Page start", ""),
        "Page end": r.get("Page end", ""),
        "DOI": r.get("DOI", ""),
        "ISBN": r.get("ISBN", ""),
        "ISSN": r.get("ISSN", ""),
        "Publisher": r.get("Publisher", ""),
        "Document Type": r.get("Document Type", ""),
        "EID": r.get("EID", ""),
        "Abstract": r.get("Abstract", ""),
    })


out = pd.DataFrame(rows)

out.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


print()
print("INSPEÇÃO DOS CASOS MANUAIS")
print("--------------------------")

for _, r in out.iterrows():

    print()
    print(r["source_record_id"])
    print(f"Title: {r['Title']}")
    print(f"Volume: {r['Volume']}")
    print(f"Issue: {r['Issue']}")
    print(f"Pages: {r['Page start']} - {r['Page end']}")
    print(f"ISBN: {r['ISBN']}")
    print(f"DOI: {r['DOI']}")
    print(f"EID: {r['EID']}")

print()
print(f"Arquivo gerado: {OUTPUT_FILE}")
print()
print("Nenhum registro foi removido.")