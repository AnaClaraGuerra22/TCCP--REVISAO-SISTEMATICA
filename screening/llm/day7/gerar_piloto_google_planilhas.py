r"""Gera planilha .xlsx legivel no Google Planilhas para o piloto humano cego.

Somente bibliotecas padrao do Python. Nao usa Ollama, nao acessa Google,
nao modifica o CSV original, o gabarito ou o decision_log.csv.

Execucao (na raiz do repositorio):
    python .\screening\llm\day7\gerar_piloto_google_planilhas.py
"""
from __future__ import annotations

import csv
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DIR = Path(__file__).resolve().parent / "audit_pilot_v1"
SOURCE = DIR / "pilot_30_humano_cego.csv"
TARGET = DIR / "pilot_30_google_planilhas.xlsx"
REQUIRED = (
    "review_order", "record_id", "title", "abstract", "author_keywords",
    "index_keywords", "document_type", "human_decision", "human_reason_code",
    "human_notes", "review_seconds",
)

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
ET.register_namespace("", NS)
ET.register_namespace("r", REL)


def node(tag: str, **attrs):
    return ET.Element(f"{{{NS}}}{tag}", {str(k): str(v) for k, v in attrs.items()})


def sub(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {str(k): str(v) for k, v in attrs.items()})


def xml(element):
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)


def col(num: int) -> str:
    out = ""
    while num:
        num, rest = divmod(num - 1, 26)
        out = chr(65 + rest) + out
    return out


def clean_text(value) -> str:
    text = "" if value is None else str(value)
    # Characters not allowed in XML 1.0; keep linguistic content untouched.
    return "".join(ch for ch in text if ch in "\t\n\r" or ord(ch) >= 32)


