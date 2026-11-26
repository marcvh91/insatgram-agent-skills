import json, re, sys
sys.path.insert(0, '../rodatge_dc')
src = open('../rodatge_dc/gen.py').read()
ns = {}
import os; os.chdir('../rodatge_dc'); exec(src.split('drop = "".join')[0].replace('open("index.html", "w")', '#'), ns)
strip = lambda t: re.sub(r'<[^>]+>', '', t)
def conv(L): return [{"id": c[0], "name": c[1], "say": strip(c[5]).replace('(pausa)', '…'), "act": strip(c[6])} for c in L]
DATA = {"drop": {"name": "Drop", "clips": conv(ns["DROP"])}, "cint": {"name": "Cintilla", "clips": conv(ns["CINT"])}}
os.chdir('../prompter'); page = open('tpl.html').read().replace('__DATA__', json.dumps(DATA, ensure_ascii=False))
open('index.html', 'w').write(page)
