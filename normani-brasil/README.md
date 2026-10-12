# Normani × Brasil 2026

Proposta de conteúdo exclusivo para a Vogue Brasil com a Normani (Meli Music, 17/10/2026), em português. Segue a identidade do deck "Tinashe · Popstar × Brasil".

- `Normani-Brasil-2026.pdf`: o deck (10 páginas, 16:9). Os tweets e as referências da Vogue US são clicáveis.
- `build.py`: gera o HTML e o PDF. Rode `python3 build.py --png` para ter também as prévias em `preview/`.

Páginas: capa, índice, visão geral, história, linha do tempo, recibos, Vogue Brasil, dia do show, time local, obrigado.

Fotos do time local ficam em `img/pessoas/<slug>.jpg` (nome em minúsculas, sem acento, com hífen).

## Versão geral da viagem

- `Normani-Brasil-2026-Geral.pdf`: o plano completo dos 5 dias em São Paulo (21 páginas, em inglês), sem foco na Vogue.
- `build_geral.py`: gera essa versão. Rode `python3 build_geral.py --png` para as prévias em `preview-geral/`.

## Influenciadores convidados

- `Normani-Influenciadores-Convidados.pdf`: página única em inglês com os convidados, foto clicável para o Instagram e seguidores.
- `build_convidados.py`: gera a página. Os @ e os seguidores ficam na lista `CONVIDADOS` no topo do arquivo.

## Perucas do front row

- `Normani-Perucas-Front-Row.pdf`: página única em inglês com as duas opções de peruca e o total para 50 unidades.
- `build_perucas.py`: gera a página. Quantidade e preços ficam em `QTD` e `OPCOES` no topo do arquivo.

## Crachás AAA

- `Normani-Crachas-AAA.pdf`: página única com três propostas de crachá (NORMANI · Brazil 2026 · AAA).
- `build_crachas.py`: gera a página. A logo "Normani" foi refeita com a fonte Mr Dafoe (`fontes/MrDafoe.woff2`, licença OFL) e brilho/estrelas em CSS.
