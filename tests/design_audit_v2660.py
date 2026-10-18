#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];css=(ROOT/'assets/app-v2-6-6-0.css').read_text();js=(ROOT/'assets/knowledge-overview.js').read_text();errors=[]
for token in ('--sk-tile-icon-size','knowledge-tile-grid','material-tile-grid','knowledge-context-back','material-context-back','kb-context-back','transform:none!important','translate:none!important','scale:none!important','@media(max-width:350px)'):
 if token not in css:errors.append('CSS fehlt: '+token)
for token in ("name:'Air Torque'","name:'Endress+Hauser'","name:'Siemens'","name:'Vacon'","name:'Sonstiges'","families:[]","level:'family'","level:'article'"):
 if token not in js:errors.append('Navigationsmodell fehlt: '+token)
for p in (ROOT/'wissensdatenbank').glob('*/index.html'):
 if p.parent.name=='werkstoff-nachschlagewerk':continue
 text=p.read_text()
 if 'knowledge-flat' not in text or 'knowledge-cartoon' in text:errors.append('Beitragsdesign falsch: '+p.parent.name)
 if 'kb-context-back' not in text:errors.append('Zurück-Chip fehlt: '+p.parent.name)
if errors:print('FAIL\n'+'\n'.join(errors));sys.exit(1)
print('PASS · Kachel-, Flachdesign-, Zurück-Chip- und ortsfeste Zustandsregeln')
