#!/usr/bin/env python3
"""
Desenha a área de trabalho do topo do README no estilo do macOS e os botões
de contato. Gera:

    assets/desktop-light.svg, assets/desktop-dark.svg
    assets/botoes/*.svg

À esquerda fica a janela "Sobre o Enzo", no jeito do "Sobre Este Mac". À direita,
o Terminal com fastfetch e cat sobre.md. Embaixo, um Dock com a stack.
Os textos ficam nas constantes logo abaixo; mude e rode de novo:

    python3 scripts/perfil.py

Os ícones do Dock vêm de scripts/icones.json (Simple Icons, CC0).
Só usa a biblioteca padrão do Python.
"""
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from tema import (CSS_BASE, SANS, TEMAS, esc, semaforo, sombra,  # noqa: E402
                  topo_arredondado)

TRACO = "─" * 13  # linha embaixo de usuário@máquina

RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
ASSETS = os.path.join(RAIZ, "assets")
ANO = datetime.date.today().year

NOME = "Enzo Rodrigues"
SUBTITULO = "Full-stack & Mobile · Monte Mor, SP"
FICHA = [  # janela "Sobre o Enzo"
    ("Empresa", "GN Solutions"),
    ("Apps", "iOS · Android · Web"),
    ("Stack", "TypeScript · Python · Swift"),
    ("Mobile", "React Native · Expo"),
    ("IA", "Claude Code · Codex"),
    ("Estudo", "ADS no IFSP"),
    ("GitHub", "desde 2022"),
]
FASTFETCH = [  # (chave, valor); a primeira linha é usuário@máquina
    ("OS", "macOS 27 · Mac mini"),
    ("Shell", "zsh"),
    ("IDE", "TTES · Xcode"),
    ("Agentes", "Claude Code · Codex"),
    ("Apps", "iOS · Android · Web"),
    ("Stack", "TypeScript · React Native · Python"),
    ("Infra", "Docker · VPS · GitHub Actions"),
]
SOBRE = [  # ("titulo", texto) | ("linha", texto, cor) | ("item", nome, descrição, destaque)
    ("titulo", "## Agora"),
    ("linha", "Dev Full-stack & Mobile na GN Solutions", "texto"),
    ("linha", "Cursando ADS no IFSP", "secundario"),
    ("titulo", "## Produtos"),
    ("item", "MoneyFin AI", "finanças com IA · ", "na App Store"),
    ("item", "Clerum", "gestão para igrejas · web + app", ""),
    ("item", "UpKeeper", "manutenção e ativos · multi-tenant", ""),
    ("titulo", "## Ferramentas que criei"),
    ("item", "TTES", "IDE macOS para agentes de código", ""),
    ("item", "Quality Gate", "ratchet de métricas no CI", ""),
]
DOCK = [  # (ícone, fundo, cor do símbolo, ativo)
    ("swift", ("#F88A36", "#FD2020"), "#FFFFFF", False),
    ("typescript", "#3178C6", None, False),
    ("react", "#20232A", "#61DAFB", False),
    ("expo", "#FFFFFF", "#000020", False),
    ("nodedotjs", "#1F2A1F", "#5FA04E", False),
    ("python", ("#3776AB", "#24557F"), "#FFD43B", False),
    ("flask", "#FFFFFF", "#000000", False),
    ("postgresql", "#336791", "#FFFFFF", False),
    ("docker", "#2496ED", "#FFFFFF", False),
    ("githubactions", "#2088FF", "#FFFFFF", False),
    None,  # separador
    ("claude", "#F5F4ED", "#D97757", True),
    ("terminal", "#1C1C1E", None, True),
]
BOTOES = [  # (arquivo, rótulo)
    ("linkedin", "LinkedIn"),
    ("email", "E-mail"),
    ("instagram", "Instagram"),
    ("gnsolutions", "GN Solutions"),
]

W, H = 960, 630
CW = 6.95          # largura de um caractere mono em 11,5 px
LINHA = 16         # altura de linha do Terminal


def icones():
    with open(os.path.join(AQUI, "icones.json"), encoding="utf-8") as f:
        return json.load(f)["icones"]


