const pptx = require('pptxgenjs');
const fs = require('fs');
const p = new pptx();
p.layout = 'LAYOUT_WIDE';               // 13.3 x 7.5
p.author = 'Equipe digital'; p.title = 'Vanessa da Mata — Rock in Rio 2026';

const INK='14110F', GOLD='A8761F', GOLDL='D4A843', BLUE='2472A3', TERRA='9E3D2A',
      W='FFFFFF', GREY='6B6459', PANEL='F4F3F0', LINE='DCD8D0';
const H='Cambria', B='Calibri';
const img = f => 'img/'+f;

const T=(s,t,o)=>s.addText(t,Object.assign({isTextBox:true,margin:0},o));

/* ---------- helpers ---------- */
function darkBg(s){ s.background={color:INK}; }
function eyebrow(s,txt,x,y,col){ T(s,txt,{x,y,w:11,h:.25,fontFace:B,fontSize:10,color:col||GOLD,charSpacing:2.4,bold:true}); }
function title(s,txt,col){ T(s,txt,{x:.75,y:.62,w:11.8,h:1.0,fontFace:H,fontSize:34,bold:true,color:col||INK}); }
function kicker(s,n,txt,col){
  T(s,n,{x:.75,y:.42,w:.6,h:.3,fontFace:B,fontSize:10,color:GOLD,bold:true,charSpacing:2});
  T(s,txt,{x:1.25,y:.42,w:10,h:.3,fontFace:B,fontSize:10,color:col||GREY,charSpacing:2});
}
function stat(s,x,y,w,val,lab,sub,col,vs){
  T(s,val,{x,y,w,h:.75,fontFace:H,fontSize:vs||40,bold:true,color:col||GOLD});
  T(s,lab,{x,y:y+.78,w,h:.5,fontFace:B,fontSize:12,color:INK,bold:true});
  if(sub) T(s,sub,{x,y:y+1.22,w,h:.4,fontFace:B,fontSize:9.5,color:GREY});
}
function note(s,txt,y){
  T(s,txt,{x:.75,y:y||6.75,w:11.8,h:.45,fontFace:B,fontSize:9,color:GREY,italic:true});
}

/* ============ 1. CAPA ============ */
let s=p.addSlide(); darkBg(s);
s.addImage({path:img('publico.jpg'),x:6.75,y:0,w:6.55,h:7.5,sizing:{type:'cover',w:6.55,h:7.5}});
T(s,'RELATÓRIO DE PERFORMANCE DIGITAL',{x:.8,y:.9,w:5.6,h:.3,fontFace:B,fontSize:10.5,color:GOLDL,bold:true,charSpacing:2.6});
T(s,'Vanessa',{x:.8,y:1.55,w:5.9,h:1.1,fontFace:H,fontSize:54,bold:true,color:W});
T(s,'da Mata',{x:.8,y:2.5,w:5.9,h:1.1,fontFace:H,fontSize:54,bold:true,color:W});
T(s,'no Rock in Rio',{x:.8,y:3.5,w:5.9,h:.85,fontFace:H,fontSize:36,italic:true,color:GOLDL});
T(s,'Palco Sunset · 7 de setembro de 2026 · 15h00',{x:.8,y:4.65,w:5.6,h:.35,fontFace:B,fontSize:14,color:W});
T(s,'Primeira atração do dia. Primeira no ar na transmissão nacional.',
  {x:.8,y:5.1,w:5.5,h:.8,fontFace:B,fontSize:13,color:'C9C2B8',lineSpacing:20});
T(s,'Apuração: 5 a 9 de setembro de 2026',{x:.8,y:6.6,w:5.6,h:.3,fontFace:B,fontSize:9.5,color:GREY,charSpacing:1.4});
s.addNotes('Abertura. O show foi a primeira atração do dia no Sunset e a primeira transmitida ao vivo — o Multishow entrou no ar às 14h45.');

