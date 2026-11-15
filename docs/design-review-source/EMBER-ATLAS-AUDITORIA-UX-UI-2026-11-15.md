# Ember Atlas — Auditoria UX/UI e plano de repaginação
**Data:** 15/11/2026 · **Objeto:** https://ember-atlas-opal.vercel.app/ · **Código:** https://github.com/dshimo0/ember-atlas

> **Escopo e limite:** este diagnóstico foi baseado no conteúdo HTML público das rotas `/`, `/demo`, `/about`, `/pitch`, na comparação com documentação pública do NASA FIRMS e em leitura do `main` do repositório GitHub. Não foi possível capturar screenshots interativos de todas as páginas num navegador instrumentado, executar filtros ou fazer testes E2E. Portanto, achados de layout/ícones são avaliação informada pela estrutura textual e pelo relato do proprietário, não alegações de pixel-perfect visual QA. O guia PDF de 31 MB especificamente apontado não abriu no leitor web; para regras de marca foi consultada a página oficial `/brand` e a edição oficial do Brand Guide de 23/05/2025. Conferir se houve revisão posterior antes da submissão.

## 1. Diagnóstico executivo

**Veredito:** produto tecnicamente mais cuidadoso do que sua aparência indica; experiência sobrecarregada, proposta de valor enterrada em controles e terminologia. Um jurado deveria responder a três perguntas em 10 segundos: *Por que MODIS e VIIRS não podem ser simplesmente somados? O que o Ember Atlas harmoniza? Onde vejo um resultado verificável?* A interface atual não dá essa hierarquia.

**Risco principal de avaliação:** o desafio é sobre **harmonização de séries históricas e calendário de atividade de queima**, não sobre ter o heatmap mais bonito. Uma estética melhor sem explicar escala de sensores, cobertura e validação vira apenas outro FIRMS com branding.

**Bloqueio técnico de comunicação:** o `main` de `dshimo0/ember-atlas` contém pipeline Python, testes, specs e documentos, mas **não apresenta diretório de frontend, package.json ou aplicação web**. O README ainda diz que o aplicativo público e a calibração estão previstos. Em contrapartida, a página `/about` do deploy descreve o repositório como contendo implementação e evidência de verificação. **É necessário identificar a origem real do deploy, sincronizar o código do app com o repositório público ou corrigir a descrição da proveniência.** Não inferir que o frontend não exista em outra pasta/repo/branch apenas por não estar no `main` verificado.

## 2. Revisão página por página

### `/` — Landing / Explore | P0
**Observado:** topo abre com “Pantanal fire activity, 2020–2024”, status “Loading validation evidence”, demo guiada, filtros geográficos, sensor, intervalo de datas, calendário e mês, mapa, ajuste de opacidade, seletor de camadas, comparação de sensores, séries mensais, validação e documentação na mesma estrutura. O mapa informa que até 4.000 pontos são amostrados para exibição, enquanto a grade usa todas as observações correspondentes. Há explicações corretas, porém densas, sobre *occupied cell-days*.

**Problema:** a tela funciona como instrumento de laboratório, não como entrada pública. Muitas decisões simultâneas, nenhuma focal. Uma pessoa não entende, no primeiro contato, por que comparar dois sensores precisa desse produto.

**Redesenho:** transformar `/` em uma landing de storytelling com:
1. Hero fotográfico editorial da Terra, marca Ember Atlas, descrição de uma frase, botões “Explore the map” e “See a 90-second demo”.
2. Uma figura didática: **o mesmo período, dois sensores, contagens diferentes** (com números reais, fonte e unidade).
3. Explicação **Observe → Align → Validate → Explore** em quatro passos curtos.
4. Preview clicável do calendário mensal (não mockup estático).
5. Resultado de validação somente se verificado, inclusive quando a calibração não atender aos critérios.
6. CTA final “Inspect the evidence”.

**Aceite:** leitor externo explica a hipótese em uma frase em 10 s; a página não mostra placeholders eternos; links levam ao explorer e documentação.

### `/explore` (ou rota efetiva de exploração) — Map UX | P0
**Observado:** combinação de seletor de área, sensor, múltiplos filtros de data, camadas “full-data occupied-day cells” e “sampled detections”, transparência, basemap, comparação, downloads e calendário. O quadro mostra “1 occupied day” num filtro, mas há estados de carregamento no HTML de origem.

