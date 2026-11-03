#!/usr/bin/env python3
"""
Desenha o diagrama "um código, três plataformas" do perfil: um card de vidro
em cima e três aparelhos embaixo (iPhone, MacBook com a web e Android),
ligados por traçados de circuito. Gera assets/plataformas.svg.

A tampa do MacBook abre como num notebook de verdade: a mesma curva e o mesmo
tempo de uma rotação 3D, feitos em 2D (SVG como imagem não tem 3D).

    python3 scripts/plataformas.py

Só usa a biblioteca padrão do Python.
"""
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from tema import MONO, SANS, esc  # noqa: E402

RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
SAIDA = os.environ.get("PLATAFORMAS_SAIDA", os.path.join(RAIZ, "assets", "plataformas.svg"))

TITULO = "Um código, três plataformas"
SUBTITULO = "React Native · Expo · React · Node.js"
APARELHOS = [  # (rótulo embaixo do aparelho)
    "iOS · App Store",
    "Web",
    "Android · Google Play",
]

SUBIR = 50          # o card e os aparelhos sobem para ocupar o lugar do antigo ícone do topo
W, H = 960, 624 - SUBIR
CX = W / 2
EASE_TAMPA = "cubic-bezier(.76,0,.24,1)"
EASE_QUIQUE = "cubic-bezier(.34,1.56,.64,1)"


def plataformas():
    with open(os.path.join(AQUI, "icones.json"), encoding="utf-8") as f:
        return json.load(f)["icones"]


def caminho(pontos):
    """Polilinha com o comprimento total, para desenhar e animar o traço."""
    d = "M" + " L".join(f"{x},{y}" for x, y in pontos)
    comp = sum(math.dist(a, b) for a, b in zip(pontos, pontos[1:]))
    return d, comp


# Regras de CSS geradas junto com o desenho (cada traço tem o seu comprimento). Tudo é
# animação CSS, para "reduzir movimento" parar tudo: os traços ficam prontos e os pulsos somem.
REGRAS = []


def desenha_linha(d, comp, inicio, dur, n, cor="#AFC0FF", op=0.32):
    """Traço que se desenha uma vez e depois um pulso de luz que percorre em loop."""
    pulso = inicio + dur + 0.4 + n * 0.5
    REGRAS.append(f"@keyframes tracar{n}{{from{{stroke-dashoffset:{comp:.1f}}}to{{stroke-dashoffset:0}}}}"
                  f".tracar{n}{{animation:tracar{n} {dur:.2f}s ease-out {inicio:.2f}s both}}"
                  f"@keyframes pulso{n}{{from{{stroke-dashoffset:26;opacity:1}}"
                  f"to{{stroke-dashoffset:{-comp:.1f};opacity:1}}}}"
                  f".pulso{n}{{animation:pulso{n} 2.6s linear {pulso:.2f}s infinite}}")
    return (f'<path class="traco tracar{n}" d="{d}" fill="none" stroke="{cor}" stroke-opacity="{op}" '
            f'stroke-width="1.4" stroke-dasharray="{comp:.1f}" stroke-dashoffset="0"/>'
            f'<path class="pulso pulso{n}" d="{d}" fill="none" stroke="url(#pulso)" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-dasharray="26 {comp + 40:.1f}" stroke-dashoffset="26" '
            f'opacity="0"/>')


def no(x, y, atraso):
    return (f'<g class="l" style="animation-delay:{atraso:.2f}s">'
            f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="#AFC0FF" stroke-opacity="0.35"/>'
            f'<circle cx="{x}" cy="{y}" r="2.6" fill="#C9D4FF"/></g>')


def fundo():
    return (f'<rect width="{W}" height="{H}" fill="url(#fundo)"/>'
            f'<ellipse cx="{CX}" cy="300" rx="420" ry="300" fill="url(#halo)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#pontos)" mask="url(#esmaecer)"/>'
            f'<rect x="18.5" y="18.5" width="{W - 37}" height="{H - 37}" rx="22" fill="none" '
            f'stroke="#FFFFFF" stroke-opacity="0.07"/>')