/* ============ 2. O SHOW EM 4 FATOS ============ */
s=p.addSlide(); kicker(s,'01','O QUE ACONTECEU'); title(s,'Um show de abertura, em condições difíceis');
const fatos=[['15h00','Primeira atração do Palco Sunset, no feriado de 7 de setembro'],
 ['14h45','O Multishow entra ao vivo — ela abre a transmissão nacional do dia'],
 ['Chuva','A tarde começa com chuva e a pista ainda enchendo'],
 ['Esgotado','Dia com ingressos esgotados, em festival com capacidade para 100 mil']];
fatos.forEach((f,i)=>{
  const x=.75+i*3.05;
  s.addShape(p.ShapeType.roundRect,{x,y:2.05,w:2.8,h:2.5,fill:{color:PANEL},rectRadius:.06,line:{color:LINE,width:.5}});
  T(s,f[0],{x:x+.28,y:2.35,w:2.3,h:.6,fontFace:H,fontSize:24,bold:true,color:GOLD});
  T(s,f[1],{x:x+.28,y:3.0,w:2.3,h:1.3,fontFace:B,fontSize:11.5,color:INK,lineSpacing:16});
});
T(s,'E ainda assim: 8º lugar entre os assuntos mais comentados do Brasil no X, no mesmo dia em que Elton John encerrava o Palco Mundo.',
  {x:.75,y:5.05,w:11.8,h:.8,fontFace:H,fontSize:17,italic:true,color:INK,lineSpacing:26});
note(s,'Grade e transmissão verificadas em fontes oficiais. Posição no trending informada pela equipe digital.');

/* ============ 3. KPIs ============ */
s=p.addSlide(); kicker(s,'02','O RESULTADO DIGITAL'); title(s,'Os números do perfil da Vanessa');
const kp=[['1,07 mi','Visualizações','Feed + stories, no período'],
 ['966 mil','Visualizações no feed','7 publicações sobre o show'],
 ['81,4 mil','Interações','Curtidas, comentários, reposts, compart. e salvos'],
 ['8,4%','Taxa de engajamento','Interações sobre visualizações do feed'],
 ['405','Novos seguidores','Atribuídos diretamente aos posts próprios'],
 ['106 mil','Visualizações em stories','8 stories medidos, de 11 publicados']];
kp.forEach((k,i)=>{
  const x=.75+(i%3)*4.0, y=1.95+Math.floor(i/3)*2.35;
  stat(s,x,y,3.6,k[0],k[1],k[2],GOLD,36);
});
note(s,'Fonte: Instagram Insights do perfil, capturado em 9 de setembro. Visualizações contam exibições, não pessoas únicas.');

/* ============ 4. HERO 1 MILHÃO ============ */
s=p.addSlide(); darkBg(s);
eyebrow(s,'ALCANCE TOTAL NO INSTAGRAM',.9,1.5,GOLDL);
T(s,'1,07',{x:.85,y:1.9,w:5,h:2.2,fontFace:H,fontSize:110,bold:true,color:GOLDL});
T(s,'MILHÃO',{x:4.6,y:3.0,w:3,h:.9,fontFace:H,fontSize:36,bold:true,color:W});
T(s,'de visualizações geradas pelo conteúdo do show',
  {x:.9,y:4.3,w:6.2,h:.9,fontFace:B,fontSize:17,color:W,lineSpacing:26});
T(s,'966 mil no feed  +  106 mil em stories',{x:.9,y:5.25,w:6.2,h:.4,fontFace:B,fontSize:13,color:GOLDL,bold:true});
s.addImage({path:img('pb.jpg'),x:8.1,y:1.3,w:4.3,h:4.9,sizing:{type:'cover',w:4.3,h:4.9}});
note(s,'Soma das visualizações de 7 publicações de feed e 8 stories medidos. Visualizações contam exibições, não pessoas únicas.',6.65);

