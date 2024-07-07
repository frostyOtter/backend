import os
from loguru import logger
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
image_folder = os.path.join(script_dir, "data/img/")

import pandas as pd
import re

def translate_vietnamese_name(name):
    # Remove accents and special characters
    name = name.strip()
    name = re.sub(r'[àáảãạăằắẳẵặâầấẩẫậ]', 'a', name)
    name = re.sub(r'[èéẻẽẹêềếểễệ]', 'e', name)
    name = re.sub(r'[ôồốổỗộơờớởỡợỏòọõó]', 'o', name)
    name = re.sub(r'[ìíỉĩị]', 'i', name)
    name = re.sub(r'[ùúủũụưừứửữự]', 'u', name)
    name = re.sub(r'[ỳýỷỹỵ]', 'y', name)
    name = re.sub(r'[đd]', 'd', name)
    name = re.sub(r'[ ]', '-', name)

    # Replace multiple spaces with a single space
    name = re.sub(r' +', ' ', name)

    # Remove leading and trailing spaces
    name = name.strip().lower()

    # Replace spaces with underscores
    name = name.replace(' ', '-')

    return name

def get_image_path(input_recipe_name:str)->str:

    alphabet_name = translate_vietnamese_name(name= input_recipe_name)
    # image_path = os.path.join(image_folder,alphabet_name.strip())
    # logger.debug(f"alphabet_name: {alphabet_name}")
    # image_path = image_path.lower().replace('-', '_')

    # if os.path.isfile(image_path + ".jpg"):
    #     # return image_path + ".jpg"
    #     return alphabet_name + ".jpg"
    # elif os.path.isfile(image_path + ".png"):
    #     # return image_path + ".png"
    #     return alphabet_name + ".png"
    
    # elif os.path.isfile(image_path + ".webp"):
    #     return alphabet_name + ".webp"
    
    # else:
    #     # return os.path.join(script_dir, "data/img", "banh_it.jpg")
    #     return "null"
    return alphabet_name + ".jpg"

def get_user_list(all_data:bool=False):
    data_path = os.path.join(script_dir,"data/user_data.csv")
    if not os.path.isfile(data_path):
        df = pd.DataFrame(columns= ["user_email", "is_premium", "trial_time"])

    df = pd.read_csv(data_path)

    if all_data:
        return df
    all_user_email = df["user_email"].tolist()
    return all_user_email

def update_user_data(user_profile:dict):
    data_path = os.path.join(script_dir,"data/user_data.csv")
    if not os.path.isfile(data_path):
        df = pd.DataFrame(columns= ["user_email", "is_premium", "trial_time"])
    
    df = pd.read_csv(data_path)
    df = pd.concat([df, pd.DataFrame([user_profile])], ignore_index=True)

    df.to_csv(data_path, index=False)

def write_new_csv(input_df:pd.DataFrame):
    data_path = os.path.join(script_dir,"data/user_data.csv")
    input_df.to_csv(data_path, index=False)

if __name__ == "__main__":
    temp_food_name = "trứng chiên hành thơm ngon, mềm xốp"
    logger.info(temp_food_name)
    food_name = translate_vietnamese_name(temp_food_name)
    logger.debug(food_name)
    image_path = get_image_path(food_name)
    logger.debug(image_path)