from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

HUMAN_FILE = BASE_DIR / "validation_human_reference_v1.csv"
LLM_FILE = BASE_DIR / "validation_llm_qwen3_4b_v1.csv"

COMPARISON_FILE = BASE_DIR / "validation_comparison_v1.csv"
MISMATCH_FILE = BASE_DIR / "validation_mismatches_v1.csv"
CONFUSION_FILE = BASE_DIR / "validation_confusion_matrix_v1.csv"
SUMMARY_FILE = BASE_DIR / "validation_comparison_summary_v1.txt"

EXPECTED_RECORDS = 30

CLASSES = [
    "include",
    "maybe",
    "exclude",
]


def normalize(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )


# =========================================================
# LEITURA
# =========================================================

human = pd.read_csv(
    HUMAN_FILE,
    encoding="utf-8-sig"
)

llm = pd.read_csv(
    LLM_FILE,
    encoding="utf-8-sig"
)

# =========================================================
# CHECAGENS ESTRUTURAIS
# =========================================================

if len(human) != EXPECTED_RECORDS:
    raise ValueError(
        f"Referencia humana possui {len(human)} registros; "
        f"esperados {EXPECTED_RECORDS}."
    )

if len(llm) != EXPECTED_RECORDS:
    raise ValueError(
        f"Saida do Qwen possui {len(llm)} registros; "
        f"esperados {EXPECTED_RECORDS}."
    )

required_human = {
    "validation_id",
    "record_id",
    "human_decision",
    "human_reason_code",
}

required_llm = {
    "validation_id",
    "record_id",
    "derived_decision",
    "derived_reason_code",
    "status",
}

missing_human = required_human - set(human.columns)
missing_llm = required_llm - set(llm.columns)

if missing_human:
    raise ValueError(
        f"Colunas ausentes na referencia humana: "
        f"{sorted(missing_human)}"
    )

if missing_llm:
    raise ValueError(
        f"Colunas ausentes na saida Qwen: "
        f"{sorted(missing_llm)}"
    )

if human["validation_id"].duplicated().any():
    raise ValueError(
        "validation_id duplicado na referencia humana."
    )

if llm["validation_id"].duplicated().any():
    raise ValueError(
        "validation_id duplicado na saida Qwen."
    )

if human["record_id"].duplicated().any():
    raise ValueError(
        "record_id duplicado na referencia humana."
    )

if llm["record_id"].duplicated().any():
    raise ValueError(
        "record_id duplicado na saida Qwen."
    )

# =========================================================
# NORMALIZACAO
# =========================================================

human["human_decision"] = normalize(
    human["human_decision"]
)

