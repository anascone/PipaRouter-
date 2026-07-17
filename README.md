# PipaRouter — Levar água até as pessoas

Plugin QGIS para montar a programação dos caminhões-pipa. Você marca no mapa
onde o caminhão enche e onde precisa entregar; o plugin monta a rota, traça o
caminho pela estrada e diz **a que horas o caminhão chega em cada lugar**.

**Funciona sem internet.**

![versão](https://img.shields.io/badge/versão-0.0.1-orange)
![experimental](https://img.shields.io/badge/status-experimental-red)
![QGIS](https://img.shields.io/badge/QGIS-3.22%2B-green)
![licença](https://img.shields.io/badge/licença-GPL--2.0-blue)

> ## ⚠️ Experimental — leia antes de usar
>
> Este plugin **ainda não foi usado numa operação real de campo**. Os
> algoritmos são testados, mas "passa nos testes" e "funciona no semiárido com
> um caminhão de verdade" são coisas diferentes.
>
> **Confira a programação antes de mandar o caminhão.** Trate a saída como
> proposta para o encarregado validar, não como ordem de serviço.
>
> Se você usar e algo não bater com a realidade,
> [abra uma issue](https://github.com/assuncaoneto/pipa-router/issues) — é
> exatamente o retorno que falta.

## Instalar
QGIS → Complementos → Gerenciar e Instalar → Instalar a partir do ZIP.
Clique no ícone do caminhão. O painel abre do lado direito.

---

## Para ter tempo e rota PRECISOS — leia isto

Por padrão o plugin estima: linha reta × 1,3 e uma velocidade média só. Serve
para triagem, **não para dizer a hora ao morador**.

Para tempo real, faça uma vez:

1. **Vetor → QuickOSM → Consulta rápida**
2. Chave `highway`, escolha o município, **Executar**
3. Salve a camada de linhas no projeto (para funcionar offline depois)
4. No PipaRouter: **Ajustes avançados → Camada de estradas** → selecione
5. Os campos `highway` e `surface` são detectados sozinhos

O rótulo em Ajustes avançados diz em que modo você está:

| | Significado |
|---|---|
| 🔴 **Tempo estimado** | Sem estradas. Linha reta, velocidade média. |
| 🟠 **Tempo aproximado** | Segue estradas, mas tudo na mesma velocidade. |
| 🟢 **Tempo pela estrada** | Cada trecho na velocidade do seu tipo de via. |

### Por que isto muda tanto

Percurso de 40 km: 12 km de BR asfaltada + 28 km de carroçável.

```
Média única de 40 km/h .....  60 min
Por tipo de via ............ 105 min
                             ─────────
ERRO ....................... +45 min (+76%)
```

O erro **não é constante** — é −33% no asfalto e +79% na terra. Por isso
nenhuma média global conserta: erra nas duas direções ao mesmo tempo. E
**acumula**: a última entrega da manhã sai 1h deslocada. O morador esperou
desde as 9h e o caminhão chegou às 11h.

## Usar várias vezes

**Salvar esta operação** (botão no topo) guarda base, frota e locais num
arquivo. Da próxima vez, **Abrir operação salva** traz tudo de volta — você só
ajusta os volumes da semana e monta a rota.

Guarda inclusive: prioridade de cada local, quantas pessoas, e quem está fora
da rota.

As estradas baixadas ficam em cache e são **reaproveitadas**: se você marcar
um ponto novo dentro de uma área já baixada, o plugin lê do disco em vez de
baixar de novo.

## Primeiro uso — as estradas

O plugin **não vem com as estradas embutidas**, e não tem como vir: o mapa do
Piauí tem ~80 MB só de arquivo bruto (~300 MB processado); o do Nordeste,
~450 MB. O repositório de plugins do QGIS limita o pacote a ~25 MB.

Em vez disso, **o plugin baixa sozinho** só a área dos seus pontos:

Ajustes avançados → **"⬇ Baixar estradas"** → três opções:

**Passo 4 do painel** (não está mais escondido em Ajustes avançados):

| Botão | Quando usar | Tempo |
|---|---|---|
| **⬇ Ao redor dos meus pontos** | operação de um dia | ~30 s |
| **▭ Desenhar a área no mapa** | uma regional inteira, para a semana | ~6 min (165×144 km) |
| **🗺 Um estado inteiro** (em Ajustes avançados) | raro — veja a ressalva | ~90 min (Piauí) |

**Desenhar a área**: aperte o botão (ele fica laranja: "Arrastando...") e
**segure o botão esquerdo do mouse e arraste** no mapa. O retângulo azul
aparece enquanto você arrasta, e o tamanho em km fica na barra de status.
Ao soltar, o plugin mostra tempo e MB estimados antes de baixar.

O Passo 4 mostra sempre o estado atual: vermelho se não há estradas, verde com
a contagem de trechos quando há.

Para área grande, o plugin quebra em pedaços de ~2.000 km² e emenda. **Se cair
no meio, o que já veio fica guardado** — mandar baixar de novo continua de onde
parou.

> **Sobre "estado inteiro":** um estado não é retângulo. A bbox do Piauí tem
> 562.000 km², mas o estado tem 251.500 — **55% do download seria Maranhão,
> Ceará e Bahia**. Se você opera uma região, desenhar a área traz o que
> interessa em ~6 min em vez de 90.

Não precisa do QuickOSM, nem enquadrar mapa, nem escolher chave. O plugin sabe
onde ficam seus pontos e busca a área certa, com 5 km de margem (a estrada
entre dois pontos costuma sair da caixa que os contém).

**Fica salvo.** Da segunda vez em diante lê do disco — sem internet. É o que
permite baixar no escritório e usar em campo. Para ver o que está guardado ou
liberar espaço: *"Ver estradas já baixadas"*.

Se você apertar MONTAR A ROTA sem ter as estradas, o plugin oferece baixar na
hora em vez de entregar uma linha reta.

> Dados © OpenStreetMap contributors (ODbL). Uso comercial liberado, exige
> atribuição.

## Como calcular a rota — três modos

Em **Ajustes avançados → Como calcular a rota**:

> **Qual usar?** Comece pela **Camada de estradas do QGIS** — é o padrão,
> funciona offline e não exige instalar nada. O servidor de rotas dá um
> traçado melhor, mas precisa de internet ou de instalação.

### 1. Servidor de rotas (melhor traçado — igual a um GPS)

**É este modo que dá as instruções de navegação.** Com ele, o resultado
mostra por onde passar:

```
--- até COHAB Ouricuri (9.0 km, 10 min) ---
  Saia na Rua da Sede, siga 400 m
  Vire à direita na Rod. Cap. Pedro Teixeira (PE-316), siga 7.8 km
  Vire à esquerda na Av. COHAB, siga 800 m
  Chegou — o destino fica à direita
```

Isso vai junto no **KMZ** (o motorista abre no celular e lê antes de sair) e
numa aba **Roteiro** da planilha, para imprimir.

O modo "Camada de estradas do QGIS" traça a rota certa no mapa, mas **não dá
as instruções** — o OSM baixado pelo QuickOSM nem sempre tem nome de rua, e
inventar manobra a partir de geometria daria instrução errada.


Usa o **OSRM**, o mesmo motor de roteamento que roda por trás de muitos apps
de navegação. A rota sai pela estrada, com as curvas, respeitando sentido de
via — porque é literalmente o algoritmo de um GPS.

Duas opções de servidor:

**a) OSM público** — não precisa instalar nada, mas exige internet e tem
limite de uso. Uma programação diária de pipa cabe tranquilo.

**b) No seu computador** — funciona **sem internet**, sem limite. Precisa
instalar uma vez:

```bash
# 1. Instale o Docker
# 2. Baixe o mapa do Nordeste (uma vez):
wget https://download.geofabrik.de/south-america/brazil/nordeste-latest.osm.pbf

# 3. Prepare (demora ~20 min, uma vez só):
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend \
  osrm-extract -p /opt/car.lua /data/nordeste-latest.osm.pbf
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend \
  osrm-partition /data/nordeste-latest.osrm
docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend \
  osrm-customize /data/nordeste-latest.osrm

# 4. Rode o servidor (toda vez que for usar):
docker run -t -i -p 5000:5000 -v "${PWD}:/data" \
  ghcr.io/project-osrm/osrm-backend \
  osrm-routed --algorithm mld /data/nordeste-latest.osrm
```

Depois é só apertar **"Testar conexão com o servidor"** no plugin.

Este modo usa o perfil de carro do OSRM. Um caminhão-pipa carregado é mais
lento — se os horários saírem otimistas, considere o modo camada, onde você
controla a velocidade por tipo de via.

### 2. Camada de estradas do QGIS

Usa o OSM que você baixou com o QuickOSM, roteando com o grafo interno do
plugin. Funciona offline sem instalar nada, e deixa você **ajustar a
velocidade por tipo de via** (carroçável, vicinal, asfalto) — o que o OSRM
não permite.

Tem o botão **"Testar a camada de estradas"**, que roda a verificação
completa e diz onde está o problema se a rota sair reta.

### 3. Estimativa (linha reta)

Linha reta × 1,3. Só para triagem rápida. **A linha no mapa não serve para o
motorista.**

---

## Erro "não consegui falar com o servidor de rotas"

Significa que você está no modo servidor e nada respondeu.

- **`WinError 10061` / "não está no ar"** — você escolheu "No meu computador"
  mas não instalou o OSRM. Troque para **"OSM público"** na lista de
  servidores, ou volte para **"Camada de estradas do QGIS"**.
- **403** — o servidor público recusou. Use a camada do QGIS, ou instale o
  servidor local.
- **429** — limite de uso do servidor público. Espere, ou instale o local.

Em todos os casos a **Camada de estradas do QGIS** funciona sem depender de
ninguém. É por isso que ela é o modo padrão.

## "Não achei estrada perto de X pontos"

O aviso é real: aquele ponto está fora da área de estradas que você baixou —
normalmente porque você baixou antes de marcá-lo.

O plugin oferece **"Baixar a área que falta"** ali mesmo, na caixa de aviso.
Um clique, e ele baixa cobrindo todos os pontos e calcula. Costuma custar
menos de 1 minuto.

Ele também avisa **na hora em que você marca** um ponto fora da área baixada,
para você não descobrir só depois de marcar tudo.

## A rota saiu RETA. E agora?

**Modo servidor:** aperte "Testar conexão". Se não responder, ou o servidor
local não está rodando, ou falta internet.

**Modo camada:** aperte "Testar a camada de estradas". Ele diz em português:
se a camada está vazia, quais tipos de via tem, se seus pontos estão dentro da
área coberta, se a rede está partida em pedaços, e um teste de rota real com
veredito.

Se ainda sair reta, **me mande o texto desse teste**.

### Por que OSRM e não Google Maps

- **Licença**: OSRM usa OpenStreetMap (ODbL) — pode exportar KMZ, planilha e
  camada, uso comercial liberado, exige só atribuição. Os Termos do Google
  Maps proíbem usar as rotas fora de um mapa Google.
- **Offline**: o OSRM roda no seu computador. O Google, não.
- **Custo**: zero. Sem chave de API, sem cobrança por requisição.

### O traçado

Com a camada de estradas, o plugin desenha **o caminho que o caminhão percorre
de verdade** — segue a via, faz as curvas, e liga o acesso da estrada até a
casa. Igual ao traçado de um app de navegação.

Isso aparece em três lugares:

- **no canvas do QGIS**, em linhas coloridas por caminhão, assim que você
  calcula
- **nas camadas** ("Ver no mapa"): `Pipa - Rotas` (linhas) e `Pipa - Paradas`
  (pontos com horário) — dá para estilizar, imprimir, exportar
- **no KMZ** para o celular do motorista

Sem a camada de estradas, o traçado é uma reta cortando a caatinga — o
motorista não tem como seguir aquilo.

---

## Como usar

**1. Onde o caminhão enche** — clique no mapa, na ETA ou no poço.

**2. Quais caminhões você tem** — já vem um. Duplo clique para editar.

**3. Onde precisa entregar** — clique no botão, depois no mapa em cada lugar.
A caixinha pergunta o nome e quanta água. Botão direito para parar.

> Não sabe o volume em m³? Informe **quantas pessoas**. O plugin calcula
> (40 L/pessoa/dia — mínimo para beber, cozinhar, higiene).

**4. Montar a rota** — um botão.

**5. Ajustar** — desmarque a caixinha de um lugar para tirá-lo da rota sem
apagar. Recalcule. Botão direito na lista tem mais opções.

## Cores no mapa

| Antes de calcular | Depois de calcular |
|---|---|
| Azul = normal | **Verde** = vai receber |
| Laranja = urgente | **Vermelho** = não entra na rota |
| Vermelho = crítico | |

---

## Leia o resultado com atenção

O resumo separa três situações que **não são a mesma coisa**:

- **Recebem tudo** — o pedido completo.
- **Recebem só parte** — o caminhão passa, mas a caixa não enche. A família
  fica sem antes do próximo giro.
- **Não recebem nada** — o caminhão não vai.

Dizer só "5 de 6 atendidos" esconderia a diferença entre as duas primeiras.
Quem decide precisa ver.

O detalhamento mostra, perna por perna: minutos de estrada, km, velocidade
efetiva, hora de chegada, quanto tempo fica, hora de saída. E fecha com onde
a jornada foi gasta: estrada / enchendo na base / atendendo / esperando.

Se sobrar gente sem água: mais um caminhão, jornada maior, tirar lugares
menos urgentes, ou marcar os prioritários como Crítico e recalcular.

---

## Como o tempo é contado

```
Em cada casa   = tempo parado (padrão 10 min)
                 + volume ÷ vazão de descarga do caminhão

Na base        = volume carregado ÷ vazão de enchimento

Na estrada     = pela malha viária, velocidade do tipo de via
                 (ou distância ÷ média, se não houver estradas)
```

### Velocidades padrão (pipa carregado)

| Tipo de via | km/h |
|---|---|
| BR / estadual asfaltada | 60 |
| Vicinal principal | 45 |
| Vicinal sem classificação | 35 |
| Rua de povoado | 25 |
| **Carroçável** | **18** |
| Trilha | 12 |

Piso de terra reduz por um fator (padrão 0,6) **quando contradiz o tipo** —
uma BR de terra cai para 36 km/h. Carroçável não é penalizada de novo: os
18 km/h já são a velocidade de uma estrada de terra.

**Estes valores são referência, não medição.** Em *Ajustes avançados → Ver
tabela de velocidades* você corrige. Se você sabe que a carroçável para
determinado povoado não faz 18 km/h com o pipa cheio, mude — o horário de
chegada depende disso.

**Cronometre uma descarga real e confira a vazão.** Se ela estiver errada,
todos os horários saem errados.

---

## Limitações — leia antes de decidir com isto

- A rota é **boa, não a melhor possível**. O problema é matematicamente
  intratável no ótimo. Use como programação-base para o encarregado validar.
- Trechos sem estrada mapeada caem para linha reta corrigida. O plugin avisa
  quantos foram.
- As velocidades por tipo de via são referência. Calibre.
- Não modela transbordo, restrição de peso em ponte, nem estrada intransitável
  na chuva.
- 40 L/pessoa/dia é referência de emergência. Se a comunidade tem outra fonte
  parcial, informe o volume direto em m³.

## Requisitos
QGIS 3.22+. `openpyxl` opcional (sem ele, exporta CSV).

---
Antonio A. Coelho Neto — Águas do Piauí / AEGEA
