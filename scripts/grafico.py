#!/usr/bin/env python3
"""
Desenha data/contributions.json (gerado por contribuicoes.py) como o gráfico de
contribuições do perfil, numa janela no estilo do macOS, em duas versões:

    assets/contrib-light.svg, assets/contrib-dark.svg

Semanas são colunas e dias são linhas, como no GitHub, mas cada dia da grade
soma o mesmo dia de todos os anos (o janeiro da grade junta todos os janeiros).
Embaixo ficam a legenda e quatro cartões de resumo, no jeito do app Saúde.

    python3 scripts/grafico.py

Só usa a biblioteca padrão do Python.
"""
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from tema import (CSS_BASE, TEMAS, data_br, esc, milhar, semaforo,  # noqa: E402
                  sombra)

RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
DADOS = os.environ.get("GRAFICO_DADOS", os.path.join(RAIZ, "data", "contributions.json"))
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
DIAS_ROTULO = {1: "seg", 3: "qua", 5: "sex"}

W = 960
QUADRO, PASSO = 12, 15
MARGEM = 16          # espaço para a sombra da janela


def _nivel(contagem, cortes):
    if contagem <= 0:
        return 0
    for i, corte in enumerate(cortes, start=1):
        if contagem <= corte:
            return i
    return 4


def mesclar(dias, ano_grade):
    """Grade de janeiro a dezembro em que cada dia soma o mesmo dia de todos os anos.

    29 de fevereiro, num ano da grade que não é bissexto, entra no dia 28.
    """
    bissexto = (ano_grade % 4 == 0 and ano_grade % 100 != 0) or ano_grade % 400 == 0
    por_dia = {}
    for d in dias:
        data = datetime.date.fromisoformat(d["date"])
        mes, dia = data.month, data.day
        if mes == 2 and dia == 29 and not bissexto:
            dia = 28
        por_dia[(mes, dia)] = por_dia.get((mes, dia), 0) + d["count"]
    positivos = sorted(n for n in por_dia.values() if n > 0)

    def corte(fracao):
        if not positivos:
            return 0
        k = (len(positivos) - 1) * fracao
        baixo = int(k)
        alto = min(baixo + 1, len(positivos) - 1)
        return positivos[baixo] + (positivos[alto] - positivos[baixo]) * (k - baixo)

    cortes = (corte(0.25), corte(0.50), corte(0.75))
    grade = []
    dia = datetime.date(ano_grade, 1, 1)
    while dia.year == ano_grade:
        n = por_dia.get((dia.month, dia.day), 0)
        grade.append({"date": dia, "count": n, "level": _nivel(n, cortes)})
        dia += datetime.timedelta(days=1)
    return grade


def plural(n, um, varios):
    return um if n == 1 else varios


