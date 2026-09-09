#!/usr/bin/env python3
"""Gera o deck em HTML e fecha em PDF (13,333in x 7,5in, 16:9)."""
import base64, glob, pathlib, subprocess, sys
B = pathlib.Path(__file__).parent
def uri(p):
    return "data:image/jpeg;base64," + base64.b64encode((B/p).read_bytes()).decode()
FOTO = {k: uri(f"img/{k}.jpg") for k in ("publico","duo","pb","perfil","capa")}
FONTES = (B/"fontes/deck.css").read_text()

OURO="#A8761F"; AZUL="#2472A3"; CLAY="#9E3D2A"
OUROD="#D2A24C"; TINTA="#16150F"; MUDO="#78736A"; FIO="#E7E4DE"

S=[]  # slides
def slide(html, dark=False, cls=""):
    S.append(f'<section class="sl {"dk" if dark else ""} {cls}">{html}</section>')

def topo(eyebrow, n, dark=False):
    return (f'<div class="topo"><span class="eb">{eyebrow}</span>'
            f'<span class="pg">{n}</span></div>')

def h1(t, sub=None):
    s = f'<p class="lead">{sub}</p>' if sub else ""
    return f'<h1>{t}</h1>{s}'

def nota(t):
    return f'<p class="nota">{t}</p>'

# ---------- gráficos ----------
def barras_h(itens, larg=560, alt_barra=22, passo=42, maxv=None, cor=OURO,
             rot_larg=210, fmt=lambda v: f"{v:,}".replace(",","."), dark=False):
    """itens: [(rotulo, sub, valor, cor_opcional)]"""
    maxv = maxv or max(i[2] for i in itens)
    h = passo*len(itens)
    txt = "#F5F3EF" if dark else TINTA
    mut = "#9A948A" if dark else MUDO
    out = [f'<svg class="g" viewBox="0 0 {rot_larg+larg+70} {h+10}">']
    for i,it in enumerate(itens):
        rot, sub, val = it[0], it[1], it[2]
        c = it[3] if len(it)>3 else cor
        y = i*passo
        w = max(2, val/maxv*larg)
        out.append(f'<text x="{rot_larg-14}" y="{y+alt_barra*0.62}" text-anchor="end" '
                   f'style="font-family:Inter;font-weight:600;font-size:13.5px;fill:{txt}">{rot}</text>')
        if sub:
            out.append(f'<text x="{rot_larg-14}" y="{y+alt_barra*0.62+15}" text-anchor="end" '
                       f'style="font-family:Inter;font-weight:300;font-size:11px;fill:{mut}">{sub}</text>')
        out.append(f'<rect x="{rot_larg}" y="{y}" width="{w:.1f}" height="{alt_barra}" rx="2" fill="{c}"/>')
        out.append(f'<text x="{rot_larg+w+10}" y="{y+alt_barra*0.72}" '
                   f'style="font-family:\'IBM Plex Mono\';font-weight:500;font-size:12.5px;fill:{mut}">{fmt(val)}</text>')
    out.append('</svg>')
    return "".join(out)

def barras_emp(cats, series, larg=520, alt=26, passo=42, rot_larg=190, dark=False):
    """empilhado 100%: cats=[nome], series=[(nome,cor,[v por cat])]"""
    txt = "#F5F3EF" if dark else TINTA
    mut = "#9A948A" if dark else MUDO
    h = passo*len(cats)
    out=[f'<svg class="g" viewBox="0 0 {rot_larg+larg+60} {h+10}">']
    for i,c in enumerate(cats):
        y=i*passo; x=rot_larg
        if rot_larg:
            out.append(f'<text x="{rot_larg-14}" y="{y+alt*0.68}" text-anchor="end" '
                       f'style="font-family:Inter;font-weight:600;font-size:13px;fill:{txt}">{c}</text>')
        for nome,cor,vals in series:
            w=vals[i]/100*larg
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(0,w-2):.1f}" height="{alt}" fill="{cor}"/>')
            if w>44:
                lab=f"{vals[i]:.1f}%".replace(".",",")
                out.append(f'<text x="{x+w/2-1:.1f}" y="{y+alt*0.68}" text-anchor="middle" '
                           f'style="font-family:\'IBM Plex Mono\';font-weight:500;font-size:11.5px;fill:#FFF">{lab}</text>')
            x+=w
    out.append('</svg>')
    return "".join(out)

def barras_grupo(cats, series, larg=560, alth=138, rot_larg=0, dark=False):
    """colunas agrupadas: series=[(nome,cor,[v])]"""
    txt = "#F5F3EF" if dark else TINTA
    mut = "#9A948A" if dark else MUDO
    fio = "#2C2A26" if dark else FIO
    n=len(cats); ns=len(series)
    passo=larg/n; bw=min(26,(passo-18)/ns)
    maxv=max(max(s[2]) for s in series)
    out=[f'<svg class="g" viewBox="0 0 {larg+20} {alth+52}">']
    for gy in (0,.5,1):
        y=alth-gy*alth
        out.append(f'<line x1="0" y1="{y:.1f}" x2="{larg}" y2="{y:.1f}" stroke="{fio}" stroke-width="1"/>')
    for i,c in enumerate(cats):
        cx=i*passo+passo/2
        for j,(nome,cor,vals) in enumerate(series):
            hh=vals[i]/maxv*alth
            x=cx-(ns*bw+ (ns-1)*3)/2 + j*(bw+3)
            out.append(f'<rect x="{x:.1f}" y="{alth-hh:.1f}" width="{bw:.1f}" height="{hh:.1f}" rx="2" fill="{cor}"/>')
        out.append(f'<text x="{cx:.1f}" y="{alth+20}" text-anchor="middle" '
                   f'style="font-family:Inter;font-weight:600;font-size:12.5px;fill:{txt}">{c}</text>')
    out.append('</svg>')
    return "".join(out)

