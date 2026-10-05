const pptxgen = require('pptxgenjs'); const fs = require('fs'); const path = require('path');
const [,, dataFile, imgBase, outFile, title] = process.argv;
const data = JSON.parse(fs.readFileSync(dataFile));
const PX = 1/90, PT = 0.8;
const pres = new pptxgen(); pres.defineLayout({name:'D', width:13.333, height:7.5}); pres.layout='D';
pres.title = title;
const parse = c => { const m=c.match(/[\d.]+/g).map(Number); const hex=m.slice(0,3).map(v=>Math.round(v).toString(16).padStart(2,'0')).join('').toUpperCase(); return {hex, a: m.length>3?m[3]:1}; };
const face = (f,w) => {
  if (f==='Inter Tight' || f==='Instrument Sans') { if (w===300) return [f+' Light',false]; if (w===500) return [f+' Medium',false]; if (w===600) return [f+' SemiBold',false]; if (w>=700) return [f,true]; }
  return [f, w>=600];
};
data.forEach((pg, i) => {
  const s = pres.addSlide();
  s.background = { path: pg.bg };
  pg.imgs.forEach((im, k) => s.addImage({ path: path.join(imgBase, `p${i+1}_img${k}.png`), x: im.x*PX, y: im.y*PX, w: im.w*PX, h: im.h*PX, transparency: Math.round((1-im.op)*100), objectName: `Foto ${k+1}` }));
  pg.texts.forEach(t => {
    const runs = [];
    t.runs.forEach((r, k) => {
      if (r.br) { if (runs.length) runs[runs.length-1].options.breakLine = true; return; }
      if (!r.t) return;
      const c = parse(r.color); const [ff, bold] = face(r.fam, r.w);
      const o = { fontFace: ff, fontSize: +(r.size*PT).toFixed(1), color: c.hex, bold, italic: r.it };
      const tr = Math.round((1 - c.a*r.op)*100); if (tr > 0) o.transparency = tr;
      if (r.ls) o.charSpacing = +(r.ls*PT).toFixed(2);
      runs.push({ text: r.t, options: o });
    });
    if (!runs.length) return;
    let x, w;
    if (t.lines > 1) { x = t.cx; w = t.cw * 1.015 + 2; }
    else { const slack = t.w*0.1 + 10; x = t.x; w = t.w + slack;
      if (t.align === 'center') x -= slack/2; else if (t.align === 'right') x -= slack; }
    let y = t.y; const o = { x: x*PX, w: w*PX, margin: 0, align: t.align === 'justify' ? 'left' : t.align, valign: 'top', isTextBox: true, fit: 'none' };
    if (t.lh) { o.lineSpacing = +(t.lh*PT).toFixed(1); y -= (t.lh - t.fh)/2; }
    o.y = y*PX; o.h = Math.max(t.h + (t.lh ? t.lh - t.fh : 0), 10)*PX;
    s.addText(runs, o);
  });
});
pres.writeFile({ fileName: outFile }).then(f => console.log('ok', f));
