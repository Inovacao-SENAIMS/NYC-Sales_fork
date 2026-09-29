# NYC Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tirar o dashboard Dash do estado quebrado/atual vazio e transformá-lo em um app funcional de análise de vendas NYC com mapa, histograma, filtros e KPIs.

**Architecture:** Centralizar carregamento e limpeza de dados em `data_loader.py`, montar layout em `index.py` compondo 3 componentes puros (`controllers`, `map`, `histogram`), e ligar tudo com callbacks filtrando um DataFrame em memória (29k linhas cabem em memória).

**Tech Stack:** Python 3.13.15, Dash 4.4.1, dash-bootstrap-components 2.0.4 (tema SLATE), pandas 3.0.6, plotly 7.1.0

**Spec:** Diagnóstico verificado em 2026-09-29 (import de `index.py` falha com `ValueError: time data "2017-07-19" doesn't match format "%m/%d/%Y"`; `app.run_server` inexistente no Dash 4.4.1; layout vazio; 3 componentes com 0 linhas) + dataset local `data/cleaned_data.csv` (29329 x 23, colunas BOROUGH … LATITUDE/LONGITUDE). Este plano é o roadmap — não há spec separado.

## Global Constraints

- Python do projeto: `.venv/bin/python` (3.13.15) — sempre usar esse binário, nunca `python` global.
- Dash 4.4.1 usa `app.run(debug=True, port=8050)` — `app.run_server` NÃO existe.
- `data/cleaned_data.csv` já está em ISO (`2017-07-19`) — nunca parsear com `format='%m/%d/%Y'`.
- Working dir tem espaço: `/Users/danillosantanadearaujo/Documents/Python Scripts/NYC Sales` — citar paths com aspas no shell.
- `data/*.csv` hoje ignorado por `.gitignore` (`/data`) — decidir tracking antes de PR.
- Commits pequenos, um por task/step final, mensagem `feat:` / `fix:` / `chore:`.
- Não commitar `.venv/`, `__pycache__/`, `.DS_Store`.

---

## Estrutura de arquivos (como vai ficar)

- Mantém: `app.py` (instância Dash), `index.py` (layout + callbacks), `assets/style.css`, `assets/logo_dark.png`
- Cria: `components/data_loader.py` (único lugar que lê CSV), `tests/test_data_loader.py`, `requirements.txt`, `README.md`
- Preenche: `components/_controllers.py` (filtros), `components/_map.py` (mapa), `components/_histogram.py` (histograma + KPIs)
- Remove do git: `__pycache__/app.cpython-313.pyc`

Cada componente expõe uma função pura que recebe DataFrame/filtros e retorna componente Dash ou Figure — sem ler CSV dentro deles. `index.py` é o único que chama `load_sales_data()` e registra callbacks.

---

### Task 1: Fazer o app subir (fix crítico)

**Files:**
- Modify: `index.py:1-22`
- Modify: `app.py:1-7`
- Test: `tests/test_smoke.py`

**Interfaces:**
- Consumes: `data/cleaned_data.csv` com coluna `SALE DATE` em `YYYY-MM-DD`
- Produces: `app.layout` não-vazio; `app.run(debug=True, port=8050)` funcional

- [ ] **Step 1: Escrever teste de smoke que falha hoje**

```python
# tests/test_smoke.py
def test_index_imports_without_error():
    import index
    assert index.app.layout is not None
    children = index.app.layout.children
    assert children is not None and len(children) > 0
```

- [ ] **Step 2: Rodar e confirmar falha**

```bash
".venv/bin/python" -m pytest tests/test_smoke.py -v
```

Expected: FAIL com `ValueError: time data "2017-07-19" doesn't match format "%m/%d/%Y"`.

- [ ] **Step 3: Corrigir `app.py` (remover duplicata e API obsoleta)**

```python
# app.py
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
```

O que mudou: removida a linha duplicada `server = app.server` e removida `app.scripts.config.serve_locally = True` (obsoleta, gera warning).