human["human_reason_code"] = (
    human["human_reason_code"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

llm["llm_decision"] = normalize(
    llm["derived_decision"]
)

llm["llm_reason_code"] = (
    llm["derived_reason_code"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

llm["status_normalized"] = normalize(
    llm["status"]
)

invalid_human = (
    set(human["human_decision"])
    - set(CLASSES)
)

invalid_llm = (
    set(llm["llm_decision"])
    - set(CLASSES)
)

if invalid_human:
    raise ValueError(
        f"Decisoes humanas invalidas: "
        f"{sorted(invalid_human)}"
    )

if invalid_llm:
    raise ValueError(
        f"Decisoes Qwen invalidas: "
        f"{sorted(invalid_llm)}"
    )

# =========================================================
# MERGE CEGO PELOS IDs
# =========================================================

llm_columns = [
    "validation_id",
    "record_id",
    "llm_decision",
    "llm_reason_code",
    "status_normalized",
]

optional_columns = [
    "primary_study",
    "primary_study_evidence",
    "operational_rag",
    "operational_rag_evidence",
    "environmental_domain",
    "environmental_domain_evidence",
    "empirical_evaluation",
    "empirical_evaluation_evidence",
    "rag_role",
    "elapsed_seconds",
]

for column in optional_columns:
    if column in llm.columns:
        llm_columns.append(column)

merged = human.merge(
    llm[llm_columns],
    on=[
        "validation_id",
        "record_id",
    ],
    how="outer",
    validate="one_to_one",
    indicator=True,
)

not_matched = merged[
    merged["_merge"] != "both"
]

if not not_matched.empty:
    raise ValueError(
        "Existem registros nao correspondentes entre "
        "humano e Qwen:\n"
        + not_matched[
            [
                "validation_id",
                "record_id",
                "_merge",
            ]
        ].to_string(index=False)
    )

merged = merged.drop(
    columns="_merge"
)

# =========================================================
# CONCORDANCIA EXATA
# =========================================================

merged["exact_match"] = (
    merged["human_decision"]
    == merged["llm_decision"]
)

exact_n = int(
    merged["exact_match"].sum()
)

exact_agreement = (
    exact_n / len(merged)
)

# =========================================================
# MATRIZ DE CONFUSAO
# =========================================================

confusion = pd.crosstab(
    merged["human_decision"],
    merged["llm_decision"],
    rownames=["Human"],
    colnames=["Qwen"],
    dropna=False,
)

confusion = confusion.reindex(
    index=CLASSES,
    columns=CLASSES,
    fill_value=0,
)

# =========================================================
# COHEN'S KAPPA MANUAL
# =========================================================

observed = exact_agreement

human_props = (
    merged["human_decision"]
    .value_counts(normalize=True)
    .reindex(
        CLASSES,
        fill_value=0
    )
)

llm_props = (
    merged["llm_decision"]
    .value_counts(normalize=True)
    .reindex(
        CLASSES,
        fill_value=0
    )
)

expected = sum(
    human_props[c]
    * llm_props[c]
    for c in CLASSES
)

if expected < 1:
    kappa = (
        (observed - expected)
        / (1 - expected)
    )
else:
    kappa = float("nan")

# =========================================================
# METRICAS DE SEGURANCA
# =========================================================

human_include = (
    merged["human_decision"]
    == "include"
)

human_maybe = (
    merged["human_decision"]
    == "maybe"
)

human_exclude = (
    merged["human_decision"]
    == "exclude"
)

human_retained = (
    merged["human_decision"]
    .isin(
        [
            "include",
            "maybe",
        ]
    )
)

qwen_exclude = (
    merged["llm_decision"]
    == "exclude"
)

include_to_exclude = int(
    (
        human_include
        & qwen_exclude
    ).sum()
)

maybe_to_exclude = int(
    (
        human_maybe
        & qwen_exclude
    ).sum()
)

false_exclusions_retained = int(
    (
        human_retained
        & qwen_exclude
    ).sum()
)

n_human_include = int(
    human_include.sum()
)

n_human_maybe = int(
    human_maybe.sum()
)

n_human_exclude = int(
    human_exclude.sum()
)

n_human_retained = int(
    human_retained.sum()
)

retained_correctly = (
    n_human_retained
    - false_exclusions_retained
)

if n_human_retained > 0:
    retention_sensitivity = (
        retained_correctly
        / n_human_retained
    )
else:
    retention_sensitivity = float("nan")

# =========================================================
# ACORDO DOS CODIGOS CE
# =========================================================

both_exclude = (
    (merged["human_decision"] == "exclude")
    &
    (merged["llm_decision"] == "exclude")
)

n_both_exclude = int(
    both_exclude.sum()
)

if n_both_exclude > 0:

    ce_match = (
        merged.loc[
            both_exclude,
            "human_reason_code"
        ]
        ==
        merged.loc[
            both_exclude,
            "llm_reason_code"
        ]
    )

    ce_exact_n = int(
        ce_match.sum()
    )

    ce_agreement = (
        ce_exact_n
        / n_both_exclude
    )

else:

    ce_exact_n = 0
    ce_agreement = float("nan")

# =========================================================
# GATE PRE-DEFINIDO
# =========================================================

gate_g1 = (
    len(merged) == EXPECTED_RECORDS
    and
    (
        merged["status_normalized"]
        == "ok"
    ).all()
)

gate_g2 = (
    include_to_exclude == 0
)

gate_g3 = (
    retention_sensitivity >= 0.90
)

gate_pass = (
    gate_g1
    and gate_g2
    and gate_g3
)

# =========================================================
# DISTRIBUICOES
# =========================================================

human_counts = (
    merged["human_decision"]
    .value_counts()
    .reindex(
        CLASSES,
        fill_value=0
    )
)

qwen_counts = (
    merged["llm_decision"]
    .value_counts()
    .reindex(
        CLASSES,
        fill_value=0
    )
)

# =========================================================
# DISCORDANCIAS
# =========================================================

mismatches = merged[
    ~merged["exact_match"]
].copy()



merged.to_csv(
    COMPARISON_FILE,
    index=False,
    encoding="utf-8-sig"
)

mismatches.to_csv(
    MISMATCH_FILE,
    index=False,
    encoding="utf-8-sig"
)

confusion.to_csv(
    CONFUSION_FILE,
    encoding="utf-8-sig"
)



summary = f"""QWEN3:4B VALIDATION COMPARISON - v1

VALIDATION SET

Records: {len(merged)}

HUMAN REFERENCE DISTRIBUTION

include: {human_counts["include"]}
maybe: {human_counts["maybe"]}
exclude: {human_counts["exclude"]}

QWEN DISTRIBUTION

include: {qwen_counts["include"]}
maybe: {qwen_counts["maybe"]}
exclude: {qwen_counts["exclude"]}

THREE-CLASS AGREEMENT

Exact matches: {exact_n}/{len(merged)}
Exact agreement: {exact_agreement:.4f}
Exact agreement (%): {exact_agreement * 100:.1f}%

Cohen's kappa: {kappa:.4f}

SCREENING SAFETY

Human include: {n_human_include}
Human maybe: {n_human_maybe}
Human retained (include + maybe): {n_human_retained}

Human include -> Qwen exclude: {include_to_exclude}
Human maybe -> Qwen exclude: {maybe_to_exclude}

False exclusions among human-retained: {false_exclusions_retained}

Retained correctly by Qwen: {retained_correctly}/{n_human_retained}

Retention sensitivity: {retention_sensitivity:.4f}
Retention sensitivity (%): {retention_sensitivity * 100:.1f}%

EXCLUSION CODE AGREEMENT

Human exclude: {n_human_exclude}
Both human and Qwen exclude: {n_both_exclude}
Exact CE matches among joint exclusions: {ce_exact_n}/{n_both_exclude}
CE exact agreement: {ce_agreement:.4f}
CE exact agreement (%): {ce_agreement * 100:.1f}%

VALIDATION GATE

G1 - 30 structurally valid outputs:
{"PASS" if gate_g1 else "FAIL"}

G2 - Human include -> Qwen exclude = 0:
{"PASS" if gate_g2 else "FAIL"}

G3 - Retention sensitivity >= 0.90:
{"PASS" if gate_g3 else "FAIL"}

FINAL GATE:
{"PASS" if gate_pass else "FAIL"}

CONFUSION MATRIX

{confusion.to_string()}
"""

SUMMARY_FILE.write_text(
    summary,
    encoding="utf-8"
)

print()
print("=" * 70)
print(summary)
print("=" * 70)
print()
print(
    f"Comparacao completa: "
    f"{COMPARISON_FILE}"
)
print(
    f"Discordancias: "
    f"{MISMATCH_FILE}"
)
print(
    f"Matriz de confusao: "
    f"{CONFUSION_FILE}"
)
print(
    f"Resumo: "
    f"{SUMMARY_FILE}"
)
print()