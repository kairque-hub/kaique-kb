// Uso: node render.js shot <html> <seletor>=<png> ...   |   node render.js pdf <html> <pdf> <largura> <altura>
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const [modo, html, ...resto] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage();
  const erros = [];
  pg.on('pageerror', e => erros.push(String(e)));
  await pg.goto('file://' + path.resolve(html));
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(500);
  if (modo === 'shot') {
    for (const par of resto) {
      const [sel, out] = par.split('=');
      await pg.locator(sel).screenshot({ path: out, omitBackground: true });
    }
  } else if (modo === 'pdf') {
    const [out, w, h] = resto;
    await pg.pdf({ path: out, width: w + 'px', height: h + 'px', printBackground: true });
  } else if (modo === 'pages') {
    const [prefixo, w, h] = resto;
    await pg.setViewportSize({ width: +w, height: +h });
    const n = await pg.locator('.slide').count();
    for (let i = 0; i < n; i++)
      await pg.locator('.slide').nth(i).screenshot({ path: `${prefixo}${String(i + 1).padStart(2, '0')}.png` });
  }
  await b.close();
  if (erros.length) { console.error('ERROS JS:', erros); process.exit(1); }
})();