def legenda(itens, dark=False):
    mut = "#9A948A" if dark else MUDO
    p="".join(f'<span><i style="background:{c}"></i>{n}</span>' for n,c in itens)
    return f'<div class="leg" style="color:{mut}">{p}</div>'

def rosca(pct, rot, sub, cor=OURO, dark=False):
    r=52; C=2*3.14159*r; on=C*pct/100
    txt = "#F5F3EF" if dark else TINTA
    mut = "#9A948A" if dark else MUDO
    fio = "#2C2A26" if dark else FIO
    return (f'<svg class="g" viewBox="0 0 140 140" style="width:150px">'
            f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{fio}" stroke-width="14"/>'
            f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{cor}" stroke-width="14"'
            f' stroke-dasharray="{on:.1f} {C-on:.1f}" transform="rotate(-90 70 70)"/>'
            f'<text x="70" y="68" text-anchor="middle" style="font-family:Newsreader;font-weight:400;font-size:31px;fill:{txt}">{rot}</text>'
            f'<text x="70" y="87" text-anchor="middle" style="font-family:Inter;font-weight:300;font-size:10.5px;fill:{mut}">{sub}</text>'
            f'</svg>')

def stats(itens, cols=3):
    c="".join(f'<div class="st"><div class="v">{v}</div><div class="k">{k}</div>'
              f'{f"<div class=s>{s}</div>" if s else ""}</div>' for v,k,s in itens)
    return f'<div class="stg" style="grid-template-columns:repeat({cols},1fr)">{c}</div>'

# ═══════════════════ SLIDES ═══════════════════
N=lambda i: f"{i:02d}"

# 01 CAPA
slide(f'''
<img class="capa-img" src="{FOTO['capa']}" alt="Vanessa da Mata no Palco Sunset">
<div class="capa-txt">
  <p class="eb ouro">Relatório de performance digital</p>
  <h1 class="tit-capa">Vanessa da&nbsp;Mata<br><em>no Rock in Rio</em></h1>
  <p class="capa-sub">Palco Sunset · 7 de setembro de 2026 · 15h00</p>
  <p class="capa-fio">Primeira atração do dia. Primeira no ar na transmissão nacional.</p>
  <div class="capa-rod"><span>Apuração de 5 a 9 de setembro de 2026</span><span>Equipe digital</span></div>
</div>
''', dark=True, cls="capa-s")

# 02 SUMÁRIO
itens_sum=[("01","O contexto","O que estava em jogo naquela tarde"),
 ("02","Alcance digital","1,07 milhão de visualizações"),
 ("03","Conteúdos","O que performou e por quê"),
 ("04","Colaborações","64% do alcance sem mídia paga"),
 ("05","Público","Quem foi alcançado, por geração"),
 ("06","Stories","A cobertura em tempo real"),
 ("07","Imprensa e TV","19 veículos e a transmissão nacional"),
 ("08","Repercussão","Trending, sentimento e leitura final")]
linhas="".join(f'<div class="sm"><span class="n">{n}</span>'
  f'<span class="t">{t}</span><span class="d">{d}</span></div>' for n,t,d in itens_sum)
slide(topo("Sumário","")+h1("O que este relatório mostra")+f'<div class="sumario">{linhas}</div>')

# 03 CONTEXTO
cards=[("15h00","Primeira atração do Palco Sunset, no feriado de 7 de setembro"),
 ("14h45","O Multishow entra ao vivo — ela abre a transmissão nacional do dia"),
 ("Chuva","A tarde começa com chuva e a pista ainda enchendo"),
 ("Esgotado","Dia com ingressos esgotados, em festival para 100 mil por dia")]
cd="".join(f'<div class="cx"><div class="cx-v">{a}</div><div class="cx-t">{b}</div></div>' for a,b in cards)
slide(topo("01 · O contexto",N(3))+h1("Um show de abertura, em condições difíceis")
 +f'<div class="cxg">{cd}</div>'
 +'<p class="frase">E ainda assim: <b>8º lugar entre os assuntos mais comentados do Brasil</b>, no mesmo dia em que Elton John encerrava o Palco Mundo.</p>'
 +nota("Grade e transmissão verificadas em fontes oficiais. Posição no trending informada pela equipe digital."))

# 04 HERO ALCANCE
slide(f'''{topo("02 · Alcance digital",N(4),True)}
<div class="hero">
  <div>
    <p class="eb ouro">Alcance total no Instagram</p>
    <div class="hero-n">1,07<span>milhão</span></div>
    <p class="hero-t">de visualizações geradas pelo conteúdo do show</p>
    <div class="hero-sp">
      <div><b>966.096</b><span>no feed · 7 publicações</span></div>
      <div><b>106.148</b><span>em stories · 8 cards medidos</span></div>
    </div>
  </div>
  <img class="hero-img" src="{FOTO['pb']}" alt="">
</div>
{nota("Visualizações contam exibições, não pessoas únicas. Fonte: Instagram Insights do perfil.")}''', dark=True)

