#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtra apenas os estudos com DECISÃO TEXTO COMPLETO = include.

Mantém todas as 29 colunas originais da aba FILA_236, acrescentando duas
colunas de auditoria: LINHA ORIGINAL e ALERTA DE CONSISTÊNCIA.

O arquivo de origem (.xlsm) NUNCA é alterado. A saída é um novo .xlsx,
sem macros, contendo apenas os registros incluídos.

Uso:
    python separar_artigos_incluidos.py "fila_texto_completo_dia10_236_COM_EXTRACAO(5).xlsm"

    python separar_artigos_incluidos.py caminho.xlsm -o somente_incluidos.xlsx

Dependência: artifact_tool (deve estar disponível no ambiente Python).
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import unicodedata
from artifact_tool import Blob, SpreadsheetFile, Workbook

ABA_ORIGEM = "FILA_236"
LINHA_CABECALHO = 3
PRIMEIRA_LINHA_DADOS = 4
ULTIMA_COLUNA_ORIGINAL = "AC"  # 29 colunas


def normalizar(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or "").strip().casefold())
    return "".join(c for c in texto if not unicodedata.combining(c))


def ultima_linha_ocupada(aba) -> int:
    # A tabela começa na linha 3 e a região atual cobre os registros de FILA_236.
    endereco = aba.get_range("B4").get_current_region().address
    partes = re.findall(r"\d+", endereco)
    if not partes:
        raise ValueError(f"Não foi possível identificar a última linha: {endereco}")
    return int(partes[-1])


def avaliar_alerta(cabecalhos: list, registro: list) -> str:
    campos = {normalizar(cab): str(registro[i] or "").strip()
              for i, cab in enumerate(cabecalhos)}
    alertas = []
    # Para os estudos incluídos, os quatro critérios de elegibilidade
    # devem estar positivos e o código principal CE deve estar vazio.
    for cab in (
        "RAG OPERACIONAL (CI1)",
        "AMBIENTAL SUBSTANTIVO (CI2)",
        "ESTUDO PRIMÁRIO (CI3)",
        "AVALIAÇÃO EMPÍRICA (CI4)",
    ):
        resposta = normalizar(campos.get(normalizar(cab), ""))
        if resposta in {"nao", "não", "no", "false"}:
            alertas.append(f"{cab}: NÃO")
        elif resposta in {"", "nr", "indefinido", "pendente"}:
            alertas.append(f"{cab}: verificar")

    codigo = campos.get(normalizar("CE PRINCIPAL"), "")
    if re.match(r"^CE[1-7]\b", codigo, flags=re.I):
        alertas.append(f"CE principal preenchido: {codigo}")

    return "; ".join(alertas) if alertas else "OK"


