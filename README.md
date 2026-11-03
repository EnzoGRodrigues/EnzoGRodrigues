<!--
  README do perfil de Enzo Rodrigues, no estilo do macOS.
  As imagens de assets/ saem dos scripts de scripts/:
    perfil.py        desenha a área de trabalho do topo e os botões (rode depois de mudar os textos)
    plataformas.py   desenha o diagrama "um código, três plataformas"
    contribuicoes.py busca as contribuições pela API do GitHub
    grafico.py       desenha o gráfico de contribuições
  O gráfico é atualizado todo dia pelo workflow .github/workflows/atualizar-grafico.yml.
  A área de trabalho e o gráfico têm versão clara e escura; o <picture> escolhe conforme o tema
  de quem visita. O diagrama é azul nos dois temas.
-->
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/desktop-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/desktop-light.svg" />
  <img src="./assets/desktop-light.svg" width="860" alt="Área de trabalho no estilo macOS: janela Sobre o Enzo com um MacBook, cargo e stack; Terminal com fastfetch e sobre.md; e um Dock com as tecnologias que eu uso" />
</picture>

## Enzo Rodrigues

**Desenvolvedor Full-stack & Mobile na GN Solutions · iOS, React Native, TypeScript, Python**

Apps para iPhone, Android e web, do banco de dados até a App Store, com agentes de IA no fluxo de trabalho.

<a href="https://www.linkedin.com/in/enzo-rodrigues/"><img src="./assets/botoes/linkedin.svg" alt="LinkedIn" /></a>
<a href="mailto:enzorodrigues272@gmail.com"><img src="./assets/botoes/email.svg" alt="E-mail" /></a>
<a href="https://www.instagram.com/_enzooyy_/"><img src="./assets/botoes/instagram.svg" alt="Instagram" /></a>

<br /><br />

<img src="./assets/plataformas.svg" width="860" alt="Diagrama: um card de código se ramifica para três aparelhos: um iPhone (iOS, App Store), um MacBook que abre a tampa e mostra um app web, e um celular Android (Google Play)" />

</div>

## Sobre mim

