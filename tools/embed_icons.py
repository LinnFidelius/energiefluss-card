#!/usr/bin/env python3
"""Bettet alle SVGs aus icons/ als data-URIs in energiefluss-card.js ein (Block EF_ICONS)."""
import base64, json, pathlib, re, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
icons = {}
for p in sorted((root / 'icons').rglob('*.svg')):
    key = p.relative_to(root / 'icons').with_suffix('').as_posix().replace('verbraucher/', '')
    icons[key] = 'data:image/svg+xml;base64,' + base64.b64encode(p.read_bytes()).decode()
js = root / 'energiefluss-card.js'
src = js.read_text(encoding='utf-8')
block = '// ICONS-START (automatisch erzeugt von tools/embed_icons.py)\nconst EF_ICONS = ' + \
    json.dumps(icons, indent=1) + ';\n// ICONS-END'
new, n = re.subn(r'// ICONS-START.*?// ICONS-END', lambda m: block, src, flags=re.S)
if n != 1:
    sys.exit('Marker ICONS-START/ICONS-END nicht gefunden')
mono = json.loads((root / 'icons' / 'mono-paths.json').read_text())
mono = {k: v for k, v in mono.items() if k in icons}   # nur Symbole, die auch in der Karte sind
mblock = '// MONO-START (automatisch erzeugt)\nconst EF_MONO = ' + json.dumps(mono, separators=(',', ':')) + ';\n// MONO-END'
new, n = re.subn(r'// MONO-START.*?// MONO-END', lambda m: mblock, new, flags=re.S)
if n != 1:
    sys.exit('Marker MONO-START/MONO-END nicht gefunden')
js.write_text(new, encoding='utf-8')
print(f'{len(icons)} Symbole eingebettet')
