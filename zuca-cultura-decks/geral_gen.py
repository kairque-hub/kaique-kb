#!/usr/bin/env python3
"""Gera geral.html no estilo manual de marca: páginas claras, cards flutuantes,
fundo verde desfocado e faixas pixeladas em degradê verde."""
import pathlib, random
from PIL import Image

B = pathlib.Path(__file__).parent
GREENS = ["#E4F0A6", "#CFE37A", "#B6D250", "#9CC03C", "#7FA833", "#62912B", "#487524", "#35591C"]


def size(img):
    return Image.open(B / "img" / img).size


def photo(img, w, h, pos="center", r=10):
    W, H = size(img)
    assert max(w / W, h / H) <= 1.0, (img, w, h, W, H)
    return f'<div class="ph" style="width:{w}px;height:{h}px;border-radius:{r}px;background-image:url(img/{img});background-position:{pos}"></div>'


def stripe(w, h=34, cols=12, seed=1):
    """Faixa pixelada: 2 linhas de blocos em degradê verde, do claro ao escuro."""
    rnd = random.Random(seed)
    cells = []
    for row in range(2):
        for c in range(cols):
            t = c / (cols - 1)
            i = min(len(GREENS) - 1, max(0, int(t * (len(GREENS) - 1) + rnd.choice([-1, 0, 0, 1]) + row)))
            cells.append(f'<i style="background:{GREENS[i]}"></i>')
    return f'<div class="stp" style="width:{w}px;height:{h}px;grid-template-columns:repeat({cols},1fr)">{"".join(cells)}</div>'


def chrome(label, n):
    return f'''  <div class="lb tl">{label}</div>
  <div class="lb tr">Zuca + Cultura Artística</div>
  <div class="lb bl">Oportunidades de marca</div>
  <div class="lb br">{n:02d}</div>'''


def page(label, n, body, cls=""):
    return f'<section class="page {cls}">\n{chrome(label, n)}\n{body}\n</section>\n'


LOGOS = '<span class="lp"><img src="img/logo_zuca_w.png" style="height:22px"></span><span class="lp"><img src="img/logo_cultura_w.png" style="height:18px"></span>'

CSS = """
:root{--bg:#F1F1EF;--ink:#171717;--mut:#6B6B66;--g:#62912B}
html,body{background:var(--bg)}
.page{background:var(--bg);padding:0;font-family:'Inter Tight',sans-serif;color:var(--ink)}
.page.bl-bg{background:url(img/blur_verde.jpg) center/cover}
.page.bl-bg2{background:url(img/blur_verde2.jpg) center/cover}
.lb{position:absolute;font-size:8.5px;font-weight:500;line-height:1.2;z-index:5}
.lb.tl{left:24px;top:20px}.lb.tr{right:24px;top:20px}.lb.bl{left:24px;bottom:18px;color:var(--mut)}.lb.br{right:24px;bottom:18px;color:var(--mut)}
.card{position:absolute;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.card.bl{background:url(img/blur_verde.jpg) center/cover}
.card.bl2{background:url(img/blur_verde2.jpg) center/cover}
.in{padding:20px 22px}
.h1{font-size:30px;font-weight:500;letter-spacing:-.035em;line-height:1.02}
.h2{font-size:22px;font-weight:500;letter-spacing:-.03em;line-height:1.05}
.tx{font-size:11px;line-height:1.45;color:#3A3A36}
.sm{font-size:9.5px;line-height:1.4;color:var(--mut)}
.big{font-size:64px;font-weight:500;letter-spacing:-.05em;line-height:.9}
.stp{display:grid;grid-template-rows:1fr 1fr;position:absolute;left:0;bottom:0}
.stp i{display:block}
.lp{display:inline-flex;align-items:center;justify-content:center;background:#171717;border-radius:999px;height:44px;padding:0 20px;margin-right:8px}
.pill{display:inline-flex;align-items:center;background:#171717;color:#fff;border-radius:999px;padding:6px 16px;font-size:11px;font-weight:500;margin:0 6px 8px 0}
.pill.w{background:#fff;color:var(--ink)}
.ph{background-size:cover;background-position:center}
.abs{position:absolute}.row{display:flex}.col{display:flex;flex-direction:column}
.cap{font-size:8.5px;color:var(--mut);margin-top:4px}
"""