def papel_de_parede(t):
    defs = (f'<linearGradient id="pp" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{t["fundo_a"]}"/>'
            f'<stop offset="1" stop-color="{t["fundo_b"]}"/></linearGradient>'
            f'<filter id="borrar" filterUnits="userSpaceOnUse" x="-200" y="-200" '
            f'width="{W + 400}" height="{H + 400}"><feGaussianBlur stdDeviation="72"/></filter>')
    manchas = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" fill-opacity="{o}"/>'
                      for x, y, r, c, o in t["manchas"])
    corpo = (f'<rect width="{W}" height="{H}" fill="url(#pp)"/>'
             f'<g filter="url(#borrar)">{manchas}</g>')
    return defs, corpo


def barra_de_menus(t):
    out = [f'<rect width="{W}" height="28" fill="{t["menu"]}" fill-opacity="{t["menu_op"]}"/>']
    menus = "".join(f'<tspan dx="20">{m}</tspan>' for m in
                    ["Arquivo", "Editar", "Visualizar", "Projetos", "Janela", "Ajuda"])
    out.append(f'<text class="sans" x="18" y="18.5" font-size="13" fill="{t["texto"]}">'
               f'<tspan font-weight="700" font-size="14">⌘</tspan>'
               f'<tspan dx="16" font-weight="700">Enzo</tspan>{menus}</text>')
    # ícones de status à direita: central de controle, busca, wi-fi, bateria e hora
    c = t["texto"]
    hx = W - 18
    out.append(f'<text class="sans" x="{hx}" y="18.5" font-size="13" font-weight="500" '
               f'fill="{c}" text-anchor="end">9:41</text>')
    bx = W - 92
    out.append(f'<rect x="{bx}" y="9" width="22" height="11" rx="3" fill="none" stroke="{c}" '
               f'stroke-opacity="0.55" stroke-width="1"/><rect x="{bx + 23.5}" y="12.5" width="1.6" '
               f'height="4" rx="0.8" fill="{c}" fill-opacity="0.55"/><rect x="{bx + 2}" y="11" '
               f'width="15" height="7" rx="1.6" fill="{c}"/>')
    wx = W - 112
    for raio, op in ((9, 1), (6, 1), (3, 1)):
        out.append(f'<path d="M{wx - raio * 0.78:.2f},{19.5 - raio * 0.62:.2f} A{raio},{raio} 0 0 1 '
                   f'{wx + raio * 0.78:.2f},{19.5 - raio * 0.62:.2f}" fill="none" stroke="{c}" '
                   f'stroke-width="1.7" stroke-linecap="round" stroke-opacity="{op}"/>')
    out.append(f'<circle cx="{wx}" cy="19.6" r="1.4" fill="{c}"/>')
    sx = W - 140
    out.append(f'<circle cx="{sx}" cy="13.5" r="4.6" fill="none" stroke="{c}" stroke-width="1.6"/>'
               f'<path d="M{sx + 3.3},{16.8} l3.6,3.6" stroke="{c}" stroke-width="1.8" '
               f'stroke-linecap="round"/>')
    cx = W - 172
    out.append(f'<rect x="{cx}" y="8" width="16" height="6" rx="3" fill="none" stroke="{c}" '
               f'stroke-width="1.3"/><circle cx="{cx + 12.5}" cy="11" r="1.6" fill="{c}"/>'
               f'<rect x="{cx}" y="15.5" width="16" height="6" rx="3" fill="none" stroke="{c}" '
               f'stroke-width="1.3"/><circle cx="{cx + 3.5}" cy="18.5" r="1.6" fill="{c}"/>')
    return "".join(out)


