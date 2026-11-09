"""Search-engine discovery, not a verified inventory of property portals."""
import json, re, time, html
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse, parse_qs, unquote
import requests
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'data'/'results.json'
TOWNS=['Chiclana de la Frontera','Conil de la Frontera','Vejer de la Frontera','Benalup-Casas Viejas','Barbate']
SOURCES={
 'Idealista':'idealista.com/inmueble/', 'Fotocasa':'fotocasa.es/es/comprar/',
 'Altamira':'altamirainmuebles.com', 'Aliseda':'alisedainmobiliaria.com',
 'Solvia':'solvia.es', 'Servihabitat':'servihabitat.com',
 'Unicaja':'unicajainmuebles.com', 'Diglo':'digloservicer.com',
 'Sareb':'sareb.es', 'BOE subastas':'subastas.boe.es',
 'Procuradores':'subastasprocuradores.com', 'eactivos':'eactivos.com',
 'Seguridad Social':'seg-social.es',
}
HEAD={'User-Agent':'Mozilla/5.0 (compatible; RadarCadiz/0.1; +https://github.com/)'}

def clean_url(u):
    if not u.startswith(('http://','https://')):return None
    p=urlparse(u)
    if p.netloc.lower().endswith('bing.com'):
        q=parse_qs(p.query)
        if q.get('url'):u=q['url'][0]
    return u

def run():
    previous={}
    if OUT.exists():
        try:previous=json.loads(OUT.read_text(encoding='utf8'))
        except (ValueError,OSError):pass
    entries={x['url']:x for x in previous.get('items',[]) if x.get('url')}
    checks=[]
    session=requests.Session()
    for source,domain in SOURCES.items():
        for town in TOWNS:
            query=f'site:{domain} "{town}" venta inmueble'
            status='error';note='';found=0
            try:
                response=session.get('https://www.bing.com/search',params={'q':query,'format':'rss'},headers=HEAD,timeout=18)
                response.raise_for_status()
                tree=ET.fromstring(response.content)
                hits=tree.findall('.//item')
                status='busqueda_indirecta';note='Resultados de índice externo; NO se ha inspeccionado el portal ni verificado el anuncio.'
                for item in hits:
                    url=clean_url(item.findtext('link','').strip())
                    if not url:continue
                    host=urlparse(url).netloc.lower().removeprefix('www.')
                    target=domain.split('/')[0]
                    if not (host==target or host.endswith('.'+target)):continue
                    title=html.unescape(re.sub('<[^>]*>','',item.findtext('title',''))).strip()
                    desc=html.unescape(re.sub('<[^>]*>','',item.findtext('description',''))).strip()
                    # Search results are leads, never verified listings.
                    if url not in entries:
                        entries[url]={'url':url,'title':title,'description':desc[:400],'source':source,'town':town,'first_seen':datetime.now(timezone.utc).isoformat(),'status':'Pista sin verificar'}
                    entries[url]['last_seen']=datetime.now(timezone.utc).isoformat()
                    found+=1
                if not hits:note='La búsqueda indirecta no devolvió resultados; NO implica ausencia de inmuebles.'
            except Exception as e:
                note=f'{type(e).__name__}: {str(e)[:130]}'
            checks.append({'source':source,'town':town,'status':status,'results':found,'note':note})
            time.sleep(.25)
    output={'updated_at':datetime.now(timezone.utc).isoformat(),'method':'Bing RSS: descubrimiento indirecto, no rastreo completo ni comprobación de fichas','items':list(entries.values()),'checks':checks}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{len(checks)} consultas; {len(entries)} pistas acumuladas')

if __name__=='__main__':run()