/* ============ 5. RANKING ============ */
s=p.addSlide(); kicker(s,'03','CONTEÚDOS'); title(s,'O que mais performou');
s.addChart(p.ChartType.bar,[{name:'Visualizações',
  labels:['Bastidores','O Rock in Rio, para um brasileiro','Te espero hoje às 15h','Colab Marie Claire','Eu te apoio em sua fé','Colab com Rubel','Reel dos lírios — globoplay + Multishow'],
  values:[37902,54466,81518,122055,172622,181780,315753]}],
  {x:.7,y:1.85,w:8.0,h:4.6,barDir:'bar',chartColors:[GOLD],showLegend:false,
   showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'#,##0',dataLabelFontSize:10,dataLabelColor:GREY,dataLabelFontFace:B,
   catAxisLabelColor:INK,catAxisLabelFontSize:10.5,catAxisLabelFontFace:B,
   valAxisLabelColor:GREY,valAxisLabelFontSize:9,valAxisHidden:true,
   valGridLine:{style:'none'},catGridLine:{style:'none'},barGapWidthPct:45});
T(s,'As três colaborações',{x:9.0,y:2.1,w:3.6,h:.4,fontFace:B,fontSize:13,bold:true,color:INK});
T(s,'64%',{x:9.0,y:2.55,w:3.6,h:1.1,fontFace:H,fontSize:56,bold:true,color:GOLD});
T(s,'das visualizações do feed vieram de 3 posts em colaboração — globoplay + Multishow, Rubel e Marie Claire.',
  {x:9.0,y:3.75,w:3.6,h:1.5,fontFace:B,fontSize:12,color:INK,lineSpacing:17});
T(s,'Nenhuma com mídia paga.',{x:9.0,y:5.2,w:3.6,h:.4,fontFace:B,fontSize:12,bold:true,color:GOLD});
note(s,'Fonte: Instagram Insights, por publicação.');

/* ============ 6. TOP 1 ============ */
s=p.addSlide(); kicker(s,'04','O CONTEÚDO Nº 1'); title(s,'315.753 visualizações em um único reel');
s.addImage({path:img('perfil.jpg'),x:.75,y:1.9,w:3.5,h:4.5,sizing:{type:'cover',w:3.5,h:4.5}});
const t1=[['215.194','visualizadores'],['26,7 mil','curtidas'],['1,3 mil','compartilhamentos'],['1,1 mil','reposts'],['921','comentários'],['9 s','tempo médio']];
t1.forEach((t,i)=>{
  const x=4.65+(i%3)*2.7, y=2.0+Math.floor(i/3)*1.35;
  T(s,t[0],{x,y,w:2.5,h:.55,fontFace:H,fontSize:24,bold:true,color:GOLD});
  T(s,t[1],{x,y:y+.55,w:2.5,h:.35,fontFace:B,fontSize:11,color:GREY});
});
s.addShape(p.ShapeType.roundRect,{x:4.65,y:4.9,w:7.9,h:1.5,fill:{color:PANEL},rectRadius:.06,line:{color:LINE,width:.5}});
T(s,'Publicado em colaboração com globoplay e Multishow, com post cruzado no Facebook. Taxa de curtidas de 12% — a mais alta da conta na faixa. É o conteúdo que transformou a transmissão de TV em alcance digital.',
  {x:4.95,y:5.1,w:7.3,h:1.1,fontFace:B,fontSize:12,color:INK,lineSpacing:17});
note(s,'315.753 visualizações: 303.021 no Instagram e 12.732 no Facebook.');

/* ============ 7. MARIE CLAIRE ============ */
s=p.addSlide(); kicker(s,'05','COLABORAÇÃO EDITORIAL'); title(s,'Marie Claire: a capa que abriu outro público');
const mc=[['122.055','visualizações'],['56.340','visualizadores'],['4,1 mil','curtidas'],['64','salvamentos']];
mc.forEach((m,i)=>{ stat(s,.75+i*3.05,2.0,2.8,m[0],m[1],null,GOLD,30); });
s.addShape(p.ShapeType.roundRect,{x:.75,y:3.75,w:5.75,h:2.6,fill:{color:PANEL},rectRadius:.06,line:{color:LINE,width:.5}});
T(s,'“Carrego um pouco de grandes mulheres no palco”',{x:1.05,y:4.0,w:5.15,h:.8,fontFace:H,fontSize:18,italic:true,color:INK,lineSpacing:24});
T(s,'Matéria de capa da Marie Claire sobre o primeiro show dela no Rock in Rio, após mais de 20 anos de carreira — publicada como colaboração no perfil.',
  {x:1.05,y:4.85,w:5.15,h:1.3,fontFace:B,fontSize:12,color:GREY,lineSpacing:17});
