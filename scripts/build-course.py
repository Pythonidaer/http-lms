"""Build guided HTTP lessons and the complete pinned MDN reference collection.

Authoring dependencies: beautifulsoup4 and markdownify. The built website has none.
"""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin
from markdownify import markdownify
from curriculum import make_course, HANDBOOK_MAP

ROOT=Path(__file__).resolve().parents[1]
MDN='https://developer.mozilla.org/en-US/docs/'
COMMIT='bf7ff749b987d530e9a6c07f23ac66f94d968e57'
inventory=json.loads((ROOT/'docs/source-inventory.json').read_text())

def macro(match):
    name=match[1].lower();args=re.findall(r'"([^"]*)"',match[2] or '')
    if name in ('specifications','compat','subpageswithsummaries','interactiveexample','embedlivesample','previousmenunext','apiref'):return ''
    badges={'experimental_inline':'Experimental','seecompattable':'Experimental: check current support','deprecated_inline':'Deprecated','non-standard_inline':'Non-standard','securecontext_header':'Requires a secure context','optional_inline':'optional'}
    if name in badges:return '('+badges[name]+')'
    if not args:return ''
    key=args[0];label=args[1] if len(args)>1 else key
    if name=='httpheader':slug='Web/HTTP/Reference/Headers/'+key
    elif name=='httpmethod':slug='Web/HTTP/Reference/Methods/'+key
    elif name=='httpstatus':slug='Web/HTTP/Reference/Status/'+key
    elif name=='csp':slug='Web/HTTP/Reference/Headers/Content-Security-Policy/'+key
    elif name=='glossary':slug='Glossary/'+key
    elif name=='domxref':slug='Web/API/'+key.removesuffix('()').replace('.','/')
    elif name=='htmlelement':slug='Web/HTML/Reference/Elements/'+key
    elif name=='svgelement':slug='Web/SVG/Reference/Element/'+key
    elif name=='cssxref':slug='Web/CSS/'+key
    elif name=='jsxref':
        key=key.removesuffix('()');slug='Web/JavaScript/Reference/'+key if key.startswith(('Operators/','Statements/')) else 'Web/JavaScript/Reference/Global_Objects/'+key.replace('.','/')
    elif name=='rfc':
        nums=re.findall(r'\d+',match[2] or '');number=nums[0] if nums else key
        return f'[RFC {number}](https://www.rfc-editor.org/rfc/rfc{number}.html)'
    else:return label
    return f'[`{label}`]({MDN+slug.replace(" ","_")})'

def clean(body,url,source_path):
    # Protect code: even HTML examples and comments must remain verbatim inert text.
    code=[]
    def protect(m):
        code.append(re.sub(r'^```([^\s`]+)[^\n]*',r'```\1',m[0]));return f'HTTP_CODE_TOKEN_{len(code)-1}'
    body=re.sub(r'^```[^\n]*\n.*?^```\s*$',protect,body,flags=re.S|re.M)
    body=re.sub(r'<!--.*?-->','',body,flags=re.S)
    body=re.sub(r'\{\{\s*([\w-]+)(?:\((.*?)\))?\s*\}\}',macro,body)
    # Markdownify only actual HTML fragments; leave source Markdown intact.
    body=re.sub(r'<(table|dl|ul|ol)(?:\s[^>]*)?>.*?</\1>',lambda m:markdownify(m[0],heading_style='ATX').strip(),body,flags=re.S)
    body=re.sub(r'<a\s[^>]*>.*?</a>',lambda m:markdownify(m[0]).strip(),body,flags=re.S)
    body=re.sub(r'<summary>(.*?)</summary>',r'**\1**',body,flags=re.S)
    body=re.sub(r'</?(?:details|div|span|sup|section)(?:\s[^>]*)?>','',body)
    body=body.replace('> [!NOTE]','> **Note:**').replace('> [!WARNING]','> **Warning:**').replace('> [!TIP]','> **Tip:**')
    body=body.replace('](/en-US/docs/',']('+MDN)
    body=re.sub(r'\]\(#([^)]*)\)',lambda m:']('+url+'#'+m[1]+')',body)
    body=re.sub(r'!\[([^\]]*)\]\(([^)]*)\)',lambda m:'[Diagram: '+m[1]+']('+ (m[2] if m[2].startswith('http') else f'https://raw.githubusercontent.com/mdn/content/{COMMIT}/'+str(Path(source_path).parent/m[2])) +')',body)
    for i,c in enumerate(code):body=body.replace(f'HTTP_CODE_TOKEN_{i}',c)
    return body.strip()

def parts(body,limit=12500):
    # Split at paragraph boundaries outside code, never in the middle of a fence.
    blocks=[];buf=[];fence=False
    for line in body.splitlines():
        if line.lstrip().startswith('```'):fence=not fence
        if not line.strip() and not fence:
            if buf:blocks.append('\n'.join(buf));buf=[]
        else:buf.append(line)
    if buf:blocks.append('\n'.join(buf))
    out=[];buf=''
    for block in blocks:
        if len(block)>limit:
            if block.startswith('```'):raise ValueError('Oversized code example')
            if buf:out.append(buf);buf=''
            # Large lists/tables are divided on complete rows, retaining their order.
            rows=block.splitlines();header=''
            if len(rows)>1 and re.match(r'^\|.*\|$',rows[0]) and re.match(r'^\|[- :|]+\|$',rows[1]):header='\n'.join(rows[:2]);rows=rows[2:]
            chunk=header
            for row in rows:
                if len(chunk)+len(row)+1>limit:out.append(chunk);chunk=header
                chunk+=(('\n' if chunk else '')+row)
            if chunk:out.append(chunk)
        elif len(buf)+len(block)+2>limit:
            out.append(buf);buf=block
        else:buf+=(('\n\n' if buf else '')+block)
    if buf:out.append(buf)
    return out