def desenhar(dados, nome_tema):
    t = TEMAS[nome_tema]
    r = dados["resumo"]
    entrada = dados["entrada"]
    grade = mesclar(dados["dias"], datetime.date.today().year)
    antes = (grade[0]["date"].weekday() + 1) % 7   # semana começa no domingo, como no GitHub
    semanas = (antes + len(grade) + 6) // 7
    largura_grade = semanas * PASSO - (PASSO - QUADRO)
    rotulos = 30

    x, y = MARGEM, 10
    w = W - 2 * MARGEM
    gx = x + (w - (rotulos + largura_grade)) / 2 + rotulos
    topo = y + 52
    gy = topo + 40
    legenda_y = gy + 7 * PASSO + 10
    cartoes_y = legenda_y + 32
    cartao_h = 86
    h = cartoes_y + cartao_h + 24 - y
    H = y + h + 26

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" role="img" aria-label="Gráfico de contribuições no GitHub">',
           f"<title>Contribuições no GitHub desde {entrada['ano']}. Cada dia da grade soma o mesmo "
           f"dia de todos os anos.</title>",
           f"<style>{CSS_BASE}</style>",
           f"<defs>{sombra('sombra', t['sombra_op'] * 0.6, dy=8, desvio=12)}</defs>",
           f'<g class="janela" style="animation-delay:.05s">',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{t["terminal"]}" '
           f'filter="url(#sombra)"/>',
           semaforo(x + 22, y + 26)]

    # barra de ferramentas unificada: título, subtítulo e a cápsula "no GitHub desde"
    out.append(f'<text class="sans" x="{x + 92}" y="{y + 23}" font-size="15" font-weight="700" '
               f'fill="{t["texto"]}">Contribuições</text>'
               f'<text class="sans" x="{x + 92}" y="{y + 39}" font-size="11" '
               f'fill="{t["secundario"]}">Todos os anos somados, mês a mês</text>')
    cap_w = 172
    cap_x = x + w - 22 - cap_w
    out.append(f'<rect x="{cap_x}" y="{y + 13}" width="{cap_w}" height="26" rx="13" '
               f'fill="{t["azul"]}" fill-opacity="0.13"/>'
               f'<text class="sans" x="{cap_x + cap_w / 2}" y="{y + 30.5}" font-size="12.5" '
               f'font-weight="600" fill="{t["t_azul"]}" text-anchor="middle">no GitHub desde '
               f'<tspan font-weight="800">{esc(entrada["ano"])}</tspan></text>')
    out.append(f'<line x1="{x}" y1="{topo + 0.5}" x2="{x + w}" y2="{topo + 0.5}" '
               f'stroke="{t["borda"]}" stroke-opacity="{t["borda_op"] * 0.7:.3f}"/>')

    # meses em cima e dias da semana à esquerda
    visto = None
    for i, d in enumerate(grade):
        col = (i + antes) // 7
        if d["date"].day <= 7 and d["date"].month != visto and col < semanas - 1:
            visto = d["date"].month
            out.append(f'<text class="sans" x="{gx + col * PASSO}" y="{gy - 9}" font-size="10.5" '
                       f'fill="{t["secundario"]}">{MESES[visto - 1]}</text>')
    for linha, nome in DIAS_ROTULO.items():
        out.append(f'<text class="sans" x="{gx - rotulos}" y="{gy + linha * PASSO + QUADRO - 2}" '
                   f'font-size="10" fill="{t["secundario"]}">{nome}</text>')

    # quadrados, um grupo por semana, aparecendo da esquerda para a direita
    colunas = [[] for _ in range(semanas)]
    for i, d in enumerate(grade):
        col, linha = divmod(i + antes, 7)
        colunas[col].append(f'<rect x="{gx + col * PASSO}" y="{gy + linha * PASSO}" '
                            f'width="{QUADRO}" height="{QUADRO}" rx="3.2" '
                            f'fill="{t["grafico"][d["level"]]}"/>')
    for col, quadros in enumerate(colunas):
        out.append(f'<g class="l" style="animation-delay:{0.25 + col * 0.018:.3f}s">'
                   f'{"".join(quadros)}</g>')

    # legenda
    fim_grade = gx + largura_grade
    lx = fim_grade - 34 - 5 * PASSO
    out.append(f'<text class="sans" x="{gx - rotulos}" y="{legenda_y + QUADRO - 2}" font-size="11" '
               f'fill="{t["secundario"]}">Cada quadrado soma o mesmo dia de todos os anos.</text>')
    out.append(f'<text class="sans" x="{lx - 7}" y="{legenda_y + QUADRO - 2}" font-size="11" '
               f'fill="{t["secundario"]}" text-anchor="end">Menos</text>')
    for cor in t["grafico"]:
        out.append(f'<rect x="{lx}" y="{legenda_y}" width="{QUADRO}" height="{QUADRO}" rx="3.2" '
                   f'fill="{cor}"/>')
        lx += PASSO
    out.append(f'<text class="sans" x="{lx + 4}" y="{legenda_y + QUADRO - 2}" font-size="11" '
               f'fill="{t["secundario"]}">Mais</text>')

    # cartões de resumo
    cartoes = [
        ("Contribuições", t["t_azul"], milhar(r["total"]), "",
         f"de {data_br(entrada['data'])} a {data_br(r['fim'])}"),
        ("Sequência atual", t["t_laranja"], str(r["atual"]), plural(r["atual"], "dia", "dias"),
         "seguidos até hoje"),
        ("Maior sequência", t["t_verde"], str(r["maior"]), plural(r["maior"], "dia", "dias"),
         "recorde de dias seguidos"),
        ("Melhor dia", t["t_rosa"], str(r["melhor"]),
         plural(r["melhor"], "contribuição", "contribuições"), f"em {data_br(r['melhor_data'])}"),
    ]
    vao = 12
    cx0 = x + 24
    cw = (w - 48 - 3 * vao) / 4
    for i, (titulo, cor, numero, unidade, rodape) in enumerate(cartoes):
        cx = cx0 + i * (cw + vao)
        un = (f'<tspan dx="5" font-size="14" font-weight="600" fill="{t["secundario"]}">'
              f'{esc(unidade)}</tspan>') if unidade else ""
        out.append(f'<g class="l" style="animation-delay:{1.1 + i * 0.1:.2f}s">'
                   f'<rect x="{cx:.1f}" y="{cartoes_y}" width="{cw:.1f}" height="{cartao_h}" rx="12" '
                   f'fill="{t["cartao"]}"/>'
                   f'<circle cx="{cx + 20:.1f}" cy="{cartoes_y + 20}" r="4" fill="{cor}"/>'
                   f'<text class="sans" x="{cx + 30:.1f}" y="{cartoes_y + 24.5}" font-size="12.5" '
                   f'font-weight="600" fill="{cor}">{esc(titulo)}</text>'
                   f'<text class="arred" x="{cx + 16:.1f}" y="{cartoes_y + 57}" font-size="28" '
                   f'font-weight="700" fill="{t["texto"]}">{esc(numero)}{un}</text>'
                   f'<text class="sans" x="{cx + 16:.1f}" y="{cartoes_y + 75}" font-size="11" '
                   f'fill="{t["secundario"]}">{esc(rodape)}</text></g>')

    out.append(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="15.5" '
               f'fill="none" stroke="{t["borda"]}" stroke-opacity="{t["borda_op"]}"/></g></svg>')
    return "".join(out)


def main():
    with open(DADOS, encoding="utf-8") as f:
        dados = json.load(f)
    for nome_tema in TEMAS:
        caminho = os.path.join(RAIZ, "assets", f"contrib-{nome_tema}.svg")
        svg = desenhar(dados, nome_tema)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"gerado {os.path.relpath(caminho, RAIZ)} ({len(svg) // 1024} KB)")


if __name__ == "__main__":
    main()
