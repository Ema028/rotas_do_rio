from graph_search import *
from streamlit_folium import st_folium
import folium

BASE_DIR  = Path(__file__).resolve().parent.parent
COORDINATES_PATH = BASE_DIR / "data" / "coordinates.json"

coordinates = load_coordinates(COORDINATES_PATH)

def limpar_rota_antiga():
    st.session_state.dados_rota = None

if "dados_rota" not in st.session_state:
    st.session_state.dados_rota = None

st.title("Rotas no Rio de Janeiro")
st.write("Insira os dados da sua viagem:")

origem_nome = st.selectbox("Qual o município de partida? ", names, on_change=limpar_rota_antiga)
origem      = municipio_id_for_name(origem_nome)

destino_nome = st.selectbox("Você quer ir pra qual município? ", names, on_change=limpar_rota_antiga)
destino      = municipio_id_for_name(destino_nome)
estrategia   = st.selectbox("Você prefere: ",["Caminho com menos kilômetros", "Caminho com menos municípios de separação", "Busca com todas as estratégias e comparar métricas"])

if st.button("Buscar caminho"):
    comparar = False

    if   estrategia == "Caminho com menos kilômetros"             : estrategia = 'a_star'
    elif estrategia == "Caminho com menos municípios de separação": estrategia = 'min_degrees'
    else:comparar = True; estrategia = 'a_star'

    if origem and destino:
        path, cost, explored = (shortest_path(origem, destino, estrategia))
        if path is None: st.error("Não foi possível encontrar um caminho entre esses municípios.")
        else: st.session_state.dados_rota = {"path"       : path       , "cost"         : cost,
                                             "explored"   : explored   , "comparar_tudo": comparar,
                                             "origem_nome": origem_nome, "destino_nome" : destino_nome}
    else:
        st.error("Município não encontrado")
        st.session_state.dados_rota = None

if st.session_state.dados_rota is not None:
    dados      = st.session_state.dados_rota
    path       = dados["path"]       ; cost        = dados["cost"]
    explored   = dados["explored"]   ; comparar    = dados["comparar_tudo"]
    origem_txt = dados["origem_nome"]; destino_txt = dados["destino_nome"]

    if comparar: print_all(origem, destino)
    else:
        print_path(path, cost, explored)

    #mapa
    pontos_do_mapa = []
    for city in path:
        city_id = city[1]
        if city_id in coordinates:
            lat = coordinates[city_id]["lat"]
            lon = coordinates[city_id]["lon"]
            pontos_do_mapa.append([lat, lon])

    if pontos_do_mapa:
        mapa = folium.Map(location=pontos_do_mapa[0], zoom_start=11)
        folium.Marker(pontos_do_mapa[0],  popup=f"Origem:  {origem_nome.title() }", icon=folium.Icon(color='green')).add_to(mapa)
        folium.Marker(pontos_do_mapa[-1], popup=f"Destino: {destino_nome.title()}", icon=folium.Icon(color='red')  ).add_to(mapa)

        for i in range(1, len(pontos_do_mapa) - 1):
            folium.CircleMarker(pontos_do_mapa[i], radius=5, color='blue', fill=True).add_to(mapa)

        folium.PolyLine(pontos_do_mapa, color="blue", weight=5, opacity=0.7).add_to(mapa)
        st_folium(mapa, width=700, height=500)