import pandas as pd
def load_csv_data(input_link:str)-> pd.DataFrame:
    df = pd.read_csv(input_link)
    df = df.drop_duplicates()
    df.columns  = ["title", "ingredients", "time", "cook", "images"]

    return df

def dataframe_to_json(input_dataframe:pd.DataFrame)-> dict:
    json_str = input_dataframe.to_json(orient='records', lines=False)
    return json_str

def pretty_response(response):
    if len(response["hits"]["hits"]) == 0:
        print("Your search returned no results.")
    else:
        for hit in response["hits"]["hits"]:
            id = hit["_id"]
            score = hit["_score"]
            title = hit["_source"]["title"]
            ingredients = hit["_source"]["ingredients"]
            cook_time = hit["_source"]["time"]
            cook = hit["_source"]["cook"]
            images = hit["_source"]["images"]
            pretty_output = f"\nID: {id}\nTitle: {title}\ingredients: {ingredients}\cook_time: {cook_time}\cook: {cook}\images: {images}\nScore: {score}"
            print(pretty_output)