- [ ] **Step 4: Corrigir `index.py` (data + run + layout mínimo)**

```python
# index.py
from dash import html
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

df_data = pd.read_csv('data/cleaned_data.csv', index_col=0)
df_data['size_m2'] = df_data["GROSS SQUARE FEET"] / 10.764
df_data = df_data[df_data['YEAR BUILT'] > 0].copy()
df_data['SALE DATE'] = pd.to_datetime(df_data['SALE DATE'], format='ISO8601')

app.layout = dbc.Container(
    children=[
        html.H1("NYC Sales Dashboard"),
        html.P(f"{len(df_data)} vendas carregadas."),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
```

O que mudou: `format='%m/%d/%Y'` → `format='ISO8601'`, `.copy()` após filtro (evita SettingWithCopy), `app.run_server` → `app.run`, layout com 2 filhos para o smoke passar.

- [ ] **Step 5: Rodar smoke e confirmar PASS**

```bash
".venv/bin/python" -m pytest tests/test_smoke.py -v
```

Expected: PASS (2 asserts).

- [ ] **Step 6: Subir app 10s e confirmar sem traceback**

```bash
".venv/bin/python" index.py &
sleep 10; curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8050/; kill %1
```

Expected: `200`.

- [ ] **Step 7: Commit**

```bash
git add app.py index.py tests/test_smoke.py
git commit -m "fix: corrige parse de data ISO, app.run e layout minimo"
```

---

### Task 2: Higiene do repo (dependências + git)

**Files:**
- Create: `requirements.txt`
- Modify: `.gitignore:1-6`
- Test: `tests/test_requirements.py` (verifica import das deps)

**Interfaces:**
- Consumes: versões instaladas (`pip freeze` do `.venv`)
- Produces: `requirements.txt` instalável; `data/` rastreado ou documentado; `__pycache__` fora do git

- [ ] **Step 1: Escrever teste de deps**

```python
# tests/test_requirements.py
def test_core_deps_importable():
    import dash
    import dash_bootstrap_components
    import pandas
    import plotly
    assert dash.__version__ == "4.4.1"
```

- [ ] **Step 2: Rodar teste**

```bash
".venv/bin/python" -m pytest tests/test_requirements.py -v
```

Expected: PASS (prova que o `.venv` tem as versões do plano).

- [ ] **Step 3: Gerar `requirements.txt` mínimo e fixo**

```
dash==4.4.1
dash-bootstrap-components==2.0.4
pandas==3.0.6
plotly==7.1.0
```

Gerar conferindo com:

```bash
".venv/bin/pip" freeze | grep -i -E "^(dash|dash-bootstrap-components|pandas|plotly)=="
```

- [ ] **Step 4: Corrigir `.gitignore` e desrastrear pycache**

Antes (atual):

```
.../data
.../test
.venv
.../venv
.DS_Store
```

Depois:

```
.venv/
venv/
__pycache__/
*.pyc
.DS_Store
```

Decisão explícita sobre dados: remover `/data` para versionar os 2 CSVs (5 MB + 13 MB, aceitável no GitHub) OU manter ignorado e documentar no README como obter. Default deste plano: versionar `data/cleaned_data.csv`, manter `data/nyc-rolling-sales.csv` ignorado por ser raw de 13 MB. Para isso, adicionar ao `.gitignore`:

```
data/nyc-rolling-sales.csv
```

E executar:

```bash
git rm --cached __pycache__/app.cpython-313.pyc
git add .gitignore requirements.txt tests/test_requirements.py
git commit -m "chore: requirements fixas, gitignore, remove pycache"
```

- [ ] **Step 5: Validar instalação limpa (opcional, 2 min)**

```bash
".venv/bin/pip" install --dry-run -r requirements.txt
```

Expected: exit 0, sem conflito.

---

### Task 3: Camada de dados centralizada (oportunidade: qualidade + performance)

**Files:**
- Create: `components/data_loader.py`
- Create: `tests/test_data_loader.py`
- Modify: `index.py:7-13` (passa a usar o loader)

