import json,re,os,sys
S=json.load(open('strings.json',encoding='utf-8'))
os.makedirs('build/i18n',exist_ok=True)
bad=0
for lang in ('en','ru','ar'):
    tr={}
    for part in (0,1,2,3,4,5,6):
        for line in open(f'tx/{lang}_{part}.txt',encoding='utf-8'):
            line=line.rstrip('\n')
            if not line.strip(): continue
            m=re.match(r'(\d+)\|\|\|(.*)$',line)
            if not m: print('bad line',lang,line[:60]); bad+=1; continue
            tr[int(m[1])]=m[2]
    out={}
    for i,e in enumerate(S):
        if i not in tr: print('missing',lang,i,e['k'][:50]); bad+=1; continue
        v=tr[i]
        key=e['k']
        if v=='=': v=e.get('src',e['k'])
        if 'Travel' in key or 'Travel' in v: continue
        out[key]=v
    json.dump(out,open(f'build/i18n/{lang}.json','w',encoding='utf-8'),ensure_ascii=False)
    print(lang,len(out))
sys.exit(1 if bad else 0)