# 05 KPIs
slide(topo("02 · Alcance digital",N(5))+h1("Os números do período")
 +stats([("966.096","Visualizações no feed","7 publicações sobre o show"),
         ("575.059","Visualizadores somados","Únicos por publicação"),
         ("81.398","Interações","Curtidas, comentários, reposts, compart. e salvos"),
         ("8,4%","Taxa de engajamento","Interações sobre visualizações do feed"),
         ("405","Novos seguidores","Atribuídos aos posts próprios"),
         ("106.148","Visualizações em stories","8 de 11 cards com dado medido")])
 +nota("A soma de visualizadores entre publicações não representa público único: a mesma pessoa pode ter visto mais de um conteúdo."))

# 06 RANKING
rank=[("Reel dos lírios","colab globoplay + Multishow",315753),
 ("Colab com Rubel","post cruzado no Facebook",181780),
 ("Eu te apoio em sua fé","reel do show",172622),
 ("Colab com Marie Claire","matéria de capa",122055),
 ("Te espero hoje às 15h","convocação, pré-show",81518),
 ("O Rock in Rio, para um brasileiro","reel do show",54466),
 ("Bastidores","reel de bastidor",37902)]
cores=[OURO,OURO,AZUL,OURO,AZUL,AZUL,AZUL]
slide(topo("03 · Conteúdos",N(6))+h1("O que mais performou","Visualizações por publicação, no período de 5 a 9 de setembro.")
 +'<div class="col2">'
 +f'<div>{barras_h([(a,b,c,cores[i]) for i,(a,b,c) in enumerate(rank)], larg=430, rot_larg=250)}</div>'
 +'<div class="lateral"><p class="lat-t">As três colaborações</p>'
 +'<div class="lat-n">64%</div>'
 +'<p class="lat-d">das visualizações do feed vieram de três posts em colaboração — globoplay + Multishow, Rubel e Marie Claire.</p>'
 +'<p class="lat-b">Nenhuma com mídia paga.</p></div></div>'
 +legenda([("Publicação em colaboração",OURO),("Publicação própria",AZUL)])
 +nota("Fonte: Instagram Insights, por publicação."))

# 07 COMPOSIÇÃO DO ALCANCE
slide(topo("04 · Colaborações",N(7))+h1("De onde veio o alcance","Composição das 966.096 visualizações do feed.")
 +barras_emp(["Origem do alcance"],
   [("Colaborações",OURO,[64.1]),("Publicações próprias",AZUL,[35.9])],
   larg=700, alt=44, passo=64, rot_larg=0)
 +legenda([("Colaborações · 619.588 visualizações",OURO),("Próprias · 346.508 visualizações",AZUL)])
 +'<div class="col3 mt">'
 +'<div class="bloco"><p class="bl-n">315.753</p><p class="bl-t">globoplay + Multishow</p>'
 +'<p class="bl-d">O reel de maior alcance do período. Transforma a transmissão de TV em conteúdo digital.</p></div>'
 +'<div class="bloco"><p class="bl-n">181.780</p><p class="bl-t">Rubel</p>'
 +'<p class="bl-d">Post cruzado no Facebook. Trouxe o público mais jovem do pacote: 72% entre 18 e 34 anos.</p></div>'
 +'<div class="bloco"><p class="bl-n">122.055</p><p class="bl-t">Marie Claire</p>'
 +'<p class="bl-d">Matéria de capa. Puxou a audiência mais madura entre as colaborações: 29,1% com 45+.</p></div>'
 +'</div>'
 +nota("Colaboração no Instagram divide a publicação entre os dois perfis, somando as duas audiências sem custo de mídia."))

# 08 TOP 1
slide(f'''{topo("03 · Conteúdos",N(8))}
<div class="col-foto">
  <img src="{FOTO['perfil']}" alt="">
  <div>
    {h1("315.753 visualizações em um único reel")}
    {stats([("215.194","visualizadores",None),("26,7 mil","curtidas",None),
            ("1,3 mil","compartilhamentos",None),("1,1 mil","reposts",None),
            ("921","comentários",None),("9 s","tempo médio de exibição",None)],cols=3)}
    <p class="destaque">Taxa de curtidas de <b>12%</b> — registrada pelo Instagram como “mais alto” para a conta. Publicado em colaboração com globoplay e Multishow, com post cruzado no Facebook.</p>
  </div>
</div>
{nota("315.753 visualizações: 303.021 no Instagram e 12.732 no Facebook.")}''')

# 09 MARIE CLAIRE
slide(topo("04 · Colaborações",N(9))+h1("Marie Claire: a capa que abriu outro público")
 +stats([("122.055","visualizações",None),("56.340","visualizadores",None),
         ("4,1 mil","curtidas",None),("64","salvamentos",None)],cols=4)
 +'<div class="col2 mt">'
 +'<div class="cita"><p class="cita-q">“Carrego um pouco de grandes mulheres no palco”</p>'
 +'<p class="cita-d">Matéria de capa da Marie Claire sobre o primeiro show dela no Rock in Rio, após mais de 20 anos de carreira — publicada como colaboração no perfil.</p></div>'
 +'<div class="painel-esc"><div class="pe-n">29,1%</div>'
 +'<p class="pe-t">do público com 45 anos ou mais</p>'
 +'<p class="pe-d">Três vezes a fatia 45+ do post em colaboração com Rubel, que ficou em 9,6%. Marca de imprensa entrega o público que o algoritmo sozinho não alcança.</p></div>'
 +'</div>'
 +nota("Fonte: Instagram Insights do post em colaboração com @marieclairebr."))

