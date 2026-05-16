from graph_search import *

st.title("Rotas no Rio de Janeiro")
st.write("Insira os dados da sua viagem:")

origem = municipio_id_for_name(st.selectbox("Qual o município de partida? ", names))
destino = municipio_id_for_name(st.selectbox("Você quer ir pra qual município? ", names))
estrategia = st.selectbox("Você prefere: ",["Caminho com menos kilômetros", "Caminho com menos municípios de separação"])

if st.button("Buscar caminho"):
    if estrategia == "Caminho com menos kilômetros": estrategia = 'less_distance'
    else: estrategia = 'min_degrees'

    if origem and destino:
        path, cost = (shortest_path(origem, destino, estrategia))

        if path is None: st.error("Não foi possível encontrar um caminho entre esses municípios.")
        else:
            st.write(f"Mínimo de {len(path)} municípios de separação:")
            print_path(path)
            st.write(f"Total de {cost:.2f}km de distância\n")

    else: st.error("Município não encontrado")