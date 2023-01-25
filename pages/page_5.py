import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import get_institutions

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/concepts',  # '/' is home page and it represents the url
                   name='Publications by concepts',  # name of page, commonly used as name of link
                   title='concepts',  # title that appears on browser's tab
                   description='concepts')

df_inst = get_institutions() #get the data


layout = dbc.Container([
    
    html.Br(),
    
    dbc.Row([
        html.H4("Literature produced by type of concepts related to the publisher", style={'text-align': 'Left'})
    ]),
    
    html.Br(),

    dbc.Row([

        dbc.Col([
            html.Label('Countries:'),
            dcc.Dropdown(id="country_concept",
                    options=["All"] + [x for x in sorted(list(df_inst.country.unique()))],
                    multi=False,
                    value="All",
                    style={'width': "70%"}
                    ),
        ], width= 5),
    ]),

    dbc.Row([
        dcc.Graph(id='plot_works_count_concept', figure={}),
    ]),

    dbc.Row([
        dcc.Graph(id='plot_cited_concept', figure={})
    ]),
    
    dbc.Row([
        dcc.Graph(id='plot_ai_concept', figure={})
    ]),

     dbc.Row([
        dcc.Graph(id='plot_relevance', figure={})
    ]),

    html.Br(),

    dbc.Row([
        dcc.Markdown("""
            **Instructions:**
            
            The bar plot above reflect the relevance of the concepts of the institution at the publication of Machine Learning works. 

            Indeed, the different concepts are the ones associated to the institution that has made the publication or been cited by other works. 
            The highest the bar, the most publications or citations the concept has produced. 

            - Use the country selector to filter the information and analyze the relevance of different concepts for the selected country.

            - Select a certain area inside the plot to zoom into the information so it is clearer to analyse the data. 
            
            """) 
    ]),
    
    html.Br(),
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    [Output(component_id='plot_works_count_concept', component_property='figure'),
    Output(component_id='plot_cited_concept', component_property='figure'),
    Output(component_id='plot_ai_concept', component_property='figure'),
    Output(component_id='plot_relevance', component_property='figure')],
    [Input(component_id='country_concept', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # Plotly Express
    if option_slctd == "All":
        dff = df_inst.copy()
    else:
        dff = df_inst[df_inst["country"] == option_slctd]
    
    
    fig_works = px.histogram(dff, x = "concepts", y = "works_count", category_orders=dict(type=[x for x in sorted(list(df_inst.concepts.unique()))]),
                                title= "Academic production per concept related to the publisher",
                                labels = {"works_count":"Articules Published","concepts":"Concept related to publisher" })
    
    fig_cited = px.histogram(dff, x = "concepts", y = "cited_by_count", category_orders=dict(type=[x for x in sorted(list(df_inst.concepts.unique()))]),
                                color_discrete_sequence=['indianred'],
                                title= "Total citations of affiliated authors per concept related to the publisher",
                                labels = {"cited_by_count":"Citations","concepts":"Concept related to publisher" })

    fig_ai = px.histogram(dff, x = "concepts", y = "ai_papers", category_orders=dict(type=[x for x in sorted(list(df_inst.concepts.unique()))]),
                                color_discrete_sequence=['darkgreen'],
                                title= "Total AI publicatoins of affiliated authors per concept related to the publisher",
                                labels = {"ai_papers":"Publications","concepts":"Concept related to publisher" })
    
    fig_relevance = px.histogram(dff, x = "concepts", y = "ai_papers", category_orders=dict(type=[x for x in sorted(list(df_inst.concepts.unique()))]),
                                color_discrete_sequence=['darkblue'],
                                title= "Relevance estimated for each concept (citations per publication)",
                                labels = {"citations_per_paper":"Relevance","concepts":"Concept related to publisher" })
                        
    return [fig_works, fig_cited, fig_ai,fig_relevance]


# ------------------------------------------------------------------------------