**Problema:** o mapa parece subordinado aos formulários, embora seja o foco da análise. Termos como *full-data occupied-day cells* e *sampled detections* são precisos para quem desenvolveu, mas pouco comunicativos para jurados. Não chamar grade discreta de “heatmap” sem explicar a quantidade.

**Nova anatomia desktop:** cabeçalho 64–72px; painel de controles simples 300–340px à esquerda; mapa ocupa o restante com mínimo 65% da viewport; legenda e cobertura visíveis na própria moldura; painel inferior retrátil para calendário e comparação. Dê prioridade ao mapa, não a uma coleção de cards.

**Duas portas para explorar:**
- **Basic:** Região, Mês, Sensor, Tipo de visualização, Legenda, Exportar.
- **Advanced:** UTC, máscara exata, tipos reportados, proveniência, fontes de processamento, filtros técnicos, grade de resolução, ajustes e validação.

**Modos cartográficos distintos:**
- **Observações pontuais:** anomalias térmicas nas coordenadas reais; agrupamento visual em zoom baixo sem transformar clusters em número de incêndios. Marca clara quando pontos são amostrados.
- **Atividade agregada:** células da grade WGS84 0,05°; preencher por dias-célula ocupados, com legenda numérica explícita e máscara da AOI.
- **Densidade suavizada:** modo opcional derivado de observações completas, explicitamente identificado como visualização suavizada; nunca usar amostra de 4.000 pontos como denominador de densidade global.
- **Comparação:** MODIS nativo versus VIIRS nativo e, somente onde a calibração foi aprovada, VIIRS ajustado; suporte espacial/temporal consistente.

**Legenda obrigatória:** título da métrica, unidade, escala estável para a comparação, extremos numéricos e estados distintos: `0 observado`, `sem recuperação`, `mês parcial`, `sem ajuste validado`. Nunca normalizar os dois sensores independentemente e depois permitir comparação visual enganosa. No zoom baixo, agregar por bin/hex ou cluster sem inventar pontos. Conteúdo detalhado aparece por seleção e não permanentemente.

**Basemap:** oferecer NASA Blue Marble/imagery onde licenças e serviços permitirem, mapa escuro de relevo e base de ruas. A imagem de contexto não precisa ser contemporânea das detecções e deve ser rotulada como tal. Renderizar dados mesmo que o serviço de tile falhe, com fallback e mensagem útil.

**Microinterações:** tooltip com indicador, sensor, UTC, plataforma, tipo reportado, nível de processamento, FRP quando houver, link da fonte e botão para exportar a seleção. Alvos de clique ≥44 × 44px em dispositivos touch; ícones 20–24px de uma única biblioteca (Phosphor ou Lucide) com texto quando ambíguos.

**Aceite:** qualquer usuário deve poder escolher Pantanal/Setembro-2024, compreender a legenda, alternar sensores, apontar uma célula e exportar os mesmos filtros sem ler um parágrafo científico.

### `/demo` — Guided demonstration | P0
**Observado:** “A guided exploration · real NASA observations”, setas Previous/Next, Restart e hero MODIS Terra contextual; o restante compartilha praticamente a estrutura textual do explorer.

**Problema:** “demo guiada” não pode ser apenas uma legenda navegando sobre uma tela ainda cheia de campos. Precisa de roteiro curto e fechado, com estado reproduzível.

**Redesenho:** 4 cenas de 15–25 s: (1) o problema de sensores; (2) mesmo mês e região; (3) grade comum e calendário; (4) validação/limitação e exportação. A cada cena, controlar a seleção real por URL/state, destacar uma única interação, permitir Skip/Back e reiniciar sem perder contexto. Adicionar “Open this state in Explore”. Evitar passeios automáticos que dependem de rede externa sem fallback.

**Aceite:** um avaliador desconhecedor do projeto completa a demo em <90 s e identifica o resultado e sua principal limitação.

### `/methods` — Methods & data | P1
**Observado:** etapas Acquire → Verify → Aggregate → Adjust → Evaluate → Compare, escopo 0,05° WGS84 e UTC, testes em holdout 2023–2024, 36 meses de treinamento e 24 de avaliação, limitações sobre cobertura de satélite, versão do produto, FRP, diferenças instrumentais e erro. O leitor web não conseguiu resolver esta rota separadamente, embora o índice da home exponha seu conteúdo; isso **não demonstra** falha no navegador real.

