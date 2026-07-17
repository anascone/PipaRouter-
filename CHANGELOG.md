# Histórico de mudanças

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [0.0.1] — 2025-07 — primeira versão pública (experimental)

Ponto de partida do repositório. O que existe hoje:

- Solver de roteirização: frota heterogênea, múltiplas viagens por caminhão,
  entrega parcial, janela de jornada, prioridade por localidade
- Roteamento pela malha viária com velocidade por tipo de via
- Download automático de estradas do OpenStreetMap (Overpass), com cache
  para uso offline
- Roteamento opcional por servidor OSRM (local ou público), com instruções
  de navegação em português
- Exportação KMZ, KML, CSV e XLSX
- Salvar/abrir operação

**Ainda não validado em campo.** Ver o aviso no README.

---

## Histórico de desenvolvimento

O que segue são as iterações internas até chegar na 0.0.1 — mantidas porque
documentam decisões e bugs que valem a pena não repetir. A numeração é do
desenvolvimento, não de versões publicadas.

### [dev 2.8.1]

#### Corrigido
- **Plugin não abria** (`AttributeError` no construtor). O Passo 4 era montado
  antes do bloco avançado, e lia `cb_via` antes de existir. Regressão
  introduzida na 2.8.0.
- Erro na abertura agora mostra arquivo, linha e traceback, em vez do genérico
  "Erro Python: consulte o registro".

### [dev 2.8.0]

#### Corrigido
- **Seleção de área no mapa não funcionava.** `FerramentaRetangulo` usava
  `pyqtSignal`, mas `QgsMapTool` é classe C++ — sinais declarados em
  subclasses Python dela não disparam de forma confiável. Reescrita com
  callback direto.
- Removido aviso falso "Ponto sem nome está fora da área": disparava sempre
  que o cache tinha qualquer região, mesmo de outro município, e rodava antes
  de o ponto ser nomeado.

#### Mudado
- Estradas promovidas de "Ajustes avançados" para **Passo 4** do fluxo
  principal. Sem estradas o plugin não faz nada útil — não é ajuste fino.
- Passo 4 mostra estado permanente: vermelho sem estradas, verde com a
  contagem de trechos.
- Botão de desenho fica laranja quando ativo; tamanho em km aparece na barra
  de status durante o arrasto.

### [dev 2.7.0]

#### Mudado
- Aviso de cobertura virou ação: botão **"Baixar a área que falta"** resolve
  na hora, em vez de mandar procurar botão.

#### Corrigido
- Após baixar pelo aviso, o cálculo seguia usando a camada antiga.
- Removidas 3 referências a botão renomeado na 2.6.

### [dev 2.6.0]

#### Adicionado
- **Desenhar a área no mapa** arrastando o mouse.
- Retry adaptativo: quadrícula que retorna 504 é subdividida em 4 e retentada.

#### Mudado
- Menu dropdown → botões visíveis.
- Quadrícula de 2.000 km² → 8.100 km² (90×90 km). Piauí: 137 min → 90 min.
- Estimativa de tempo passou a usar custo real (12 s + área/130) em vez de
  25 s fixos por consulta.

### [dev 2.5.0]

#### Adicionado
- Download de área grande em quadrículas, retomável: cada pedaço é gravado ao
  chegar; queda de rede não perde o que já veio.
- Costura de ~300 m entre quadrículas, para não cortar estrada na divisa.
- Download por estado (com aviso: a bbox do Piauí tem 562.000 km² contra
  251.500 do estado — 55% seria de estados vizinhos).

### [dev 2.4.0]

#### Corrigido
- **Falso positivo na checagem de cobertura.** Usava `extent()` da camada — a
  caixa das linhas, não da área baixada. Uma base 300 m ao norte da estrada
  mais setentrional era acusada de estar fora. Agora mede distância real
  (limite: 3 km).

#### Adicionado
- Salvar/abrir operação (base, frota, locais, prioridades, quem está fora).
- Cache reusa área maior já baixada, em vez de exigir bbox idêntica.

### [dev 2.3.0]

#### Adicionado
- **Download automático de estradas** via API Overpass, sem QuickOSM.
  Margem de 5 km em volta dos pontos (a estrada entre dois pontos costuma sair
  da caixa que os contém).
- Cache em GeoPackage no perfil do QGIS: segunda vez lê do disco, offline.
- 3 espelhos Overpass com fallback.

#### Nota
Não é possível embutir as estradas no plugin: Piauí = ~80 MB de PBF (~300 MB
processado), Nordeste = ~450 MB. O repositório QGIS limita o pacote a ~25 MB.

### [dev 2.2.0]

#### Adicionado
- **Instruções de navegação** ("Vire à direita na Rod. Cap. Pedro Teixeira
  (PE-316), siga 10,6 km"), traduzidas do OSRM para português.
- Roteiro no KMZ (motorista lê no celular) e em aba da planilha.
- Fusão de segmentos consecutivos da mesma via: uma linha "siga 10,6 km" em
  vez de três "continue na PE-316".

#### Corrigido
- Planilha crashava ao salvar (`StyleProxy` atribuído a `cell.fill`).
- Roteiro no KMZ saía numa linha só (`<pre>` não preserva `\n` vindo de CDATA).

### [dev 2.1.0]

#### Mudado
- Servidor OSRM público passou a ser o padrão (o local exige instalar Docker —
  ninguém tem no primeiro uso).
- Mensagens de erro em português, sem stack trace: `HTTPConnectionPool(...):
  Max retries exceeded` → "o servidor não respondeu".
- Fallback automático: se o local não responde, testa o público e oferece.
- Tratamento específico para 403, 429, 502/503/504.
- User-Agent identificado (política de uso da OSM pede).

### [dev 2.0.0]

#### Adicionado
- **Roteamento por servidor OSRM** — o mesmo motor de um GPS. Local
  (offline, sem limite) ou público.
- `/table` traz a matriz N×N numa requisição; geometrias sob demanda com cache.
- Codec de polyline validado contra a especificação oficial.
- Três modos: servidor OSRM, camada QGIS, estimativa.

#### Nota sobre licença
OSRM usa OpenStreetMap (ODbL): exportação para KMZ/planilha/camada é
permitida. Os Termos do Google Maps proíbem usar rotas fora de um mapa Google.

### [dev 1.5.0]

#### Corrigido
- **Rotas saíam retas.** `QgsGraphBuilder` descarta a ligação entre aresta e
  feição; a geometria era reconstruída por proximidade espacial, o que
  falhava. Reescrito com grafo próprio: cada aresta guarda sua polilinha.
- Efeito colateral: o grafo virou Python puro, testável fora do QGIS.

#### Adicionado
- Botão "Testar a camada de estradas": diagnóstico completo em português
  (rede partida, tipos de via, distância dos pontos até a estrada).

### [dev 1.2.0]

#### Adicionado
- Tempo por classe de via (asfalto, vicinal, carroçável). Velocidade média
  única dava erro de até 76%.

### [dev 1.1.0]

#### Mudado
- Diálogo de 5 abas → painel lateral com passos numerados e marcação por
  clique no mapa.
- Relato honesto de atendimento: separa "recebe tudo" / "recebe parte" /
  "não recebe", em vez de inflar a contagem de pessoas atendidas.

### [dev 1.0.0]

Versão inicial: solver CVRP com múltiplas viagens, frota heterogênea,
entrega parcial e janela de jornada.