P = []

# 01 CAPA
P.append(f'''<section class="page bl-bg">
  <div class="lb tl">Proposta<br>comercial</div><div class="lb tr">2026–2028</div>
  <div class="abs" style="left:24px;top:210px;font-size:84px;font-weight:500;letter-spacing:-.05em;line-height:.95">Oportunidades<br>de marca</div>
  <div class="abs row" style="left:24px;bottom:28px;align-items:center">{LOGOS}</div>
  <div class="lb br" style="color:var(--ink)">Zuca + Cultura Artística</div>
</section>
''')

# 02 ÍNDICE
idx = [("Quem somos", "01"), ("A parceria", "02"), ("Espaços", "03"), ("Oportunidades", "04"), ("Prêmio 2028", "05")]
P.append(f'''<section class="page" style="background:#fff">
  <div class="lb tl">Proposta<br>comercial</div><div class="lb tr">Zuca + Cultura Artística</div>
  <div class="abs" style="left:24px;right:24px;bottom:34px">{"".join(f'<div class="row" style="justify-content:space-between;font-size:52px;font-weight:500;letter-spacing:-.04em;line-height:1.08"><span>{a}</span><span>{b}</span></div>' for a, b in idx)}</div>
</section>
''')

# 03 NÚMEROS
nums = [("26", "shows por ano: 13 no Auditório e 13 no Teatro Principal"), ("921", "lugares em dois palcos de padrão internacional"),
        ("13", "entrevistas ao vivo do Papo de Música, que viram anuário"), ("2", "festas de rua gratuitas por ano, da Roosevelt ao Copan"),
        ("1.000+", "artistas inscritos no Edital Zuca 2025"), ("5–6 mil", "assinantes e patronos do Cultura Artística")]
