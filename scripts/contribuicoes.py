#!/usr/bin/env python3
"""
Busca o calendário de contribuições de um usuário do GitHub, ano a ano desde a
criação da conta, pela API GraphQL, e grava data/contributions.json com os dias,
um resumo (total, sequências, melhor dia) e a data de criação da conta.

O calendário é o mesmo que aparece no perfil público. Contribuições em
repositórios privados entram só como contagem, e só se o perfil estiver
configurado para mostrá-las.

Precisa de um token em GITHUB_TOKEN. No Actions é o token padrão do workflow;
na sua máquina:

    GITHUB_TOKEN=$(gh auth token) python3 scripts/contribuicoes.py

Só usa a biblioteca padrão do Python.
"""
import datetime
import json
import os
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
USUARIO = os.environ.get("GRAFICO_USUARIO", "EnzoGRodrigues")
SAIDA = os.environ.get("GRAFICO_DADOS", os.path.join(AQUI, "..", "data", "contributions.json"))
CONSULTA = """
query($login: String!, $de: DateTime!, $ate: DateTime!) {
  user(login: $login) {
    createdAt
    contributionsCollection(from: $de, to: $ate) {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""


def consultar(token, de, ate, tempo_limite=30):
    corpo = json.dumps({"query": CONSULTA,
                        "variables": {"login": USUARIO, "de": de, "ate": ate}}).encode()
    pedido = urllib.request.Request("https://api.github.com/graphql", data=corpo, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": f"perfil-{USUARIO}",
    })
    with urllib.request.urlopen(pedido, timeout=tempo_limite) as resposta:
        dados = json.load(resposta)
    if dados.get("errors"):
        raise RuntimeError(dados["errors"][0].get("message", "erro na API GraphQL"))
    usuario = dados["data"]["user"]
    if not usuario:
        raise RuntimeError(f"usuário {USUARIO} não encontrado")
    dias = [d for semana in usuario["contributionsCollection"]["contributionCalendar"]["weeks"]
            for d in semana["contributionDays"]]
    return usuario["createdAt"][:10], dias


def historico(token):
    agora = datetime.datetime.now(datetime.timezone.utc)
    hoje = agora.date().isoformat()
    criada, _ = consultar(token, f"{agora.year}-01-01T00:00:00Z", agora.strftime("%Y-%m-%dT%H:%M:%SZ"))
    por_data = {}
    for ano in range(int(criada[:4]), agora.year + 1):
        de = f"{max(f'{ano}-01-01', criada)}T00:00:00Z"
        ate = agora.strftime("%Y-%m-%dT%H:%M:%SZ") if ano == agora.year else f"{ano}-12-31T23:59:59Z"
        _, dias = consultar(token, de, ate)
        for d in dias:
            if criada <= d["date"] <= hoje:
                por_data[d["date"]] = {"date": d["date"], "count": d["contributionCount"]}
    dias = [por_data[k] for k in sorted(por_data)]
    if len(dias) < 300:
        raise RuntimeError(f"esperava o histórico desde {criada}, vieram {len(dias)} dias")
    return criada, dias


def resumo(dias):
    total = sum(d["count"] for d in dias)
    maior = seguidos = 0
    for d in dias:
        seguidos = seguidos + 1 if d["count"] else 0
        maior = max(maior, seguidos)
    atual = 0
    # o dia de hoje ainda pode estar vazio sem quebrar a sequência
    cauda = dias[:-1] if dias and not dias[-1]["count"] else dias
    for d in reversed(cauda):
        if not d["count"]:
            break
        atual += 1
    melhor = max(dias, key=lambda d: d["count"])
    return {"total": total, "atual": atual, "maior": maior,
            "melhor": melhor["count"], "melhor_data": melhor["date"],
            "inicio": dias[0]["date"], "fim": dias[-1]["date"]}


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("defina GITHUB_TOKEN (ex.: GITHUB_TOKEN=$(gh auth token))")
    criada, dias = historico(token)
    dados = {"usuario": USUARIO,
             "gerado_em": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "entrada": {"data": criada, "ano": int(criada[:4])},
             "resumo": resumo(dias), "dias": dias}
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    r = dados["resumo"]
    print(f"gerado {os.path.normpath(SAIDA)}: {r['total']} contribuições desde {criada[:4]}, "
          f"sequência atual {r['atual']}, maior {r['maior']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:  # mensagem curta no log do Actions
        print(f"erro ao buscar as contribuições: {erro}", file=sys.stderr)
        sys.exit(1)