def cell(row, coordinate: str, value, style: int, integer: bool = False):
    if value is None or value == "":
        sub(row, "c", r=coordinate, s=style)
        return
    if integer:
        c = sub(row, "c", r=coordinate, s=style)
        sub(c, "v").text = str(int(value))
        return
    c = sub(row, "c", r=coordinate, s=style, t="inlineStr")
    content = sub(c, "is")
    t = sub(content, "t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = clean_text(value)


def merged(sheet, target: str):
    # merges are appended by caller after sheetData
    return target


def add_sheet(rows, widths, freeze=(0, 0), merge=(), filter_range=None, validation=False):
    sheet = node("worksheet")
    svs = sub(sheet, "sheetViews")
    sv = sub(svs, "sheetView", workbookViewId=0, showGridLines=0)
    x, y = freeze
    if x or y:
        pane = sub(sv, "pane", topLeftCell=f"{col(x+1)}{y+1}", activePane="bottomRight", state="frozen")
        if x:
            pane.set("xSplit", str(x))
        if y:
            pane.set("ySplit", str(y))
        sub(sv, "selection", pane="bottomRight", activeCell=f"E{y+1}", sqref=f"E{y+1}")
    sub(sheet, "sheetFormatPr", defaultRowHeight=20)
    columns = sub(sheet, "cols")
    for i, width in enumerate(widths, 1):
        sub(columns, "col", min=i, max=i, width=width, customWidth=1)

    body = sub(sheet, "sheetData")
    for idx, (height, values, styles, numeric) in enumerate(rows, 1):
        row = sub(body, "row", r=idx, ht=height, customHeight=1)
        for j, val in enumerate(values, 1):
            cell(row, f"{col(j)}{idx}", val, styles[j-1], j-1 in numeric)

    if merge:
        mm = sub(sheet, "mergeCells", count=len(merge))
        for rng in merge:
            sub(mm, "mergeCell", ref=rng)
    if filter_range:
        sub(sheet, "autoFilter", ref=filter_range)
    if validation:
        dvs = sub(sheet, "dataValidations", count=2)
        for rng, vals, msg in (
            ("E4:E33", "include,exclude,maybe", "Selecione include, exclude ou maybe"),
            ("F4:F33", "CE1,CE2,CE3,CE4", "Preencha somente se a decisao for exclude"),
        ):
            dv = sub(dvs, "dataValidation", type="list", allowBlank=1, showDropDown=0,
                     showErrorMessage=1, errorStyle="stop", errorTitle="Valor invalido",
                     error=msg, sqref=rng)
            sub(dv, "formula1").text = f'"{vals}"'

    sub(sheet, "pageMargins", left=0.3, right=0.3, top=0.5, bottom=0.5, header=0.2, footer=0.2)
    return xml(sheet)


def add_color(e, value):
    sub(e, "color", rgb="FF" + value.lstrip("#"))


def styles_xml():
    root = node("styleSheet")
    fonts = sub(root, "fonts", count=5)
    for bold, sz, color in ((False, 10, "172B4D"), (True, 16, "FFFFFF"),
                            (True, 10, "FFFFFF"), (True, 10, "1D4ED8"),
                            (False, 10, "475569")):
        f = sub(fonts, "font")
        if bold:
            sub(f, "b")
        sub(f, "sz", val=sz)
        add_color(f, color)
        sub(f, "name", val="Arial")

    fills = sub(root, "fills", count=9)
    sub(fills, "fill").append(ET.Element(f"{{{NS}}}patternFill", {"patternType": "none"}))
    sub(fills, "fill").append(ET.Element(f"{{{NS}}}patternFill", {"patternType": "gray125"}))
    for rgb in ("102A43", "1D4ED8", "EAF2FF", "FFFFFF", "F5F8FD", "FFF4CE", "FFF0B3"):
        fill = sub(fills, "fill")
        pat = sub(fill, "patternFill", patternType="solid")
        sub(pat, "fgColor", rgb="FF" + rgb)
        sub(pat, "bgColor", indexed=64)

    borders = sub(root, "borders", count=2)
    borders.append(node("border"))
    b = sub(borders, "border")
    for side in ("left", "right", "top", "bottom"):
        el = sub(b, side, style="hair")
        sub(el, "color", rgb="FFD5DEE8")
    sub(b, "diagonal")

    csx = sub(root, "cellStyleXfs", count=1)
    sub(csx, "xf", numFmtId=0, fontId=0, fillId=0, borderId=0)
    cfx = sub(root, "cellXfs", count=12)
    # Styles: default, title, description, header, fixed odd, fixed even,
    # edit odd, edit even, key id, guide title, guide subtitle, guide body
    styles = [
        (0, 0, 0, "left", "center", 1),
        (1, 2, 0, "left", "center", 1),
        (4, 4, 0, "left", "center", 1),
        (2, 3, 1, "center", "center", 1),
        (0, 5, 1, "left", "top", 1),
        (0, 6, 1, "left", "top", 1),
        (0, 7, 1, "left", "top", 1),
        (0, 8, 1, "left", "top", 1),
        (3, 4, 1, "left", "top", 1),
        (1, 2, 0, "left", "center", 1),
        (3, 4, 0, "left", "center", 1),
        (0, 5, 0, "left", "top", 1),
    ]
    for f_id, fill_id, b_id, horiz, vert, wrap in styles:
        xf = sub(cfx, "xf", numFmtId=0, fontId=f_id, fillId=fill_id, borderId=b_id,
                 xfId=0, applyFont=1, applyFill=1, applyBorder=1, applyAlignment=1)
        sub(xf, "alignment", horizontal=horiz, vertical=vert, wrapText=wrap)
    cstyles = sub(root, "cellStyles", count=1)
    sub(cstyles, "cellStyle", name="Normal", xfId=0, builtinId=0)
    sub(root, "dxfs", count=0)
    sub(root, "tableStyles", count=0, defaultTableStyle="TableStyleMedium2", defaultPivotStyle="PivotStyleLight16")
    return xml(root)


def build_xlsx(articles):
    headers = ["ORDEM", "ID", "TITULO", "RESUMO / ABSTRACT", "DECISAO HUMANA *",
               "CODIGO CE", "JUSTIFICATIVA HUMANA", "TEMPO (s)",
               "TIPO DE DOCUMENTO", "PALAVRAS-CHAVE", "TERMOS INDEXADOS"]
    lengths = [8, 12, 47, 85, 20, 13, 48, 14, 22, 37, 37]
    vals = []
    vals.append((34, ["PILOTO CEGO  |  TRIAGEM POR TITULO E RESUMO"] + [""]*10, [1]+[1]*10, set()))
    vals.append((30, ["30 registros · preencher as colunas amarelas E–H · nao consultar o gabarito Qwen · nao alterar o CSV original"] + [""]*10,
                 [2]+[2]*10, set()))
    vals.append((34, headers, [3]*11, set()))
    for i, r in enumerate(articles):
        order = int(r["review_order"])
        record = [order, r["record_id"], r["title"], r["abstract"],
                  r["human_decision"], r["human_reason_code"],
                  r["human_notes"], r["review_seconds"], r["document_type"],
                  r["author_keywords"], r["index_keywords"]]
        stripe = 4 if i % 2 == 0 else 5
        edit = 6 if i % 2 == 0 else 7
        fmt = [stripe, 8, stripe, stripe, edit, edit, edit, edit, stripe, stripe, stripe]
        vals.append((130, record, fmt, {0}))

    worksheet = add_sheet(vals, lengths, freeze=(2, 3), merge=["A1:K1", "A2:K2"],
                          filter_range="A3:K33", validation=True)
    gvals = [
        (40, ["GUIA RAPIDO — TRIAGEM HUMANA CEGA"]+[""]*6, [9]*7, set()),
        (34, ["ETAPA: titulo/resumo. Nao ler os PDFs completos ainda; nao consultar o gabarito do Qwen."]+[""]*6, [10]*7, set()),
    ]
    guidance = [
        ("1 · LEITURA", "Leia titulo, abstract e, se necessario, as palavras-chave e o tipo do documento."),
        ("2 · INCLUDE", "Marque include se o estudo aparenta ser elegivel para avaliacao do texto completo."),
        ("3 · EXCLUDE", "Marque exclude somente quando houver evidencia suficiente de inelegibilidade no titulo/resumo."),
        ("4 · MAYBE", "Marque maybe se houver incerteza; esses artigos avancam para verificacao posterior."),
        ("5 · CE1", "Nao possui RAG operacional integrado: recuperacao + geracao sustentada por conteudo recuperado."),
        ("6 · CE2", "Dominio nao e ambiental/sustentabilidade ambiental de maneira explicita e substantiva."),
        ("7 · CE3", "Estudo secundario, revisao, survey, editorial ou outra publicacao nao primaria."),
        ("8 · CE4", "Proposta sem avaliacao empirica, com evidencia suficiente para essa conclusao."),
        ("9 · NOTAS", "Registre uma justificativa curta; para exclude, preencha tambem o codigo CE correspondente."),
        ("10 · TEMPO", "Informe a duracao aproximada em segundos. Ex.: 75 para 1 minuto e 15 segundos."),
        ("11 · EXPORTAR", "Ao terminar, no Google Planilhas: Arquivo > Fazer download > Microsoft Excel (.xlsx)."),
        ("12 · PRESERVAR", "Nao modifique IDs/titulos/resumos. Nao copie decisoes ao decision_log.csv neste momento."),
    ]
    for heading, description in guidance:
        gvals.append((49, [heading, description]+[""]*5, [10, 11]+[11]*5, set()))
    guide = add_sheet(gvals, [19, 67, 15, 15, 15, 15, 15], freeze=(0,2),
                      merge=["A1:G1", "A2:G2"] + [f"B{k}:G{k}" for k in range(3, len(gvals)+1)])

    # Required Office Open XML files, deliberately independent of any external library.
    ct = ET.Element("Types", xmlns=CT)
    ET.SubElement(ct, "Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(ct, "Default", Extension="xml", ContentType="application/xml")
    for target, mime in (
        ("/xl/workbook.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"),
        ("/xl/worksheets/sheet1.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"),
        ("/xl/worksheets/sheet2.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"),
        ("/xl/styles.xml", "application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"),
    ):
        ET.SubElement(ct, "Override", PartName=target, ContentType=mime)
    relroot = ET.Element("Relationships", xmlns=PKG)
    ET.SubElement(relroot, "Relationship", Id="rId1", Type=REL+"/officeDocument", Target="xl/workbook.xml")
    wb = node("workbook")
    views = sub(wb, "bookViews")
    sub(views, "workbookView", activeTab=0)
    wbsheets = sub(wb, "sheets")
    for i, name in enumerate(("TRIAGEM", "GUIA"), 1):
        sh = sub(wbsheets, "sheet", name=name, sheetId=i)
        sh.set(f"{{{REL}}}id", f"rId{i}")
    wrels = ET.Element("Relationships", xmlns=PKG)
    for i in (1,2):
        ET.SubElement(wrels, "Relationship", Id=f"rId{i}", Type=REL+"/worksheet", Target=f"worksheets/sheet{i}.xml")
    ET.SubElement(wrels, "Relationship", Id="rId3", Type=REL+"/styles", Target="styles.xml")

    with zipfile.ZipFile(TARGET, "x", compression=zipfile.ZIP_DEFLATED) as z:
        for name, content in (
            ("[Content_Types].xml", ET.tostring(ct, encoding="utf-8", xml_declaration=True)),
            ("_rels/.rels", ET.tostring(relroot, encoding="utf-8", xml_declaration=True)),
            ("xl/workbook.xml", xml(wb)),
            ("xl/_rels/workbook.xml.rels", ET.tostring(wrels, encoding="utf-8", xml_declaration=True)),
            ("xl/worksheets/sheet1.xml", worksheet),
            ("xl/worksheets/sheet2.xml", guide),
            ("xl/styles.xml", styles_xml()),
        ):
            z.writestr(name, content)
    with zipfile.ZipFile(TARGET) as z:
        assert z.testzip() is None, "Falha no arquivo XLSX."


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"CSV original do piloto nao encontrado: {SOURCE}")
    if TARGET.exists():
        raise FileExistsError(f"Arquivo de destino ja existe; nao vou sobrescrever: {TARGET}")
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(fp)
        missing = set(REQUIRED) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV de entrada com colunas ausentes: {sorted(missing)}")
        articles = list(reader)
    if len(articles) != 30:
        raise ValueError(f"Esperados 30 registros; encontrado: {len(articles)}")
    ids = [row["record_id"].strip() for row in articles]
    if len(set(ids)) != 30 or any(not re.fullmatch(r"R\d{4}", rid) for rid in ids):
        raise ValueError("IDs vazios, duplicados ou fora do padrao R0001")
    if sorted(int(row["review_order"]) for row in articles) != list(range(1,31)):
        raise ValueError("A sequencia do piloto nao corresponde a 1..30")
    if any(row["human_decision"].strip() or row["human_reason_code"].strip() for row in articles):
        raise ValueError("O CSV original do piloto ja possui decisoes. Para evitar perder trabalho, verifique antes de continuar.")
    if any(not row["title"].strip() or not row["abstract"].strip() for row in articles):
        raise ValueError("Ha registros sem titulo ou resumo")

    build_xlsx(articles)
    print("PLANILHA GOOGLE GERADA COM SUCESSO")
    print("Artigos: 30 | IDs: unicos | Gabarito do Qwen: NAO incluido")
    print("Colunas de preenchimento: E (decisao), F (CE), G (notas), H (segundos)")
    print("Arquivo:", TARGET)
    print("Importe o .xlsx no Google Planilhas. Nao importe o CSV antigo.")
    print("Nenhum CSV, resultado do Qwen ou decision_log.csv foi alterado.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERRO:", exc, file=sys.stderr)
        raise SystemExit(1)