def cabecalho():
    return (f'<g class="l" style="animation-delay:.1s">'
            f'<text class="sans" x="44" y="62" font-size="19" font-weight="700" fill="#FFFFFF">'
            f'{esc(TITULO)}</text>'
            f'<text class="sans" x="44" y="84" font-size="12.5" fill="#FFFFFF" fill-opacity="0.6">'
            f'{esc(SUBTITULO)}</text></g>')


def card_central():
    ox, oy, ow, oh = CX - 168, 178, 336, 196
    ix, iy, iw, ih, r = ox + 12, oy + 12, ow - 24, oh - 24, 18
    perimetro = 2 * (iw + ih) - (8 - 2 * math.pi) * r
    tracos = [
        [(ix, iy + 44), (ix + 40, iy + 44), (ix + 60, iy + 24), (ix + 112, iy + 24)],
        [(ix + iw, iy + 62), (ix + iw - 38, iy + 62), (ix + iw - 58, iy + 42), (ix + iw - 58, iy)],
        [(ix, iy + 132), (ix + 48, iy + 132), (ix + 68, iy + 152), (ix + 68, iy + ih)],
        [(ix + iw, iy + 140), (ix + iw - 42, iy + 140), (ix + iw - 66, iy + 164), (ix + iw - 66, iy + ih)],
        [(ix + 116, iy + ih), (ix + 116, iy + 140), (ix + 136, iy + 120)],
        [(ix + 196, iy), (ix + 196, iy + 26), (ix + 216, iy + 46), (ix + 250, iy + 46)],
    ]
    linhas = "".join(f'<path d="{caminho(p)[0]}" fill="none" stroke="#C7D2FF" stroke-opacity="0.16" '
                     f'stroke-width="1.2"/>' for p in tracos)
    nos = "".join(f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="#FFFFFF" stroke-opacity="0.1"/>'
                  f'<circle cx="{x}" cy="{y}" r="7.5" fill="#AFC0FF" fill-opacity="0.55"/>'
                  for x, y in [(ix + 68, iy + 86), (ix + iw - 44, iy + 36), (ix + iw - 72, iy + 128)])
    borda = (f"M{ix + r},{iy} H{ix + iw - r} A{r},{r} 0 0 1 {ix + iw},{iy + r} V{iy + ih - r} "
             f"A{r},{r} 0 0 1 {ix + iw - r},{iy + ih} H{ix + r} A{r},{r} 0 0 1 {ix},{iy + ih - r} "
             f"V{iy + r} A{r},{r} 0 0 1 {ix + r},{iy} Z")
    return (f'<g class="janela" style="animation-delay:.25s">'
            f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="28" fill="#FFFFFF" fill-opacity="0.03" '
            f'stroke="#FFFFFF" stroke-opacity="0.15"/>'
            f'<clipPath id="recorte-card"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r}"/>'
            f'</clipPath>'
            f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r}" fill="url(#vidro)" '
            f'stroke="#C3CEFF" stroke-opacity="0.4"/>'
            f'<g clip-path="url(#recorte-card)">{linhas}{nos}'
            f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih / 2}" fill="url(#brilho)" opacity="0.5"/></g>'
            f'<text class="mono" x="{CX}" y="{iy + ih / 2 + 21}" font-size="60" font-weight="700" '
            f'fill="#E2E8FF" text-anchor="middle" filter="url(#sombra-icone)">{{ }}</text>'
            f'<path class="luz" d="{borda}" fill="none" stroke="url(#luz-borda)" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-dasharray="110 {perimetro - 110:.1f}" stroke-dashoffset="0"/></g>'
            + _regra_luz(perimetro))


def _regra_luz(perimetro):
    """A luz que corre pela borda do card; parada no canto de cima se reduzir movimento."""
    REGRAS.append(f"@keyframes luz{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:{-perimetro:.1f}}}}}"
                  f".luz{{animation:luz 5s linear .8s infinite}}")
    return ""


def moldura(cx, rotulo, atraso):
    x, y, w, h = cx - 120, 404, 240, 196
    return (f'<g class="l" style="animation-delay:{atraso:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.025" '
            f'stroke="#FFFFFF" stroke-opacity="0.1"/>'
            f'<text class="sans" x="{cx}" y="{y + h - 13}" font-size="12" font-weight="600" fill="#FFFFFF" '
            f'fill-opacity="0.72" text-anchor="middle">{esc(rotulo)}</text></g>')


