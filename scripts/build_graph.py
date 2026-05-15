import pandas as pd
import geopandas as gpd

mapa_rj = gpd.read_file('../data/malha_municipios_rj_ibge/RJ_Municipios_2025.shp')
#print(mapa_rj.head())
#print(mapa_rj.info())
#print(mapa_rj['CD_MUN'].head())
#print(mapa_rj['NM_MUN'].head())
mapa_rj['CD_MUN'] = pd.to_numeric(mapa_rj['CD_MUN'])

municipios_base = []

#converter para um sistema de metros ao invés de graus -> cálculo de distância ser em km
mapa_rj = mapa_rj.to_crs(epsg=31983)

for id, cidade in mapa_rj.iterrows():
    neighbors = mapa_rj[mapa_rj.geometry.touches(cidade.geometry)]

    neighbors_list = []
    for id, neighbor in neighbors.iterrows():
        dist = cidade.geometry.centroid.distance(neighbor.geometry.centroid)/1000
        neighbors_list.append(f"{neighbor['NM_MUN']}:{round(dist, 2)}")

    municipios_base.append({
        "id": id,
        "name": cidade['NM_MUN'],
        "neighbors": ",".join(neighbors_list)
    })

pd.DataFrame(municipios_base).to_csv('../data/municipios_final.csv', index=False)