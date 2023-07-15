# Servidor Bokeh

Em virtude do servidor bokeh precisar ser hospedado para a sua plena execução, foi feito este fork, para executá-lo no serviço de hospegaem [steamlit](https://streamlit.io/), que possui uma biblioteca própria do python e que pode ser mesclada com a biblioteca Bokeh, como apenas as visualizações do estudante Sillas Rocha da Costa necessitavam de uma hospedagem, apenas elas foram disponibilizadas no serviço, pois a página com as visualizações de todos os estudantes não seria suportada na versão gratuita, deste modo, será feita a importação do link da página no html final do projeto, https://gtironi.github.io/icd_bokeh_a2, permitindo as interações com o bokeh server e respeitando o limite da versão gratuita do [steamlit](https://streamlit.io/).

O projeto completo está disponível em https://github.com/gtironi/icd_bokeh_a2.