def reference(item):
    path=item['path'];local='docs/mdn/'+path.removeprefix('files/en-us/')
    raw=(ROOT/local).read_text();front,text=raw.split('---',2)[1:]
    title=re.search(r'^title: (.+)$',front,re.M)[1].strip('"\'')
    slug=re.search(r'^slug: (.+)$',front,re.M)[1];url=MDN+slug
    id='ref-'+hashlib.sha256(slug.encode()).hexdigest()[:16]
    intro='Optional reference. Consult this page when a lesson or a real request needs it; it is not required for the final assessment.\n\nSource: ['+title+']('+url+'). Adapted from MDN contributors under [CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/). Snapshot: 2026-10-07.'
    flags=[]
    for badge in ('experimental','deprecated','non-standard'):
        if re.search(r'^\s*- '+re.escape(badge)+r'\s*$',front,re.M):flags.append(badge)
    if flags:intro+='\n\n**Source flags:** '+', '.join(flags)+'. Verify current support before adopting this feature.'
    chunks=[];heading=title;buf=[];fence=False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):fence=not fence
        if not fence and re.match(r'^#{2,6} ',line):
            if '\n'.join(buf).strip():chunks.append((heading,'\n'.join(buf)))
            heading=re.sub(r'^#+ ','',line);buf=[]
        else:buf.append(line)
    if '\n'.join(buf).strip():chunks.append((heading,'\n'.join(buf)))
    slides=[dict(id=id+'-s1',title='How to use this reference',body=intro)]
    for heading,body in chunks:
        if heading.lower() in ('specifications','browser compatibility'):
            body=f'Consult [MDN’s current {heading.lower()} section]({url}#{heading.lower().replace(" ","_")}) for generated specification links and engine-support tables.'
        else:body=clean(body,url,path)
        if not body:continue
        for i,piece in enumerate(parts(body)):
            slides.append(dict(id=id+f'-s{len(slides)+1}',title=heading+(f' — part {i+1}' if len(parts(body))>1 else ''),body=piece))
    source=dict(title=title,url=url,lessonId=id,sourcePath=local,upstreamPath=path,upstreamBlob=item['sha'],sha256=hashlib.sha256(raw.encode()).hexdigest(),headings=re.findall(r'^#{2,6} (.+)$',text,re.M),flags=flags)
    return dict(id=id,type='slides',title=title,optional=True,slides=slides),source

course=make_course();groups=defaultdict(list);sources=[]
for item in inventory:
    lesson,source=reference(item);sources.append(source);path=item['path']
    if '/web/http/guides/' in path:group='Guides and troubleshooting'
    elif '/headers/content-security-policy/' in path:group='Content Security Policy directives'
    elif '/headers/permissions-policy/' in path:group='Permissions Policy directives'
    elif '/headers/' in path:group='Headers'
    elif '/methods/' in path:group='Methods'
    elif '/status/' in path:group='Status codes'
    elif not path.startswith('files/en-us/web/http/'):group='Supplemental browser and JavaScript foundations'
    else:group='HTTP indexes and specifications'
    groups[group].append(lesson)
refchildren=[]
for i,(name,nodes) in enumerate(groups.items()):
    # Header names sort alphabetically; numeric status names already sort naturally.
    nodes.sort(key=lambda n:n['title'].lower())
    refchildren.append(dict(id=f'reference-group-{i+1}',type='section',title=name,collapsed=True,children=nodes))
course['sections'].append(dict(id='reference-library',type='section',title='Reference library — optional',collapsed=True,children=refchildren))
(ROOT/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
embedded=json.dumps(course,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
(ROOT/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Learn HTTP with guided lessons, practical exercises and a complete MDN HTTP reference collection."><title>HTTP</title><link rel="stylesheet" href="lms.css"><script src="vendor/marked.umd.js" defer></script><script src="lesson-markdown.js" defer></script><script src="lms-runtime.js" defer></script></head><body class="lms-export-body"><div id="lms-root"></div><script id="lms-course-data" type="application/json">'+embedded+'</script></body></html>\n')
manifest=dict(retrievedAt='2026-10-07',mdnCommit=COMMIT,mdnHttpPages=sum('/web/http/' in s['upstreamPath'] for s in sources),supplementalPages=sum('/web/http/' not in s['upstreamPath'] for s in sources),handbook=dict(title='HTTP Networking in JavaScript – Handbook for Beginners',author='Lane Wagner',url='https://www.freecodecamp.org/news/http-full-course/',adaptation='Map all eleven technical top-level topics to original lessons. No full article text or code reproduction; technical details are grounded in the licensed MDN references.',topics=HANDBOOK_MAP),sources=sources)
(ROOT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
flat=[]
def walk(nodes):
    for n in nodes:
        if n['type']=='section':walk(n['children'])
        else:flat.append(n)
walk(course['sections'])
stats=dict(coreDecks=sum(n['type']=='slides' and not n.get('optional') for n in flat),coreSlides=sum(len(n.get('slides',[])) for n in flat if not n.get('optional')),referenceDecks=sum(bool(n.get('optional')) for n in flat),referenceSlides=sum(len(n.get('slides',[])) for n in flat if n.get('optional')),moduleQuizzes=sum(n['type']=='quiz' for n in flat),moduleQuestions=sum(len(n.get('questions',[])) for n in flat),finalQuestions=len(course['finalQuiz']['questions']))
(ROOT/'course-stats.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats))
