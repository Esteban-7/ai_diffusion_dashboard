import pymongo 
import json
import pandas as pd
import plotly.express as px 
import itertools
from tqdm import tqdm

import psutil
from multiprocessing.dummy import Pool
from itertools import islice

class network_process():

    def __init__(self):
        client = pymongo.MongoClient("localhost",27017)
        db = client["AI_papers"]
        self.collection = db["articles_light"]
        self.collection_institutions = db["institutions"]

        self.docs =  self.collection.find({})
        #self.docs =  self.collection.aggregate([
        #    { "$sample": { "size": 1000 } }
        #])

        self.institutions_edgelist = []
        self.countries_edgelist = []
        self.types_edgelist = []
        self.concepts_edgelist = []


    def get_combinations(self, elements):
              
        tuples = []
        
        if len(list(elements)) > 0:
            tuples = list(itertools.combinations(elements,2))    
        
        return tuples


    def create_edgelist_df(self, combinations):
        origins = []
        targets = []
        weights = []
        done = []
        for couple in combinations:
            if couple not in done:
                origin = couple[0]
                target = couple[1]
                weight = combinations.count(couple)
                origins.append(origin)
                targets.append(target)    
                weights.append(weight)
                done.append(couple)    

        edgelist = pd.DataFrame({"origin":origins,"target":targets,"weight":weights}).drop_duplicates()
        edgelist = edgelist.reset_index(drop = True)
        return edgelist


    def edgelists_from_papers(self,doc):
        institutions = []
        countries = []
        types = []
        concepts = []
        for author in doc["authorships"]:
            try:        
                for institution in author["institutions"]:
                    full_doc = self.collection_institutions.find_one({"id":institution["id"]})
                    
                    institutions.append(institution["id"]) 
                    countries.append(full_doc["geo"]["country"])
                    types.append(full_doc["type"])
                    concepts.append(full_doc["x_concepts"][0]["display_name"])
            except:
                pass
        
        institutions = list(set(institutions))
        countries = list(set(countries))
        types = list(set(types))
        concepts = list(set(concepts))
        
        if None in institutions: institutions.remove(None)
        if None in countries: countries.remove(None)
        if None in types: types.remove(None)
        if None in concepts: concepts.remove(None)

        institutions.sort()
        countries.sort()
        types.sort()
        concepts.sort()

        #self.institutions_edgelist = self.institutions_edgelist + self.get_combinations(institutions)
        self.countries_edgelist = self.countries_edgelist + self.get_combinations(countries)
        self.types_edgelist = self.types_edgelist + self.get_combinations(types)
        self.concepts_edgelist = self.concepts_edgelist + self.get_combinations(concepts)      


    def split_every(self,n, iterable):
        i = iter(iterable)
        piece = list(islice(i, n))
        while piece:
            yield piece
            piece = list(islice(i, n))


    def process_chunks(self,):
        i = 0
        for chunk in tqdm(self.split_every(20000,self.docs)):
            print(f"Chunk:{i}")
            self.institutions_edgelist = []
            self.countries_edgelist = []
            self.types_edgelist = []
            self.concepts_edgelist = []
            
            pool = Pool(7)
            pool.map(self.edgelists_from_papers,chunk)
            
            countries_edgelist_df = self.create_edgelist_df(self.countries_edgelist)
            countries_edgelist_df.to_csv("data/edgelists/countries.csv", mode="a", index=False, header=False)

            types_edgelist_df = self.create_edgelist_df(self.types_edgelist)
            types_edgelist_df.to_csv("data/edgelists/types.csv", mode="a", index=False, header=False)
            
            concepts_edgelist_df = self.create_edgelist_df(self.concepts_edgelist)
            concepts_edgelist_df.to_csv("data/edgelists/concepts.csv", mode="a", index=False, header=False)
            i = i+1

    
    def clean_df(self, df):
        x = pd.read_csv(f"data/edgelists/{df}.csv")
        x.columns = ["target","origin","weight"]
        x = x.groupby(["target","origin"]).sum().reset_index()
        x.to_csv(f"data/edgelists/{df}.csv", mode="w", index=False)



class institution_process():
    
    def __init__(self, year = 0):

        self.hash_table = {}
        client = pymongo.MongoClient("localhost",27017)
        db = client["AI_papers"]
        self.collection = db["articles_light"]

        
        self.docs =  self.collection.find({})
        self.year = year
        if self.year != 0:
            self.docs =  self.collection.find({"publication_year":self.year})
        #self.docs =  self.collection.aggregate([
        #    { "$sample": { "size": 1000 } }
        #])

    def find_institution(self, doc):
        institutions = []
        try:
            for author in doc["authorships"]:
                for institution in author["institutions"]:
                    id_institution = institution["id"]
                    if id_institution in self.hash_table:
                        self.hash_table[id_institution] = self.hash_table[id_institution] + 1
                    else:
                        self.hash_table[id_institution] = 1
        except:
            pass

    def split_every(self,n, iterable):
        i = iter(iterable)
        piece = list(islice(i, n))
        while piece:
            yield piece
            piece = list(islice(i, n))


    def hash_fill(self,):
        i = 0
        for chunk in self.split_every(20000,self.docs):
            print(f"Chunk:{i}")
            self.hash_table = {}
            pool = Pool(6)
            pool.map(self.find_institution,chunk)

            df = pd.DataFrame.from_dict(self.hash_table,orient='index', columns=['ai_papers'])
            df = df.reset_index()
            df = df.rename(columns = {"index":"id"}) 
            df.to_csv(f"data/AI_publications_{str(self.year)}.csv", mode="a",index=False)
            i = i+1

    def clean_df(self):
        df = pd.read_csv(f"data/AI_publications_{str(self.year)}.csv")
        df = df[df.id != "id"]
        df["ai_papers"] = pd.to_numeric(df["ai_papers"])
        df = df.groupby(["id"]).sum()
        df = df.reset_index()
        df.to_csv(f"data/AI_publications_{str(self.year)}.csv",index=False)