s.addShape(p.ShapeType.roundRect,{x:6.8,y:3.75,w:5.75,h:2.6,fill:{color:INK},rectRadius:.06});
T(s,'29,1%',{x:7.1,y:3.95,w:5.15,h:.9,fontFace:H,fontSize:40,bold:true,color:GOLDL});
T(s,'do público com 45 anos ou mais',{x:7.1,y:4.85,w:5.15,h:.4,fontFace:B,fontSize:13,bold:true,color:W});
T(s,'Três vezes a fatia 45+ do post em colaboração com Rubel, que ficou em 9,6%. Marca de imprensa entrega o público que o algoritmo sozinho não alcança.',
  {x:7.1,y:5.3,w:5.15,h:1.0,fontFace:B,fontSize:11.5,color:'C9C2B8',lineSpacing:16});
note(s,'Fonte: Instagram Insights do post em colaboração com @marieclairebr.');

/* ============ 8. PÚBLICOS COMPLEMENTARES ============ */
s=p.addSlide(); kicker(s,'06','PÚBLICO'); title(s,'Cada conteúdo trouxe uma geração diferente');
s.addChart(p.ChartType.bar,[
 {name:'Marie Claire',labels:['18-24','25-34','35-44','45-54','55+'],values:[12.8,30.1,26.5,19.1,10.0]},
 {name:'Reel dos lírios',labels:['18-24','25-34','35-44','45-54','55+'],values:[10.0,28.1,26.2,21.2,13.5]},
 {name:'Colab com Rubel',labels:['18-24','25-34','35-44','45-54','55+'],values:[29.2,43.0,15.7,6.2,3.4]}],
 {x:.7,y:1.9,w:8.1,h:4.4,barDir:'col',chartColors:[TERRA,GOLD,BLUE],showLegend:true,legendPos:'b',
  legendFontFace:B,legendFontSize:11,legendColor:INK,
  showValue:false,catAxisLabelColor:INK,catAxisLabelFontSize:11,catAxisLabelFontFace:B,
  valAxisLabelColor:GREY,valAxisLabelFontSize:9,valAxisLabelFormatCode:'0"%"',
  valGridLine:{color:LINE,size:.5},catGridLine:{style:'none'},barGapWidthPct:55});
T(s,'A leitura',{x:9.1,y:2.0,w:3.5,h:.4,fontFace:B,fontSize:13,bold:true,color:INK});
T(s,'O colab com Rubel concentrou 72% do público entre 18 e 34 anos. A Marie Claire puxou 45+. O reel de maior alcance ficou no meio, equilibrado.',
  {x:9.1,y:2.5,w:3.5,h:1.6,fontFace:B,fontSize:12,color:INK,lineSpacing:17});
T(s,'Um pacote de conteúdo só cobre três gerações se for desenhado para isso.',
  {x:9.1,y:4.2,w:3.5,h:1.5,fontFace:H,fontSize:14,italic:true,color:GOLD,lineSpacing:21});
note(s,'Distribuição etária dos visualizadores, por publicação. Fonte: Instagram Insights.');

/* ============ 9. FORA DA BOLHA ============ */
s=p.addSlide(); darkBg(s);
kicker(s,'07','ALCANCE ORGÂNICO','C9C2B8');
T(s,'Metade do alcance veio de quem não segue',{x:.75,y:.62,w:11.8,h:1.0,fontFace:H,fontSize:34,bold:true,color:W});
const bol=[['57,4%','Eu te apoio em sua fé','172.622 visualizações · 274 novos seguidores'],
 ['43,8%','O Rock in Rio, para um brasileiro','54.466 visualizações · 54 novos seguidores'],
 ['42,5%','Te espero hoje às 15h','81.518 visualizações · 64 novos seguidores']];