**Interfaces:**
- Consumes: `data/cleaned_data.csv`
- Produces: `load_sales_data(path: str = "data/cleaned_data.csv") -> pandas.DataFrame` com colunas extras `size_m2: float` e `SALE DATE: datetime64[ns]`, sem `YEAR BUILT == 0`, sem `SettingWithCopyWarning`

- [ ] **Step 1: Escrever teste que falha (sem loader)**

```python
# tests/test_data_loader.py
import pandas as pd

def test_load_sales_data_shape_and_types():
    from components.data_loader import load_sales_data
    df = load_sales_data("data/cleaned_data.csv")
    assert len(df) > 29000
    assert "size_m2" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["SALE DATE"])
    assert (df["YEAR BUILT"] > 0).all()
    assert (df["size_m2"] > 0).all()
```

- [ ] **Step 2: Rodar e ver FAIL**

```bash
".venv/bin/python" -m pytest tests/test_data_loader.py -v
```

Expected: FAIL com `ModuleNotFoundError: components.data_loader`.

- [ ] **Step 3: Implementação mínima**

```python
# components/data_loader.py
import pandas as pd

SQFT_TO_M2 = 10.764

def load_sales_data(path: str = "data/cleaned_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)
    df = df[df["YEAR BUILT"] > 0].copy()
    df["size_m2"] = df["GROSS SQUARE FEET"] / SQFT_TO_M2
    df["SALE DATE"] = pd.to_datetime(df["SALE DATE"], format="ISO8601")
    df = df.dropna(subset=["LATITUDE", "LONGITUDE"])
    return df
```

Nota: `dropna` remove as 11 linhas sem coords encontradas na verificação (evita ponto fantasma no mapa).

- [ ] **Step 4: Rodar e ver PASS**

```bash
".venv/bin/python" -m pytest tests/test_data_loader.py -v
```

Expected: PASS.

- [ ] **Step 5: Refatorar `index.py` para usar o loader**

```python
from components.data_loader import load_sales_data
df_data = load_sales_data("data/cleaned_data.csv")
```

Remover de `index.py` as 4 linhas de manipulação inline (`size_m2`, filtro, `to_datetime`).

- [ ] **Step 6: Commit**

```bash
git add components/data_loader.py tests/test_data_loader.py index.py
git commit -m "feat: centraliza carga de dados com loader testado"
```

**Oportunidades futuras (não implementar agora):** cache com `flask_caching` ou `dcc.Store`; coluna `PRICE_PER_M2`; filtro de outliers (`SALE PRICE` max 2.21B distorce média — winsorizar ou filtrar `>0`); geocodificar os 11 nulos em vez de dropar.

---

### Task 4: Filtros (controllers) — oportunidade de UX

**Files:**
- Modify: `components/_controllers.py:1-0` (hoje vazio)
- Test: `tests/test_controllers.py`

**Interfaces:**
- Consumes: `df: DataFrame` (para extrair opções de BOROUGH e BUILDING CLASS CATEGORY)
- Produces: `build_controllers(df) -> dash_bootstrap_components.Row` com ids fixos: `filter-borough`, `filter-building`, `filter-price`, `filter-year`

- [ ] **Step 1: Teste de ids**

```python
# tests/test_controllers.py
def test_controllers_exposes_expected_ids():
    from components.data_loader import load_sales_data
    from components._controllers import build_controllers
    df = load_sales_data("data/cleaned_data.csv")
    layout = build_controllers(df)
    ids = set()

    def walk(node):
        if hasattr(node, "id") and node.id:
            ids.add(node.id)
        for child in getattr(node, "children", []) or []:
            if isinstance(child, (list, tuple)):
                for c in child:
                    walk(c)
            else:
                walk(child)
    walk(layout)
    assert {"filter-borough", "filter-building", "filter-price", "filter-year"} <= ids
```

- [ ] **Step 2: Rodar, ver FAIL**

```bash
".venv/bin/python" -m pytest tests/test_controllers.py -v
```

Expected: FAIL (`build_controllers` não existe).