**Problema:** bom material científico apresentado com densidade muito alta e pouca visualização do raciocínio. São importantes, mas deveriam estar à disposição sob demanda.

**Redesenho:** Overview com esquema de quatro etapas; tabs Data Sources / Methods / Validation / Reproduce / Limits; gráfico comparativo do MAE e signed bias em mesma unidade; manifesto e snapshot no topo; tabelas técnicas recolhíveis; código e fontes com copiar URL. Quando ajuste falha, mostre decisão claramente, não só números pequenos.

**Aceite:** do mês exibido até CSV e validation.json rastreáveis, com produto, datas, versão, AOI e interpretação correta. Acessível sem login.

### `/about` — Mission / People | P1
**Observado:** esta é uma das rotas com conteúdo próprio. Hero “Fire history. Measured across sensors.”, fotografia NASA Blue Marble com crédito; atlas com oito cartões de áreas (Pantanal, Southern Amazon, Cerrado, Gran Chaco, California, Southeastern Australia, Iberian Peninsula, Siberia), coordenadas e imagens MODIS, explicação do método e perfil Diego Shimohama. Perfil usa marcador textual “DS”.

**Problema:** a página é uma mistura de índice de regiões, missão científica, proveniência, perfil e créditos. Oito cartões com coordenadas dominam uma narrativa institucional. O `DS` parece avatar provisório. O valor não é somente uma vitrine de oito fotos de 01/09/2024.

**Redesenho:** abrir com missão e uma imagem real grande; seção “What problem are we solving?” em duas colunas; “What we built” em três features; oito regiões num atlas filtrável ou link “Explore study areas”, com **selo por região**: data available / partial / sensor-native only / harmonization validated. Perfil do criador em faixa editorial, com foto autorizada ou composição tipográfica cuidada. Créditos e advertências no final. Não inflar escopo validado do Pantanal para outras áreas.

**Aceite:** About informa o que o projeto é, o que demonstrou, quem é o autor, de onde vieram os dados, o que ainda não é validado.

### `/pitch` — Judges presentation | P0
**Observado:** ao consultar `/pitch`, o extrator recebeu o mesmo HTML-base da página principal. Pode ser renderização client-side; não é prova de página quebrada, mas reforça a necessidade de screenshot E2E autenticado/anônimo. O produto tem texto técnico suficiente, mas não deve despejá-lo em slides.

**Redesenho:** 7 quadros cinematográficos, navegáveis em tela cheia e com botão de PDF quando possível, alinhados ao desafio (e não inventando mercado, investidores ou parceria NASA):
1. **HOOK:** “Did the fire record change, or did the sensor?”
2. **THE GAP:** mudança na resolução/sensibilidade de MODIS x VIIRS, com fonte oficial.
3. **NASA DATA:** período, área Pantanal, produtos e cobertura real.
4. **THE METHOD:** same grid + same UTC day + fit independent holdout.
5. **THE PRODUCT:** mapa interativo + calendário ano/mês, clicável.
6. **THE EVIDENCE:** teste de 2023–2024, resultados reais e decisão de aceite/rejeição.
7. **IMPACT & LIMITS:** quais decisões de investigação são apoiadas, sem afirmar prever ignições ou incêndios evitados; CTA para reproduzir.

Este pitch visual NÃO substitui automaticamente o material obrigatório do portal. Confirmar no guia de submissão de 2026 a mídia/duração permitida. Nunca inserir métricas placeholders como resultados.

**Aceite:** modo teclado, sem scroll involuntário, uma mensagem por quadro, números legíveis à distância e CTA do repositório/relatório.

### Repositório GitHub `dshimo0/ember-atlas` — Credibilidade | P0
**Observado no `main`:** `AGENTS.md`, `README.md`, `docs/`, `scripts/`, `specs/`, `tests/`; pipeline Python e artefatos de planejamento. Não há diretório frontend/arquivo package.json listado na raiz e o README diz que a web app e calibração estão no plano. Não há logo no root do `main` verificado, apesar do relato de um logo colocado no root local. O deploy aponta para uma aplicação mais ampla do que o código publicamente rastreável.