bol.forEach((b,i)=>{
  const x=.75+i*4.0;
  T(s,b[0],{x,y:2.2,w:3.6,h:1.0,fontFace:H,fontSize:48,bold:true,color:GOLDL});
  T(s,'de não seguidores',{x,y:3.2,w:3.6,h:.35,fontFace:B,fontSize:11.5,color:W,bold:true});
  T(s,b[1],{x,y:3.7,w:3.6,h:.6,fontFace:B,fontSize:13,color:W,lineSpacing:17});
  T(s,b[2],{x,y:4.35,w:3.6,h:.6,fontFace:B,fontSize:10.5,color:'C9C2B8',lineSpacing:15});
});
T(s,'Conteúdo que só circula entre seguidores documenta o show. Conteúdo que sai da base constrói audiência nova — e foi o que aconteceu.',
  {x:.75,y:5.5,w:11.8,h:.9,fontFace:H,fontSize:16,italic:true,color:GOLDL,lineSpacing:24});
note(s,'Fonte: aba Público de cada reel no Instagram Insights.',6.7);

/* ============ 10. POST DE CONVOCAÇÃO ============ */
s=p.addSlide(); kicker(s,'08','TIMING'); title(s,'O post de convocação foi o mais curtido de todos');
T(s,'16,1%',{x:.75,y:2.0,w:4.0,h:1.5,fontFace:H,fontSize:76,bold:true,color:GOLD});
T(s,'de taxa de curtidas',{x:.75,y:3.45,w:4.0,h:.4,fontFace:B,fontSize:14,bold:true,color:INK});
T(s,'A maior da conta na faixa analisada — registrada pelo próprio Instagram como “mais alto”.',
  {x:.75,y:3.95,w:4.0,h:1.0,fontFace:B,fontSize:12,color:GREY,lineSpacing:17});
s.addShape(p.ShapeType.roundRect,{x:5.3,y:1.95,w:7.25,h:3.2,fill:{color:PANEL},rectRadius:.06,line:{color:LINE,width:.5}});
T(s,'“Te espero hoje às 15h no Palco Sunset”',{x:5.65,y:2.2,w:6.6,h:.55,fontFace:H,fontSize:20,bold:true,color:INK});
T(s,'Publicado horas antes do show, marcando o compromisso com o público. Resultado: 81.518 visualizações, 50.341 visualizadores, 42,5% deles fora da base de seguidores, e 64 novos seguidores.',
  {x:5.65,y:2.85,w:6.6,h:1.3,fontFace:B,fontSize:12.5,color:INK,lineSpacing:18});
T(s,'Convocar não é só avisar: é criar hora marcada. O público apareceu — e curtiu mais do que em qualquer outro conteúdo do período.',
  {x:5.65,y:4.15,w:6.6,h:.9,fontFace:B,fontSize:12,italic:true,color:GOLD,lineSpacing:17});
T(s,'405 novos seguidores atribuídos diretamente às publicações próprias do período.',
  {x:.75,y:5.6,w:11.8,h:.5,fontFace:H,fontSize:16,italic:true,color:INK});
note(s,'Taxas de curtidas conforme o painel “O que afeta suas visualizações” do Instagram.');

/* ============ 11. STORIES ============ */
s=p.addSlide(); kicker(s,'09','COBERTURA EM TEMPO REAL'); title(s,'Stories: o show narrado enquanto acontecia');
const st=[['11','stories publicados'],['106 mil','visualizações'],['95,6 mil','espectadores somados'],['6.878','interações']];
st.forEach((t,i)=>{ stat(s,.75+i*3.05,1.95,2.8,t[0],t[1],null,GOLD,32); });
s.addChart(p.ChartType.bar,[{name:'Espectadores',
  labels:['Look do dia','Bastidores em P&B','Nos bastidores','Palco em luz vermelha','Vista do público','No palco com o convidado','Céu da Cidade do Rock'],
  values:[10100,9794,9770,9138,8958,8823,8320]}],
  {x:.7,y:3.6,w:7.6,h:2.9,barDir:'bar',chartColors:[GOLD],showLegend:false,
   showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'#,##0',dataLabelFontSize:9,dataLabelColor:GREY,dataLabelFontFace:B,
   catAxisLabelColor:INK,catAxisLabelFontSize:9.5,catAxisLabelFontFace:B,
   valAxisHidden:true,valGridLine:{style:'none'},catGridLine:{style:'none'},barGapWidthPct:40});