def tela_celular(x, y, w, h, cor_a, cor_b, destaque, n):
    """Interface genérica de app: barra, card colorido, gráfico e lista."""
    barras = "".join(f'<rect x="{x + 8 + i * 9}" y="{y + 84 - a}" width="6" height="{a}" rx="2" '
                     f'fill="{destaque}" fill-opacity="{0.45 + i * 0.1:.2f}"/>'
                     for i, a in enumerate([10, 16, 12, 22, 18, 26]))
    linhas = "".join(f'<circle cx="{x + 13}" cy="{y + 100 + i * 14}" r="4" fill="#FFFFFF" fill-opacity="0.18"/>'
                     f'<rect x="{x + 21}" y="{y + 97 + i * 14}" width="{w - 30 - i * 8}" height="5" rx="2.5" '
                     f'fill="#FFFFFF" fill-opacity="0.14"/>' for i in range(3))
    return (f'<linearGradient id="card{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{cor_a}"/>'
            f'<stop offset="1" stop-color="{cor_b}"/></linearGradient>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0F1638"/>'
            f'<rect x="{x + 8}" y="{y + 18}" width="26" height="5" rx="2.5" fill="#FFFFFF" fill-opacity="0.5"/>'
            f'<rect x="{x + 8}" y="{y + 28}" width="{w - 16}" height="28" rx="7" fill="url(#card{n})"/>'
            f'<rect x="{x + 14}" y="{y + 35}" width="22" height="4" rx="2" fill="#FFFFFF" fill-opacity="0.7"/>'
            f'<rect x="{x + 14}" y="{y + 43}" width="34" height="7" rx="3" fill="#FFFFFF" fill-opacity="0.95"/>'
            f'{barras}{linhas}')


def celular(cx, tipo, atraso, logos):
    w, h = 72, 148
    x, y = cx - w / 2, 414
    sx, sy, sw, sh = x + 4, y + 4, w - 8, h - 8
    raio = 15 if tipo == "ios" else 12
    if tipo == "ios":
        detalhe = f'<rect x="{cx - 12}" y="{sy + 5}" width="24" height="7" rx="3.5" fill="#000000"/>'
        logo, cor_logo, cores = logos["apple"]["d"], "#FFFFFF", ("#0A84FF", "#5E5CE6", "#64D2FF")
    else:
        detalhe = f'<circle cx="{cx}" cy="{sy + 8}" r="2.8" fill="#000000"/>'
        logo, cor_logo, cores = logos["android"]["d"], "#3DDC84", ("#30D158", "#00A389", "#3DDC84")
    n = 1 if tipo == "ios" else 3
    liga = atraso + 1.15
    return (f'<g class="aparelho" style="animation-delay:{atraso:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raio + 3}" fill="#12141C" stroke="#9AA8E6" '
            f'stroke-opacity="0.6" stroke-width="1.4"/>'
            f'<clipPath id="tela{n}"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="{raio}"/></clipPath>'
            f'<g clip-path="url(#tela{n})">'
            f'{tela_celular(sx, sy, sw, sh, cores[0], cores[1], cores[2], n)}'
            f'<g class="boot" style="animation-delay:{liga:.2f}s">'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#000000"/>'
            f'<path transform="translate({cx - 10},{sy + sh / 2 - 12}) scale({20 / 24:.4f})" d="{logo}" '
            f'fill="{cor_logo}"/></g>'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#reflexo)"/></g>'
            f'{detalhe}</g>')