# 10 PÚBLICO POR GERAÇÃO
slide(topo("05 · Público",N(10))+h1("Cada conteúdo trouxe uma geração diferente","Distribuição etária dos visualizadores, por publicação.")
 +barras_grupo(["18-24","25-34","35-44","45-54","55+"],
   [("Colab com Rubel",AZUL,[29.2,43.0,15.7,6.2,3.4]),
    ("Reel dos lírios",OURO,[10.0,28.1,26.2,21.2,13.5]),
    ("Colab Marie Claire",CLAY,[12.8,30.1,26.5,19.1,10.0])], larg=700, alth=180)
 +legenda([("Colab com Rubel",AZUL),("Reel dos lírios",OURO),("Colab Marie Claire",CLAY)])
 +'<p class="frase mt">Rubel concentrou <b>72% do público entre 18 e 34 anos</b>; Marie Claire e o reel de maior alcance puxaram <b>45+</b>.</p>'
 +nota("Percentual de visualizadores por faixa etária. Fonte: Instagram Insights, aba Público."))

# 11 SEGUIDORES x NÃO SEGUIDORES
slide(topo("05 · Público",N(11))+h1("Metade do alcance veio de quem não segue","Composição da audiência de cada reel com dado disponível.")
 +barras_emp(["Eu te apoio em sua fé","O Rock in Rio, para um brasileiro","Te espero hoje às 15h","Bastidores"],
   [("Não seguidores",OURO,[57.4,43.8,42.5,41.0]),("Seguidores",AZUL,[42.6,56.2,57.5,59.0])],
   larg=520, rot_larg=250)
 +legenda([("Não seguidores",OURO),("Seguidores",AZUL)])
 +'<div class="col3 mt">'
 +'<div class="bloco"><p class="bl-n">57,4%</p><p class="bl-t">de não seguidores no melhor caso</p>'
 +'<p class="bl-d">“Eu te apoio em sua fé” — 172.622 visualizações e 274 novos seguidores.</p></div>'
 +'<div class="bloco"><p class="bl-n">405</p><p class="bl-t">novos seguidores no período</p>'
 +'<p class="bl-d">Atribuídos diretamente às publicações próprias. As colaborações não atribuem seguidor.</p></div>'
 +'<div class="bloco"><p class="bl-n">4 de 4</p><p class="bl-t">reels acima de 41% fora da base</p>'
 +'<p class="bl-d">Conteúdo que só circula entre seguidores documenta. Conteúdo que sai da base constrói audiência.</p></div>'
 +'</div>'
 +nota("Fonte: aba Público de cada reel no Instagram Insights."))

# 12 ENGAJAMENTO POR PUBLICAÇÃO
eng=[("Te espero hoje às 15h","81.518 visualizações",11.9),
 ("O Rock in Rio, para um brasileiro","54.466 visualizações",10.0),
 ("Reel dos lírios","315.753 visualizações",9.6),
 ("Eu te apoio em sua fé","172.622 visualizações",9.2),
 ("Bastidores","37.902 visualizações",8.0),
 ("Colab com Rubel","181.780 visualizações",6.8),
 ("Colab com Marie Claire","122.055 visualizações",3.7)]
slide(topo("03 · Conteúdos",N(12))+h1("Alcance grande não é o mesmo que engajamento alto","Taxa de engajamento por publicação: interações sobre visualizações.")
 +'<div class="col2">'
 +f'<div>{barras_h([(a,b,c) for a,b,c in eng], larg=330, rot_larg=280, fmt=lambda v: f"{v:.1f}%".replace(".",","))}</div>'
 +'<div class="lateral"><p class="lat-t">O topo da lista</p><div class="lat-n">16,1%</div>'
 +'<p class="lat-d">de taxa de curtidas no post de <b>convocação</b>, publicado horas antes do show — a maior da conta no período, marcada pelo Instagram como “mais alto”.</p>'
 +'<p class="lat-b">Convocar não é avisar: é marcar hora.</p></div></div>'
 +nota("Interações somam curtidas, comentários, reposts, compartilhamentos e salvamentos."))

# 13 STORIES
st=[("Palco em luz vermelha","9.138 espectadores",971),("Agradecimento","8.271 espectadores",946),
 ("Vista do público","8.958 espectadores",877),("Nos bastidores","9.770 espectadores",794),
 ("Look do dia","10.100 espectadores",783),("No palco com o convidado","8.823 espectadores",756)]
slide(topo("06 · Stories",N(13))+h1("O show narrado enquanto acontecia")
 +stats([("11","stories publicados",None),("106.148","visualizações",None),
         ("95.599","espectadores somados",None),("6.878","interações",None)],cols=4)
 +'<div class="col2 mt">'
 +f'<div>{barras_h([(a,b,c) for a,b,c in st], larg=210, rot_larg=250, passo=32, alt_barra=17)}</div>'
 +'<div class="lateral"><p class="lat-t">Interações por card</p>'
 +'<div class="lat-n">11,4%</div>'
 +'<p class="lat-d">no card mais forte: 946 interações sobre 8.271 espectadores. A audiência caiu menos de 20% do primeiro ao último card.</p>'
 +'<p class="lat-b">A sequência prendeu.</p></div></div>'
 +nota("Rótulos descritivos atribuídos a partir da capa de cada card. Fonte: Instagram Insights de stories."))