T(s,'A retenção não caiu',{x:8.7,y:3.75,w:3.85,h:.4,fontFace:B,fontSize:13,bold:true,color:INK});
T(s,'Do primeiro ao último story do dia, a audiência variou pouco — sinal de que a sequência prendeu, em vez de cansar. A taxa de resposta chegou a 946 interações em um único card.',
  {x:8.7,y:4.25,w:3.85,h:1.8,fontFace:B,fontSize:11.5,color:INK,lineSpacing:17});
note(s,'Rótulos descritivos atribuídos a partir da capa de cada card. Fonte: Instagram Insights de stories.');

/* ============ 12. IMPRENSA E TV ============ */
s=p.addSlide(); kicker(s,'10','IMPRENSA E TV'); title(s,'O digital não trabalhou sozinho');
const im=[['19','veículos publicaram sobre a apresentação','Censo verificado, URL a URL'],
 ['9','matérias dedicadas, com repórter','g1, Terra e CNN Brasil entre elas'],
 ['14 mi','seguidores do maior perfil que publicou','@g1 no X, com crítica favorável'],
 ['3','sinais de TV e streaming ao vivo','Multishow, Canal Bis e Globoplay aberto']];
im.forEach((k,i)=>{ const x=.75+(i%2)*6.05, y=1.95+Math.floor(i/2)*2.3;
  T(s,k[0],{x,y,w:1.7,h:.8,fontFace:H,fontSize:40,bold:true,color:GOLD});
  T(s,k[1],{x:x+1.8,y:y+.05,w:4.1,h:.7,fontFace:B,fontSize:13,bold:true,color:INK,lineSpacing:17});
  T(s,k[2],{x:x+1.8,y:y+.8,w:4.1,h:.5,fontFace:B,fontSize:11,color:GREY});
});
s.addShape(p.ShapeType.roundRect,{x:.75,y:6.4,w:11.8,h:.75,fill:{color:PANEL},rectRadius:.05,line:{color:LINE,width:.5}});
T(s,'“Vanessa da Mata constrói show coeso no Rock in Rio entre clássicos e hits de seus 20 anos de carreira”   —   g1',
  {x:1.05,y:6.55,w:11.2,h:.45,fontFace:H,fontSize:13.5,italic:true,color:INK});

/* ============ 13. TRENDING E SENTIMENTO ============ */
s=p.addSlide(); darkBg(s);
kicker(s,'11','REPERCUSSÃO','C9C2B8');
T(s,'O país comentou — e comentou bem',{x:.75,y:.62,w:11.8,h:1.0,fontFace:H,fontSize:34,bold:true,color:W});
T(s,'#8',{x:.9,y:2.1,w:3.2,h:1.6,fontFace:H,fontSize:88,bold:true,color:GOLDL});
T(s,'nos assuntos mais comentados do Brasil no X',{x:.9,y:3.75,w:3.6,h:.9,fontFace:B,fontSize:13.5,color:W,lineSpacing:19});
T(s,'Conquistado a partir das 15h, no primeiro show do dia.',{x:.9,y:4.7,w:3.6,h:.7,fontFace:B,fontSize:11,color:'C9C2B8',lineSpacing:15});
s.addShape(p.ShapeType.line,{x:5.1,y:2.2,w:0,h:3.2,line:{color:'3A352E',width:1}});
T(s,'93%',{x:5.9,y:2.1,w:3.2,h:1.6,fontFace:H,fontSize:88,bold:true,color:GOLDL});
T(s,'de sentimento positivo entre quem se posicionou',{x:5.9,y:3.75,w:3.6,h:.9,fontFace:B,fontSize:13.5,color:W,lineSpacing:19});
T(s,'14 manifestações elogiosas contra 1 crítica — e a crítica foi ao festival, não ao show.',
  {x:5.9,y:4.7,w:3.7,h:.9,fontFace:B,fontSize:11,color:'C9C2B8',lineSpacing:15});