def macbook(cx, cy):
    """MacBook visto de frente, como a imagem do aparelho no "Sobre" do macOS:
    tampa com moldura preta e notch, tela azul e base de alumínio mais larga."""
    lw, lh = 140, 92                 # tampa
    lx, ly = cx - lw / 2, cy - 52
    b = ly + lh                      # dobradiça
    bw = 168                         # base
    bx = cx - bw / 2
    tx, ty, tw, th = lx + 4.5, ly + 4.5, lw - 9, lh - 10   # tela
    ty_c = ty + th / 2
    anel = 2 * 3.14159 * 9
    return (f'<ellipse cx="{cx}" cy="{b + 9}" rx="{bw / 2 - 8}" ry="3.2" fill="#000000" '
            f'fill-opacity="0.3" filter="url(#borrar-leve)"/>'
            # tampa: abre a partir da dobradiça, como no diagrama de plataformas
            f'<g class="tampa-mac">'
            f'<rect x="{lx - 1.6}" y="{ly - 1.6}" width="{lw + 3.2}" height="{lh + 1.6}" rx="8.6" '
            f'fill="url(#mac-aro)"/>'
            f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="7" fill="#0A0A0C"/>'
            f'<clipPath id="mac-recorte"><rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="2.5"/>'
            f'</clipPath>'
            f'<g clip-path="url(#mac-recorte)">'
            f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="url(#mac-tela)"/>'
            f'<ellipse cx="{lx + 46}" cy="{ly + 28}" rx="58" ry="26" fill="#FFFFFF" fill-opacity="0.16"/>'
            # boot: tela escura com um anel carregando, que some e revela o papel de parede
            f'<g class="boot-mac"><rect x="{tx}" y="{ty}" width="{tw}" height="{th}" fill="#0E0F14"/>'
            f'<circle cx="{cx}" cy="{ty_c}" r="9" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" '
            f'stroke-width="2"/>'
            f'<circle class="gira" cx="{cx}" cy="{ty_c}" r="9" fill="none" stroke="#6AA8FF" '
            f'stroke-width="2" stroke-linecap="round" stroke-dasharray="{anel * 0.28:.1f} {anel:.1f}"/>'
            f'</g></g>'
            f'<rect x="{cx - 10}" y="{ly + 2}" width="20" height="6.5" rx="2.4" fill="#0A0A0C"/></g>'
            # base: começa um pouco mais larga e assenta enquanto a tampa abre
            f'<g class="base-mac">'
            f'<path d="M{bx},{b} H{bx + bw} V{b + 3.6} Q{bx + bw},{b + 7} {bx + bw - 7},{b + 7} '
            f'H{bx + 7} Q{bx},{b + 7} {bx},{b + 3.6} Z" fill="url(#mac-base)"/>'
            f'<line x1="{bx + 2}" y1="{b + 0.5}" x2="{bx + bw - 2}" y2="{b + 0.5}" stroke="#FFFFFF" '
            f'stroke-opacity="0.75"/>'
            f'<rect x="{cx - 14}" y="{b}" width="28" height="2.4" rx="1.2" fill="#000000" '
            f'fill-opacity="0.2"/></g>')


# Abertura da tampa: mesma curva e duração do diagrama (e da referência da ToDesktop).
# Fica depois de CSS_BASE no <style>, com o próprio bloco de "reduzir movimento".
CSS_MAC = """
@keyframes tampa-mac{from{transform:scaleY(.015)}to{transform:none}}
@keyframes base-mac{from{transform:scaleX(1.08)}to{transform:none}}
@keyframes some{0%,60%{opacity:1}100%{opacity:0}}
@keyframes gira{to{transform:rotate(360deg)}}
.tampa-mac{animation:tampa-mac 1.5s cubic-bezier(.76,0,.24,1) .35s both;transform-box:fill-box;transform-origin:50% 100%}
.base-mac{animation:base-mac 1.5s cubic-bezier(.76,0,.24,1) .35s both;transform-box:fill-box;transform-origin:50% 50%}
.boot-mac{animation:some 1.4s ease-in 1.6s both}
.gira{animation:gira .7s linear 1.4s 4;transform-box:fill-box;transform-origin:50% 50%}
@media (prefers-reduced-motion:reduce){.tampa-mac,.base-mac,.gira{animation:none}.boot-mac{animation:none;opacity:0}}
"""