# 14 IMPRENSA — CENSO
slide(topo("07 · Imprensa e TV",N(14))+h1("A cobertura de imprensa","Censo de veículos verificado URL a URL, entre 5 e 9 de setembro.")
 +'<div class="col2">'
 +f'<div>{barras_h([("Porte nacional","g1, Terra, CNN, Exame, InfoMoney, Rolling Stone, Billboard",7,OURO),("Vertical de música e cultura","POPLine, Semana Pop, Quenty, TMDQA!",4,AZUL),("Regional e independente","Folha de Curitiba, NC News, Portal Democrata e outros",8,CLAY)], larg=280, rot_larg=250, passo=54, alt_barra=24, fmt=lambda v: str(v))}</div>'
 +'<div class="lateral"><p class="lat-t">Total mapeado</p><div class="lat-n">19</div>'
 +'<p class="lat-d">veículos publicando sobre a apresentação, dos quais <b>9 com matéria dedicada</b> — texto próprio, com repórter cobrindo o show.</p>'
 +'<p class="lat-b">2 republicações automáticas foram deduplicadas.</p></div></div>'
 +'<p class="frase mt">“Vanessa da Mata constrói show coeso no Rock in Rio entre clássicos e hits de seus 20 anos de carreira” — <b>g1</b></p>'
 +nota("O censo é um piso: cobertura em vídeo, rádio e veículos não indexados não aparece aqui."))

# 15 ALCANCE DOS VEÍCULOS
slide(topo("07 · Imprensa e TV",N(15))+h1("O alcance dos veículos que publicaram","Audiência mensal por domínio, entre os veículos com dado público.")
 +barras_h([("globo.com","g1 · matéria dedicada, com crítica favorável",621.92,OURO),
            ("cnnbrasil.com.br","CNN Brasil · matéria com declaração da artista",65.97,OURO),
            ("terra.com.br","Terra · matéria dedicada",52.17,OURO)],
    larg=500, rot_larg=250, passo=54, alt_barra=24,
    fmt=lambda v: f"{v:,.2f} mi".replace(",","·").replace(".",",").replace("·","."))
 +'<div class="col3 mt">'
 +'<div class="bloco"><p class="bl-n">740,06 mi</p><p class="bl-t">universo potencial mensal</p>'
 +'<p class="bl-d">Soma das visitas mensais dos três domínios. É o universo do veículo, não o alcance da matéria.</p></div>'
 +'<div class="bloco"><p class="bl-n">14 mi</p><p class="bl-t">seguidores do @g1 no X</p>'
 +'<p class="bl-d">O maior perfil que publicou sobre o show, com juízo de valor positivo no título.</p></div>'
 +'<div class="bloco"><p class="bl-n">16 de 19</p><p class="bl-t">veículos sem audiência pública</p>'
 +'<p class="bl-d">Fecham o número quando o clipping da assessoria trouxer a audiência de cada um.</p></div>'
 +'</div>'
 +nota("Visitas mensais por domínio via Semrush: globo.com em jun/2026, demais em dez/2025. Audiência potencial não é alcance da matéria."))

# 16 TV
slide(f'''{topo("07 · Imprensa e TV",N(16),True)}
{h1("O show abriu a transmissão nacional")}
<div class="tl">
  <div class="tl-i"><span class="tl-h">14h45</span><span class="tl-t">Multishow entra ao vivo</span><span class="tl-d">A transmissão nacional do dia começa quinze minutos antes do show.</span></div>
  <div class="tl-i on"><span class="tl-h">15h00</span><span class="tl-t">Vanessa abre o Palco Sunset</span><span class="tl-d">Primeira atração transmitida do dia, em sinal aberto no Globoplay para não assinantes.</span></div>
  <div class="tl-i"><span class="tl-h">16h20</span><span class="tl-t">Canal Bis entra na grade</span><span class="tl-d">Os sinais passam a se revezar a cada 30 minutos.</span></div>
  <div class="tl-i"><span class="tl-h">23h45</span><span class="tl-t">Elton John na TV aberta</span><span class="tl-d">Único show do dia na Globo — oito horas depois do Sunset abrir.</span></div>
</div>
<p class="frase-esc">A audiência aferida da faixa <b>não foi divulgada</b> por emissora ou instituto. Pela equivalência oficial de 2026 da Kantar IBOPE, cada ponto no Painel Nacional representa <b>699.962 pessoas</b> — o conversor fica pronto para quando o dado chegar.</p>
{nota("Grade de transmissão verificada em fontes oficiais do festival e da emissora.")}''', dark=True)

# 17 TRENDING + SENTIMENTO
slide(f'''{topo("08 · Repercussão",N(17),True)}
{h1("O país comentou — e comentou bem")}
<div class="rep">
  <div class="rep-c">
    <div class="rep-n">#8</div>
    <p class="rep-t">nos assuntos mais comentados do Brasil no X</p>
    <p class="rep-d">Conquistado a partir das 15h, no primeiro show do dia, contra oito atrações entre Mundo e Sunset.</p>
  </div>
  <div class="rep-c">
    {rosca(93,"93%","positivo",OUROD,True)}
    <p class="rep-t2">de sentimento positivo entre quem se posicionou</p>
    <p class="rep-d">14 manifestações elogiosas contra 1 crítica — e a crítica foi ao festival, não ao show.</p>
  </div>
  <img class="rep-img" src="{FOTO['duo']}" alt="">
</div>
{nota("Posição no trending informada pela equipe digital. Sentimento conforme apuração publicada pelo agregador Quenty em 8 de setembro; amostra de 15 manifestações.")}''', dark=True)

