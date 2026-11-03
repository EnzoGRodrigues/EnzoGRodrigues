"""
Cores, fontes e peças comuns dos desenhos do perfil, no estilo do macOS.

Cada desenho sai em duas versões, clara e escura. O README escolhe a certa
com <picture> e prefers-color-scheme, conforme o tema de quem visita.
Só usa a biblioteca padrão do Python.
"""
from html import escape

SANS = ("-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', 'Helvetica Neue', "
        "'Segoe UI', Roboto, Arial, sans-serif")
ARREDONDADA = ("ui-rounded, 'SF Pro Rounded', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
               "'Segoe UI', Roboto, Arial, sans-serif")
MONO = ("'SF Mono', ui-monospace, Menlo, Monaco, 'JetBrains Mono', 'Cascadia Mono', Consolas, "
        "'DejaVu Sans Mono', monospace")

# Cores de sistema da Apple (Human Interface Guidelines), versão clara e escura.
TEMAS = {
    "light": {
        "texto": "#1D1D1F", "secundario": "#6E6E73", "terciario": "#8E8E93",
        "separador": "#D2D2D7", "borda": "#000000", "borda_op": 0.14,
        "janela": "#F6F6F7", "terminal": "#FFFFFF", "barra_titulo": "#ECECEE",
        "botao": "#FFFFFF", "botao_borda": "#000000", "botao_borda_op": 0.14,
        "cartao": "#F5F5F7", "sombra_op": 0.20,
        "menu": "#FFFFFF", "menu_op": 0.42, "dock": "#FFFFFF", "dock_op": 0.34,
        "dock_borda": "#FFFFFF", "dock_borda_op": 0.6,
        "azul": "#007AFF", "indigo": "#5856D6", "roxo": "#AF52DE", "rosa": "#FF2D55",
        "vermelho": "#FF3B30", "laranja": "#FF9500", "amarelo": "#FFCC00", "verde": "#34C759",
        "menta": "#00C7BE", "ciano": "#32ADE6",
        # tons para texto sobre fundo branco (contraste maior)
        "t_azul": "#0066CC", "t_indigo": "#4B48C8", "t_roxo": "#9A3DC9", "t_verde": "#1F8A3A",
        "t_laranja": "#C45500", "t_rosa": "#D70F45",
        "fundo_a": "#E4ECFF", "fundo_b": "#FBE7F3",
        "manchas": [(150, 130, 240, "#8CB4FF", 0.9), (820, 110, 230, "#C3A6FF", 0.85),
                    (720, 580, 270, "#FFB4CF", 0.8), (120, 560, 230, "#9BE7E4", 0.8),
                    (470, 320, 210, "#FFFFFF", 0.55)],
        "grafico": ["#E8EBF2", "#BFD8FF", "#7EB3FF", "#3B8CFF", "#0062D6"],
    },
    "dark": {
        "texto": "#F5F5F7", "secundario": "#A1A1A6", "terciario": "#8E8E93",
        "separador": "#3A3A3C", "borda": "#FFFFFF", "borda_op": 0.13,
        "janela": "#252527", "terminal": "#1C1C1E", "barra_titulo": "#2C2C2E",
        "botao": "#3A3A3C", "botao_borda": "#FFFFFF", "botao_borda_op": 0.10,
        "cartao": "#2C2C2E", "sombra_op": 0.55,
        "menu": "#000000", "menu_op": 0.28, "dock": "#2C2C2E", "dock_op": 0.5,
        "dock_borda": "#FFFFFF", "dock_borda_op": 0.16,
        "azul": "#0A84FF", "indigo": "#5E5CE6", "roxo": "#BF5AF2", "rosa": "#FF375F",
        "vermelho": "#FF453A", "laranja": "#FF9F0A", "amarelo": "#FFD60A", "verde": "#30D158",
        "menta": "#63E6E2", "ciano": "#64D2FF",
        "t_azul": "#409CFF", "t_indigo": "#8E8CFF", "t_roxo": "#D17BF7", "t_verde": "#30D158",
        "t_laranja": "#FFB340", "t_rosa": "#FF6482",
        "fundo_a": "#0A0F1F", "fundo_b": "#170B25",
        "manchas": [(150, 130, 240, "#1E4FD8", 0.75), (820, 110, 230, "#6A2FD0", 0.7),
                    (720, 580, 270, "#A3285E", 0.6), (120, 560, 230, "#0B7F86", 0.6),
                    (470, 320, 210, "#0D1530", 0.6)],
        "grafico": ["#2C2C2E", "#0F3A6E", "#1257A8", "#0A78F0", "#5AAEFF"],
    },
}

# Respeita "reduzir movimento": sem animação, tudo aparece pronto.
CSS_BASE = """
.sans{font-family:%s}
.mono{font-family:%s}
.arred{font-family:%s}
@keyframes aparecer{from{opacity:0}to{opacity:1}}
@keyframes abrir{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:none}}
@keyframes subir{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
@keyframes piscar{50%%{opacity:0}}
.janela{animation:abrir .6s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:50%% 50%%}
.l{animation:aparecer .2s ease-out both}
.dock{animation:subir .7s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:50%% 100%%}
.cursor{animation:piscar 1.1s steps(1) infinite}
@media (prefers-reduced-motion:reduce){.janela,.l,.dock,.cursor{animation:none}}
""" % (SANS, MONO, ARREDONDADA)


def esc(texto):
    return escape(str(texto), quote=True)


def data_br(iso):
    ano, mes, dia = iso[:10].split("-")
    return f"{dia}/{mes}/{ano}"


def milhar(n):
    return f"{n:,}".replace(",", ".")


def sombra(id_, opacidade, dy=14, desvio=18):
    return (f'<filter id="{id_}" x="-25%" y="-25%" width="150%" height="160%">'
            f'<feDropShadow dx="0" dy="{dy}" stdDeviation="{desvio}" flood-color="#000" '
            f'flood-opacity="{opacidade}"/></filter>')


def semaforo(x, y, so_fechar=False, t=None):
    """Os três botões do canto da janela. so_fechar deixa minimizar e zoom apagados."""
    cores = [("#FF5F57", "#E2463F"), ("#FEBC2E", "#E1A116"), ("#28C840", "#1AAB29")]
    partes = []
    for i, (cor, borda) in enumerate(cores):
        if so_fechar and i > 0:
            apagado = "#D1D1D6" if t and t["texto"] == "#1D1D1F" else "#4A4A4E"
            cor, borda = apagado, apagado
        partes.append(f'<circle cx="{x + i * 20}" cy="{y}" r="6" fill="{cor}" '
                      f'stroke="{borda}" stroke-width="0.6"/>')
    return "".join(partes)


def topo_arredondado(x, y, w, h, r):
    """Caminho de um retângulo só com os cantos de cima arredondados (barra de título)."""
    return (f"M{x},{y + h} V{y + r} A{r},{r} 0 0 1 {x + r},{y} H{x + w - r} "
            f"A{r},{r} 0 0 1 {x + w},{y + r} V{y + h} Z")
