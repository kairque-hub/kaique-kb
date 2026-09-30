#!/usr/bin/env python3
"""Gera geral.html (layout corporativo: navegação no topo, faixa de título, blocos laranja)."""
import pathlib
from PIL import Image

B = pathlib.Path(__file__).parent
NAV = ["Quem somos", "A parceria", "Espaços e ativações", "Prêmio 2028"]


def size(img):
    return Image.open(B / "img" / img).size


def photo(img, w, h, pos="center"):
    """Foto em moldura w×h preenchendo sem ampliar além da resolução original."""
    W, H = size(img)
    assert max(w / W, h / H) <= 1.0, (img, w, h, W, H)
    return f'<div class="ph" style="width:{w}px;height:{h}px;background-image:url(img/{img});background-position:{pos}"></div>'


def head(active, title, desc):
    nav = "".join(f'<span class="{"on" if i == active else ""}">{n}</span>' for i, n in enumerate(NAV))
    return f'''  <div class="nav">{nav}</div>
  <div class="hd"><div class="tt">{title}</div><div class="ds">{desc}</div></div>'''


def page(active, title, desc, body, n):
    return f'''<section class="page">
{head(active, title, desc)}
{body}
  <div class="pn">{n:02d}</div>
</section>
'''


CSS = """
:root{--nv:#14204A;--o:#E8540F;--g:#8A90A2;--ln:#D9DCE3}
html,body{background:#fff}
.page{background:#fff;padding:0;font-family:'Noto Sans',sans-serif;color:var(--nv)}
.nav{position:absolute;right:60px;top:18px;display:flex;gap:64px;font-size:8.5px;color:#9CA1B0}
.nav span.on{color:var(--nv);font-weight:600}
.hd{position:absolute;left:0;right:0;top:44px;height:92px;border-bottom:1px solid var(--ln);display:flex;align-items:center;padding:0 40px;gap:40px}
.hd .tt{font-size:32px;font-weight:500;letter-spacing:-.01em;white-space:nowrap}
.hd .ds{font-size:10.5px;line-height:1.5;font-weight:500;max-width:460px}
.pn{position:absolute;right:40px;bottom:18px;font-size:9px;color:#9CA1B0}
.ph{background-size:cover;background-position:center}
.abs{position:absolute}
.row{display:flex}.col{display:flex;flex-direction:column}
.f1{flex:1}
.tx{font-size:11.5px;line-height:1.55}
.sm{font-size:9.5px;line-height:1.5;color:#5A6178}
.btn{display:inline-block;border:1.4px solid currentColor;border-radius:999px;padding:7px 20px;font-size:11px;font-weight:600}
.cell{border-right:1px solid var(--ln);border-bottom:1px solid var(--ln);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px 24px}
.big{font-size:52px;font-weight:400;letter-spacing:-.02em;line-height:1}
.big small{font-size:22px}
.lbl{font-size:13px;font-weight:600;line-height:1.3}
.bar{width:3px;background:var(--o);border-radius:2px;flex:none}
.circ{position:absolute;border:1.5px solid var(--nv);border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-size:12px;font-weight:600}
.pill{display:inline-block;border:1.2px solid var(--nv);border-radius:999px;padding:5px 16px;font-size:11px;font-weight:600;margin:0 6px 8px 0}
.cap{font-size:9px;color:var(--g);margin-top:4px}
"""

pages = []

# 01 CAPA
pages.append(f'''<section class="page">
  <div class="abs" style="left:0;top:0;width:640px;height:675px">
    <div class="abs row" style="left:40px;top:32px;align-items:flex-end;gap:18px"><img src="img/logo_zuca.png" style="height:34px;display:block"><img src="img/logo_cultura.png" style="height:27px;display:block"></div>
    <div class="abs" style="left:60px;top:175px;width:520px">
      <div style="font-size:50px;font-weight:600;line-height:1.12;letter-spacing:-.01em">Oportunidades de marca na música brasileira</div>
      <div class="tx" style="margin-top:22px;font-weight:500;width:470px">A tradição do Cultura Artística e a curadoria contemporânea da Zuca, a Casa da Música Brasileira, juntas no centro de São Paulo. Uma agenda contínua de shows, conteúdo, formação e experiências para a marca assinar.</div>
      <div style="margin-top:26px"><span class="btn">Proposta 2026–2028</span></div>
    </div>
  </div>
  <div class="abs" style="left:640px;top:0">{photo("zuca_fachada_dia.jpg", 560, 675, "42% center")}</div>
  <div class="abs row" style="left:0;right:0;bottom:22px;font-size:12px;font-weight:500">
    <span style="width:300px;text-align:center;color:#5A6178">Quem somos</span><span style="width:300px;text-align:center;color:#5A6178">A parceria</span><span style="width:300px;text-align:center;color:#fff">Espaços e ativações</span><span style="width:300px;text-align:center;color:#fff">Prêmio 2028</span>
  </div>
</section>
''')

