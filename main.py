
from bokeh.plotting import curdoc
from visualizacoes import gera_layout_sillas


layout_sillas = gera_layout_sillas("data/spotify_youtube_year.csv")

curdoc().add_root(layout_sillas)

