import pandas as pd
import networkx as nx
import community as community_louvain
from get_data import get_institutions

def get_network(file, filter_1 = "All", filter_2 = "All"):
    
    if file == "countries":
        variable = "country"
    elif file == "types":
        variable = "type"
    else:
        variable = "concepts"
    
    edgelist = pd.read_csv(f"data/edgelists/{file}.csv")

    if filter_1 != "All":
        edgelist = edgelist.loc[(edgelist["target"]==filter_1) | (edgelist["origin"]==filter_1)]
    
    
    edgelist = edgelist[["origin","target","weight"]]
    edgelist = edgelist.rename(columns = {"origin": "source"})
    edgelist_dict = edgelist.to_dict("index")
    edges_list = []
    for edge in edgelist_dict:
        edges_list.append({"data":edgelist_dict[edge]})
    
    g = nx.from_pandas_edgelist(edgelist,source = "source",target="target", edge_attr = "weight")

    df_inst = get_institutions()
    df_inst = df_inst[[variable,"works_count","cited_by_count","ai_papers"]]
    df_inst = df_inst[df_inst[variable] != 'unkown' ]
    df_inst = df_inst.groupby(variable).sum()
    di = df_inst.to_dict()
    publications = di["works_count"]
    citations = di['cited_by_count']
    ai_papers = di['ai_papers']

    nx.set_node_attributes(g, publications,"publications")
    nx.set_node_attributes(g, citations,"citations")
    nx.set_node_attributes(g, ai_papers,"ai_papers")

    centrality_eigen = nx.eigenvector_centrality_numpy(g, weight='weight')
    nx.set_node_attributes(g, centrality_eigen, 'centrality_eigen')

    partition = community_louvain.best_partition(g, random_state = 1)
    nx.set_node_attributes(g, partition, 'community')

    nodes = dict(g.nodes(data=True))
    data = []
    for node in nodes:
        elem = {**{"id":node},**nodes[node]}
        data.append({"data":elem})
    
    nodes_names = []
    for node in data:
        nodes_names.append(node["data"]["id"])

    if filter_2 != "All":
        data_ = []
        for node in data:
            if node["data"]["community"] == filter_2:
                data_.append(node)
        data = data_
        
        nodes_names = []
        for node in data:
            nodes_names.append(node["data"]["id"])
        
        edges_list_ = []
        for edge in edges_list:
            if (edge["data"]["source"] in nodes_names and edge["data"]["target"] in nodes_names):
                edges_list_.append(edge)
        
        edges_list = edges_list_
    
    elements = data + edges_list

    if file == "countries":
        coordinates = pd.read_csv("data/coordinates.csv", sep = ";")
        for point in data:
            country_name = point["data"]["id"]
            try:
                point["position"] = {"x":float(coordinates[coordinates["country"]==country_name]["longitude"]),"y":float(coordinates[coordinates["country"]==country_name]["latitude"])}
            except:
                print(point)


    return [elements, nodes_names, data]