**Correção:** identificar project ID/Root Directory/commit exato no Vercel; executar `git remote -v`, `git status`, `git log -5 --oneline` no workspace que possui o app; preservar histórico; trazer frontend + assets + package lock + dataset manifest verificado para o repositório com provenance e testes. Atualizar README com `Live Demo`, `Challenge`, `Architecture`, `Data Coverage`, `Run Locally`, `Validation`, `Limitations`, `Screenshots`, `Resources`, `Submission`. Não publicar `FIRMS_MAP_KEY` nem requests com chave.

**Aceite:** GitHub público reproduz ou documenta inequivocamente o app publicado, com commit/source root indicado e screenshots reais. Código científico não pode desaparecer numa repaginação.

## 3. Benchmark correto: NASA FIRMS

O FIRMS não é elegante porque tem mais brilho; ele resolve três tarefas de primeira: **ver uma base cartográfica reconhecível**, **identificar deteções marcadas de forma clara** e **controlar rapidamente período/sensor/camadas**. A interface oficial inclui blue marble, streets, topographic, imagens reais e sensor MODIS/VIIRS, modos simple/time based, timeline, capture e share. O mapa identifica explicitamente anomalias térmicas, não incêndios únicos.

**O que Ember Atlas deve copiar como princípio:** mapa grande, entrada simples, legenda evidente, detalhes progressivos, captura/exportação reproduzível. **O que deve fazer que FIRMS não é seu foco central:** comparar períodos históricos a partir de uma métrica harmonizada com método e avaliação transparentes, calendário ano × mês e distinção explícita entre dado ausente e zero. Não alegar que FIRMS não possui histórico ou filtros avançados.

## 4. Design system profissional

**Ember Atlas independente:** navy profundo, azul elétrico como cor analítica, branco de alto contraste, laranja somente para atividade térmica; cinza para indisponibilidade. Tipografia Inter ou equivalente para produto. Ícones Phosphor/Lucide lineares com stroke consistente; legenda de texto onde o pictograma sozinho não comunica. H1 64–80px desktop, título de seção 32–40px, corpo 16–18px, rótulos 13–15px, números alinhados em monoespaçada/tabular. Áreas clicáveis ≥44px, foco visível, contraste mínimo 4.5:1.

**Identidade do evento (se usar logo oficial):** a marca NASA Space Apps deve vir do kit oficial sem distorção ou rearranjo. Paleta oficial: Deep Blue `#07173F`, Electric Blue `#0042A6`, Neon Blue `#0960E1`, Blue Yonder `#2E96F5`, Rocket Red `#E43700`, Martian Red `#8E1100`, Neon Yellow `#EAFE07`, branco `#FFFFFF`. Amarelo neon é ACENTO, não fundo dominante. Fonts oficiais Fira Sans/Overpass; ícones Feather/Phosphor. Foto preferencialmente em moldura circular para posts; não colocar texto por cima de fotografia em material que siga estritamente o guia. O logo NASA Meatball/Worm não equivale ao logo NASA Space Apps e não deve ser usado no produto sem autorização. **Ember Atlas é projeto participante independente**, não “NASA product”. Fonte oficial: https://www.spaceappschallenge.org/brand/ e guia de 23/05/2025.

## 5. Dados oficiais da edição/challenge

**Evento:** NASA International Space Apps Challenge **2026**, **14–15 de novembro de 2026**, tema **The Next Frontier**. **Desafio:** *Harmonization of MODIS and VIIRS Hot Spots* (Earth Science / Software; Advanced/Intermediate). O desafio pede um web app com calendário de atividade de queima baseado em hotspots de fogo ativo, harmonizando MODIS e VIIRS, para examinar padrões, condições incomuns e períodos críticos numa AOI. **Submissão:** página oficial 2026 indica janela até **23:59 de 15/11/2026 no horário local**; verificar regras atuais e confirmação do Team Owner. Fontes: https://www.spaceappschallenge.org/2026/ e https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/.