# 02 NÚMEROS
cells = [("26", "", "shows por ano: 13 no Auditório e 13 no Teatro Principal"),
         ("921", "", "lugares em dois palcos de padrão internacional"),
         ("13", "", "entrevistas ao vivo do Papo de Música, que viram anuário"),
         ("2", "", "festas de rua gratuitas por ano, da Roosevelt ao Copan"),
         ("1.000", "+", "artistas inscritos no Edital Zuca 2025"),
         ("5–6", "mil", "assinantes e patronos do Cultura Artística")]
grid = "".join(f'<div class="cell" style="{"border-right:none;" if i % 3 == 2 else ""}{"border-bottom:none;" if i > 2 else ""}"><div class="big">{a}<small>{b}</small></div><div class="sm" style="margin-top:10px;max-width:220px">{c}</div></div>' for i, (a, b, c) in enumerate(cells))
pages.append(page(1, "A parceria em números", "Um celeiro criativo e um palco histórico, com uma agenda que a marca pode assinar o ano inteiro.",
    f'  <div class="abs" style="left:0;right:0;top:137px;bottom:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr">{grid}</div>', 2))

# 03 ZUCA
pages.append(page(0, "Zuca", "A Casa da Música Brasileira: um espaço de encontros, descobertas e celebrações, aberto em outubro de 2024 numa casa modernista de Warchavchik (1930).",
f'''  <div class="abs" style="left:0;top:137px;width:400px;height:538px;background:var(--o);color:#fff;padding:34px 40px">
    <div style="font-size:22px;font-weight:600;line-height:1.25">O que construímos</div>
    <div class="tx" style="margin-top:16px">Desde a inauguração, a Casa se firmou como palco de inovação e referência para a música brasileira contemporânea.</div>
    <div class="tx" style="margin-top:10px">Em 2025, consolidou uma programação viva, com experiências que aproximaram artistas, público e marcas: dezenas de eventos, milhares de pessoas impactadas e ampla repercussão na imprensa e nas redes.</div>
    <div class="tx" style="margin-top:10px">Edital de novos talentos, estúdios, podcast, Prosa e Jam, com Jota.pê como embaixador.</div>
    <div style="margin-top:22px"><span class="btn">@acasadamusicabrasileira</span></div>
  </div>
  <div class="abs" style="left:400px;top:137px">{photo("zuca_musica.jpg", 800, 538, "center 45%")}</div>''', 3))

# 04 CULTURA
aq = [("a_fachada.jpg", "Fachada"), ("a_teatro.jpg", "Teatro Principal"), ("a_auditorio.jpg", "Auditório"),
      ("a_foyer.jpg", "Foyer"), ("a_hall.jpg", "Hall"), ("a_corredor.jpg", "Salas de estudo")]
aqg = "".join(f'<div>{photo(f, 200, 150)}<div class="cap">{c}</div></div>' for f, c in aq)
pages.append(page(0, "Cultura Artística", "Um patrimônio nacional desde 1912: teatro de Rino Levi, com painel de Di Cavalcanti, tombado nas esferas federal, estadual e municipal.",
f'''  <div class="abs" style="left:40px;top:170px;width:420px">
    <div class="row" style="gap:14px"><div class="bar"></div><div style="font-size:15px;line-height:1.5;font-style:italic">“Heitor Villa-Lobos e Camargo Guarnieri prepararam com carinho especial o concerto de inauguração do Teatro Cultura Artística e de abertura da temporada de 1950.”<div class="sm" style="font-style:normal;margin-top:6px">Ivan Ângelo</div></div></div>
    <div class="tx" style="margin-top:22px">Na época, era um dos maiores e mais modernos complexos culturais da América Latina, com destaque para a acústica das salas. Seus palcos abrigaram espetáculos memoráveis de teatro, música, canto e dança.</div>
    <div class="tx" style="margin-top:10px">Reaberto em 2024, tem Teatro Principal de 771 lugares e Auditório de 150.</div>
  </div>
  <div class="abs" style="left:500px;top:170px;display:grid;grid-template-columns:repeat(3,200px);gap:14px 16px">{aqg}</div>''', 4))

