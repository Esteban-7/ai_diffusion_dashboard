import pymongo
import json
import pandas as pd
import numpy as np

def connection_institutions():
    client = pymongo.MongoClient("localhost",27017)
    db = client["AI_papers"]
    collection = db["institutions"]
    return collection


def total_publications_2012(id):
    pub_2012 = 0
    
    collection = connection_institutions()
    inst = collection.find_one({"id":id})
    
    try:
        for year in inst["counts_by_year"]:
            if year["year"] == 2012:
                pub_2012 = year["works_count"]
    except:
        pass
    
    return pub_2012


def total_publications_2020(id):
    pub_2020 = 0
    
    collection = connection_institutions()
    inst = collection.find_one({"id":id})
    
    try:
        for year in inst["counts_by_year"]:
            if year["year"] == 2020:
                pub_2020 = year["works_count"]
    except:
        pass

    return pub_2020

def ai_publications_12_20():
    #creates a data frame with the total publications and total ai publications for 2012 and 2020 fo institution. calculates the growth in the participation of ai publications
    ai_12 = pd.read_csv("data/AI_publications_2012.csv") #this ones are created by the class institution_process in the process_papers script
    ai_20 = pd.read_csv("data/AI_publications_2020.csv")
    ai = ai_12.merge(ai_20, how = "outer", on = "id").fillna(1)
    ai = ai.rename(columns={"ai_papers_x":"ai_papers_2012","ai_papers_y":"ai_papers_2020"})
    ai["total_2012"] = ai["id"].apply(total_publications_2012)
    ai["total_2020"] = ai["id"].apply(total_publications_2020)
    ai["ai_prcnt_2012"] = (ai["ai_papers_2012"]/ai["total_2012"]) * 100
    ai["ai_prcnt_2020"] = (ai["ai_papers_2020"]/ai["total_2020"]) * 100
    ai["ai_growth"] = (ai["ai_prcnt_2020"] - ai["ai_prcnt_2012"])/ai["ai_prcnt_2012"]
    ai.to_csv("data/ai_growth.csv", index=False)





def build_institutions_df():
    collection = connection_institutions()

    docs = collection.find({})
    columns = ["id","name", "type","works_count","cited_by_count","country","region","city","latitude","longitude","concepts"]
    ids = []
    names = []
    types = []
    works = []
    citations = []
    countries = []
    regions = []
    cities = []
    lats = []
    longs = []
    concepts = []

    for doc in docs:
        ids.append(doc["id"])
        names.append(doc["display_name"])
        types.append(doc["type"])
        works.append(doc["works_count"])
        citations.append(doc["cited_by_count"])
        countries.append(doc["geo"]["country"])
        regions.append(doc["geo"]["region"])
        cities.append(doc["geo"]["city"])
        lats.append(doc["geo"]["latitude"])
        longs.append(doc["geo"]["longitude"])
        try:
            concepts.append(doc["x_concepts"][0]["display_name"])
        except:
            concepts.append("Unknown") 
    
    df_inst = pd.DataFrame(list(zip(ids, names, types, works,citations,countries,regions,cities,lats,longs,concepts)),
               columns = columns)

    df_inst = df_inst.fillna("unkown")

    df_inst["citations_per_paper"] = df_inst["cited_by_count"]/df_inst["works_count"]
    df_inst.replace([np.inf, -np.inf], 0, inplace=True)
    
    df_public = pd.read_csv("data/AI_publications.csv")
    df_inst = df_inst.merge(df_public, on ="id", how = "left")
    
    df_inst = df_inst.fillna(0)

    df_growth = pd.read_csv("data/ai_growth.csv")
    df_inst = df_inst.merge(df_growth, on ="id", how = "left")
    df_inst = df_inst.fillna(0)
    
    del ids, names, types, works,citations,countries,regions,cities,lats,longs

    df_inst["AI_penetration"] = df_inst["ai_papers"]/df_inst["works_count"]
    df_inst = df_inst.fillna(0)
    
    df_inst.to_csv("data/df_inst.csv")

    pass
    

def get_institutions():
    
    df = pd.read_csv("data/df_inst.csv")
    return df

def build_institutions_years():
    ## querys the information of the publications and citations per insitution on a given year
    collection = connection_institutions()
    docs = collection.find({})

    year = []
    ids = []
    types = []
    country = []
    works_count = []
    cited_by_count = []

    no_info = []

    for doc in docs:
        try:
            for i in range(11):
                year.append(doc["counts_by_year"][i]["year"])
                ids.append(doc["id"])
                types.append(doc["type"])
                country.append(doc["geo"]["country"])
                works_count.append(doc["counts_by_year"][i]["works_count"])
                cited_by_count.append(doc["counts_by_year"][i]["cited_by_count"])
        except:
            no_info.append(doc["id"])
    
    df_years = pd.DataFrame(list(zip(year,ids,types,country,works_count,cited_by_count)),
                       columns = ["year","id","type","country","works_count","cited_by_count"])
    df_years = df_years[df_years["year"]<2022]
    df_years = df_years.fillna("unknown")
    df_years["citations_per_paper"] = df_years["cited_by_count"]/df_years["works_count"]
    df_years.replace([np.inf, -np.inf], 0, inplace=True)
    df_years = df_years.fillna(0)
    df_years.to_csv("data/df_years.csv")
    #return df_years


def get_institutions_years():
    df = pd.read_csv("data/df_years.csv")
    
    return df 