def macbook(atraso):
    lx, ly, lw, lh = CX - 100, 428, 200, 126
    sx, sy, sw, sh = lx + 7, ly + 7, lw - 14, lh - 12
    abre = atraso
    liga = atraso + 1.5
    tiles = "".join(f'<rect x="{sx + 40 + i * 48}" y="{sy + 26}" width="42" height="24" rx="4" fill="#FFFFFF" '
                    f'fill-opacity="0.08"/><rect x="{sx + 45 + i * 48}" y="{sy + 32}" width="16" height="3" '
                    f'rx="1.5" fill="{c}"/><rect x="{sx + 45 + i * 48}" y="{sy + 39}" width="26" height="5" '
                    f'rx="2" fill="#FFFFFF" fill-opacity="0.8"/>'
                    for i, c in enumerate(["#BF5AF2", "#0A84FF", "#30D158"]))
    grafico = (f'<path d="M{sx + 42},{sy + 96} L{sx + 62},{sy + 84} L{sx + 82},{sy + 88} L{sx + 102},{sy + 72} '
               f'L{sx + 122},{sy + 78} L{sx + 142},{sy + 62} L{sx + 176},{sy + 58}" fill="none" '
               f'stroke="#8E8CFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    menu = "".join(f'<rect x="{sx + 6}" y="{sy + 22 + i * 11}" width="{20 - (i % 2) * 6}" height="4" rx="2" '
                   f'fill="#FFFFFF" fill-opacity="{0.5 if i == 0 else 0.2}"/>' for i in range(6))
    globo = (f'<circle cx="{CX}" cy="{sy + sh / 2}" r="12" fill="none" stroke="#FFFFFF" stroke-width="1.6"/>'
             f'<ellipse cx="{CX}" cy="{sy + sh / 2}" rx="5" ry="12" fill="none" stroke="#FFFFFF" '
             f'stroke-width="1.4"/><path d="M{CX - 12},{sy + sh / 2} H{CX + 12} M{CX - 10},{sy + sh / 2 - 6} '
             f'H{CX + 10} M{CX - 10},{sy + sh / 2 + 6} H{CX + 10}" stroke="#FFFFFF" stroke-width="1.2"/>')
    return (f'<g class="base" style="animation-delay:{abre:.2f}s">'
            f'<path d="M{CX - 122},{ly + lh} H{CX + 122} V{ly + lh + 5} Q{CX + 122},{ly + lh + 10} '
            f'{CX + 114},{ly + lh + 10} H{CX - 114} Q{CX - 122},{ly + lh + 10} {CX - 122},{ly + lh + 5} Z" '
            f'fill="url(#metal)"/>'
            f'<rect x="{CX - 22}" y="{ly + lh}" width="44" height="3.5" rx="1.75" fill="#2C3C9C"/></g>'
            f'<g class="tampa" style="animation-delay:{abre:.2f}s">'
            f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="9" fill="#12141C" stroke="#9AA8E6" '
            f'stroke-opacity="0.6" stroke-width="1.4"/>'
            f'<clipPath id="tela2"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="3"/></clipPath>'
            f'<g clip-path="url(#tela2)">'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#0F1638"/>'
            f'<rect x="{sx}" y="{sy}" width="32" height="{sh}" fill="#FFFFFF" fill-opacity="0.05"/>'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="14" fill="#FFFFFF" fill-opacity="0.06"/>'
            f'<circle cx="{sx + 7}" cy="{sy + 7}" r="2.2" fill="#FF5F57"/>'
            f'<circle cx="{sx + 14}" cy="{sy + 7}" r="2.2" fill="#FEBC2E"/>'
            f'<circle cx="{sx + 21}" cy="{sy + 7}" r="2.2" fill="#28C840"/>'
            f'{menu}{tiles}{grafico}'
            f'<g class="boot" style="animation-delay:{liga:.2f}s">'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#000000"/>{globo}</g>'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#reflexo)"/></g>'
            f'<circle cx="{CX}" cy="{ly + 3.6}" r="1.3" fill="#3A3F55"/></g>')