Sou desenvolvedor Full-stack & Mobile na [GN Solutions](https://gnsolutions.com.br), empresa de tecnologia e IA, e curso Análise e Desenvolvimento de Sistemas no IFSP. Trabalho de ponta a ponta: modelo o banco, escrevo a API, construo o app e cuido do caminho até a produção, seja uma VPS ou a App Store.

Na GN, trabalho nos produtos da casa: o MoneyFin AI, app de finanças pessoais publicado na App Store; o Clerum, plataforma de gestão para igrejas; e o UpKeeper, sistema de manutenção e ativos em produção para vários clientes. Também cuido das ferramentas que mantêm os projetos saudáveis: design system, quality gate no CI, monitoramento da infraestrutura e o padrão de commits e releases do time.

Uso IA como ferramenta de engenharia, não só como autocomplete. Crio meus próprios agentes, skills e mods para o Claude Code (revisão de PR, auditoria de segurança, testes, deploy iOS) e estou construindo uma IDE nativa para macOS que coloca vários agentes de código para trabalhar em paralelo.

## O que eu faço

- Apps para iOS e Android com React Native e Expo: login com Apple e Google, assinaturas in-app, updates OTA e publicação pela EAS.
- Plataformas web com React e Node.js ou Python/Flask, PostgreSQL, pagamentos com Stripe e recursos de IA.
- Deploy por tag, CI no GitHub Actions e infraestrutura própria com Docker, Traefik e VPS, monitorada com Grafana, Prometheus e Loki.
- Ferramentas para o time: design system, quality gate com ratchet de métricas, releases automáticas e agentes de IA no fluxo de PR.

**Domino:** TypeScript, React, React Native, Expo, Node.js, Python, Flask, PostgreSQL, Drizzle, SQLAlchemy, Swift, SwiftUI, Docker e GitHub Actions.

**Stacks que uso nos projetos:** Expo Router, TanStack Query, Tailwind, shadcn/ui, Express, Next.js, Vite, Stripe, API da OpenAI, Resend, Open Finance (Pluggy), Sentry, EAS, Traefik, Grafana, Prometheus e Loki.

**IAs que uso no dia a dia:** Claude Code e Codex.

## Projetos em destaque

- **[MoneyFin AI](https://moneyfin.ai)** · Controle financeiro pessoal com IA: contas, cartões, orçamentos, metas, assistente e sincronização bancária via Open Finance. Versão web e app na [App Store](https://apps.apple.com/br/app/moneyfin-ai/id6761278897). Sou o principal desenvolvedor do app e do web. <sub>Stack: React, Node.js, Express, PostgreSQL, Drizzle, Stripe, API da OpenAI · app em Expo e React Native, com compras in-app e OTA</sub>
- **[Clerum](https://clerum.ai)** · Plataforma de gestão para igrejas: membros, finanças, escalas, eventos e comunicação com a comunidade. Deploy por tag, com mais de 120 releases. O app do tesoureiro, em Expo, está em desenvolvimento. <sub>Stack: TypeScript, React, Express, PostgreSQL, Drizzle, Stripe, API da OpenAI, Docker, Traefik</sub>
- **[upkeeper](https://upkeeper.com.br)** · Gestão de manutenção, patrimônio e ordens de serviço, multi-tenant e em produção: abertura de OS por QR code, relatórios em PDF, leitura de checklist por foto e interface em português e espanhol. Hoje também desenho a próxima versão, em TypeScript. <sub>Stack: Python, Flask, SQLAlchemy, Alembic, PostgreSQL, Docker, Traefik</sub>
- **TTES** · Projeto pessoal: IDE nativa para macOS que roda agentes de código (Claude Code e Codex) em paralelo, um git worktree por tarefa. Os terminais dos agentes continuam vivos mesmo com o app fechado. <sub>Stack: Swift 6, SwiftUI, AppKit, SwiftTerm, GRDB</sub>
- **GN Quality Gate** · Ratchet de métricas no CI: nenhum PR pode piorar erros de lint e de tipos, duplicação ou tamanho de arquivo, e a cobertura só sobe. Roda como GitHub Action e como plugin do Claude Code nos projetos da GN. <sub>Stack: Node.js, GitHub Actions, ESLint, tsc, Vitest, jscpd, osv-scanner</sub>
- **Ferramentas do time** · Design system com tokens e componentes compartilhados entre os produtos, plugin de commits semânticos com releases automáticas e monitoramento da infraestrutura como código. <sub>Stack: React, Tailwind, tsup, Docker Compose, Grafana, Prometheus, Loki</sub>
- **Sites e sistemas sob demanda** · Sites institucionais e ferramentas internas para empresas. <sub>Stack: Next.js, React, Vite, Tailwind, shadcn/ui, Sanity, PostgreSQL</sub>

## Contato

<a href="https://www.linkedin.com/in/enzo-rodrigues/">LinkedIn</a> · <a href="mailto:enzorodrigues272@gmail.com">enzorodrigues272@gmail.com</a> · <a href="https://www.instagram.com/_enzooyy_/">Instagram @&#95;enzooyy&#95;</a> · <a href="https://gnsolutions.com.br">GN Solutions</a>

<div align="center">

<!-- gráfico de contribuições, atualizado pelo workflow diário -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/contrib-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/contrib-light.svg" />
  <img src="./assets/contrib-light.svg" width="860" alt="Gráfico de contribuições no GitHub desde 2022, com o mesmo dia de todos os anos somado, e o resumo: total, sequência atual, maior sequência e melhor dia" />
</picture>

</div>

<p align="center"><i>Se quiser conversar sobre apps, IA ou engenharia de software, é só me chamar.</i></p>