s.addImage({path:img('duo.jpg'),x:10.0,y:1.9,w:2.55,h:3.9,sizing:{type:'cover',w:2.55,h:3.9}});
note(s,'Posição no trending informada pela equipe digital. Sentimento conforme apuração publicada pelo agregador Quenty em 8 de setembro.',6.6);

/* ============ 14. PLAYBOOK ============ */
s=p.addSlide(); kicker(s,'12','O QUE O TIME FEZ'); title(s,'Cinco decisões, cinco resultados');
const pb=[['Marcar hora com o público','O post de convocação teve a maior taxa de curtidas da conta: 16,1%'],
 ['Transformar a TV em conteúdo','O colab com globoplay e Multishow virou o maior reel: 315.753 visualizações'],
 ['Somar marcas, não só perfis','As 3 colaborações responderam por 64% das visualizações do feed'],
 ['Buscar público fora da base','Três posts com mais de 42% de visualizadores não seguidores'],
 ['Narrar em tempo real','11 stories no ar durante o show, com retenção estável do primeiro ao último']];
pb.forEach((t,i)=>{
  const y=1.9+i*.98;
  T(s,String(i+1).padStart(2,'0'),{x:.75,y,w:.6,h:.5,fontFace:H,fontSize:20,bold:true,color:GOLD});
  T(s,t[0],{x:1.5,y,w:4.0,h:.5,fontFace:B,fontSize:14,bold:true,color:INK});
  T(s,t[1],{x:5.7,y:y+.03,w:6.85,h:.7,fontFace:B,fontSize:12.5,color:GREY,lineSpacing:17});
  if(i<4) s.addShape(p.ShapeType.line,{x:.75,y:y+.82,w:11.8,h:0,line:{color:LINE,width:.5}});
});
note(s,'Todos os indicadores desta página vêm do Instagram Insights do perfil.');

/* ============ 15. METODOLOGIA ============ */
s=p.addSlide(); kicker(s,'13','METODOLOGIA'); title(s,'De onde vem cada número');
const me=[['Dados de Instagram','Insights do perfil da Vanessa da Mata, capturados em 9 de setembro de 2026. Cobrem 7 publicações de feed e 11 stories do período.'],
 ['Visualizações','Contam exibições, não pessoas únicas. Somas entre publicações podem incluir a mesma pessoa mais de uma vez.'],
 ['Visualizadores','Únicos por publicação. A soma entre publicações não é um público único.'],
 ['Imprensa','Censo de 19 veículos verificados URL a URL, entre 5 e 9 de setembro. Duas republicações automáticas foram deduplicadas.'],
 ['Sentimento','Apuração publicada por terceiro sobre 15 manifestações. Amostra pequena: indica direção, não volume.'],
 ['Não medido','Audiência aferida da transmissão de TV, não divulgada por emissora ou instituto. Nenhum valor foi estimado.']];
me.forEach((m,i)=>{
  const x=.75+(i%2)*6.05, y=1.95+Math.floor(i/2)*1.6;
  T(s,m[0],{x,y,w:5.6,h:.35,fontFace:B,fontSize:12,bold:true,color:GOLD});
  T(s,m[1],{x,y:y+.38,w:5.6,h:1.0,fontFace:B,fontSize:11,color:GREY,lineSpacing:15});
});
T(s,'Nenhum número deste relatório foi estimado. O que não é público está marcado como não disponível.',
  {x:.75,y:6.7,w:11.8,h:.4,fontFace:H,fontSize:13,italic:true,color:INK});

p.writeFile({fileName:'Vanessa-da-Mata-Rock-in-Rio-2026-Apresentacao.pptx'})
 .then(f=>console.log('OK:',f));