# 05 ALIANÇA (diagrama de círculos)
pages.append(page(1, "A aliança", "A Zuca lança e gerencia a nova geração da música brasileira. O Cultura Artística dá o palco. Juntos, ocupam o centro histórico, da Roosevelt ao Copan.",
f'''  <div class="abs" style="left:465px;top:180px;width:300px;height:430px">
    <svg class="abs" style="left:0;top:0" width="300" height="430" viewBox="0 0 300 430"><circle cx="150" cy="215" r="130" fill="none" stroke="#14204A" stroke-width="1.2"/><path d="M232 110 l6 -2 -2 6" fill="none" stroke="#14204A" stroke-width="1.2"/><path d="M228 330 l-6 3 1 -6" fill="none" stroke="#14204A" stroke-width="1.2"/><path d="M28 225 l0 -7 5 4" fill="none" stroke="#14204A" stroke-width="1.2"/></svg>
    <div class="circ" style="left:88px;top:40px;width:124px;height:124px"><img src="img/logo_zuca.png" style="height:26px"></div>
    <div class="circ" style="left:196px;top:215px;width:124px;height:124px;border-color:var(--o)"><img src="img/logo_cultura.png" style="height:22px"></div>
    <div class="circ" style="left:-20px;top:215px;width:124px;height:124px;background:var(--o);border-color:var(--o);color:#fff">A marca</div>
    <div class="abs" style="left:95px;top:175px;width:110px;text-align:center;font-size:11px;font-weight:600;line-height:1.4">Polo cultural no centro de SP</div>
  </div>
  <div class="abs row" style="left:40px;top:185px;width:360px;gap:14px"><div class="bar"></div><div><div class="lbl">Zuca: celeiro e polo criativo</div><div class="tx" style="margin-top:6px">Curadoria artística, projetos urbanos, formação de novos nomes, conteúdos digitais e atração da comunidade jovem.</div></div></div>
  <div class="abs row" style="left:40px;top:430px;width:360px;gap:14px"><div class="bar"></div><div><div class="lbl">A marca: presença contínua</div><div class="tx" style="margin-top:6px">Assina produtos que acontecem o ano inteiro, com exclusividade de categoria, conteúdo próprio e relacionamento com o público.</div></div></div>
  <div class="abs row" style="left:830px;top:300px;width:330px;gap:14px"><div class="bar"></div><div><div class="lbl">Cultura Artística: o palco</div><div class="tx" style="margin-top:6px">Palcos de padrão internacional, chancela de excelência cultural e conexão com uma base engajada de assinantes e patronos.</div></div></div>''', 5))

# 06 ECOSSISTEMA ZUCA (colunas com foto)
cols = [("edital.jpg", "center top", "Edital de Música", "Descoberta, mentoria e aceleração de novos talentos de todo o Brasil. 1.000+ inscritos em 2025, com documentário anual."),
        ("zuca_estudio.jpg", "center", "Zuca Podcast", "Histórias da música brasileira pela memória de artistas, músicos e personalidades da indústria."),
        ("prosa.jpg", "center top", "Prosa", "Espaço de pensamento, troca e provocação sobre os caminhos da música e do entretenimento."),
        ("jam.jpg", "center top", "Zuca Jam", "Criação livre e coletiva entre intérpretes e compositores, com novas formas de expressão.")]
cc = "".join(f'<div style="border-right:{"1px solid var(--ln)" if i < 3 else "none"}">{photo(f, 300, 250, p)}<div style="padding:18px 22px"><div class="lbl" style="font-size:16px">{t}</div><div class="tx" style="margin-top:8px;color:#3A4260">{d}</div></div></div>' for i, (f, p, t, d) in enumerate(cols))
pages.append(page(2, "Ecossistema Zuca", "Quatro produtos que já existem e já têm público na Casa, e que a marca pode assinar e levar para o digital.",
    f'  <div class="abs" style="left:0;right:0;top:137px;display:grid;grid-template-columns:repeat(4,300px)">{cc}</div>', 6))

# 07 O PALCO
rows = [("Teatro Principal", "771 lugares", "Som e luz de última geração. Casa da Série Petrobras e de grandes apresentações."),
        ("Auditório", "150 lugares", "Espaço intimista da Série Zuca, ideal para gravações ao vivo e lançamentos."),
        ("Espaço aberto para a rua", "", "Conexão direta com o trânsito de pedestres do centro, para ativações urbanas."),
        ("Livraria Fauna e galerias", "", "Exposições, lançamentos de livros, palestras e encontros exclusivos.")]
