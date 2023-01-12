import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import get_institutions

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Home',  # name of page, commonly used as name of link
                   title='home',  # title that appears on browser's tab
                   description='home')


layout = html.Div([
    html.H1("Home", style={'text-align': 'left'}),

    html.H4("Purpose", style={'text-align': 'left'}),
    dcc.Markdown("""
    In the past decade, AI has gained significant relevance in a variety of fields. 
    It has been implemented in everything from healthcare and transportation to finance and education. In healthcare, 
    AI is being used to analyze medical images and assist with diagnoses, while in transportation, it is being used to develop self-driving cars. 
    In finance, AI is being used to identify patterns and make trading decisions, and in education, it is being used to personalize learning for students.
     For that AI, is being part of the reality of many of us in the current years, thus it is important to know how this process of democratization and growth of AI is

    The present data visualization tool aims at the understanding on how Machine Learning spreads around in the academic world. 
    Indeed, the insights gotten from the analysis of the diffusion on Machine Learning can help us identify the main boosters of this field 
    so that policy makers can in time, boost the main producers of innovation. This chain effect could potentially improve the quality of different 
    investigations by redirecting budget allocations, can help limit the extend of AI to avoid harm in the communities, and even create a deeper impact
     by proposing policies that benefit from the networks created in the production of AI.
    
    """),

    html.H4("Data source", style={'text-align': 'left'}),
    dcc.Markdown("""
    OpenAlex offers information about scientific publications, authors, institutions, events around the world and also shows how they are interconnected with each other. 
    Thus, you get access to a graph with millions of entities and billions of connections between them.
     OpenAlex is an open-source Project, for that, all the information about the recollection of the data related to the articles, 
     authors, and others is completely free access on the GitHub. OpenAlex gathers metainformation about publications from different
      projects such as the already unsupported MAG, Crossref and plenty others. Thus, OpenAlex uses different computational tools to obtain 
    and process metadata about scientific publications from different sources and provide a comprehensive and global database.
    
    """),

    html.H4("Definitions", style={'text-align': 'left'}),
    dcc.Markdown("""
    As we use the information offered By OpenAlex, it is important to clarify different definitions used in the visualizations:
    
    -	Id: unique identifier for each institution
    -	Display_name: name of the institution
    -	Type: type of the institution (education, healthcare, company, archive, among others)
    -	Works_count: number of works (publications) made by authors affiliated to the institution.
    -	Cited_by_count: total publications that cite an article produced by an author affiliated to the institution. 
    -	Country, Region, City, Latitude & longitude: geographical information of the institution. 
    -	Counts_by_year: total number of publications and citations related to the institution per year between 2012 and 2022.
    -	X_concepts: the concepts frequently applied to the publications affiliated to the institution, that is, the concept or topic that the institution is mostly related to. 

    A more extensive and comprehensive description of the data source and definitions can be found in https://docs.openalex.org/.

    In addition we add two important statistics to the analysis>
    
    - AI publications: the aggregated number of publications that are related to Artificial Intelligence and different keywords.
    - Citations per paper: the ratio between the works_count and cited_by_count variable. This ratio of citations per paper offers a proxy
    of how well known the institution that published is and in that way a proxy to the leverl of excelence or relevance of said institution. 
    - AI Adaptation: AI related publications as proportion of total publications.

    The code source of this project as well as a more detailed description is found in https://github.com/Esteban-7/ai_diffusion_dashboard.git
"""),
    
])
