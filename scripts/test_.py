import pytest
from utils.graph import *

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "municipios_final.csv"

@pytest.fixture
def check_data_loaded():
    if not municipios or not names: pytest.fail("base não carregada")


def test_distancia_zero_mesmo_municipio():
    id_rio = names.get("rio de janeiro")
    if id_rio:
        path, cost = shortest_path(id_rio, id_rio)
        assert cost == 0
        assert len(path) == 1
        assert path[0][1] == id_rio


ROTAS = [("sao goncalo", "rio de janeiro"),
         ("niteroi", "duque de caxias"),
         ("rio de janeiro", "niteroi"),
         ("duque de caxias", "sao goncalo"),
         ("mage", "itaborai"),
         ("belford roxo", "cabo frio")]

@pytest.mark.parametrize("origem_nome, destino_nome", ROTAS)
def test_estrategia_menor_distancia_menor_que_bfs(origem_nome, destino_nome):
    source = names.get(origem_nome)
    target = names.get(destino_nome)

    path_bfs, cost_bfs = shortest_path(source, target, strategy='min_degrees')
    path    , cost     = shortest_path(source, target, strategy='less_distance')

    assert cost <= cost_bfs, f"Menor distância deu {cost}km e bfs deu {cost_bfs}km"