rr = "".join(f'<div class="row" style="gap:18px;padding:16px 0;border-top:1px solid var(--ln)"><div style="width:170px;flex:none"><div class="lbl">{a}</div><div class="sm">{b}</div></div><div class="tx">{c}</div></div>' for a, b, c in rows)
pages.append(page(2, "O palco", "Infraestrutura de classe mundial no centro de São Paulo, reaberta em 2024 com padrão internacional de som e luz.",
f'''  <div class="abs" style="left:40px;top:165px;width:500px">{rr}</div>
  <div class="abs" style="left:600px;top:137px">{photo("teatro.jpg", 600, 340)}</div>
  <div class="abs row" style="left:600px;top:477px">{photo("auditorio.jpg", 300, 198)}{photo("foyer_rua.jpg", 300, 198)}</div>''', 7))

# 08 CAFÉ PETRA
cr = [("Naming rights", "Café Petra no Cultura Artística, com a marca assinando o espaço no horário comercial e na agenda noturna de shows."),
      ("Exclusividade de portfólio", "Venda exclusiva de todo o portfólio de bebidas do Grupo Petrópolis em todos os eventos do local."),
      ("Conexão com a rua", "O espaço aberto leva a marca ao trânsito de pedestres do centro e às ativações do Cultura para a Rua."),
      ("Ativação gastronômica", "Operação da Esse eu Posso, com cardápio de chef renomado, focado em comida saudável e bem-estar.")]
crr = "".join(f'<div class="row" style="gap:14px;margin-bottom:22px"><div class="bar"></div><div><div class="lbl">{a}</div><div class="tx" style="margin-top:4px">{b}</div></div></div>' for a, b in cr)
pages.append(page(2, "Café Petra", "O café ganha o nome da marca e vira o ponto de convivência do teatro, com fluxo diário e atendimento exclusivo em dias de evento.",
f'''  <div class="abs row" style="left:0;top:137px">{photo("cafe2_salao.jpg", 360, 538)}{photo("cafe2_bar.jpg", 360, 538, "center 40%")}</div>
  <div class="abs" style="left:760px;top:175px;width:400px">{crr}</div>''', 8))

# 09 OPORTUNIDADES
op = [("01", "Naming rights do café", "Exclusividade de categoria e de todo o portfólio de bebidas nos eventos, com verba de trade contínua."),
      ("02", "Cultura para a Rua", "2 festas por ano, aos domingos, com rua fechada e acesso gratuito: show de encontro, 2 DJs e atividades para crianças e pets."),
      ("03", "Série Brasilidades", "26 shows por ano com venda de ingressos: 13 no Auditório, com curadoria Zuca, e 13 no Teatro Principal."),
      ("04", "Mentoria e capacitação", "Mentorias na Zuca para jovens da periferia, com estágio no Cultura em produção, som, luz, bilheteria, regência, roadie e mídias sociais."),
      ("05", "Papo de Música e Anuário", "13 entrevistas ao vivo com Fabiane Pereira, no YouTube, que viram o Anuário da Cultura Brasileira."),
      ("06", "Clube de assinantes", "5 a 6 mil assinantes e patronos, com Jovens Patronos e prioridade e desconto para clientes e colaboradores da marca.")]
og = "".join(f'<div class="cell" style="align-items:flex-start;text-align:left;justify-content:flex-start;padding:30px 34px;{"border-right:none;" if i % 3 == 2 else ""}{"border-bottom:none;" if i > 2 else ""}"><div style="font-size:13px;font-weight:700;color:var(--o)">{n}</div><div style="font-size:22px;font-weight:600;margin-top:14px">{t}</div><div class="tx" style="margin-top:14px;color:#3A4260;font-size:13px">{d}</div></div>' for i, (n, t, d) in enumerate(op))
pages.append(page(2, "Oportunidades", "Seis frentes para a marca ativar, com exclusividade de segmento e presença o ano inteiro.",
    f'  <div class="abs" style="left:0;right:0;top:137px;bottom:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr">{og}</div>', 9))

