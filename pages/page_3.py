import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import get_institutions

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/institution',  # '/' is home page and it represents the url
                   name='Publications by Institutions',  # name of page, commonly used as name of link
                   title='institution',  # title that appears on browser's tab
                   description='institution')

df_inst = get_institutions() #get the data


layout = dbc.Container([

    html.Br(),

    dbc.Row([
        html.H4("Literature produced by type of institution", style={'text-align': 'Left'})
    ]),
    
    html.Br(),

    dbc.Row([

        dbc.Col([
            html.Label('Countries:'),
            dcc.Dropdown(id="country",
                    options=["All"] + [x for x in sorted(list(df_inst.country.unique()))],
                    multi=False,
                    value="All",
                    style={'width': "70%"}
                    ),
        ], width= 5),
    ]),

    dbc.Row([
        dcc.Graph(id='plot_works_count', figure={}),
    ]),

    dbc.Row([
        dcc.Graph(id='plot_cited', figure={})
    ]),
    
    dbc.Row([
        dcc.Graph(id='plot_ai', figure={})
    ]),

        
    html.Br(),

    dbc.Row([
        dcc.Markdown("""
            **Instructions:**
            
            In the plots it can be identified the amount of publications made by different types of institutions or the citations to their different publications.

            Use the countries selector to find out the participation on production of Machine Learning by type of institution by a selected country in the pie chart.
            The second pie chart shows the participation of each type of institutions recieved by a selected country. 
            
            """)
    ]),

    html.Br(),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@callback(
    [Output(component_id='plot_works_count', component_property='figure'),
    Output(component_id='plot_cited', component_property='figure'),
    Output(component_id='plot_ai', component_property='figure')],
    [Input(component_id='country', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # Plotly Express
    if option_slctd == "All":
        dff = df_inst.copy()
    else:
        dff = df_inst[df_inst["country"] == option_slctd]
    
    
    pie_works = px.pie(dff, values = "works_count", names = "type",title = "Academic production per type of institution",
                        labels= {"works_count":"Publications","cited_by_count":"Citations"})

    pie_cited = px.pie(dff, values = "cited_by_count", names = "type",title = "Total Citations per type of insitution",
                        labels= {"works_count":"Publications","cited_by_count":"Citations"})
    
    pie_ai = px.pie(dff, values = "ai_papers", names = "type",title = "Total AI publications per type of insitution",
                        labels= {"works_count":"Publications","ai_papers":"AI publications"})


    #fig_works = px.histogram(dff, x = "type", y = "works_count", category_orders=dict(type=[x for x in sorted(list(df_inst.type.unique()))]),
#                                title= "Academic production per type of insitution",
#                                labels = {"works_count":"Articules Published","type":"Type of institutions" })
    #fig_cited = px.histogram(dff, x = "type", y = "cited_by_count", category_orders=dict(type=[x for x in sorted(list(df_inst.type.unique()))]),
 #                               color_discrete_sequence=['indianred'],
 #                               title= "Total citations of affiliated authors per type of insitution",
 #                               labels = {"cited_by_count":"Citations","type":"Type of institutions" })
                        
    return [pie_works, pie_cited,pie_ai]


# ------------------------------------------------------------------------------