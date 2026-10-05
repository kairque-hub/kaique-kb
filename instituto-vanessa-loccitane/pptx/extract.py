"""Extrai de um deck HTML: textos (com posição/estilo), imagens e fundo de cada página."""
import glob, json, pathlib, sys
from playwright.sync_api import sync_playwright
D = pathlib.Path(sys.argv[1]); src = sys.argv[2]; out = pathlib.Path(sys.argv[3]); out.mkdir(exist_ok=True)
css = "\n".join((D/"fontes"/f).read_text() for f in ["intertight.css", "instrument.css", "caslon.css"]) + "\n" + (D/"deck.css").read_text()
build = D/".pptx.build.html"; build.write_text((D/src).read_text().replace("/*{{CSS}}*/", css))
JS = r"""
() => {
 const pages=[...document.querySelectorAll('.page')]; const res=[];
 const isInline = el => { const d=getComputedStyle(el).display; return d==='inline' };
 const blockOf = n => { let e=n.parentElement; while(e && isInline(e)) e=e.parentElement; return e };
 const opa = el => { let o=1; while(el){ o*=parseFloat(getComputedStyle(el).opacity); el=el.parentElement } return o };
 pages.forEach((pg,pi)=>{
  const pr=pg.getBoundingClientRect(); const groups=new Map();
  const tw=document.createTreeWalker(pg,NodeFilter.SHOW_TEXT);
  let n; while(n=tw.nextNode()){ if(!n.textContent.trim()) continue;
    const ps=getComputedStyle(n.parentElement); if(ps.visibility==='hidden'||ps.display==='none') continue;
    const b=blockOf(n); if(!groups.has(b)) groups.set(b,[]); }
  const texts=[];
  for(const [b] of groups){
    const runs=[]; let rng=document.createRange(); let first=null,last=null;
    const walk = el => { for(const c of el.childNodes){
      if(c.nodeType===3){ if(!c.textContent.length) continue; const s=getComputedStyle(c.parentElement);
        let t=c.textContent.replace(/\s+/g,' '); if(s.textTransform==='uppercase') t=t.toUpperCase();
        runs.push({t,color:s.color,size:parseFloat(s.fontSize),fam:s.fontFamily.split(',')[0].replace(/['"]/g,'').trim(),
          w:parseInt(s.fontWeight),it:s.fontStyle==='italic',ls:s.letterSpacing==='normal'?0:parseFloat(s.letterSpacing),op:opa(c.parentElement)});
        if(c.textContent.trim()){ first=first||c; last=c } }
      else if(c.nodeType===1){ if(c.tagName==='BR'){runs.push({br:1});continue}
        if(!isInline(c)) continue; walk(c) } } };
    walk(b); if(!first) continue;
    rng.setStart(first,0); rng.setEnd(last,last.textContent.length);
    const rects=[...rng.getClientRects()].filter(r=>r.width>0); const r=rng.getBoundingClientRect();
    const bs=getComputedStyle(b); const lh=bs.lineHeight==='normal'?null:parseFloat(bs.lineHeight);
    const lines=new Set(rects.map(q=>Math.round(q.top))).size;
    // trim leading/trailing spaces
    while(runs.length&&(runs[0].br||!runs[0].t.trim())&&!runs[0].br) runs.shift();
    if(runs.length) runs[0].t=runs[0].t.replace(/^ /,''); if(runs.length&&runs.at(-1).t) runs.at(-1).t=runs.at(-1).t.replace(/ $/,'');
    let align=bs.textAlign; if(align==='start')align='left'; if(align==='end')align='right';
    const br=b.getBoundingClientRect(); const cx=br.left+parseFloat(bs.paddingLeft)+parseFloat(bs.borderLeftWidth)-pr.left; const cw=b.clientWidth-parseFloat(bs.paddingLeft)-parseFloat(bs.paddingRight);
    texts.push({cx,cw,fh:rects[0].height,x:r.left-pr.left,y:r.top-pr.top,w:r.width,h:r.height,align,lh,lines,runs});
  }
  const imgs=[...pg.querySelectorAll('img')].filter(i=>getComputedStyle(i).display!=='none').map(i=>{const r=i.getBoundingClientRect();
    return {x:r.left-pr.left,y:r.top-pr.top,w:r.width,h:r.height,src:i.getAttribute('src'),rad:parseFloat(getComputedStyle(i).borderTopLeftRadius)||0,op:opa(i)}});
  res.push({texts,imgs});
 });
 // congela bordas que usam currentColor e esconde textos e imagens
 for(const el of document.querySelectorAll('.page *')){ const s=getComputedStyle(el);
   for(const k of ['borderTopColor','borderRightColor','borderBottomColor','borderLeftColor']) el.style[k]=s[k]; }
 const st=document.createElement('style'); st.textContent='.page, .page *{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important} .page img{visibility:hidden!important}';
 document.head.appendChild(st);
 return res;
}"""
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
    pg.goto(build.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    data = pg.evaluate(JS); pg.wait_for_timeout(300)
    for i in range(len(data)):
        f = out/f"bg{i+1:02d}.png"; pg.locator(".page").nth(i).screenshot(path=str(f)); data[i]["bg"] = str(f)
    b.close()
build.unlink()
(out/"data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
print(len(data), "páginas;", sum(len(d["texts"]) for d in data), "textos;", sum(len(d["imgs"]) for d in data), "imagens")