# 10 PRÊMIO
pages.append(page(3, "Prêmio 2028", "Contrato plurianual de 3 anos, com a criação de uma premiação inédita na cena cultural do país.",
f'''  <div class="abs" style="left:40px;top:175px;width:640px">
    <div style="font-size:30px;font-weight:600;line-height:1.2">Prêmio Cultura Artística Brasileira: o primeiro grande prêmio unificado das artes no Brasil</div>
    <div style="margin-top:22px"><span class="pill">Música</span><span class="pill">Cinema</span><span class="pill">Literatura</span><span class="pill">Moda</span><span class="pill" style="background:var(--o);border-color:var(--o);color:#fff">Artes Plásticas</span></div>
    <div class="row" style="gap:14px;margin-top:24px"><div class="bar"></div><div><div class="lbl">Grande diferencial</div><div class="tx" style="margin-top:4px">Além de consagrar artistas nos palcos e nas telas, o prêmio reconhece quem move a cultura nos bastidores: empresários, curadores, diretores de fotografia, produtores executivos e diretores artísticos.</div></div></div>
  </div>
  <div class="abs" style="left:800px;top:137px;width:400px;height:538px;background:#F2F3F6;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <img src="img/trofeu_foto.jpg" style="width:270px;display:block;border-radius:4px"><div class="cap">Imagem meramente ilustrativa</div>
  </div>''', 10))

# 11 NOITE (roadmap em escada)
steps = [("Rua", "Tapete ligando a Roosevelt ao Copan, com público na calçada."),
         ("Abertura", "Show de encontro entre um artista consagrado e um talento do Edital."),
         ("Cerimônia", "771 lugares, entregas por pilar, com prêmios de frente e de bastidor."),
         ("Depois", "Pós-cerimônia no Café Petra e na rua, com Zuca Jam.")]
st = ""
for i, (t, d) in enumerate(steps):
    x = 40 + i * 280
    y = 420 - i * 60
    st += f'<div class="abs" style="left:{x}px;top:{y}px;width:270px"><div class="sm" style="color:var(--o);font-weight:700">Tempo {i+1}</div><div style="background:var(--o);color:#fff;font-size:13px;font-weight:600;padding:8px 14px;margin-top:4px">{t}</div><div class="sm" style="margin-top:8px;padding-right:20px">{d}</div></div>'
    st += f'<div class="abs" style="left:{x}px;top:{y+30}px;width:1px;height:{675-y-30}px;background:var(--ln)"></div>'
ent = ["<b>Naming do prêmio:</b> “apresentado por [marca]”.", "<b>Patrocínio por pilar,</b> com exclusividade de segmento.",
       "<b>Prêmio de bastidores</b> assinado pela marca.", "<b>After no Café Petra</b> no encerramento da noite.",
       "<b>Tapete e rua:</b> experiência e amostragem.", "<b>Conteúdo e anuário:</b> bastidores e capítulo patrocinado.",
       "<b>ESG:</b> formação dos jovens que operam a cerimônia."]
pages.append(page(3, "A noite do prêmio", "A premiação em quatro tempos, com a marca presente da rua ao after.",
f'''  {st}
  <div class="abs" style="left:40px;top:165px;width:560px">
    <div class="lbl">Entradas de marca</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 24px;margin-top:10px">{"".join(f'<div class="sm" style="color:var(--nv)">{e}</div>' for e in ent)}</div>
  </div>''', 11))

# 12 OBRIGADO
pages.append(f'''<section class="page">
  <div class="abs row" style="left:40px;top:32px;align-items:flex-end;gap:18px"><img src="img/logo_zuca.png" style="height:30px;display:block"><img src="img/logo_cultura.png" style="height:24px;display:block"></div>
  <div class="abs" style="left:60px;top:230px;width:480px">
    <div style="font-size:50px;font-weight:600">Obrigado</div>
    <div class="tx" style="margin-top:16px">Vamos construir juntos uma presença de marca que vive a música brasileira o ano inteiro.</div>
    <div class="tx" style="margin-top:18px;font-weight:600">comercial@talitamoraiis.com</div>
    <div class="sm" style="margin-top:4px">@acasadamusicabrasileira · @culturaartistica</div>
    <div style="margin-top:24px"><span class="btn">Fale com a gente</span></div>
  </div>
  <div class="abs" style="left:640px;top:0">{photo("auditorio.jpg", 560, 675, "60% center")}</div>
</section>
''')

html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Zuca + Cultura Artística · Oportunidades de marca</title>
<style>/*{{{{CSS}}}}*/
{CSS}</style></head><body>
{"".join(pages)}</body></html>
'''
(B / "geral.html").write_text(html)
print("ok", len(pages))
