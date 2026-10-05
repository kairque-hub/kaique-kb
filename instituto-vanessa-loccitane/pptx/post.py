import json, pathlib, re, sys
from PIL import Image, ImageStat
D=pathlib.Path(sys.argv[1]); d=json.load(open(D/'data.json'))
for pg in d:
    bg=Image.open(pg['bg']).convert('RGB')
    for t in pg['texts']:
        box=(int(t['x']*2),int(t['y']*2),int((t['x']+max(t['w'],2))*2),int((t['y']+max(t['h'],2))*2))
        mean=ImageStat.Stat(bg.crop(box)).median
        for r in t['runs']:
            if 'color' not in r: continue
            m=[float(v) for v in re.findall(r'[\d.]+',r['color'])]; a=(m[3] if len(m)>3 else 1)*r['op']
            if a<0.999:
                c=[round(m[k]*a+mean[k]*(1-a)) for k in range(3)]
                r['color']=f'rgb({c[0]},{c[1]},{c[2]})'; r['op']=1
    j=pg['bg'].replace('.png','.jpg'); bg.save(j,quality=90); pg['bg']=str(pathlib.Path(j).resolve())
json.dump(d,open(D/'data.json','w'),ensure_ascii=False)
