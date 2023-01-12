#en esta página debe ir una gráfica de línea de tiempoi con selector de tipo de 
#insituticon, año y pais qye muestra el numerp de publicaciones y citas

import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from get_data import get_institutions_years

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/timeline',  # '/' is home page and it represents the url
                   name='Evolution of publicatoins in time',  # name of page, commonly used as name of link
                   title='timeline',  # title that appears on browser's tab
                   description='Timeline in productions')

#-----------------------------------------------------------------------------------------------------------------------------------
df_years = get_institutions_years()

#-----------------------------------------------------------------------------------------------------------------------------------

layout = dbc.Container([
    html.Br(),
    
    dbc.Row([
        html.H4("Academic production and citations on Machine Learning evolution in time ", style={'text-align': 'left'})
    ]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.Label('Countries:'),
            dcc.Dropdown(id="country",
                options=["All"] + [x for x in sorted(list(df_years.country.unique()))],
                multi=False,
                value="All",
                style={'width': "70%"}
                )
        ], width= 5),

        dbc.Col([
            html.Label('Type of institution:'),
            dcc.Dropdown(id="type",
                options=["All"] + [x for x in sorted(list(df_years.type.unique()))],
                multi=False,
                value="All",
                style={'width': "70%"}
                )
        ], width= 5),
    ]),

    dbc.Row([
        
        dbc.Col([
            dcc.Graph(id = "historic_publications", figure={})
        ],width = 6),
        
        dbc.Col([
            dcc.Graph(id = "historic_citations", figure={})
        ],width = 6)
        
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "historic_relevance", figure={})
        ],width = 12),
    ]),

    html.Br(),
    
    dbc.Row([
        
        dcc.Markdown("""
            **Instructions:**
            
            The plot lines above represent the evolution of the publications and citations accross time. The timelapse is between 
            2012 and 2021. It is to be noted that 2021 numbers can not be entirely accurate given recent updates.

            On the left it can be seen the evolution on the amount of articles published. On the right there is the evolution of 
            the total citations.
        
            - Use the countries selector to filter the information by a given country. In this case the total of publications and citations will only be related to 
            the selected country. 
            - Use the institutions selector to filter the informastion by a type of institution. In such case the plots will only show the 
            information on publications made by such type of institutions and the total amount of citations related to such institution.  
            
            """)        
    ])

])


# ------------------------------------------------------------------------------
@callback(
    [Output(component_id="historic_publications", component_property="figure"),
    Output(component_id="historic_citations", component_property="figure"),
    Output(component_id="historic_relevance", component_property="figure")],
    [Input(component_id = "country", component_property = "value"),
    Input(component_id = "type", component_property = "value")]
)
def update_plot(country,type):
    
    if country == "All":
        dff = df_years.copy()
    else:
        dff = df_years[df_years["country"]==country]
    
    if type != "All":
        dff = dff[dff["type"]==type]
    
    dff = dff.groupby("year").sum()

    fig = px.line(dff,  y = "works_count",labels = {"year":"Year","works_count":"Publications"},
                    title= "Total amount of Publications")

    fig_2 = px.line(dff,  y = "cited_by_count",labels = {"year":"Year","cited_by_count": "Citations"},
                    title= "Total amount of Citations of authors afiiliated",
                    color_discrete_sequence=['indianred'])

    fig_3 = px.line(dff,  y = "citations_per_paper",labels = {"year":"Year","citations_per_paper": "Relevance"},
                    title= "Relevance estimated per year (citations per paper)",
                    color_discrete_sequence=['darkgreen'])
    
    return [fig,fig_2,fig_3]