- [ ] **Step 3: Implementação**

```python
# components/_controllers.py
from dash import dcc
import dash_bootstrap_components as dbc

def build_controllers(df) -> dbc.Row:
    boroughs = sorted(df["BOROUGH"].dropna().unique().tolist())
    buildings = sorted(df["BUILDING CLASS CATEGORY"].dropna().unique().tolist())
    year_min = int(df["YEAR BUILT"].min())
    year_max = int(df["YEAR BUILT"].max())
    price_max = float(df["SALE PRICE"].quantile(0.99))

    return dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id="filter-borough",
                    options=[{"label": str(b), "value": b} for b in boroughs],
                    multi=True,
                    placeholder="Borough (todos)",
                ),
                md=3,
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="filter-building",
                    options=[{"label": b, "value": b} for b in buildings],
                    multi=True,
                    placeholder="Building class (todas)",
                ),
                md=3,
            ),
            dbc.Col(
                dcc.RangeSlider(
                    id="filter-price",
                    min=0,
                    max=price_max,
                    value=[0, price_max],
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                md=3,
            ),
            dbc.Col(
                dcc.RangeSlider(
                    id="filter-year",
                    min=year_min,
                    max=year_max,
                    value=[year_min, year_max],
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                md=3,
            ),
        ]
    )
```

Usa quantil 99 para `price_max` porque o max absoluto (2.21B) inutilizaria o slider — decisão vinda da verificação (`describe`).

- [ ] **Step 4: Rodar, ver PASS**

```bash
".venv/bin/python" -m pytest tests/test_controllers.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add components/_controllers.py tests/test_controllers.py
git commit -m "feat: adiciona barra de filtros com ids estaveis"
```

---

### Task 5: Mapa — oportunidade de visualização principal

**Files:**
- Modify: `components/_map.py`
- Test: `tests/test_map.py`

**Interfaces:**
- Consumes: `filtered_df: DataFrame` com `LATITUDE`, `LONGITUDE`, `SALE PRICE`, `ADDRESS`
- Produces: `build_map_figure(filtered_df, lat_center: float, lon_center: float) -> plotly.graph_objs.Figure` usando `scatter_mapbox`, amostra max 5000 pontos

- [ ] **Step 1: Teste**

```python
# tests/test_map.py
def test_map_figure_has_data():
    from components.data_loader import load_sales_data
    from components._map import build_map_figure
    df = load_sales_data("data/cleaned_data.csv").head(500)
    fig = build_map_figure(df, df["LATITUDE"].mean(), df["LONGITUDE"].mean())
    assert len(fig.data) == 1
    assert len(fig.data[0].lat) == 500
```

- [ ] **Step 2: Rodar, ver FAIL**

```bash
".venv/bin/python" -m pytest tests/test_map.py -v
```

- [ ] **Step 3: Implementação**

```python
# components/_map.py
import plotly.express as px

MAX_POINTS = 5000

def build_map_figure(df, lat_center: float, lon_center: float):
    sample = df.head(MAX_POINTS) if len(df) > MAX_POINTS else df
    fig = px.scatter_mapbox(
        sample,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="SALE PRICE",
        hover_name="ADDRESS",
        hover_data=["NEIGHBORHOOD", "SALE PRICE", "SALE DATE"],
        zoom=10,
        center={"lat": lat_center, "lon": lon_center},
        height=600,
    )
    fig.update_layout(mapbox_style="carto-darkmatter", margin={"l": 0, "r": 0, "t": 0, "b": 0})
    return fig
```

`carto-darkmatter` combina com tema SLATE. `MAX_POINTS` evita travar o browser com 29k markers.

- [ ] **Step 4: Rodar, ver PASS**

```bash
".venv/bin/python" -m pytest tests/test_map.py -v
```

- [ ] **Step 5: Commit**

```bash
git add components/_map.py tests/test_map.py
git commit -m "feat: adiciona figura de mapa com amostragem"
```

**Oportunidade futura:** cluster por `H3`/`geohash` ou `density_mapbox`; cor por `PRICE_PER_M2` em vez de preço absoluto.