def janela_sobre(t, x, y, w, h):
    cx = x + w / 2
    out = [f'<g class="janela" style="animation-delay:.05s">',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["janela"]}" '
           f'filter="url(#sombra)"/>',
           semaforo(x + 20, y + 20, so_fechar=True, t=t)]
    out.append(macbook(cx, y + 106))
    out.append(f'<text class="sans" x="{cx}" y="{y + 194}" font-size="24" font-weight="700" '
               f'letter-spacing="-0.3" fill="{t["texto"]}" text-anchor="middle">{esc(NOME)}</text>')
    out.append(f'<text class="sans" x="{cx}" y="{y + 215}" font-size="12" '
               f'fill="{t["secundario"]}" text-anchor="middle">{esc(SUBTITULO)}</text>')
    # ficha, rótulo alinhado à direita e valor à esquerda, como no "Sobre Este Mac"
    rx_, vx = x + 104, x + 114
    for i, (rotulo, valor) in enumerate(FICHA):
        ly = y + 250 + i * 21
        out.append(f'<text class="sans" x="{rx_}" y="{ly}" font-size="11.5" font-weight="600" '
                   f'fill="{t["texto"]}" text-anchor="end">{esc(rotulo)}</text>'
                   f'<text class="sans" x="{vx}" y="{ly}" font-size="11.5" '
                   f'fill="{t["secundario"]}">{esc(valor)}</text>')
    by = y + 400
    out.append(f'<rect x="{cx - 74}" y="{by}" width="148" height="24" rx="12" fill="{t["botao"]}" '
               f'stroke="{t["botao_borda"]}" stroke-opacity="{t["botao_borda_op"]}"/>'
               f'<text class="sans" x="{cx}" y="{by + 16}" font-size="12" font-weight="500" '
               f'fill="{t["texto"]}" text-anchor="middle">Mais Informações…</text>')
    out.append(f'<text class="sans" x="{cx}" y="{y + h - 26}" font-size="9.5" '
               f'fill="{t["terciario"]}" text-anchor="middle">™ e © 2022–{ANO} '
               f'{esc(NOME)}.</text>'
               f'<text class="sans" x="{cx}" y="{y + h - 13}" font-size="9.5" '
               f'fill="{t["terciario"]}" text-anchor="middle">Todos os direitos reservados.</text>')
    out.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="13.5" '
               f'fill="none" stroke="{t["borda"]}" stroke-opacity="{t["borda_op"]}"/></g>')
    return "".join(out)


def prompt(t, x, y, comando, inicio, n):
    """Prompt '~ ❯' que aparece e um comando que é digitado letra por letra."""
    px = x + 4 * CW + 2
    largura = len(comando) * CW + 4
    duracao = inicio + 0.12 + len(comando) * 0.045
    chave = inicio / duracao
    return (f'<text class="mono l" style="animation-delay:{inicio:.2f}s" x="{x}" y="{y}" '
            f'font-size="11.5" xml:space="preserve"><tspan fill="{t["t_azul"]}" '
            f'font-weight="700">~</tspan><tspan fill="{t["t_roxo"]}" font-weight="700"> ❯</tspan>'
            f'</text><clipPath id="dig{n}"><rect x="{px}" y="{y - 12}" height="16" '
            f'width="{largura:.1f}"><animate attributeName="width" values="0;0;{largura:.1f}" '
            f'keyTimes="0;{chave:.3f};1" dur="{duracao:.2f}s" fill="freeze"/></rect></clipPath>'
            f'<text class="mono" x="{px}" y="{y}" font-size="11.5" fill="{t["texto"]}" '
            f'clip-path="url(#dig{n})">{esc(comando)}</text>')


