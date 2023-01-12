import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from get_data import get_institutions

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/heatmap',  # '/' is home page and it represents the url
                   name='Heatmap',  # name of page, commonly used as name of link
                   title='heatmap',  # title that appears on browser's tab
                   description='Heatmaps')

#-----------------------------------------------------------------------------------------------------------------------------------

df_inst = get_institutions() #get the data

#-----------------------------------------------------------------------------------------------------------------------------------
layout = dbc.Container([
    
    html.Br(),

    dbc.Row([
        html.H4("Geographical distribution of Machine Learning academic production", style={'text-align': 'left'})
    ]),

    html.Br(),

    dbc.Row([
        
        dbc.Col([
            html.Label('Variable:'),
            dcc.Dropdown(id="indicator",
                options=[
                    {"label": "Publications","value": "works_count"},
                    {"label": "Citations","value": "cited_by_count"},
                    {"label": "AI Publications","value": "ai_papers"},
                    {"label": "Citations per paper","value": "citations_per_paper"},
                    {"label":"AI participation in total papers 2012","value":"ai_prcnt_2012"},
                    {"label":"AI participation in total papers 2020","value":"ai_prcnt_2020"},
                    {"label":"Growth in the participation of AI","value":"ai_growth"},
                    ],
                multi=False,
                value="works_count",
                style={'width': "80%"}
                )
        ], width= 4),

        dbc.Col([
            html.Label('Countries:'),
            dcc.Dropdown(id="country",
                options=["All"] + [x for x in sorted(list(df_inst.country.unique()))],
                multi=False,
                value="All",
                style={'width': "80%"}
                )
        ], width= 4),

        dbc.Col([
            html.Label('Type of institution:'),
            dcc.Dropdown(id="institution",
                options=["All"] + [x for x in sorted(list(df_inst.type.unique()))],
                multi=False,
                value="All",
                style={'width': "80%"}
                )
        ], width= 4)
        
        ]),

        

    dbc.Row([
        dbc.Col([
            
        html.Br(),
        dcc.Graph(id = "heatmap_works", figure = {})    
        
        ], width = 12)
    ]),

    dbc.Row([
        dbc.Col([
        html.Label('AI growth & relevance of institutions.'),
        html.Br(),
        dcc.Graph(id = "scatter", figure = {})    
        
        ], width = 12)
    ]),

    dbc.Row([
        html.Br(),

        dbc.Row([
            dcc.Markdown("""
            **Instructions:**

            In this part of the website you can find the geographical distribution on the production of Machine Learning academic publications. 
            
            The heatmap shows what areas of the planet are the most important in terms of academic papers produced related to Machine Learning.
            In the map, the bar on the right shows the amount of articles produced or citations by grographical area. The brightest the color, 
            the most important the geographical are is. 

            Use the different selectors to navigate through the data. 
            - The variable selector allows to see either the amount of publications made by region or the total citations related to the region.
            - The countries selector allows to filter different countries so the scale can be adjusted and this focus on the production of the specified area.
            - The institution selector allows to filter the publications or citations in function of the type of institution that has produced the content.  
            """)
    ]),
    ])
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    [Output(component_id='heatmap_works', component_property='figure'),
    Output(component_id='scatter', component_property='figure')],
    [Input(component_id='country', component_property='value'),
    Input(component_id='indicator', component_property='value'),
    Input(component_id='institution', component_property='value')]
)
def update_graph(option_slctd,indicator_selected,institution):
    print(option_slctd)
    print(type(option_slctd))

    # Plotly Express
    if option_slctd == "All":
        dff = df_inst.copy()    
    else:
        dff = df_inst[df_inst["country"] == option_slctd]
    
    if institution != "All":
        dff = dff[dff["type"] == institution]
    

    if indicator_selected == 'works_count':
        title = "Concentration of literature production"    
    elif indicator_selected == "ai_papers":
        title = "Concentrations of AI publications"
    elif indicator_selected == "citations_per_paper":
        title = "Relevance of institution (citations per paper)"
    elif indicator_selected == "ai_prcnt_2012":
        title = "Proportion of AI publications in the total of publications by the institution: 2012"
    elif indicator_selected == "ai_prcnt_2020":
        title = "Proportion of AI publications in the total of publications by the institution: 2020"
    elif indicator_selected == "ai_growth":
        title = "Growth in the participation of the AI articles in the total of the publications between 2012 and 2020"
    else:
        title = "Concentrations of citations"
    
    fig = px.density_mapbox(dff, lat='latitude', lon='longitude', z=indicator_selected, radius=10,
                    center=dict(lat=2.2, lon=21), zoom=1,
                    mapbox_style="stamen-terrain", title = title, height = 750,
                    labels= {"works_count":"Publications","cited_by_count":"Citations",
                            "ai_papers":"AI Publications","citations_per_paper":"Relevance",
                            "ai_prcnt_2012":"Proportion of AI articles","ai_prcnt_2020":"Proportion of AI articles",
                            "ai_growth":"Growth in AI participation",
                            })

    scatter = px.scatter(dff[dff["ai_growth"]!=0], x = "citations_per_paper",y = "ai_growth",  trendline="ols",trendline_color_override="red",
                            labels={"citations_per_paper":"relevance","ai_growth":"AI adoptation"})       
    return [fig, scatter]


# ------------------------------------------------------------------------------