# 18 PLAYBOOK
pb=[("Marcar hora com o público","O post de convocação teve a maior taxa de curtidas da conta: 16,1%"),
 ("Transformar a TV em conteúdo","O colab com globoplay e Multishow virou o maior reel: 315.753 visualizações"),
 ("Somar marcas, não só perfis","As três colaborações responderam por 64% das visualizações do feed"),
 ("Buscar público fora da base","Quatro reels com mais de 41% de visualizadores não seguidores"),
 ("Narrar em tempo real","11 stories no ar durante o show, com queda de audiência abaixo de 20%"),
 ("Entregar o ângulo à imprensa","9 matérias dedicadas com o mesmo enquadramento de 20 anos de carreira")]
li="".join(f'<div class="pb"><span class="pb-n">{i+1:02d}</span>'
  f'<span class="pb-t">{a}</span><span class="pb-d">{b}</span></div>' for i,(a,b) in enumerate(pb))
slide(topo("08 · Repercussão",N(18))+h1("O que o time fez","Cada decisão, com o resultado que ela produziu.")
 +f'<div class="pbg">{li}</div>')

# 19 INSIGHTS
ins=[("O show abriu a transmissão nacional do dia.","O Multishow entrou no ar às 14h45 e Vanessa foi a primeira atração transmitida."),
 ("1,07 milhão de visualizações no Instagram.","966.096 no feed e 106.148 em stories, com 8,4% de engajamento."),
 ("64% do alcance veio de colaborações.","Três parcerias — globoplay + Multishow, Rubel e Marie Claire — sem mídia paga."),
 ("Metade do alcance chegou fora da base.","Quatro reels com mais de 41% de visualizadores não seguidores e 405 novos seguidores."),
 ("Cobertura unânime em tom positivo.","9 matérias dedicadas, nenhuma negativa, encabeçadas por crítica favorável do g1.")]
li="".join(f'<div class="in"><span class="in-n">{i+1:02d}</span>'
  f'<div><p class="in-t">{a}</p><p class="in-d">{b}</p></div></div>' for i,(a,b) in enumerate(ins))
slide(topo("08 · Repercussão",N(19))+h1("Cinco conclusões")+f'<div class="ing">{li}</div>')

# 20 METODOLOGIA
me=[("Dados de Instagram","Insights do perfil, capturados em 9 de setembro de 2026. Cobrem 7 publicações de feed e 11 stories."),
 ("Visualizações","Contam exibições, não pessoas únicas. Somas entre publicações podem incluir a mesma pessoa mais de uma vez."),
 ("Visualizadores","Únicos por publicação. A soma entre publicações não representa público único."),
 ("Imprensa","Censo de 19 veículos verificados URL a URL. Duas republicações automáticas foram deduplicadas."),
 ("Audiência de veículos","Visitas mensais por domínio via Semrush. Universo potencial do veículo, não alcance da matéria."),
 ("Sentimento","Apuração publicada por terceiro sobre 15 manifestações. Amostra pequena: indica direção, não volume."),
 ("Audiência de TV","Não divulgada por emissora ou instituto. Nenhum valor foi estimado a partir dela."),
 ("Não medido","Menções em redes sociais, que exigiriam ferramenta de escuta com acesso às APIs das plataformas.")]
li="".join(f'<div class="me"><p class="me-t">{a}</p><p class="me-d">{b}</p></div>' for a,b in me)
slide(topo("Metodologia e fontes",N(20))+h1("De onde vem cada número")
 +f'<div class="meg">{li}</div>'
 +'<p class="frase">Nenhum número deste relatório foi estimado. O que não é público está marcado como não disponível.</p>')

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
@page{size:13.333in 7.5in;margin:0}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;
  font-family:Inter,sans-serif;color:#16150F;font-size:14px;line-height:1.5}