cards = ""
for i, (a, b) in enumerate(nums):
    x = 60 + (i % 3) * 364
    y = 70 + (i // 3) * 278
    if i in (1, 5):
        cards += f'<div class="card bl" style="left:{x}px;top:{y}px;width:344px;height:258px"><div class="in"><div class="big" style="font-size:{58 if len(a) > 4 else 72}px;">{a}</div><div class="tx" style="margin-top:12px;width:220px">{b}</div></div><div class="abs row" style="right:14px;bottom:14px"><span class="lp" style="height:28px;padding:0 12px"><img src="img/logo_zuca_w.png" style="height:13px"></span></div></div>'
    else:
        cards += f'<div class="card" style="left:{x}px;top:{y}px;width:344px;height:258px"><div class="in"><div class="big" style="font-size:{58 if len(a) > 4 else 72}px">{a}</div><div class="tx" style="margin-top:12px;width:230px">{b}</div></div>{stripe(344, 36, 12, i)}</div>'
P.append(page("A parceria<br>em números", 3, cards))

# 04 ZUCA
P.append(page("Quem somos<br>Zuca", 4, f'''  <div class="card" style="left:60px;top:70px;width:500px;height:535px">
    <div class="in" style="padding:26px 28px">
      <div class="row" style="justify-content:space-between;align-items:flex-start"><div class="h1" style="width:320px">A Casa da Música Brasileira</div><span class="lp" style="height:34px;padding:0 14px;margin:0"><img src="img/logo_zuca_w.png" style="height:17px"></span></div>
      <div class="tx" style="margin-top:22px">Um espaço de encontros, descobertas e celebrações. Desde a inauguração, em outubro de 2024, a Casa se firmou como palco de inovação e referência para a música brasileira contemporânea.</div>
      <div class="tx" style="margin-top:10px">Em 2025, consolidou uma programação viva, com experiências que aproximaram artistas, público e marcas: dezenas de eventos, milhares de pessoas impactadas e ampla repercussão na imprensa e nas redes.</div>
      <div class="tx" style="margin-top:10px">Funciona numa casa modernista de Gregori Warchavchik (1930), tombada pelo Iphan, com Jota.pê como embaixador.</div>
    </div>{stripe(500, 44, 14, 7)}
  </div>
  <div class="card" style="left:580px;top:70px;width:560px;height:535px;padding:16px;background:#fff">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
      <div>{photo("zuca_fachada_dia.jpg", 258, 172)}<div class="cap">Fachada</div></div>
      <div>{photo("zuca_musica.jpg", 258, 172)}<div class="cap">Convivência</div></div>
      <div>{photo("zuca_estudio.jpg", 258, 172)}<div class="cap">Estúdio</div></div>
      <div>{photo("zuca_jardim_petra.jpg", 258, 172)}<div class="cap">Jardim</div></div>
    </div>
  </div>'''))

# 05 CULTURA
aq = [("a_fachada.jpg", "Fachada"), ("a_teatro.jpg", "Teatro Principal"), ("a_auditorio.jpg", "Auditório"), ("a_foyer.jpg", "Foyer"), ("a_hall.jpg", "Hall"), ("a_corredor.jpg", "Salas de estudo")]
P.append(page("Quem somos<br>Cultura Artística", 5, f'''  <div class="card" style="left:60px;top:70px;width:440px;height:535px">
    <div class="in" style="padding:26px 28px">
      <div class="row" style="justify-content:space-between;align-items:flex-start"><div class="h1">Um patrimônio nacional</div><span class="lp" style="height:34px;padding:0 14px;margin:0"><img src="img/logo_cultura_w.png" style="height:14px"></span></div>
      <div style="font-size:15px;line-height:1.4;letter-spacing:-.01em;margin-top:22px">“Heitor Villa-Lobos e Camargo Guarnieri prepararam com carinho especial o concerto de inauguração do Teatro Cultura Artística e de abertura da temporada de 1950.”</div>
      <div class="sm" style="margin-top:6px">Ivan Ângelo</div>
      <div class="tx" style="margin-top:18px">Projeto de Rino Levi, com painel de Di Cavalcanti na fachada, tombado nas esferas federal, estadual e municipal. Reaberto em 2024, com Teatro Principal de 771 lugares e Auditório de 150.</div>
    </div>{stripe(440, 44, 12, 9)}
  </div>
  <div class="card" style="left:520px;top:70px;width:620px;height:535px;padding:18px">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px 12px">{"".join(f'<div>{photo(f, 187, 150)}<div class="cap">{c}</div></div>' for f, c in aq)}</div>
  </div>'''))

# 06 ALIANÇA (como a página de logo)
P.append(page("A parceria", 6, f'''  <div class="abs row" style="left:0;right:0;top:230px;justify-content:center;align-items:center">
    <span class="lp" style="height:60px;padding:0 28px"><img src="img/logo_zuca_w.png" style="height:30px"></span>
    <span class="lp" style="height:60px;padding:0 28px"><img src="img/logo_cultura_w.png" style="height:25px"></span>
    <span class="lp" style="height:60px;padding:0 30px;color:#fff;font-size:30px;font-weight:500;letter-spacing:-.03em;background:var(--g)">+ sua marca</span>
  </div>
  <div class="abs row" style="left:120px;right:120px;top:360px;gap:40px">
    <div style="flex:1"><div class="h2" style="font-size:18px">Zuca: o celeiro</div><div class="tx" style="margin-top:8px">Curadoria artística, projetos urbanos, formação de novos nomes, conteúdos digitais e atração da comunidade jovem.</div></div>
    <div style="flex:1"><div class="h2" style="font-size:18px">Cultura: o palco</div><div class="tx" style="margin-top:8px">Palcos de padrão internacional, chancela de excelência cultural e base engajada de assinantes e patronos.</div></div>
    <div style="flex:1"><div class="h2" style="font-size:18px">A marca: o ano todo</div><div class="tx" style="margin-top:8px">Juntos, ocupam o centro histórico, da Roosevelt ao Copan. A marca assina essa agenda, com exclusividade de categoria.</div></div>
  </div>''', "") .replace('<section class="page ">', '<section class="page" style="background:#fff">'))

# 07 ECOSSISTEMA (como IG Story)
eco = [("edital.jpg", "center top", "Edital de Música", "Descoberta, mentoria e aceleração de novos talentos de todo o Brasil. 1.000+ inscritos em 2025."),
       ("prosa.jpg", "center top", "Prosa", "Pensamento, troca e provocação sobre os caminhos da música e do entretenimento."),
       ("jam.jpg", "center top", "Zuca Jam", "Criação livre e coletiva entre intérpretes e compositores.")]
cc = ""
xs = [130, 370, 850]
for (f, p, t, d), x in zip(eco, xs):
    cc += f'<div class="card" style="left:{x}px;top:95px;width:220px;height:480px;border-radius:18px"><div style="padding:12px">{photo(f, 196, 172, p, 12)}</div><div style="padding:6px 16px"><div class="h2" style="font-size:20px">{t}</div><div class="tx" style="margin-top:8px">{d}</div></div>{stripe(220, 34, 8, len(t))}</div>'
cc += f'<div class="card bl2" style="left:610px;top:75px;width:220px;height:520px;border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center"><span class="pill w" style="font-size:24px;padding:10px 26px;letter-spacing:-.02em">Zuca</span><div style="font-size:13px;font-weight:500;text-align:center;margin-top:18px;width:160px">+ Zuca Podcast: a música brasileira pela memória de quem fez</div></div>'
P.append(page("Espaços<br>Ecossistema Zuca", 7, cc))

# 08 O PALCO
rows = [("Teatro Principal", "771 lugares", "Som e luz de última geração. Casa da Série Petrobras."), ("Auditório", "150 lugares", "Intimista, ideal para gravações ao vivo e lançamentos."),
        ("Espaço aberto para a rua", "", "Conexão com o trânsito de pedestres do centro."), ("Livraria Fauna e galerias", "", "Exposições, lançamentos, palestras e encontros.")]
rr = "".join(f'<div class="row" style="gap:14px;padding:12px 0;border-top:1px solid #E6E6E2"><div style="width:150px;flex:none"><div style="font-size:12.5px;font-weight:500">{a}</div><div class="sm">{b}</div></div><div class="tx">{c}</div></div>' for a, b, c in rows)
P.append(page("Espaços<br>O palco", 8, f'''  <div class="card" style="left:60px;top:70px;width:440px;height:535px"><div class="in" style="padding:26px 28px"><div class="h1">O palco de classe mundial</div><div style="margin-top:24px">{rr}</div></div>{stripe(440, 44, 12, 21)}</div>
  <div class="card" style="left:520px;top:70px;width:620px;height:535px;padding:18px">
    {photo("teatro.jpg", 584, 330)}<div class="cap">Teatro Principal</div>
    <div class="row" style="gap:12px;margin-top:10px"><div>{photo("auditorio.jpg", 286, 140)}<div class="cap">Auditório</div></div><div>{photo("foyer_rua.jpg", 286, 140)}<div class="cap">Foyer aberto para a rua</div></div></div>
  </div>'''))

# 09 CAFÉ PETRA
cr = [("Naming rights", "Café Petra no Cultura Artística, no horário comercial e na agenda noturna."), ("Exclusividade de portfólio", "Todo o portfólio de bebidas do Grupo Petrópolis em todos os eventos."),
      ("Conexão com a rua", "A marca no trânsito de pedestres do centro e no Cultura para a Rua."), ("Ativação gastronômica", "Operação da Esse eu Posso, com chef focado em bem-estar.")]
P.append(page("Espaços<br>Café Petra", 9, f'''  <div class="card bl" style="left:60px;top:70px;width:440px;height:535px"><div class="in" style="padding:26px 28px">
    <div class="h1" style="font-size:40px">Café Petra no Cultura Artística</div>
    <div class="tx" style="margin-top:14px;font-size:12px;color:var(--ink)">O café ganha o nome da marca e vira o ponto de convivência do teatro, com fluxo diário e atendimento exclusivo em dias de evento.</div>
    <div style="margin-top:22px">{"".join(f'<div style="background:#fff;border-radius:8px;padding:10px 14px;margin-bottom:8px"><div style="font-size:12px;font-weight:600;color:var(--ink)">{a}</div><div class="sm" style="margin-top:2px">{b}</div></div>' for a, b in cr)}</div>
  </div></div>
  <div class="card" style="left:520px;top:70px;width:620px;height:535px;padding:18px">
    <div class="row" style="gap:12px"><div>{photo("cafe2_bar.jpg", 290, 480)}<div class="cap">Balcão</div></div>
    <div class="col" style="gap:12px"><div>{photo("cafe2_balcao.jpg", 282, 222)}<div class="cap">Café e foyer</div></div><div>{photo("cafe2_salao.jpg", 282, 222)}<div class="cap">Salão</div></div></div></div>
  </div>'''))

# 10 OPORTUNIDADES (como IG Post)
op = [("Naming rights do café", "Exclusividade de categoria e de portfólio, com verba de trade contínua."),
      ("Cultura para a Rua", "2 festas por ano, aos domingos, com rua fechada, show de encontro, 2 DJs e atividades para crianças e pets."),
      ("Série Brasilidades", "26 shows por ano: 13 no Auditório e 13 no Teatro Principal."),
      ("Mentoria e capacitação", "Jovens da periferia, com estágio no Cultura em produção, som, luz, bilheteria, regência, roadie e mídias sociais."),
      ("Papo de Música e Anuário", "13 entrevistas ao vivo com Fabiane Pereira, no YouTube, que viram o Anuário da Cultura Brasileira."),
      ("Clube de assinantes", "5 a 6 mil assinantes e patronos, com prioridade e desconto para clientes da marca.")]
oc = ""
for i, (t, d) in enumerate(op):
    x = 60 + (i % 3) * 364
    y = 70 + (i // 3) * 278
    if i in (2, 3):
        oc += f'<div class="card bl{"2" if i == 3 else ""}" style="left:{x}px;top:{y}px;width:344px;height:258px"><div class="in"><div class="sm">{i+1:02d}</div><div class="h2" style="margin-top:14px">{t}</div></div><div class="abs" style="left:22px;right:22px;bottom:20px"><span class="pill w" style="font-size:10px;white-space:normal;line-height:1.35;border-radius:10px;padding:8px 12px">{d}</span></div></div>'
    else:
        oc += f'<div class="card" style="left:{x}px;top:{y}px;width:344px;height:258px"><div class="in"><div class="sm">{i+1:02d}</div><div class="h2" style="margin-top:14px">{t}</div><div class="tx" style="margin-top:10px;width:280px">{d}</div></div>{stripe(344, 36, 12, 40+i)}</div>'
P.append(page("Oportunidades", 10, oc))

# 11 PRÊMIO (como ID Badge)
P.append(page("Prêmio 2028", 11, f'''  <div class="card" style="left:150px;top:95px;width:280px;height:480px;border-radius:10px"><div class="in">
    <div class="h2">Prêmio Cultura Artística Brasileira</div>
    <div class="tx" style="margin-top:10px">O primeiro grande prêmio unificado das artes no Brasil, num contrato plurianual de 3 anos.</div>
    <div style="margin-top:16px"><span class="pill">Música</span><span class="pill">Cinema</span><span class="pill">Literatura</span><span class="pill">Moda</span><span class="pill" style="background:var(--g)">Artes Plásticas</span></div>
  </div>{stripe(280, 40, 10, 51)}</div>
  <div class="card bl" style="left:460px;top:75px;width:280px;height:520px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <img src="img/trofeu_foto.jpg" style="width:220px;display:block;border-radius:6px"><div class="cap" style="color:#fff">Imagem meramente ilustrativa</div></div>
  <div class="card" style="left:770px;top:95px;width:280px;height:480px;border-radius:10px"><div class="in">
    <div class="h2">Grande diferencial</div>
    <div class="tx" style="margin-top:10px">Além de consagrar artistas nos palcos e nas telas, o prêmio reconhece quem move a cultura nos bastidores: empresários, curadores, diretores de fotografia, produtores executivos e diretores artísticos.</div>
  </div>{stripe(280, 40, 10, 52)}</div>'''))

# 12 A NOITE (como Presentation)
steps = [("Rua", "Tapete da Roosevelt ao Copan, com público na calçada."), ("Abertura", "Show de encontro entre artista consagrado e talento do Edital."),
         ("Cerimônia", "771 lugares, entregas por pilar, prêmios de frente e de bastidor."), ("Depois", "Pós-cerimônia no Café Petra e na rua, com Zuca Jam.")]
ent = ["Naming do prêmio: “apresentado por [marca]”", "Patrocínio por pilar, com exclusividade", "Prêmio de bastidores assinado pela marca",
       "After no Café Petra", "Tapete e rua: experiência e amostragem", "Conteúdo e anuário com capítulo patrocinado", "ESG: formação dos jovens da cerimônia"]
P.append(page("Prêmio 2028<br>A noite", 12, f'''  <div class="card bl" style="left:60px;top:90px;width:520px;height:300px"><div class="in" style="padding:24px 26px">
    <div class="h1" style="font-size:36px">A noite<br>em 4 tempos.</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:22px">{"".join(f'<div style="background:#fff;border-radius:8px;padding:9px 12px;color:var(--ink)"><div style="font-size:11.5px;font-weight:600">{i+1}. {t}</div><div class="sm" style="margin-top:2px">{d}</div></div>' for i, (t, d) in enumerate(steps))}</div>
  </div></div>
  <div class="card" style="left:600px;top:90px;width:540px;height:300px"><div class="in" style="padding:24px 26px">
    <div class="h1" style="font-size:36px">Entradas de marca</div>
    <div style="margin-top:16px">{"".join(f'<div class="tx" style="padding:4px 0;border-top:1px solid #EEE">{e}</div>' for e in ent)}</div>
  </div>{stripe(540, 30, 16, 61)}</div>
  <div class="abs" style="left:60px;top:430px;width:1080px;font-size:44px;font-weight:500;letter-spacing:-.04em;line-height:1.02">Da rua ao after, a marca presente<br>em toda a noite da cultura brasileira.</div>'''))

# 13 CONTATO
P.append(f'''<section class="page bl-bg2">
  <div class="lb tl">Contato</div><div class="lb tr">Zuca + Cultura Artística</div>
  <div class="abs" style="left:0;right:0;top:230px;text-align:center">
    <span class="pill w" style="font-size:44px;padding:16px 40px;letter-spacing:-.03em;font-weight:500">Vamos construir juntos</span>
    <div style="font-size:15px;font-weight:600;margin-top:26px">comercial@talitamoraiis.com</div>
    <div style="font-size:12px;margin-top:6px">@acasadamusicabrasileira · @culturaartistica</div>
  </div>
  <div class="abs row" style="left:24px;bottom:28px;align-items:center">{LOGOS}</div>
  <div class="lb br" style="color:var(--ink)">13</div>
</section>
''')

html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Zuca + Cultura Artística · Oportunidades de marca</title>
<style>/*{{{{CSS}}}}*/
{CSS}</style></head><body>
{"".join(P)}</body></html>
'''
(B / "geral.html").write_text(html)
print("ok", len(P))