def terminal(t, x, y, w, h):
    out = [f'<g class="janela" style="animation-delay:.18s">',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["terminal"]}" '
           f'filter="url(#sombra)"/>',
           f'<path d="{topo_arredondado(x, y, w, 30, 14)}" fill="{t["barra_titulo"]}"/>',
           f'<line x1="{x}" y1="{y + 30.5}" x2="{x + w}" y2="{y + 30.5}" stroke="{t["borda"]}" '
           f'stroke-opacity="{t["borda_op"]}"/>',
           semaforo(x + 20, y + 15),
           f'<text class="sans" x="{x + w / 2}" y="{y + 19.5}" font-size="12" font-weight="600" '
           f'fill="{t["secundario"]}" text-anchor="middle">enzo — -zsh — 80×24</text>']
    x0 = x + 18
    y0 = y + 54
    out.append(prompt(t, x0, y0, "fastfetch", 0.8, 1))
    # "logo" do fastfetch: um ícone de app com { }
    lx, ly, lado = x0, y0 + 14, 96
    out.append(f'<g class="l" style="animation-delay:1.45s">'
               f'<rect x="{lx}" y="{ly}" width="{lado}" height="{lado}" rx="23" fill="url(#icone)"/>'
               f'<text class="mono" x="{lx + lado / 2}" y="{ly + lado / 2 + 11}" font-size="32" '
               f'font-weight="700" fill="#FFFFFF" text-anchor="middle">{{ }}</text></g>')
    ix = lx + lado + 22
    iy = y0 + 22
    atraso = 1.5
    out.append(f'<text class="mono l" style="animation-delay:{atraso:.2f}s" x="{ix}" y="{iy}" '
               f'font-size="11.5" font-weight="700"><tspan fill="{t["t_indigo"]}">enzo</tspan>'
               f'<tspan fill="{t["texto"]}">@</tspan><tspan fill="{t["t_indigo"]}">mac-mini</tspan>'
               f'</text>')
    out.append(f'<text class="mono l" style="animation-delay:{atraso + 0.04:.2f}s" x="{ix}" '
               f'y="{iy + LINHA}" font-size="11.5" fill="{t["terciario"]}">'
               f'{TRACO}</text>')
    for i, (chave, valor) in enumerate(FASTFETCH):
        ly2 = iy + (i + 2) * LINHA
        out.append(f'<text class="mono l" style="animation-delay:{atraso + 0.08 + i * 0.05:.2f}s" '
                   f'x="{ix}" y="{ly2}" font-size="11.5" xml:space="preserve">'
                   f'<tspan fill="{t["t_azul"]}" font-weight="700">{esc(chave.ljust(9))}</tspan>'
                   f'<tspan fill="{t["texto"]}">{esc(valor)}</tspan></text>')
    cores = ["vermelho", "laranja", "amarelo", "verde", "menta", "ciano", "azul", "indigo", "roxo",
             "rosa"]
    cy_ = iy + (len(FASTFETCH) + 2) * LINHA - 9
    blocos = "".join(f'<rect x="{ix + i * 22}" y="{cy_}" width="18" height="10" rx="3" '
                     f'fill="{t[c]}"/>' for i, c in enumerate(cores))
    out.append(f'<g class="l" style="animation-delay:{atraso + 0.5:.2f}s">{blocos}</g>')

    # cat sobre.md
    sy = cy_ + 40
    out.append(prompt(t, x0, sy, "cat sobre.md", 2.25, 2))
    atraso = 2.25 + 0.12 + 12 * 0.045 + 0.15
    yy = sy
    for i, linha in enumerate(SOBRE):
        yy += LINHA + (5 if linha[0] == "titulo" else 0)
        d = f'style="animation-delay:{atraso + i * 0.06:.2f}s"'
        if linha[0] == "titulo":
            corpo = f'<tspan fill="{t["t_laranja"]}" font-weight="700">{esc(linha[1])}</tspan>'
        elif linha[0] == "linha":
            corpo = f'<tspan fill="{t[linha[2]]}">{esc(linha[1])}</tspan>'
        else:
            _, nome, desc, destaque = linha
            corpo = (f'<tspan fill="{t["texto"]}" font-weight="700">{esc(nome.ljust(14))}</tspan>'
                     f'<tspan fill="{t["secundario"]}">{esc(desc)}</tspan>')
            if destaque:
                corpo += f'<tspan fill="{t["t_verde"]}" font-weight="700">{esc(destaque)}</tspan>'
        out.append(f'<text class="mono l" {d} x="{x0}" y="{yy}" font-size="11.5" '
                   f'xml:space="preserve">{corpo}</text>')
    fim = atraso + len(SOBRE) * 0.06 + 0.2
    yy += LINHA + 8
    out.append(f'<g class="l" style="animation-delay:{fim:.2f}s"><text class="mono" x="{x0}" '
               f'y="{yy}" font-size="11.5" xml:space="preserve"><tspan fill="{t["t_azul"]}" '
               f'font-weight="700">~</tspan><tspan fill="{t["t_roxo"]}" font-weight="700"> ❯'
               f'</tspan></text><rect class="cursor" x="{x0 + 4 * CW + 2}" y="{yy - 10.5}" '
               f'width="7" height="13.5" rx="1" fill="{t["azul"]}"/></g>')
    out.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="13.5" '
               f'fill="none" stroke="{t["borda"]}" stroke-opacity="{t["borda_op"]}"/></g>')
    return "".join(out)


