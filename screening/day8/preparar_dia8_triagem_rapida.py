#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dia 8: prepara fila humana de 509 registros no Google Planilhas, sem Ollama.

Salvar este arquivo em: screening/day8/preparar_dia8_triagem_rapida.py
Executar NA RAIZ do repositorio:
  python ./screening/day8/preparar_dia8_triagem_rapida.py

Somente Python padrao. Nao modifica: CSVs originais, protocolo,
logs humanos, resultados do Qwen ou arquivos anteriores.
"""

from __future__ import annotations
import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DAY8 = ROOT / 'screening' / 'day8'
BASE = ROOT / 'search' / 'exports' / 'processed' / 'records_deduplicated.csv'
LOG = ROOT / 'screening' / 'decision_log.csv'
PILOT = ROOT / 'screening' / 'llm' / 'day7' / 'audit_pilot_v1' / 'pilot_30_humano_cego.csv'
QWEN = ROOT / 'screening' / 'llm' / 'day7' / 'audit_pilot_v1' / 'qwen_539_audited_summary.csv'
OUTPUT = DAY8 / 'triagem_dia8_509_google_planilhas.xlsx'
METHOD = DAY8 / 'day8_screening_procedure_DRAFT.md'
MANIFEST = DAY8 / 'day8_input_manifest.json'
BLOCK_SIZE = 25

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
ET.register_namespace('', NS)
ET.register_namespace('r', REL)


def read_csv(path):
    if not path.is_file():
        raise RuntimeError(f'Arquivo necessario nao encontrado: {path}')
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def index_unique(rows, context):
    d = {}
    for row in rows:
        rid = str(row.get('record_id', '')).strip()
        if not re.fullmatch(r'R\d{4}', rid) or rid in d:
            raise RuntimeError(f'ID invalido/duplicado em {context}: {rid}')
        d[rid] = row
    return d


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def node(tag, **a):
    return ET.Element(f'{{{NS}}}{tag}', {str(k):str(v) for k,v in a.items()})


def sub(parent, tag, **a):
    return ET.SubElement(parent, f'{{{NS}}}{tag}', {str(k):str(v) for k,v in a.items()})


def xml(e):
    return ET.tostring(e, encoding='utf-8', xml_declaration=True)


def letter(x):
    s = ''
    while x:
        x, y = divmod(x-1, 26)
        s = chr(65+y)+s
    return s


def plain(v):
    return ''.join(c for c in str(v or '') if c in '\r\n\t' or ord(c)>=32)


def put(row, col, index, value, style=0, numeric=False):
    attrs = dict(r=f'{letter(col)}{index}', s=style)
    if value is None or str(value) == '':
        sub(row, 'c', **attrs)
    elif numeric:
        c=sub(row, 'c', **attrs)
        sub(c, 'v').text=str(int(value))
    else:
        c=sub(row, 'c', t='inlineStr', **attrs)
        is_=sub(c, 'is'); t=sub(is_, 't')
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        t.text=plain(value)


def sheet_xml(rows, widths, freeze_x=0, freeze_y=0, merges=(), filter_range=None, validation_range=None):
    sheet=node('worksheet')
    views=sub(sheet,'sheetViews'); view=sub(views,'sheetView',workbookViewId=0,showGridLines=0)
    if freeze_x or freeze_y:
        pane=sub(view,'pane',topLeftCell=f'{letter(freeze_x+1)}{freeze_y+1}',activePane='bottomRight',state='frozen')
        if freeze_x: pane.set('xSplit',str(freeze_x))
        if freeze_y: pane.set('ySplit',str(freeze_y))
        sub(view,'selection',pane='bottomRight',activeCell=f'E{freeze_y+1}',sqref=f'E{freeze_y+1}')
    sub(sheet,'sheetFormatPr',defaultRowHeight=20)
    cols=sub(sheet,'cols')
    for i,w in enumerate(widths,1):sub(cols,'col',min=i,max=i,width=w,customWidth=1)
    body=sub(sheet,'sheetData')
    for n,(height,values,styles,numeric) in enumerate(rows,1):
        r=sub(body,'row',r=n,ht=height,customHeight=1)
        for j,val in enumerate(values,1):put(r,j,n,val,styles[j-1],j-1 in numeric)
    if merges:
        mm=sub(sheet,'mergeCells',count=len(merges))
        for ref in merges:sub(mm,'mergeCell',ref=ref)
    if filter_range:sub(sheet,'autoFilter',ref=filter_range)
    if validation_range:
        end=validation_range
        dvs=sub(sheet,'dataValidations',count=2)
        for ref,values in ((f'F4:F{end}','include,exclude,maybe'),(f'G4:G{end}','CE1,CE2,CE3,CE4')):
            dv=sub(dvs,'dataValidation',type='list',allowBlank=1,showDropDown=0,
                   showErrorMessage=1,errorStyle='stop',errorTitle='Valor invalido',
                   error='Selecione um valor da lista',sqref=ref)
            sub(dv,'formula1').text=f'"{values}"'
    sub(sheet,'pageMargins',left=.3,right=.3,top=.5,bottom=.5,header=.2,footer=.2)
    return xml(sheet)


def styles_xml():
    root=node('styleSheet')
    fonts=sub(root,'fonts',count=5)
    for bold,size,color in ((False,10,'1F2937'),(True,16,'FFFFFF'),(True,10,'FFFFFF'),(True,10,'1D4ED8'),(False,10,'475569')):
        f=sub(fonts,'font')
        if bold:sub(f,'b')
        sub(f,'sz',val=size);sub(f,'color',rgb='FF'+color);sub(f,'name',val='Arial')
    fills=sub(root,'fills',count=9)
    for patt in ('none','gray125'):sub(sub(fills,'fill'),'patternFill',patternType=patt)
    for color in ('11243A','155E75','E5F1FA','FFFFFF','F5F8FA','FFF3C4','FFE6A8'):
        p=sub(sub(fills,'fill'),'patternFill',patternType='solid')
        sub(p,'fgColor',rgb='FF'+color);sub(p,'bgColor',indexed=64)
    borders=sub(root,'borders',count=2)
    sub(borders,'border')
    b=sub(borders,'border')
    for side in ('left','right','top','bottom'):
        x=sub(b,side,style='hair');sub(x,'color',rgb='FFDBE4EC')
    sub(b,'diagonal')
    sub(sub(root,'cellStyleXfs',count=1),'xf',numFmtId=0,fontId=0,fillId=0,borderId=0)
    cfx=sub(root,'cellXfs',count=10)
    defs=[(0,0,0,'left','center'),(1,2,0,'left','center'),(4,4,0,'left','center'),
          (2,3,1,'center','center'),(0,5,1,'left','top'),(0,6,1,'left','top'),
          (0,7,1,'left','top'),(0,8,1,'left','top'),(3,4,1,'left','top'),(0,5,0,'left','top')]
    for font,fill,border,align,vert in defs:
        xf=sub(cfx,'xf',numFmtId=0,fontId=font,fillId=fill,borderId=border,xfId=0,
               applyFont=1,applyFill=1,applyBorder=1,applyAlignment=1)
        sub(xf,'alignment',horizontal=align,vertical=vert,wrapText=1)
    sub(sub(root,'cellStyles',count=1),'cellStyle',name='Normal',xfId=0,builtinId=0)
    sub(root,'dxfs',count=0)
    sub(root,'tableStyles',count=0,defaultTableStyle='TableStyleMedium2',defaultPivotStyle='PivotStyleLight16')
    return xml(root)


def build_xlsx(queue,path):
    header=['BLOCO','ORDEM','ID','TITULO','RESUMO / ABSTRACT','DECISAO HUMANA *',
            'CODIGO CE','JUSTIFICATIVA HUMANA','REVISOR','DATA (AAAA-MM-DD)',
            'TEMPO (s)','TIPO DE DOCUMENTO','PALAVRAS-CHAVE','TERMOS INDEXADOS']
    w=[10,10,13,48,80,20,13,52,20,20,12,25,35,35]
    ncol=len(header)
    tri=[(39,['DIA 8  |  TRIAGEM HUMANA POR TITULO E RESUMO']+['']*(ncol-1),[1]*ncol,set()),
         (35,['509 registros fora do piloto assistido  •  25 por bloco  •  preencha as colunas AMARELAS F–K  •  use o filtro BLOCO']+['']*(ncol-1),[2]*ncol,set()),
         (37,header,[3]*ncol,set())]
    for i,r in enumerate(queue):
        default=4 if i%2==0 else 5; edit=6 if i%2==0 else 7
        items=[(i//BLOCK_SIZE)+1,i+1,r['record_id'],r['title'],r['abstract'],
               '','','','','','',r['document_type'],r['author_keywords'],r['index_keywords']]
        tri.append((125,items,[default,default,8,default,default]+[edit]*6+[default]*3,{0,1}))
    tri_xml=sheet_xml(tri,w,freeze_x=3,freeze_y=3,merges=['A1:N1','A2:N2'],filter_range=f'A3:N{len(queue)+3}',validation_range=len(queue)+3)
    guide_lines=[
        ('OBJETIVO','Tratar 509 registros ainda nao avaliados no piloto assistido; 30 do piloto exigem tratamento separado.'),
        ('1 - PRIMEIRO BLOCO','Na aba TRIAGEM use filtro de BLOCO = 1; sao 25 artigos. Leia titulo e resumo, sem PDF integral.'),
        ('2 - INCLUDE','Aparenta atender aos criterios; segue para avaliacao de texto completo.'),
        ('3 - EXCLUDE','Somente se houver evidencia clara de inelegibilidade; escolha CE1-CE4 e escreva justificativa.'),
        ('4 - MAYBE','Quando houver incerteza; deixar CE em branco e encaminhar ao texto completo.'),
        ('CE1','Nao possui RAG operacional (recuperacao externa integrada a geracao).'),
        ('CE2','Aplicacao fora do dominio ambiental / sustentabilidade ambiental substantiva.'),
        ('CE3','Estudo secundario, anais agregados, review, editorial ou outra publicacao nao primaria.'),
        ('CE4','Apenas proposta sem avaliacao empirica; nao presumir ausencia apenas porque abstract nao tem numeros.'),
        ('REGISTRO','Preencha revisor, data, notas e, se possivel, tempo em segundos. Se revisor unico, documentar limitacao.'),
        ('SEGUNDO REVISOR','Para publicacao, priorizar segundo revisor humano independente ou descrever a limitacao no manuscrito.'),
        ('QWEN','Nao usar sugestoes como decisoes humanas. Referencia separada: day7/audit_pilot_v1/qwen_539_audited_summary.csv.'),
        ('PILOTO 30','As 30 decisoes do piloto foram assistidas pelo ChatGPT. Nao contar como validacao humana cega.'),
        ('REGISTROS PENDENTES','R0141 nao esta nesta fila (divergencia previa). As 47 decisoes anteriores estao no decision_log.csv.'),
        ('EXPORTAR','Ao terminar um bloco, Google Planilhas: Arquivo > Fazer download > Microsoft Excel (.xlsx). Salve backup.'),
        ('NAO ALTERAR','Nao sobrescrever decision_log.csv, protocolo ou resultados do Qwen antes de conferir e aprovar metodo.'),
    ]
    gw=[25,96]+[15]*12
    guide=[(42,['DIA 8  |  GUIA DE TRIAGEM']+['']*13,[1]*14,set()),
           (34,['Metodo proposto — confirmar revisor(es) e eventuais alteracoes de procedimento com a orientacao']+['']*13,[2]*14,set())]
    for label,desc in guide_lines:
        guide.append((53,[label,desc]+['']*12,[8,9]+[9]*12,set()))
    guide_xml=sheet_xml(guide,gw,freeze_y=2,merges=['A1:N1','A2:N2']+[f'B{i}:N{i}' for i in range(3,len(guide)+1)])
    types=ET.Element('Types',xmlns=CT)
    ET.SubElement(types,'Default',Extension='rels',ContentType='application/vnd.openxmlformats-package.relationships+xml')
    ET.SubElement(types,'Default',Extension='xml',ContentType='application/xml')
    for dest,mime in (('/xl/workbook.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'),
        ('/xl/worksheets/sheet1.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'),
        ('/xl/worksheets/sheet2.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'),
        ('/xl/styles.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml')):
        ET.SubElement(types,'Override',PartName=dest,ContentType=mime)
    relroot=ET.Element('Relationships',xmlns=PKG)
    ET.SubElement(relroot,'Relationship',Id='rId1',Type=REL+'/officeDocument',Target='xl/workbook.xml')
    wb=node('workbook');sub(sub(wb,'bookViews'),'workbookView',activeTab=0)
    sheets=sub(wb,'sheets')
    for i,name in enumerate(('TRIAGEM','GUIA'),1):
        sh=sub(sheets,'sheet',name=name,sheetId=i);sh.set(f'{{{REL}}}id',f'rId{i}')
    wrels=ET.Element('Relationships',xmlns=PKG)
    for i in (1,2):ET.SubElement(wrels,'Relationship',Id=f'rId{i}',Type=REL+'/worksheet',Target=f'worksheets/sheet{i}.xml')
    ET.SubElement(wrels,'Relationship',Id='rId3',Type=REL+'/styles',Target='styles.xml')
    with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name, content in (('[Content_Types].xml',ET.tostring(types,encoding='utf-8',xml_declaration=True)),
            ('_rels/.rels',ET.tostring(relroot,encoding='utf-8',xml_declaration=True)),
            ('xl/workbook.xml',xml(wb)),
            ('xl/_rels/workbook.xml.rels',ET.tostring(wrels,encoding='utf-8',xml_declaration=True)),
            ('xl/worksheets/sheet1.xml',tri_xml),('xl/worksheets/sheet2.xml',guide_xml),('xl/styles.xml',styles_xml())):
            z.writestr(name,content)
    with zipfile.ZipFile(path,'r') as z:
        if z.testzip() is not None:raise RuntimeError('XLSX gerado com erro no ZIP')


def main():
    bcols,base=read_csv(BASE); lcols,log=read_csv(LOG)
    pcols,pilot=read_csv(PILOT); qcols,qwen=read_csv(QWEN)
    if (len(base),len(log),len(pilot),len(qwen)) != (587,587,30,539):
        raise RuntimeError('Contagens inesperadas. Esperado: 587 base, 587 log, 30 piloto, 539 Qwen.')
    bidx=index_unique(base,'base'); lidx=index_unique(log,'log'); pidx=index_unique(pilot,'piloto'); qidx=index_unique(qwen,'Qwen')
    if set(bidx) != set(lidx):raise RuntimeError('IDs base vs log diferentes')
    if not {'title','abstract','author_keywords','index_keywords','document_type'}.issubset(set(bcols)):
        raise RuntimeError('Colunas bibliograficas ausentes')
    decided={k for k,v in lidx.items() if v.get('decision','').strip() in ('include','exclude','maybe')}
    if len(decided)!=47:raise RuntimeError(f'Esperadas 47 decisoes no log; observadas {len(decided)}')
    if 'R0141' not in lidx or lidx['R0141'].get('decision','').strip():
        raise RuntimeError('R0141 nao esta pendente')
    if set(qidx) != (set(bidx)-decided-{'R0141'}):
        raise RuntimeError('Cobertura do Qwen nao coincide com os 539 registros esperados')
    if not set(pidx).issubset(set(qidx)):raise RuntimeError('Piloto com IDs nao pertencentes aos 539')
    if Counter(row['derived_decision'] for row in qwen)!=Counter({'include':175,'exclude':251,'maybe':113}):
        raise RuntimeError('Resultados do Qwen divergem do Dia 7')
    remaining=set(qidx)-set(pidx)
    if len(remaining)!=509:raise RuntimeError('Fila nao possui 509 registros')
    queue=[bidx[rid] for rid in sorted(remaining)]
    if any(not r['title'].strip() or not r['abstract'].strip() for r in queue):
        raise RuntimeError('Fila possui titulo ou resumo vazio')
    if OUTPUT.exists() or METHOD.exists() or MANIFEST.exists():
        raise RuntimeError('Um ou mais arquivos de saida ja existem. Nenhum arquivo sera sobrescrito.')
    DAY8.mkdir(parents=True,exist_ok=True)
    procedure='''# Dia 8 — Procedimento operacional de triagem (RASCUNHO)\n\n> Este documento descreve a organizacao proposta; nao altera o protocolo v1.0 congelado. Confirmar com a orientacao antes de formalizar mudancas metodologicas.\n\n## Proveniencia e escopo\n\n- Base: 587 estudos apos deduplicacao.\n- 47 decisoes humanas preexistentes: manter no `screening/decision_log.csv`.\n- 539 sugestoes do Qwen ja auditadas; nenhuma e decisao oficial.\n- 30 artigos de piloto assistido por ChatGPT, identificados em `screening/llm/day7/audit_pilot_v1/`; nao equivalem a revisao humana cega/independente.\n- 509 restantes: fila desta planilha, em 21 blocos (20 de 25 e 1 de 9).\n- R0141: divergencia de calibracao pendente, fora da fila.\n\n## Procedimento proposto\n\n1. Revisor humano examina titulo + resumo (e metadados se preciso).\n2. Usar `include` para elegibilidade aparente; `exclude` SOMENTE se houver evidencia clara de CE1–CE4; `maybe` para incerteza.\n3. Em caso `exclude`, registrar o codigo principal e uma justificativa curta, baseada no resumo.\n4. Registrar identificador, revisor e data. Nao classificar sugestoes de Qwen como julgamento humano.\n5. Preferir revisores humanos independentes e procedimento de consenso; se nao houver, explicitar limitacao e considerar revisao independente do texto completo.\n6. Separar os 30 do piloto para auditoria adicional, as 10 divergencias, o codigo R0280 e R0141 para resolucao.\n7. Antes de copiar decisoes para o log oficial, auditar IDs, justificativas e eventuais mudancas no procedimento.\n\n## Regras metodologicas\n\n- Usar `screening/exclusion_codes.md` e `protocol/protocol_v1.0.md`, versao congelada.\n- CE2: dimensao ambiental precisa ser explicita e substantiva. Agricultura/energia/edificios/ESG nao bastam por si.\n- CE4: ausencia de experimentos descritos no abstract nao e automaticamente evidencia de ausencia de avaliacao; na duvida usar maybe.\n- Os 37 registros com multiplos criterios negativos no Qwen serao auditados antes de eventual exclusao formal.\n- Nenhum registro pode ser excluido automaticamente pelo Qwen com base neste piloto assistido.\n- Alteracoes metodologicas substantivas devem ser aprovadas e documentadas em `protocol/amendments.md`.\n\n## Tarefa imediata\n\nAbrir `triagem_dia8_509_google_planilhas.xlsx` no Google Planilhas.\nFiltrar BLOCO = 1 e preencher 25 artigos. Exportar em XLSX antes de fechar a sessao.\n\n## Resultado do primeiro bloco\n\n- Inicio: [preencher]\n- Termino: [preencher]\n- Revisor(es): [preencher]\n- Include: [preencher]\n- Exclude: [preencher]\n- Maybe: [preencher]\n- Pendencias: [preencher]\n'''
    build_xlsx(queue,OUTPUT)
    METHOD.write_text(procedure,encoding='utf-8')
    meta={'created_at':datetime.now().astimezone().isoformat(),'input_sha256':{
        p.relative_to(ROOT).as_posix():sha256(p) for p in (BASE,LOG,PILOT,QWEN)},
        'counts':{'base':587,'existing_human':47,'pilot_assisted':30,'qwen_suggestions':539,'queue_new':509,'blocks':(509+BLOCK_SIZE-1)//BLOCK_SIZE},
        'output_file':OUTPUT.relative_to(ROOT).as_posix(),
        'note':'Planilha nao contem sugestoes do Qwen. Nao altera logs nem protocolo.'}
    MANIFEST.write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    print('\nDIA 8: FILA GERADA COM SUCESSO')
    print('Base: 587 | ja decididos: 47 | piloto assistido separado: 30 | R0141 pendente: 1')
    print('Nova fila humana: 509 artigos | 21 blocos (20x25 + 1x9)')
    print('Google Planilhas:',OUTPUT)
    print('Procedimento (RASCUNHO):',METHOD)
    print('Hashes:',MANIFEST)
    print('NENHUMA decisao humana ou sugestao do Qwen foi alterada.')
    print('ACAO: abra o .xlsx no Google Planilhas, filtre BLOCO=1 e avalie 25 titulos/resumos.')


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('ERRO DIA 8:',exc,file=sys.stderr)
        sys.exit(1)
