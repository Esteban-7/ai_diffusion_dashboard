import dash
from dash import Dash,dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from networks import get_network
import dash_cytoscape as cyto
from get_data import get_institutions


# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/networks',  # '/' is home page and it represents the url
                   name='Networks',  # name of page, commonly used as name of link
                   title='networks',  # title that appears on browser's tab
                   description='networks')

df_inst = get_institutions() 

x = get_network("countries")
countries_network  = x[0]
nodes_names_countries = x[1]
del x

types_network = get_network("types")[0]
concepts_network = get_network("concepts")[0]


layout = dbc.Container([
    html.Br(),

    dbc.Row([
        html.H4("Networks created by the publication on Machine Learning", style={'text-align': 'left'})
    ]),

    html.Br(),

    dcc.Tabs(children = [
            
            dcc.Tab(label='Countries', children=[

                dbc.Row([
                    dbc.Col([
                        html.Label('Countries:'),
                        dcc.Dropdown(id="country_network",
                        options=["All"] + [x for x in sorted(nodes_names_countries)],
                        multi=False,
                        value="All",
                        style={'width': "80%"}
                        ),
                    ]),
                    
                    dbc.Col([
                        html.Label('Community:'),
                        dcc.Dropdown(id="community_country_network",
                        options=["All"] + [0,1,2,3,4,5],
                        multi=False,
                        value="All",
                        style={'width': "80%"}
                        ),
                    ]),
                    
                    dbc.Col([
                        html.Label('Layout:'),
                        dcc.Dropdown(id="update_layout_countries",
                        value='concentric',
                        clearable=False,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                            ],
                        style={'width': "80%"}
                        ),
                    ])
                ]),

                dbc.Row([
                cyto.Cytoscape(
                    id='graph_countries',
                    layout={'name': 'concentric'},
                    style={'width': '100%', 'height': '700px'},
                    elements=countries_network,
                    stylesheet = [
                        {
                            "selector": "node",
                            "style": {"content": "data(id)"} 
                        },
                        {
                            "selector": "edge",
                            #"style": {'line-color':"#BFD5E0",
                            "style": {'line-color':"mapData(weight,0,500,#F1F7F9, #343C40)",
                                        'curve-style':"bezier"
                                        }
                        },
                        {
                            "selector": "[community = 0]",
                            "style": {'background-color': '#18BC9C',}
                        },
                                                {
                            "selector": "[community = 1]",
                            "style": {'background-color': '#2C3E50',}
                        },
                        {
                            "selector": "[community = 2]",
                            "style": {'background-color': '#F39C12',}
                        },
                        {
                            "selector": "[community = 3]",
                            "style": {'background-color': '#E74C3C',}
                        },
                        {
                            "selector": "[community = 4]",
                            "style": {'background-color': '#3498DB',}
                        },
                        {
                            "selector": "[community = 5]",
                            "style": {'background-color': '#3BD0DB',}
                        },
                    ])
                ])
                                 

                    
            ]),

            dcc.Tab(label='Institutions', children=[
               dbc.Row([
                    dbc.Col([
                        html.Label('Layout:'),
                        dcc.Dropdown(id="update_layout_types",
                        value='circle',
                        clearable=False,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                            ],
                        style={'width': "80%"}
                        ),
                    ])
               ]),
               
               dbc.Row([
                 cyto.Cytoscape(
                    id='graph_types',
                    layout={'name': 'circle'},
                    style={'width': '100%', 'height': '800px'},
                    elements=types_network,
                    stylesheet = [
                        {
                            "selector": "node",
                            "style": {"content": "data(id)"} 
                        },
                        {
                            "selector": "edge",
                            "style": {'line-color':"mapData(weight,0,500,#F1F7F9, #343C40)",
                                        'curve-style':"bezier"}
                        },
                        {
                            "selector": "[community = 0]",
                            "style": {'background-color': '#18BC9C',}
                        },
                                                {
                            "selector": "[community = 1]",
                            "style": {'background-color': '#2C3E50',}
                        },
                        {
                            "selector": "[community = 2]",
                            "style": {'background-color': '#F39C12',}
                        },
                        {
                            "selector": "[community = 3]",
                            "style": {'background-color': '#E74C3C',}
                        },
                        {
                            "selector": "[community = 4]",
                            "style": {'background-color': '#3498DB',}
                        },
                        {
                            "selector": "[community = 5]",
                            "style": {'background-color': '#3BD0DB',}
                        },

                    ]) 
               ])
            ]),

            dcc.Tab(label='Concepts', children=[
                dbc.Row([
                    dbc.Col([
                        html.Label('Layout:'),
                        dcc.Dropdown(id="update_layout_concepts",
                        value='grid',
                        clearable=False,
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                            ],
                        style={'width': "80%"}
                        ),
                    ])
               ]),
               
               dbc.Row([
                 cyto.Cytoscape(
                    id='graph_concepts',
                    layout={'name': 'grid'},
                    style={'width': '100%', 'height': '800px'},
                    elements=concepts_network,
                    stylesheet = [
                        {
                            "selector": "node",
                            "style": {"content": "data(id)"} 
                        },
                        {
                            "selector": "edge",
                            "style": {'line-color':"mapData(weight,0,500,#F1F7F9, #343C40)",
                                        'curve-style':"bezier"}
                        },
                        {
                            "selector": "[community = 0]",
                            "style": {'background-color': '#18BC9C',}
                        },
                                                {
                            "selector": "[community = 1]",
                            "style": {'background-color': '#2C3E50',}
                        },
                        {
                            "selector": "[community = 2]",
                            "style": {'background-color': '#F39C12',}
                        },
                        {
                            "selector": "[community = 3]",
                            "style": {'background-color': '#E74C3C',}
                        },
                        {
                            "selector": "[community = 4]",
                            "style": {'background-color': '#3498DB',}
                        },
                        {
                            "selector": "[community = 5]",
                            "style": {'background-color': '#3BD0DB',}
                        },

                    ]) 
               ])
            ]),
        ]),
    
    html.Br(),

    dbc.Row([
        dcc.Markdown("""
            **Instructions:**
            
            In the Network tab it can be seen the networks created among nations, institutions and concepts by the publication on Machine Learning.

            In this case, the information from the papers published on Machine Learning is used. A relationship between two parts is made when one publication
            is made by different authors, the authors represent different institutions, for this, a relationship between the institutions is created. If the 
            institutions belong to different countries, then an international relationship is made. The strength of the relationship is given by the amount of 
            pubilcations made together, this is represented in the color of the edge (the line connecting the nodes), the darker the line, the stronger the connection.

            When several relationships are made in different groups of countries, communities are created. That is, subgroups that have a strongest relationship 
            among them that with the rest of the countries. The different communities are shown by having different colours in the network map. The communities 
            have been automatically estimated according to the data provided. 

            
            -   Use the country selector to find all countries that have a relationship with a given country. 
            -   Use the community selector to browse through different communities of countries, institutions or concepts. 
            -   Use the layout selector to design different patterns with the members of the networks.
            """)
    ]),

    html.Br(),
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@callback(
    [Output(component_id='graph_countries',component_property="layout"),
    Output(component_id='graph_countries',component_property="elements"),
    Output(component_id='graph_types',component_property="layout"),
    Output(component_id='graph_concepts',component_property="layout"),],
    [Input(component_id="update_layout_countries",component_property="value"),
    Input(component_id="country_network",component_property="value"),
    Input(component_id="community_country_network",component_property="value"),
    Input(component_id="update_layout_types",component_property="value"),
    Input(component_id="update_layout_concepts",component_property="value"),]
)
def update_layout(layout, country,community_country,layout_types,layout_concepts):
    
    countries_network  = get_network(file = "countries",filter_1 =country,filter_2=community_country)[0]

    
    return [{'name': layout,'animate': True}, countries_network,
            {'name': layout_types,'animate': True},
            {'name': layout_concepts,'animate': True}]