CSS = f"""
.sans{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
@keyframes aparecer{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes abrir{{from{{opacity:0;transform:translateY(10px) scale(.96)}}to{{opacity:1;transform:none}}}}
@keyframes quique{{from{{opacity:0;transform:translateY(26px) scale(.85)}}to{{opacity:1;transform:none}}}}
@keyframes tampa{{from{{transform:scaleY(.015)}}to{{transform:none}}}}
@keyframes base{{from{{transform:scaleX(1.09)}}to{{transform:none}}}}
@keyframes apagar{{0%,55%{{opacity:1}}100%{{opacity:0}}}}
.l{{animation:aparecer .35s ease-out both}}
.janela{{animation:abrir .6s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:50% 50%}}
.aparelho{{animation:quique .9s {EASE_QUIQUE} both;transform-box:fill-box;transform-origin:50% 100%}}
.tampa{{animation:tampa 1.5s {EASE_TAMPA} both;transform-box:fill-box;transform-origin:50% 100%}}
.base{{animation:base 1.5s {EASE_TAMPA} both;transform-box:fill-box;transform-origin:50% 50%}}
.boot{{animation:apagar 1.3s ease-in both}}
"""
# vem depois das REGRAS geradas, para vencer as regras de cada traço
REDUZIR_MOVIMENTO = (
    "@media (prefers-reduced-motion:reduce){"
    ".l,.janela,.aparelho,.tampa,.base,.traco,.pulso,.luz{animation:none}"
    ".boot{animation:none;opacity:0}}"
)


def desenhar():
    REGRAS.clear()
    logos = plataformas()
    esq, ce = caminho([(CX - 168, 276), (CX - 252, 276), (CX - 302, 326), (CX - 302, 404)])
    meio, cm = caminho([(CX, 374), (CX, 404)])
    dir_, cd = caminho([(CX + 168, 276), (CX + 252, 276), (CX + 302, 326), (CX + 302, 404)])
    defs = (
        '<defs>'
        '<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0E2A"/>'
        '<stop offset=".5" stop-color="#101B6A"/><stop offset="1" stop-color="#1C3DE0"/></linearGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#4C6BFF" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#4C6BFF" stop-opacity="0"/></radialGradient>'
        '<pattern id="pontos" width="18" height="18" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="1.5" r=".9" fill="#FFFFFF" fill-opacity=".16"/></pattern>'
        '<radialGradient id="fade"><stop offset=".3" stop-color="#FFFFFF"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
        f'<mask id="esmaecer"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
        '<linearGradient id="brilho" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".3"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="vidro" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#7A8FFF" stop-opacity=".38"/>'
        '<stop offset="1" stop-color="#3A54E6" stop-opacity=".22"/></linearGradient>'
        '<linearGradient id="luz-borda" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#5FA0FF" stop-opacity="0"/><stop offset=".6" stop-color="#7FB2FF"/>'
        '<stop offset="1" stop-color="#FFFFFF"/></linearGradient>'
        '<linearGradient id="pulso" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
        '<stop offset="1" stop-color="#7FB2FF"/></linearGradient>'
        '<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9DB0FF"/>'
        '<stop offset="1" stop-color="#4A62E0"/></linearGradient>'
        '<linearGradient id="reflexo" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset=".35" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/>'
        '<stop offset=".65" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        '<filter id="sombra-icone" x="-30%" y="-30%" width="160%" height="170%">'
        '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".35"/></filter>'
        f'<clipPath id="cartao"><rect width="{W}" height="{H}" rx="24"/></clipPath>'
        '</defs>')
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{esc(TITULO)}">',
        f"<title>{esc(TITULO)}: do código para iPhone, web e Android</title>",
        "",  # <style>, preenchido no fim, depois que os traços registram as REGRAS
        defs,
        '<g clip-path="url(#cartao)">',
        fundo(), cabecalho(),
        f'<g transform="translate(0,{-SUBIR})">',
        desenha_linha(esq, ce, 0.55, 0.55, 1),
        desenha_linha(meio, cm, 0.55, 0.3, 2),
        desenha_linha(dir_, cd, 0.55, 0.55, 3),
        card_central(),
        moldura(CX - 302, APARELHOS[0], 0.7),
        moldura(CX, APARELHOS[1], 0.7),
        moldura(CX + 302, APARELHOS[2], 0.7),
        no(CX - 302, 404, 1.1), no(CX, 404, 0.9), no(CX + 302, 404, 1.1),
        celular(CX - 302, "ios", 1.05, logos),
        macbook(1.1),
        celular(CX + 302, "android", 1.25, logos),
        "</g></g></svg>",
    ]
    partes[2] = f"<style>{CSS}{''.join(REGRAS)}{REDUZIR_MOVIMENTO}</style>"
    return "".join(partes)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    svg = desenhar()
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"gerado {os.path.relpath(SAIDA, RAIZ)} ({len(svg) // 1024} KB)")
