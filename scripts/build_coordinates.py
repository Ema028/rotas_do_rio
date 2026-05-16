import geopandas as gpd
from pathlib import Path
from src.load_data import normalize_name
from src.graph_search import municipio_id_for_name
import json

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "coordinates.json"
MAPA_PATH = BASE_DIR / "data" / "malha_municipios_rj_ibge" / "RJ_Municipios_2025.shp"

mapa_rj           = gpd.read_file(MAPA_PATH)
mapa_rj           = mapa_rj.to_crs(epsg=4326) #sistema de coordenadas geograficas padrao

coordinates = {}

for index, linha in mapa_rj.iterrows():
    city_id = municipio_id_for_name(normalize_name(linha['NM_MUN']))

    centroid             = linha['geometry'].centroid
    coordinates[city_id] = {"lat": centroid.y, "lon": centroid.x}

with open(DATA_PATH, "w", encoding="utf-8") as f: json.dump(coordinates, f, indent=4, ensure_ascii=False)