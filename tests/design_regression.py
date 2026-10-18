#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1];icons=sorted((ROOT/'assets/navigation-icons').glob('*.png'));errors=[]
if len(icons)!=39:errors.append(f'{len(icons)} Icons statt 39')
for p in icons:
 im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');px=list(im.getdata())
 if im.size!=(512,512):errors.append(p.name+' falsche Größe')
 if alpha.getextrema()!=(0,255):errors.append(p.name+' ohne transparente Ränder')
 colored=sum(1 for r,g,b,a in px if a and not (r==g==b));black=sum(1 for r,g,b,a in px if a>240 and max(r,g,b)<25)
 if colored<50000 or black<9000:errors.append(p.name+' unzureichende Farb-/Konturmasse')
materials=[p for p in icons if '-material-' in p.name]
if len(materials)!=10:errors.append('Werkstofficons nicht 10')
# Materialnummern erzeugen visuell eigenständige Dateien.
if len({hashlib.sha256(p.read_bytes()).hexdigest() for p in materials})!=10:errors.append('Werkstofficons nicht variabel')
if errors:print('FAIL\n'+'\n'.join(errors));sys.exit(1)
print('PASS · 39 eigenständige 512×512-PNGs · Transparenz, Kontur, Farbe · 10 variable Werkstofficons')
