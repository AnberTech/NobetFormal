#!/usr/bin/env python3
"""Formal Nöbet Çözücü rehber sayfalarını üretir (yalnız Türkçe): <slug>/index.html, sitemap.xml, llms.txt'deki rehber listesi.

Kullanım (depo kökünden):  python3 _src/build_guides.py
- Araç tek dosyadır (index.html) ve elle düzenlenir; bu script ona DOKUNMAZ.
- Metinler: _src/guides/tr.json. Sayfa şablonu: _src/guide_page.py (WeddingInvite deposundaki ile aynı dosya).
Jekyll "_" ile başlayan klasörleri yayınlamaz; _src sitede görünmez.
"""
import datetime
import json
import os
import re
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import guide_page  # noqa: E402

SITE = 'https://anbertech.github.io/'
BASE = SITE + 'NobetFormal/'
EMAIL = 'destek.anbertech@gmail.com'
TOPICS = ('liste', 'adil')
THEME = (":root{--bg:#f8fafc;--card:#ffffff;--soft:#eef2ff;--line:#e2e8f0;--ink:#1e293b;--muted:#475569;--acc:#4f46e5;"
         "--f-head:-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;--f-text:-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;"
         "--f-ui:-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif}")
GC = '<script data-goatcounter="https://anbertech.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    with open(os.path.join(SRC, 'guides', 'tr.json'), encoding='utf-8') as f:
        t = json.load(f)
    errs = guide_page.check('tr', t, None, TOPICS)
    if errs:
        sys.exit('guides/tr.json hatalı:\n  ' + '\n  '.join(errs))
    url_of = lambda c, x: BASE + t[f'{x}_slug'] + '/'
    org = {'@type': 'Organization', '@id': SITE + '#org', 'name': 'AnberTech', 'url': SITE, 'email': EMAIL}
    for x in TOPICS:
        page = guide_page.render(code='tr', dirn='ltr', og_locale='tr_TR', lang_names={'tr': 'Türkçe'}, built=['tr'], x=x, t=t, topics=TOPICS,
                                 url_of=url_of, home_url=lambda c: BASE, cta_url=BASE, brand='Formal Nöbet Çözücü', site_name='Formal Nöbet Çözücü',
                                 org=org, email=EMAIL, theme_css=THEME, analytics=GC, icon=BASE + 'favicon.png')
        write(os.path.join(ROOT, t[f'{x}_slug'], 'index.html'), page)
    today = datetime.date.today().isoformat()
    urls = [BASE] + [url_of('tr', x) for x in TOPICS]
    write(os.path.join(ROOT, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls) + '</urlset>\n')
    # llms.txt: "## Guides" bölümünü yeniden yaz (dosyanın geri kalanı elle tutulur)
    p = os.path.join(ROOT, 'llms.txt')
    with open(p, encoding='utf-8') as f:
        llms = f.read()
    llms = re.sub(r'\n## Guides \(Turkish\)\n.*?(?=\n## |\Z)', '', llms, flags=re.S).rstrip('\n') + '\n'
    llms += '\n## Guides (Turkish)\n\n' + ''.join(f'- [{t[f"{x}_name"]}]({url_of("tr", x)}): {t[f"{x}_card"]}\n' for x in TOPICS)
    write(p, llms)
    print('rehber:', ', '.join(t[f'{x}_slug'] for x in TOPICS))


if __name__ == '__main__':
    main()
