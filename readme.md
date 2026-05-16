# Rotas do Rio

Aplicação interativa para cálculo e visualização de rotas entre municípios do estado do Rio de Janeiro utilizando algoritmos clássicos de busca em grafos e dados geoespaciais reais do IBGE.

## Demonstração
![Demonstração](demo_rotas_rio.gif)

---

## Funcionalidades

- Busca por menor número de municípios utilizando Breadth-First Search (BFS)
- Busca por menor distância utilizando Custo Uniforme (Dijkstra)
- Busca otimizada com heurística utilizando A*
- Comparação de métricas entre algoritmos
- Visualização interativa das rotas em mapa
- Interface web com Streamlit
- Dados geoespaciais reais do IBGE

---

## Algoritmos Implementados

### Busca em Largura (BFS)

Utilizada para encontrar o caminho com menor número de municípios percorridos.

### Busca de Custo Uniforme (Dijkstra)

Utilizada para encontrar o caminho com menor distância total em quilômetros.

### Algoritmo A*

Implementação otimizada utilizando heurística baseada na distância geográfica entre centroides municipais através da fórmula de Haversine.

---

## Comparação de Métricas

A aplicação compara:

- Distância total da rota
- Quantidade de municípios percorridos
- Nós explorados
- Tempo de execução

Exemplo:

```txt
Busca em Largura (BFS)
8 municípios | 145.3km | 31 nós explorados

Custo Uniforme (Dijkstra)
6 municípios | 102.8km | 14 nós explorados

Algoritmo A*
6 municípios | 102.8km | 7 nós explorados
```

---

## Tecnologias Utilizadas

- Python
- Streamlit
- Folium
- GeoPandas
- Shapely
- Pandas

---

## Fonte dos Dados

Os dados municipais foram obtidos a partir da malha municipal oficial do IBGE referente ao estado do Rio de Janeiro.

A adjacência entre municípios foi construída automaticamente utilizando geoprocessamento com GeoPandas e Shapely.

---

## Estrutura do Projeto

```txt
rotas_do_rio/
│
├── data/
│   ├── municipios_final.csv
│   ├── coordinates.json
│   └── malha_municipios_rj_ibge/
│
├── scripts/
│   ├── build_graph.py
│   └── build_coordinates.py
│
├── src/
│   ├── app.py
│   ├── graph_search.py
│   ├── heuristic.py
│   ├── load_data.py
│   └── structs.py
│
├── tests/
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---
## Arquitetura

```txt
Malha municipal do IBGE
        ↓
Processamento geoespacial com GeoPandas
        ↓
Construção do grafo de municípios
        ↓
Algoritmos de busca (BFS, UCS e A*)
        ↓
Visualização interativa com Streamlit e Folium
```
---

## Como Executar

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd rotas_do_rio
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Executar aplicação

```bash
streamlit run src/app.py
```

---

## Visualização em Mapa

A aplicação utiliza Folium para exibir:

- origem e destino
- municípios intermediários
- rota calculada
- representação geográfica do caminho

---

## Melhorias Futuras

- Otimização da fila de prioridade com heapq
- Visualização animada da busca
- Deploy em nuvem
- Comparação visual entre algoritmos

---