**Textos sugeridos, verificados pela ideia e sem extrapolar resultado:**
- Claim curto: “The same Earth. Different sensors.”
- Claim de produto: “Making MODIS and VIIRS thermal observations easier to compare across time.”
- Aviso: “Thermal detections are not unique fires or burned area.”
- Rodapé: “An independent NASA Space Apps Challenge 2026 project. Data: NASA FIRMS. Editorial imagery: NASA Blue Marble/GIBS, where applicable.”

## 6. Produção visual / hero LinkedIn

Três artes PNG acompanham esta auditoria, contendo a Terra baseada em mosaico NASA Blue Marble (base raster redistribuída com Basemap; projeção ortográfica estilizada):
- `ember-atlas-hero-1920x1080.png` — header/hero do site.
- `ember-atlas-linkedin-1200x627.png` — imagem horizontal para compartilhamento.
- `ember-atlas-linkedin-1080x1350.png` — publicação vertical para feed.

**Atenção:** são peças editoriais e não visuais de dados de fogo/2024; nenhum hotspot foi criado. O wordmark é tipográfico temporário, pois o logo local aprovado não está no `main` consultado. Ao integrar no site, trocar pelo logo real. Para share cards, gerar também `og:image`, `twitter:image`, `og:title`, `og:description`, nome do projeto e `canonical`, com arte de 1200 × 630 ou proporção compatível. Crédito da imagem no texto alternativo/site.

## 7. Roadmap prático com critérios de aceite

### P0 — antes de divulgar/submeter
- [ ] Confirmar repositório e commit do deploy; link público para fonte completa.
- [ ] Introduzir landing enxuta com hero, CTA para mapa, proposta de valor e calendário.
- [ ] Abrir mapa já com AOI e mês verificáveis, basemap visualmente legível e legenda numérica.
- [ ] Separar explicitamente *point detections*, *occupied cell-days* e *smoothed density*, com unidade correta.
- [ ] Reduzir controles visíveis; filtros avançados em drawer; ícones padronizados, alvos de toque adequados.
- [ ] Publicar uma demo de até 90 s (produto) e um pitch com 7 quadros que reproduzam resultados reais.
- [ ] Corrigir descrições de cobertura/validação nas oito áreas e links do About.
- [ ] Preparar mídia e submissão no formato confirmado pelo portal, conferir status de *Submit for Judging*.

### P1 — depois de estabilizar P0
- [ ] Calendário central ano × mês com cor de escala fixa; missing/zero/parcial distintos.
- [ ] Comparação swipe e detalhes de outliers; histórico de sensores, harmonização e limitações visíveis.
- [ ] Methods com navegação por evidência e gráficos de MAE/bias; exportação concorda com UI.
- [ ] Responsivo mobile, testes com leitor de tela, navegação por teclado e foco.
- [ ] Metadata SEO/social e screenshots reais do app.

### Testes críticos
1. Confrontar número do mapa × tabela × CSV para o mesmo AOI/mês/sensor.
2. Confirmar que ponto exibido como amostra não vira densidade do dataset completo.
3. Confirmar que o ajuste Pantanal não aparece como válido em outra região.
4. Validar zero, missing e parcial em URLs de estado e calendários.
5. Confirmar que `/pitch`, `/methods` e `/about` carregam em sessão anônima com JS, sem erros em console.
6. Verificar fallback de tiles e erro de rede; preservar versão verificada quando FIRMS está indisponível.
7. Corrigir acessibilidade de controles em 390 × 844 e 1440 × 900.
8. Rodar testes do frontend e `python -m unittest discover -s tests`, build, preview, e somente então publicar.

---
## Fontes públicas consultadas
- App: https://ember-atlas-opal.vercel.app/ e https://ember-atlas-opal.vercel.app/about
- Repositório: https://github.com/dshimo0/ember-atlas
- Requisitos originais: https://github.com/dshimo0/ember-atlas/blob/main/specs/001-product.md
- Auditoria interna: https://github.com/dshimo0/ember-atlas/blob/main/docs/Ember-Atlas-Judging-Review.md
- NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/map/ e https://firms2.modaps.eosdis.nasa.gov/map/index.html
- 2026 NASA Space Apps: https://www.spaceappschallenge.org/2026/
- Desafio: https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/
- Marca: https://www.spaceappschallenge.org/brand/
- Guia oficial acessível (edição 2025): https://assets.spaceappschallenge.org/media/documents/Space_Apps_Brand_Guide_-_23_May_2025.pdf