def dock(t, base_y):
    lado, vao, margem, sep = 44, 10, 12, 21
    n = sum(1 for item in DOCK if item)
    largura = margem * 2 + n * lado + (n - 1) * vao + (sep - vao)
    x = (W - largura) / 2
    altura = lado + 22
    paths = icones()
    out = [f'<g class="dock" style="animation-delay:.45s">',
           f'<rect x="{x}" y="{base_y}" width="{largura}" height="{altura}" rx="20" '
           f'fill="{t["dock"]}" fill-opacity="{t["dock_op"]}" stroke="{t["dock_borda"]}" '
           f'stroke-opacity="{t["dock_borda_op"]}"/>']
    ix = x + margem
    iy = base_y + 9
    grad = 0
    for item in DOCK:
        if item is None:
            out.append(f'<line x1="{ix + (sep - vao) / 2 - vao / 2 + 5:.1f}" y1="{iy + 6}" '
                       f'x2="{ix + (sep - vao) / 2 - vao / 2 + 5:.1f}" y2="{iy + lado - 6}" '
                       f'stroke="{t["texto"]}" stroke-opacity="0.22"/>')
            ix += sep - vao
            continue
        nome, fundo, cor, ativo = item
        if isinstance(fundo, tuple):
            grad += 1
            out.append(f'<linearGradient id="g{grad}" x1="0" y1="0" x2="0" y2="1">'
                       f'<stop offset="0" stop-color="{fundo[0]}"/>'
                       f'<stop offset="1" stop-color="{fundo[1]}"/></linearGradient>')
            preenchimento = f"url(#g{grad})"
        else:
            preenchimento = fundo
        if nome == "swift":
            # o símbolo do Swift já é um quadrado arredondado com o pássaro vazado
            escala = lado / 24
            out.append(f'<clipPath id="recorte-swift"><rect x="{ix}" y="{iy}" width="{lado}" '
                       f'height="{lado}" rx="10"/></clipPath>'
                       f'<g filter="url(#sombraicone)"><g clip-path="url(#recorte-swift)">'
                       f'<rect x="{ix + 3}" y="{iy + 3}" width="{lado - 6}" height="{lado - 6}" '
                       f'rx="12" fill="#FFFFFF"/><path transform="translate({ix},{iy}) '
                       f'scale({escala:.4f})" d="{paths[nome]["d"]}" fill="{preenchimento}"/></g></g>')
            ix += lado + vao
            continue
        out.append(f'<g filter="url(#sombraicone)"><rect x="{ix}" y="{iy}" width="{lado}" '
                   f'height="{lado}" rx="10" fill="{preenchimento}"/></g>')
        if nome == "typescript":
            out.append(f'<text class="sans" x="{ix + lado - 6}" y="{iy + lado - 7}" font-size="17" '
                       f'font-weight="700" fill="#FFFFFF" text-anchor="end">TS</text>')
        elif nome == "terminal":
            out.append(f'<rect x="{ix + 0.5}" y="{iy + 0.5}" width="{lado - 1}" height="{lado - 1}" '
                       f'rx="9.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.18"/>'
                       f'<text class="mono" x="{ix + 9}" y="{iy + 27}" font-size="15" '
                       f'font-weight="700" fill="#FFFFFF">&gt;_</text>')
        else:
            escala = 26 / 24
            out.append(f'<path transform="translate({ix + 9},{iy + 9}) scale({escala:.4f})" '
                       f'd="{paths[nome]["d"]}" fill="{cor}"/>')
        if ativo:
            out.append(f'<circle cx="{ix + lado / 2}" cy="{iy + lado + 7}" r="2" '
                       f'fill="{t["texto"]}" fill-opacity="0.6"/>')
        ix += lado + vao
    out.append("</g>")
    return "".join(out)