def filtrar(origem: Path, destino: Path) -> tuple[int, int, list[str]]:
    if not origem.is_file():
        raise FileNotFoundError(f"Planilha não encontrada: {origem}")
    if origem.resolve() == destino.resolve():
        raise ValueError("O arquivo de saída precisa ser diferente da origem.")

    entrada = SpreadsheetFile.import_xlsx(Blob.load(str(origem)))
    aba = entrada.worksheets.get_item(ABA_ORIGEM)
    cabecalhos = aba.get_range(f"A{LINHA_CABECALHO}:{ULTIMA_COLUNA_ORIGINAL}{LINHA_CABECALHO}").values[0]
    colunas = {normalizar(c): indice for indice, c in enumerate(cabecalhos)}
    if normalizar("DECISÃO TEXTO COMPLETO") not in colunas:
        raise ValueError("Não encontrei a coluna 'DECISÃO TEXTO COMPLETO' na linha 3.")
    indice_decisao = colunas[normalizar("DECISÃO TEXTO COMPLETO")]
    indice_id = colunas.get(normalizar("ID"), 1)

    ultima = ultima_linha_ocupada(aba)
    registros = aba.get_range(f"A{PRIMEIRA_LINHA_DADOS}:{ULTIMA_COLUNA_ORIGINAL}{ultima}").values
    incluidos = []
    ids = set()
    alertas_ids = []
    contagens = Counter()

    for linha_excel, registro in enumerate(registros, start=PRIMEIRA_LINHA_DADOS):
        if not any(c is not None and str(c).strip() for c in registro):
            continue
        decisao = normalizar(registro[indice_decisao])
        contagens[decisao or "(vazio)"] += 1
        if decisao != "include":
            continue
        codigo = str(registro[indice_id] or "").strip()
        if not codigo:
            raise ValueError(f"Registro incluído na linha {linha_excel} sem ID.")
        if codigo in ids:
            raise ValueError(f"ID duplicado entre incluídos: {codigo}")
        ids.add(codigo)
        alerta = avaliar_alerta(cabecalhos, registro)
        if alerta != "OK":
            alertas_ids.append(f"{codigo}: {alerta}")
        incluidos.append(list(registro) + [linha_excel, alerta])

    if not incluidos:
        raise ValueError("Nenhum registro 'include' encontrado na aba FILA_236.")

    # Criar arquivo independente: só registros incluídos, nenhuma outra decisão.
    saida = Workbook.create()
    plan = saida.worksheets.add("INCLUIDOS")
    colunas_saida = list(cabecalhos) + ["LINHA ORIGINAL (FILA_236)", "ALERTA DE CONSISTÊNCIA"]
    plan.get_range("A1:AE1").values = [colunas_saida]
    fim = len(incluidos) + 1
    plan.get_range(f"A2:AE{fim}").values = incluidos

    # Formatação profissional e filtros; os dados textuais permanecem completos.
    cab = plan.get_range("A1:AE1")
    cab.format = {
        "fill": "#163A4A",
        "font": {"bold": True, "color": "#FFFFFF"},
        "row_height": 35,
        "wrap_text": True,
        "vertical_alignment": "center",
    }
    plan.get_range(f"A2:AE{fim}").format.row_height = 30
    plan.freeze_panes.freeze_rows(1)
    plan.tables.add(f"A1:AE{fim}", True, "TabelaEstudosIncluidos")

    # Larguras controladas, principalmente para texto extenso (sem autofit excessivo).
    larguras = {
        "A": 10, "B": 13, "C": 15, "D": 55, "E": 65, "F": 22,
        "G": 27, "H": 50, "I": 19, "J": 22, "K": 24,
        "L": 22, "M": 23, "N": 26, "O": 17, "P": 60,
        "Q": 60, "R": 15, "S": 17, "T": 22,
        "U": 65, "V": 60, "W": 60, "X": 60, "Y": 60,
        "Z": 60, "AA": 60, "AB": 60, "AC": 55,
        "AD": 25, "AE": 55,
    }
    for coluna, largura in larguras.items():
        plan.get_range(f"{coluna}1:{coluna}{fim}").format.column_width = largura

    # Destacar somente os registros suspeitos, sem removê-los nem reclassificá-los.
    for indice, registro in enumerate(incluidos, start=2):
        if registro[-1] != "OK":
            plan.get_range(f"AE{indice}").format.fill = "#FDE8D3"
            plan.get_range(f"AE{indice}").format.font.color = "#9A3412"
            plan.get_range(f"N{indice}").format.fill = "#FDE8D3"

    destino.parent.mkdir(parents=True, exist_ok=True)
    SpreadsheetFile.export_xlsx(saida).save(str(destino))
    print(f"Arquivo de origem: {origem}")
    print(f"Registros de origem: {sum(contagens.values())} — {dict(contagens)}")
    print(f"Artigos incluídos exportados: {len(incluidos)}")
    print(f"Arquivo de saída: {destino}")
    if alertas_ids:
        print("AVISOS (não alterados automaticamente):")
        for aviso in alertas_ids:
            print(f"  - {aviso}")
    return sum(contagens.values()), len(incluidos), alertas_ids


def main():
    parser = argparse.ArgumentParser(description="Gera Excel com os estudos include da aba FILA_236.")
    parser.add_argument("origem", type=Path, help="Caminho para a planilha de triagem .xlsm")
    parser.add_argument("-o", "--saida", type=Path, default=None,
                        help="Caminho .xlsx de saída (opcional)")
    args = parser.parse_args()
    saida = args.saida or args.origem.with_name("artigos_incluidos_filtrados.xlsx")
    filtrar(args.origem, saida)


if __name__ == "__main__":
    main()
