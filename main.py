
# Importações do módulo de visualização
import streamlit as st
from bokeh.io import curdoc
from bokeh.models import HoverTool, LegendItem
from visualizacoes import read_data
from visualizacoes import visualizacoes_sillas


st.set_page_config(
    layout="wide",
    menu_items=None,
    initial_sidebar_state="auto",
)

new_margins = """
<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

body {
  background-color: #f5f5f5;
  color: #000;
}
</style>
"""

st.markdown("<h1 align=center>Visualizações das Músicas do Spotify</h1>", unsafe_allow_html=True)

st.markdown(new_margins, unsafe_allow_html=True)

categories = ["Danceability", "Energy", "Valence", "Speechiness", "Acousticness"]

path = "./data/spotify_youtube_year.csv"

all_music_names = read_data.get_column_observations(path, "Track", sort_column = "Stream")

firts_music_data = read_data.csv_filter_by_name_to_cds(path, "Track", all_music_names[0])

first_music_values, firts_music_row = firts_music_data


filter_plot = visualizacoes_sillas.gera_plot_categorias_sillas(path)

médias = filter_plot.renderers[0]
selected_music = filter_plot.renderers[1]
hover_musica = filter_plot.select(HoverTool)[0]

density_plot = visualizacoes_sillas.gera_plot_densidade_sillas(path)

density_hist = density_plot.renderers[0]
musics = density_plot.renderers[1]
music_star = density_plot.renderers[2]

years_plot = visualizacoes_sillas.gera_plot_anos_sillas(path)


def update_spotify_player(spotify_uri):
    spotify_player_html = f"""
    <iframe src="https://open.spotify.com/embed?uri={spotify_uri}"
            width="640" height="160" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """
    with columns_selection[0]:
        st.components.v1.html(spotify_player_html, height = 275)


def update_music_selected(new_music):

        new_data = read_data.csv_filter_by_name_to_cds(path, "Track", new_music, lowercase = True)
        values, row = new_data

        music_uri = row.data["Uri"][0]
        update_spotify_player(music_uri)

        new_legend = LegendItem(label = new_music, renderers = [médias, selected_music])
        filter_plot.legend.items[1] = new_legend

        new_artist = row.data["Artist"][0]
        hover_musica.tooltips = [("Valor", "@Values"),
                                ("Artista", new_artist)]

        filter_plot.title.text = f"Níveis de {new_music}"

        first_music_values.data["Values"] = values.data["Values"]
        music_star.data_source.data = dict(row.data)


def update_category_selected(new_category):

    new_histogram_data = read_data.histogram_data(path, new_category, proportion_column="Stream")
     
    density_plot.title.text = f"{new_category} X Vezes tocadas no Spotify (Em bilhões)"
    density_plot.xaxis.axis_label = new_category

    density_hist.data_source.data = dict(new_histogram_data.data)
    music_star.glyph.x = new_category
    musics.glyph.x = new_category


with st.container():
    columns_selection = st.columns(2)
    selectec_music = columns_selection[0].selectbox("Músicas Disponíveis (Selecione de acordo com como aparece no Spotify):",
                                                    all_music_names)
    update_music_selected(selectec_music)
    
    selected_category = columns_selection[0].selectbox("Categorias:", categories)
    update_category_selected(selected_category)

    columns_selection[1].bokeh_chart(filter_plot)


def streamlit_music_callback():
    if selectec_music != st.session_state.selectec_music:
        update_music_selected(selectec_music)
        st.session_state.selectec_music = selectec_music

def streamlit_category_callback():
    if selected_category != st.session_state.selected_category:  
        update_category_selected(selected_category)
        st.session_state.selected_category = selected_category


with st.container():
    plot_columns = st.columns(2)

    plot_columns[0].bokeh_chart(density_plot)

    plot_columns[1].bokeh_chart(years_plot)


st.bokeh_chart(visualizacoes_sillas.gera_explicacoes_sillas())

curdoc().add_next_tick_callback([streamlit_music_callback, streamlit_category_callback])