---

### Task 6: Histograma + KPIs — oportunidade analítica

**Files:**
- Modify: `components/_histogram.py`
- Test: `tests/test_histogram.py`

**Interfaces:**
- Consumes: `filtered_df: DataFrame`
- Produces: `build_histogram_figure(filtered_df) -> Figure` (distribuição de `SALE PRICE`, log) + `build_kpi_cards(filtered_df) -> dbc.Row` com ids `kpi-count`, `kpi-median`, `kpi-ppm2`

- [ ] **Step 1: Teste**

```python
# tests/test_histogram.py
def test_histogram_and_kpis():
    from components.data_loader import load_sales_data
    from components._histogram import build_histogram_figure, build_kpi_cards
    df = load_sales_data("data/cleaned_data.csv").head(1000)
    fig = build_histogram_figure(df)
    assert len(fig.data) == 1
    cards = build_kpi_cards(df)
    assert cards is not None
```

- [ ] **Step 2: Rodar, ver FAIL**

```bash
".venv/bin/python" -m pytest tests/test_histogram.py -v
```

- [ ] **Step 3: Implementação**

```python
# components/_histogram.py
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

def build_histogram_figure(df):
    fig = px.histogram(df, x="SALE PRICE", nbins=50, log_y=True, height=300)
    fig.update_layout(margin={"l": 10, "r": 10, "t": 10, "b": 10}, paper_bgcolor="rgba(0,0,0,0)")
    return fig

def build_kpi_cards(df):
    count = len(df)
    median = df["SALE PRICE"].median() if count else 0
    ppm2 = (df["SALE PRICE"] / df["size_m2"]).median() if count else 0
    return dbc.Row(
        [
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Vendas"), html.H3(f"{count:,}", id="kpi-count")])), md=4),
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Mediana"), html.H3(f"${median:,.0f}", id="kpi-median")])), md=4),
            dbc.Col(dbc.Card(dbc.CardBody([html.H6("$/m² mediana"), html.H3(f"${ppm2:,.0f}", id="kpi-ppm2")])), md=4),
        ]
    )
```

Log-Y porque a cauda (max 2.21B vs mediana 620k) achata o histograma linear.

- [ ] **Step 4: Rodar, ver PASS**

```bash
".venv/bin/python" -m pytest tests/test_histogram.py -v
```

- [ ] **Step 5: Commit**

```bash
git add components/_histogram.py tests/test_histogram.py
git commit -m "feat: adiciona histograma log e KPIs"
```

**Oportunidade futura:** série temporal mensal de mediana por borough; boxplot por building class.

---

### Task 7: Montar layout + callbacks (integração)

**Files:**
- Modify: `index.py`
- Test: manual via `curl` + teste de filtro

**Interfaces:**
- Consumes: `build_controllers`, `build_map_figure`, `build_histogram_figure`, `build_kpi_cards`, `load_sales_data`
- Produces: `app.layout` = header + controllers + kpis + mapa + histograma; callback `update_dashboard(filter-borough, filter-building, filter-price, filter-year) -> (map figure, hist figure, kpis)`

- [ ] **Step 1: Reescrever `index.py` completo**