def defs_macbook(nome_tema):
    """Gradientes do MacBook da janela "Sobre"; o alumínio fica um tom abaixo no tema escuro."""
    aro, base = ((("#E6E6EA", "#A9A9AF"), ("#F0F0F3", "#B4B4B9")) if nome_tema == "light"
                 else (("#BDBDC3", "#6F6F76"), ("#CFCFD4", "#8A8A90")))
    return (f'<linearGradient id="mac-aro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{aro[0]}"/>'
            f'<stop offset="1" stop-color="{aro[1]}"/></linearGradient>'
            f'<linearGradient id="mac-base" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{base[0]}"/>'
            f'<stop offset="1" stop-color="{base[1]}"/></linearGradient>'
            f'<linearGradient id="mac-tela" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#8CC4FF"/>'
            f'<stop offset=".5" stop-color="#3F8EF6"/><stop offset="1" stop-color="#1D5FD6"/></linearGradient>'
            f'<filter id="borrar-leve" x="-20%" y="-300%" width="140%" height="700%">'
            f'<feGaussianBlur stdDeviation="3"/></filter>')


def desenhar(nome_tema):
    t = TEMAS[nome_tema]
    defs_pp, papel = papel_de_parede(t)
    defs = (f"<defs>{defs_pp}{sombra('sombra', t['sombra_op'])}"
            f"{sombra('sombraicone', 0.22, dy=1, desvio=1.4)}"
            f'<linearGradient id="icone" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#0A84FF"/><stop offset=".55" stop-color="#5E5CE6"/>'
            f'<stop offset="1" stop-color="#BF5AF2"/></linearGradient>'
            f"{defs_macbook(nome_tema)}"
            f'<clipPath id="tela"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>')
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Área de trabalho no estilo macOS de {esc(NOME)}">',
        f"<title>{esc(NOME)}: Sobre o Enzo, Terminal com fastfetch e sobre.md, e o Dock com a stack"
        f"</title>",
        f"<style>{CSS_BASE}{CSS_MAC}</style>",
        defs,
        '<g clip-path="url(#tela)">',
        papel,
        barra_de_menus(t),
        janela_sobre(t, 36, 50, 318, 476),
        terminal(t, 376, 50, 548, 476),
        dock(t, 546),
        "</g>",
        "</svg>",
    ]
    return "".join(partes)


def botao(rotulo):
    """Botão em cápsula azul, como os botões de ação da Apple, com uma seta ↗."""
    largura = round(len(rotulo) * 8.1 + 54)
    altura = 36
    tx = 20
    ax = largura - 26
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" '
            f'viewBox="0 0 {largura} {altura}" role="img" aria-label="{esc(rotulo)}">'
            f"<title>{esc(rotulo)}</title>"
            f'<rect width="{largura}" height="{altura}" rx="18" fill="#0071E3"/>'
            f'<text x="{tx}" y="23" font-family="{esc(SANS)}" '
            f'font-size="14.5" font-weight="500" fill="#FFFFFF">{esc(rotulo)}</text>'
            f'<path d="M{ax},{23} L{ax + 8},{15} M{ax + 2},{15} H{ax + 8} V{21}" fill="none" '
            f'stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            f"</svg>")


def main():
    os.makedirs(os.path.join(ASSETS, "botoes"), exist_ok=True)
    for nome_tema in TEMAS:
        caminho = os.path.join(ASSETS, f"desktop-{nome_tema}.svg")
        svg = desenhar(nome_tema)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"gerado {os.path.relpath(caminho, RAIZ)} ({len(svg) // 1024} KB)")
    for arquivo, rotulo in BOTOES:
        caminho = os.path.join(ASSETS, "botoes", f"{arquivo}.svg")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(botao(rotulo))
    print(f"gerados {len(BOTOES)} botões em assets/botoes/")


if __name__ == "__main__":
    main()
