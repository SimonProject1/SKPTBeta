#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for p in ROOT.rglob('*'):
 if p.resolve()==Path(__file__).resolve():continue
 if not p.is_file() or p.suffix.lower() not in {'.html','.css','.js','.json','.webmanifest','.py','.svg'}:continue
 try:text=p.read_text()
 except UnicodeDecodeError:continue
 if any(x in text for x in ('2.6.5.5','v2-6-5-5','V2.6.5.5')):errors.append(f'Altversion in {p.relative_to(ROOT)}')
for required in ('assets/app-v2-6-6-0.css','assets/app-v2-6-6-0.js','manifest-v2-6-6-0.webmanifest','assets/search-index-v2-6-6-0.json','UEBERGABE-V2.6.6.0-Beta.txt'):
 if not (ROOT/required).is_file():errors.append(f'Fehlt: {required}')
if errors:print('FAIL\n'+'\n'.join(errors));sys.exit(1)
print('PASS · keine operative Altversion · V2.6.6.0-Dateinamen vollständig')