```python
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from components.data_loader import load_sales_data
from components._controllers import build_controllers
from components._map import build_map_figure
from components._histogram import build_histogram_figure, build_kpi_cards

df_data = load_sales_data("data/cleaned_data.csv")
mean_lat = df_data["LATITUDE"].mean()
mean_lon = df_data["LONGITUDE"].mean()

app.layout = dbc.Container(
    children=[
        html.H1("NYC Sales Dashboard"),
        build_controllers(df_data),
        html.Div(id="kpi-row"),
        dcc.Graph(id="map-graph"),
        dcc.Graph(id="hist-graph"),
    ],
    fluid=True,
)

@app.callback(
    [Output("map-graph", "figure"), Output("hist-graph", "figure"), Output("kpi-row", "children")],
    [Input("filter-borough", "value"), Input("filter-building", "value"),
     Input("filter-price", "value"), Input("filter-year", "value")],
)
def update_dashboard(boroughs, buildings, price_range, year_range):
    dff = df_data
    if boroughs:
        dff = dff[dff["BOROUGH"].isin(boroughs)]
    if buildings:
        dff = dff[dff["BUILDING CLASS CATEGORY"].isin(buildings)]
    if price_range:
        dff = dff[(dff["SALE PRICE"] >= price_range[0]) & (dff["SALE PRICE"] <= price_range[1])]
    if year_range:
        dff = dff[(dff["YEAR BUILT"] >= year_range[0]) & (dff["YEAR BUILT"] <= year_range[1])]
    return (
        build_map_figure(dff, mean_lat, mean_lon),
        build_histogram_figure(dff),
        build_kpi_cards(dff),
    )

if __name__ == "__main__":
    app.run(debug=True, port=8050)
```

- [ ] **Step 2: Rodar suite completa**

```bash
".venv/bin/python" -m pytest tests/ -v
```

Expected: 6 arquivos PASS, 0 FAIL.

- [ ] **Step 3: Subir e checar 200**

```bash
".venv/bin/python" index.py &
sleep 10; curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8050/; kill %1
```

Expected: `200`.

- [ ] **Step 4: Commit**

```bash
git add index.py
git commit -m "feat: integra layout com callbacks e filtros"
```

---

### Task 8: README + verificação final

**Files:**
- Create: `README.md`
- Test: `pytest tests/ -v` + `curl` 200

- [ ] **Step 1: Criar `README.md` mínimo**

```markdown
# NYC Sales Dashboard

Dashboard Dash das vendas de imóveis NYC (29k vendas, `data/cleaned_data.csv`).

## Rodar

".venv/bin/python" -m pip install -r requirements.txt
".venv/bin/python" index.py
# abrir http://127.0.0.1:8050/

## Testes

".venv/bin/python" -m pytest tests/ -v
```

- [ ] **Step 2: Verificação final (evidência antes de declarar pronto)**

```bash
".venv/bin/python" -m pytest tests/ -v
".venv/bin/python" -m py_compile app.py index.py components/*.py
```

Expected: 0 failures, COMPILE OK. Só então declarar "pronto".

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: adiciona README de run e testes"
```

---

## Oportunidades pós-MVP (backlog priorizado)

1. **Outliers:** `SALE PRICE` tem max 2.21B vs p75 950k — adicionar toggle "excluir top 1%" e coluna `PRICE_PER_M2`.
2. **Tempo:** página/tab de série mensal (`SALE DATE` → mediana móvel por borough).
3. **Geo:** trocar scatter por `density_mapbox` + filtro por NEIGHBORHOOD/ZIP.
4. **Performance:** `dcc.Store` + amostragem adaptativa; teste com 29k pontos filtrados mede <1s?
5. **Qualidade:** `pandera`/`great_expectations` no loader; CI `pytest` no GitHub Actions.
6. **Deploy:** `gunicorn index:server`, `Procfile`/`Dockerfile` — `server = app.server` já exposto em `app.py`.

## Self-Review

1. **Spec coverage:** parse ISO (T1), `app.run` (T1), layout vazio (T1+T7), componentes vazios (T4-T6), duplicata `server` (T1), `/data` ignorado (T2), sem requirements (T2), pycache commitado (T2), `describe` outliers (T4+T6+backlog), nulos LAT/LON (T3). Sem gaps.
2. **Placeholder scan:** nenhum `TBD/TODO/implement later`; todos os steps têm código + comando + expected.
3. **Type consistency:** `load_sales_data(path: str) -> DataFrame` usado igual em T3-T6; ids `filter-*`, `map-graph`, `hist-graph`, `kpi-row`, `kpi-count/median/ppm2` consistentes entre T4-T7; `build_map_figure(df, lat, lon)`, `build_histogram_figure(df)`, `build_kpi_cards(df)`, `build_controllers(df)` com assinaturas estáveis.