.sl{width:1280px;height:720px;position:relative;overflow:hidden;
  background:#fff;padding:52px 72px 42px;page-break-after:always;display:flex;flex-direction:column}
.sl:last-child{page-break-after:auto}
.sl.dk{background:#111110;color:#F5F3EF}

/* topo */
.topo{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid #E7E4DE;padding-bottom:11px;margin-bottom:34px}
.dk .topo{border-color:#2C2A26}
.eb{font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.2em;
  text-transform:uppercase;color:#78736A}
.dk .eb{color:#9A948A}
.eb.ouro{color:#A8761F}.dk .eb.ouro{color:#D2A24C}
.pg{font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.14em;color:#B5AFA4}
.dk .pg{color:#5C574F}

h1{font-family:Newsreader,serif;font-weight:400;font-size:37px;line-height:1.08;
  letter-spacing:-.015em;max-width:20ch}
.dk h1{color:#F5F3EF}
.lead{font-size:14px;color:#78736A;margin-top:11px;max-width:66ch;font-weight:300}
.dk .lead{color:#9A948A}
.nota{font-size:10.5px;line-height:1.45;color:#A5A096;margin-top:auto;padding-top:10px;font-weight:300}
.dk .nota{color:#6B665E}

/* capa */
.capa-s{padding:0;flex-direction:row;background:#0B0A09}
.capa-img{width:545px;height:720px;object-fit:cover;object-position:center center;flex:none}
.capa-txt{flex:1;padding:0 72px;display:flex;flex-direction:column;justify-content:center;position:relative}
.tit-capa{font-family:Newsreader,serif;font-weight:400;font-size:70px;line-height:1.02;
  letter-spacing:-.025em;color:#fff;margin:24px 0 0;max-width:none}
.tit-capa em{font-style:italic;font-weight:300;color:#D2A24C}
.capa-sub{margin-top:38px;font-size:15px;color:#fff;font-weight:400;letter-spacing:.01em}
.capa-fio{margin-top:10px;font-size:13.5px;color:#B9B2A6;font-weight:300;max-width:40ch;line-height:1.55}
.capa-rod{position:absolute;left:72px;right:72px;bottom:46px;display:flex;justify-content:space-between;gap:30px;
  font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:#7E786E}

/* sumário */
.sumario{margin-top:30px;border-top:1px solid #E7E4DE}
.sm{display:grid;grid-template-columns:52px 250px 1fr;gap:20px;align-items:baseline;
  padding:15px 0;border-bottom:1px solid #E7E4DE}
.sm .n{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#A8761F;letter-spacing:.1em}
.sm .t{font-family:Newsreader,serif;font-size:19px;font-weight:400}
.sm .d{font-size:12.5px;color:#78736A;font-weight:300}

/* contexto */
.cxg{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:36px;border-top:1px solid #E7E4DE}
.cx{padding:24px 26px 0 0;border-right:1px solid #E7E4DE}
.cx:last-child{border-right:none}
.cx-v{font-family:Newsreader,serif;font-size:34px;font-weight:400;color:#A8761F;letter-spacing:-.02em}
.cx-t{font-size:12.5px;color:#3E3A33;margin-top:12px;line-height:1.5;font-weight:300;max-width:24ch}
.frase{font-family:Newsreader,serif;font-size:19.5px;line-height:1.4;font-weight:300;
  margin-top:30px;max-width:82ch}
.frase b{font-weight:500;color:#A8761F}
.frase.mt{margin-top:20px}
.frase-esc{font-family:Newsreader,serif;font-size:17px;line-height:1.5;font-weight:300;
  color:#C7C0B4;margin-top:32px;max-width:96ch}
.frase-esc b{color:#D2A24C;font-weight:400}

/* hero */
.hero{display:grid;grid-template-columns:1fr 340px;gap:60px;align-items:center;flex:1}
.hero-n{font-family:Newsreader,serif;font-size:132px;line-height:.92;font-weight:400;
  color:#D2A24C;letter-spacing:-.04em;margin-top:14px;display:flex;align-items:baseline;gap:18px}
.hero-n span{font-size:34px;letter-spacing:.02em;color:#F5F3EF;font-weight:300}
.hero-t{font-size:17px;color:#F5F3EF;margin-top:22px;font-weight:300;max-width:32ch;line-height:1.5}
.hero-sp{display:flex;gap:52px;margin-top:40px;border-top:1px solid #2C2A26;padding-top:22px}
.hero-sp b{font-family:'IBM Plex Mono',monospace;font-size:20px;color:#D2A24C;font-weight:500;display:block}
.hero-sp span{font-size:11.5px;color:#9A948A;font-weight:300;display:block;margin-top:5px}
.hero-img{width:340px;height:430px;object-fit:cover;object-position:center 22%}

/* stats */
.stg{display:grid;gap:0;margin-top:24px;border-top:1px solid #E7E4DE}
.stg .st{padding:17px 24px 17px 0;border-right:1px solid #E7E4DE;border-bottom:1px solid #E7E4DE}
.dk .stg,.dk .stg .st{border-color:#2C2A26}
.stg .st:nth-child(3n){border-right:none}
.st .v{font-family:Newsreader,serif;font-size:33px;font-weight:400;color:#A8761F;letter-spacing:-.02em;line-height:1}
.dk .st .v{color:#D2A24C}
.st .k{font-size:12.5px;font-weight:500;margin-top:11px;line-height:1.35}
.st .s{font-size:11px;color:#8C867C;margin-top:5px;font-weight:300;line-height:1.4}

/* colunas */
.col2{display:grid;grid-template-columns:1fr 300px;gap:52px;margin-top:20px;align-items:start}
.col3{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid #E7E4DE}
.dk .col3{border-color:#2C2A26}
.col3.mt{margin-top:20px}
.bloco{padding:15px 26px 0 0;border-right:1px solid #E7E4DE}
.bloco:last-child{border-right:none}
.bl-n{font-family:Newsreader,serif;font-size:29px;color:#A8761F;font-weight:400;letter-spacing:-.02em}
.bl-t{font-size:12.5px;font-weight:600;margin-top:9px}
.bl-d{font-size:11.5px;color:#78736A;margin-top:7px;line-height:1.5;font-weight:300;max-width:30ch}
.lateral{border-left:1px solid #E7E4DE;padding-left:30px}
.lat-t{font-size:12px;font-weight:600;letter-spacing:.01em}
.lat-n{font-family:Newsreader,serif;font-size:56px;color:#A8761F;font-weight:400;
  letter-spacing:-.03em;line-height:1;margin:12px 0 16px}
.lat-d{font-size:12.5px;color:#78736A;line-height:1.55;font-weight:300}
.lat-d b{color:#16150F;font-weight:600}
.lat-b{font-size:12.5px;color:#A8761F;font-weight:600;margin-top:14px}

/* foto + texto */
.col-foto{display:grid;grid-template-columns:300px 1fr;gap:52px;flex:1;align-items:start}
.col-foto>img{width:300px;height:400px;object-fit:cover;object-position:center 20%}
.destaque{font-size:13px;line-height:1.6;color:#3E3A33;margin-top:26px;
  border-top:1px solid #E7E4DE;padding-top:18px;font-weight:300;max-width:62ch}
.destaque b{color:#A8761F;font-weight:600}

/* citação e painel escuro */
.cita{border-left:2px solid #A8761F;padding-left:26px}
.cita-q{font-family:Newsreader,serif;font-size:26px;font-style:italic;font-weight:300;line-height:1.32}
.cita-d{font-size:12.5px;color:#78736A;margin-top:16px;line-height:1.55;font-weight:300;max-width:44ch}
.painel-esc{background:#111110;padding:28px 30px;color:#F5F3EF}
.pe-n{font-family:Newsreader,serif;font-size:52px;color:#D2A24C;font-weight:400;letter-spacing:-.03em;line-height:1}
.pe-t{font-size:13px;font-weight:600;margin-top:12px}
.pe-d{font-size:11.5px;color:#9A948A;margin-top:10px;line-height:1.55;font-weight:300}

/* gráficos */
.g{width:100%;height:auto;margin-top:16px;overflow:visible}
.leg{display:flex;flex-wrap:wrap;gap:9px 26px;margin-top:12px;font-size:11.5px;font-weight:300}
.leg span{display:flex;align-items:center;gap:8px}
.leg i{width:9px;height:9px;border-radius:1px;display:inline-block}

/* timeline */
.tl{margin-top:34px;border-left:1px solid #2C2A26;padding-left:0}
.tl-i{display:grid;grid-template-columns:90px 290px 1fr;gap:24px;align-items:baseline;
  padding:15px 0 15px 26px;border-bottom:1px solid #2C2A26;position:relative}
.tl-i::before{content:"";position:absolute;left:-4px;top:24px;width:7px;height:7px;
  border-radius:50%;background:#111110;border:1px solid #5C574F}
.tl-i.on::before{background:#D2A24C;border-color:#D2A24C}
.tl-h{font-family:'IBM Plex Mono',monospace;font-size:13px;color:#D2A24C;letter-spacing:.04em}
.tl-t{font-size:14px;font-weight:600;color:#F5F3EF}
.tl-d{font-size:12px;color:#9A948A;font-weight:300;line-height:1.5}

/* repercussão */
.rep{display:grid;grid-template-columns:1fr 1fr 300px;gap:52px;margin-top:34px;align-items:start;flex:1}
.rep-c{border-left:1px solid #2C2A26;padding-left:28px}
.rep-n{font-family:Newsreader,serif;font-size:110px;color:#D2A24C;font-weight:400;
  letter-spacing:-.04em;line-height:.9}
.rep-t{font-size:14px;color:#F5F3EF;margin-top:22px;font-weight:400;line-height:1.45;max-width:24ch}
.rep-t2{font-size:14px;color:#F5F3EF;margin-top:18px;font-weight:400;line-height:1.45;max-width:24ch}
.rep-d{font-size:11.5px;color:#9A948A;margin-top:12px;line-height:1.55;font-weight:300;max-width:30ch}
.rep-img{width:300px;height:360px;object-fit:cover;object-position:center 18%}

/* playbook */
.pbg{margin-top:26px;border-top:1px solid #E7E4DE}
.pb{display:grid;grid-template-columns:52px 320px 1fr;gap:22px;align-items:baseline;
  padding:15px 0;border-bottom:1px solid #E7E4DE}
.pb-n{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:#A8761F;letter-spacing:.1em}
.pb-t{font-size:14px;font-weight:600}
.pb-d{font-size:12.5px;color:#78736A;font-weight:300;line-height:1.5}

/* insights */
.ing{margin-top:30px;border-top:1px solid #E7E4DE}
.in{display:grid;grid-template-columns:60px 1fr;gap:22px;padding:20px 0;border-bottom:1px solid #E7E4DE}
.in-n{font-family:Newsreader,serif;font-size:30px;color:#A8761F;font-weight:400;line-height:1}
.in-t{font-family:Newsreader,serif;font-size:21px;font-weight:400;line-height:1.3}
.in-d{font-size:12.5px;color:#78736A;margin-top:7px;font-weight:300}

/* metodologia */
.meg{display:grid;grid-template-columns:1fr 1fr;gap:22px 60px;margin-top:30px}
.me-t{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:#A8761F;margin-bottom:6px}
.me-d{font-size:11.5px;color:#78736A;line-height:1.55;font-weight:300}
.mt{margin-top:30px}
"""

html = ("<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
        "<title>Vanessa da Mata — Rock in Rio 2026</title>"
        f"<style>{FONTES}\n{CSS}</style></head><body>"
        + "".join(S) + "</body></html>")
(B/"deck.build.html").write_text(html)

from playwright.sync_api import sync_playwright
exe = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]
pdf = B/"Vanessa-da-Mata-Rock-in-Rio-2026-Apresentacao.pdf"
erros=[]
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width":1280,"height":720})
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto((B/"deck.build.html").as_uri()); pg.wait_for_timeout(1200)
    pg.emulate_media(media="print")
    pg.pdf(path=str(pdf), width="13.333in", height="7.5in", print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"})
    b.close()
if erros: print("ERROS:", erros); sys.exit(1)
print(f"{pdf.name}: {pdf.stat().st_size/1024/1024:.2f} MB · {len(S)} slides")
