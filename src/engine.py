import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# load libraries
sys.path.append(base_dir)
import elasticsearch
from loguru import logger
from pydantic import BaseModel
from src.utils import get_user_list, update_user_data, write_new_csv
from src.momo_wallet import gen_momo_payment_url
from ast import literal_eval

class RecipeModel(BaseModel):
    title:str
    ingredients:str
    time:int
    cook:str
    images:str

class user_profile(BaseModel):
    user_email:str
    is_premium:bool
    trial_time:int

class SearchEngine:
    def __init__(self, id_name:str, api_key:str, index_name:str, user_index:str)->None:
        # init client
        self.client = elasticsearch.Elasticsearch(
                cloud_id= id_name,
                api_key= api_key
            )

        self.index_name = index_name
        self.user_index = user_index

    def update_recipe(self, input_recipe:RecipeModel)->None:
        try:
            recipe = input_recipe.model_dump_json()
            recipe = literal_eval(recipe)
            recipe_list = []
            recipe_list.append({"index": {"_index": "recipes"}})
            recipe_list.append(recipe)

            self.client.bulk(index = self.index_name, operations= recipe_list, refresh=True)
            print("Updated 1 record")
            return "Success"
        except Exception as e:
            print(e)
            return "Failed"
        
    def search_one_feature(self, input_query:str, input_feature:str)->dict:
        response = self.client.search(
            index= self.index_name,
            query={"match": {input_feature: {"query": input_query}}}
        )
        if len(response["hits"]["hits"]) == 0:
            logger.debug(f"Your search in {input_feature} returned no results, query: {input_query}")
            return {}
        else:
            response = response["hits"]["hits"]

        return response


    def search_many_feature(self, input_query:str, input_features:list)->dict:
        if not isinstance(input_features, list):
            logger.debug("features input must be in a list")
            return {}
        if len(input_features) == 1:
            logger.debug("Use search_one_feature if searching a single field.")
            return {}
        
        response = self.client.search(
                index= self.index_name,
                query={"multi_match": {"query": input_query, "fields": input_features}},
                )
        if len(response["hits"]["hits"]) == 0:
            logger.debug(f"Your search in {input_features} returned no results, query: {input_query}")
            return {}
        else:
            response = response["hits"]["hits"]
            
        return response
    
    def delete_one_record(self, input_feature:str):
        pass

    def check_user(self, input_user_email:str)->bool:
        list_users = get_user_list()
        print("all user:", list_users)
        if input_user_email in list_users:
            return True
        else:
            return False
        
    def check_trial_time(self, input_user_email:str) -> int:
        if self.check_user(input_user_email = input_user_email):
            all_data = get_user_list(all_data=True)
            current_user_info = all_data[all_data["user_email"] == input_user_email]
            if current_user_info["is_premium"].values[0]:
                return 10
            
            else:
                trial_time_left = current_user_info["trial_time"].values[0]
                return int(trial_time_left)

        else:
            return 0
        
    def update_trial_time(self, input_user_email:str) -> int:
        all_data = get_user_list(all_data=True)
        current_user_info = all_data[all_data["user_email"] == input_user_email]
        trial_time_left = current_user_info["trial_time"].values[0] - 1
        if trial_time_left < 0:
            trial_time_left = 0

        all_data.loc[all_data["user_email"] == input_user_email, "trial_time"] = trial_time_left
        
        write_new_csv(all_data)
        
    def check_premium_status(self, input_user_email:str)->bool:
        all_data = get_user_list(all_data=True)
        if len(all_data)!= 0:
            if not self.check_user(input_user_email= input_user_email):
                user_profile = {
                    "user_email": input_user_email,
                    "is_premium": False,
                    "trial_time": 5
                }
                update_user_data(user_profile= user_profile)
                return False
            else:
                current_user_info = all_data[all_data["user_email"] == input_user_email]
                return current_user_info["is_premium"].values[0]
        else:
            user_profile = {
                "user_email": input_user_email,
                "is_premium": False,
                "trial_time": 5
            }
            update_user_data(user_profile= user_profile)
            return False
            
    def generate_momo_payment_url(self, input_user_email:str)-> str:
        if not self.check_user(input_user_email= input_user_email):
            user_profile = {
                "user_email": input_user_email,
                "is_premium": False,
                "trial_time": 5
            }
            update_user_data(user_profile= user_profile)

        payment_url = gen_momo_payment_url()
        return payment_url
