
import pathlib
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Body, HTTPException
from starlette.middleware.cors import CORSMiddleware
from src.engine import SearchEngine
from src.momo_wallet import gen_momo_payment_url, get_order_status
from src.utils import get_image_path
from loguru import logger
wd = pathlib.Path(__file__).parent.resolve()
load_dotenv(dotenv_path=os.path.join(wd,'.env'))

from pydantic import BaseModel

class UserEmail(BaseModel):
    user_email:str

class IngredientModel(BaseModel):
    user_input:str

class RecipeModel(BaseModel):
    title:str
    ingredients:str
    time:int
    cook:str
    images:str

es_id = os.environ.get("ES_ID")
es_api = os.environ.get("ES_API")
index_name = os.environ.get("INDEX_NAME")
user_index = os.environ.get("USER_INDEX")

search_engine = SearchEngine(
    id_name= es_id,
    api_key= es_api,
    index_name= index_name,
    user_index= user_index
)



app = FastAPI()

origins = ["*"]
 
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

### Standard health checks
@app.get("/", tags=["Health Check"])
async def root():
    return "hello world!"

@app.get("/get")
async def get_config():
    return

@app.get("/login", tags = ['login/signup'])
async def login():
    return {"status": True, "message": "authorized"}

@app.get("/signup", tags = ['login/signup'])
async def signup():
    return {"status":True, "message": "signup completed"}

@app.get("/trend", tags=['index'])
async def trend():
    return [{
        "recipe_name": "recipe_name",
        "time_estimate": "time_estimate",
        "recipe_img": "recipe_img"
    }]

@app.get("/search_one_feature", tags=['search'])
async def search_one_feature(user_input:IngredientModel):
    print("user_input:", user_input)
    results = search_engine.search_one_feature(input_query= user_input.user_input, input_feature= "ingredients")
    if results != {}:
        return results
    return {}

# [{'_index': 'recipes',
#   '_id': 'T3tJs48BIJMJcnTjzG8I',
#   '_score': 0.2876821,
#   '_ignored': ['cook.keyword'],
#   '_source': {'title': 'trứng chiên hành thơm ngon, mềm xốp',
#    'ingredients': '3 quả trứng gà hoặc trứng vịt, 2 củ hành khô, hành lá, hạt nêm, nước mắm, bột ngọt, hạt tiêu, dầu ăn',
#    'time': 10,
#    'cook': 'Cách làm trứng chiên\nBước 1 Sơ chế nguyên liệu\nHành khô bóc vỏ, rửa sạch rồi thái lát mỏng.\nHành lá rửa sạch, thái nhỏ.\nĐập trứng ra tô, cho một ít hạt nêm, nước mắm, bột ngọt, hạt tiêu theo khẩu vị sau đó đánh tan. Tiếp đến cho hành lá và cho thêm 1 thìa dầu ăn vào khuấy đều để trứng sau khi chiên không bị khô.\nBước 2 Chiên trứng\nBắc chảo lên bếp, cho dầu ăn vào, cho hành khô vào phi thơm, sau đó cho trứng vào chiên.\nĐun nhỏ lửa chiên đến khi trứng vàng xốp thì khéo léo cuộn trứng lại cho đẹp mắt rồi tắt bếp.\nGắp trứng ra dĩa và dùng dao cắt miếng vừa ăn.\nBước 3 Thành phẩm\nTrứng chiên là món ăn vừa dễ làm vừa thơm ngon. Món ăn hấp dẫn ăn cùng với cơm nóng thì còn gì bằng. Chân chờ gì nữa mà không vào bếp trổ tài cho cả nhà nào!\n',
#    'images': 'link/to/images.jpg'}}]
# import urllib.parse

# def decode_url(encoded_string):
#     return urllib.parse.unquote(encoded_string)

@app.post("/search_multi_features", tags=['search'])
async def search_multi_features(user_input:IngredientModel):
    # query = decode_url(encoded_string= user_input)
    # results = search_engine.search_many_feature(input_query = query, input_features= ["title", "ingredients"])
    results = search_engine.search_many_feature(input_query = user_input.user_input, input_features= ["title", "ingredients"])
    if results != []:
        for result in results:
            logger.debug(result['_source']['title'])
            image_path = get_image_path(input_recipe_name= result['_source']['title'])
            result['_source']['images'] = image_path.strip()
            logger.debug(result['_source']['images'])
        return results
    return []

@app.post("/update_recipes", tags = ["search"])
async def update_recipes(user_input:RecipeModel):
    result = search_engine.update_recipe(input_recipe= user_input)
    if result == "Success":
        return "True"
    else: return "False"

# [{'_index': 'recipes',
#   '_id': 'T3tJs48BIJMJcnTjzG8I',
#   '_score': 0.2876821,
#   '_ignored': ['cook.keyword'],
#   '_source': {'title': 'trứng chiên hành thơm ngon, mềm xốp',
#    'ingredients': '3 quả trứng gà hoặc trứng vịt, 2 củ hành khô, hành lá, hạt nêm, nước mắm, bột ngọt, hạt tiêu, dầu ăn',
#    'time': 10,
#    'cook': 'Cách làm trứng chiên\nBước 1 Sơ chế nguyên liệu\nHành khô bóc vỏ, rửa sạch rồi thái lát mỏng.\nHành lá rửa sạch, thái nhỏ.\nĐập trứng ra tô, cho một ít hạt nêm, nước mắm, bột ngọt, hạt tiêu theo khẩu vị sau đó đánh tan. Tiếp đến cho hành lá và cho thêm 1 thìa dầu ăn vào khuấy đều để trứng sau khi chiên không bị khô.\nBước 2 Chiên trứng\nBắc chảo lên bếp, cho dầu ăn vào, cho hành khô vào phi thơm, sau đó cho trứng vào chiên.\nĐun nhỏ lửa chiên đến khi trứng vàng xốp thì khéo léo cuộn trứng lại cho đẹp mắt rồi tắt bếp.\nGắp trứng ra dĩa và dùng dao cắt miếng vừa ăn.\nBước 3 Thành phẩm\nTrứng chiên là món ăn vừa dễ làm vừa thơm ngon. Món ăn hấp dẫn ăn cùng với cơm nóng thì còn gì bằng. Chân chờ gì nữa mà không vào bếp trổ tài cho cả nhà nào!\n',
#    'images': 'link/to/images.jpg'}}]


@app.post("/get_momo_payment_url", tags =['momo'])
async def get_momo_payment_url(user_email:str)->tuple[str, str]:
    print(user_email)
    # payUrl, orderId = search_engine.generate_momo_payment_url(input_user_email=user_email)
    payUrl, orderId = gen_momo_payment_url()
    return payUrl, orderId

@app.get("/check_order_status", tags=['momo'])
async def check_order_status(order_id:str):
    response = get_order_status(input_order_id= order_id)
    if response == 0:
        return "True"
    else: 
        print("check_order_status code:", response)
        return "False"


@app.post("/check_if_user_already_exist", tags= ['user'])
async def check_if_user_already_exist(user_email:str):
    print(user_email)
    return str(search_engine.check_user(input_user_email= user_email))

@app.post("/get_trial_time_left", tags= ['user'])
async def get_trial_time_left(user_email:UserEmail)->int:
    result = search_engine.check_trial_time(input_user_email= user_email.user_email)
    print("trial time left: ", result)
    return result

@app.post("/update_trial_time_left", tags= ['user'])
async def update_trial_time_left(user_email:UserEmail)->None:
    return search_engine.update_trial_time(input_user_email = user_email.user_email)


@app.post("/get_user_premium_status", tags=['user'])
async def get_user_premium_status(user_email:UserEmail):
    print(user_email)
    return str(search_engine.check_premium_status(input_user_email= user_email.user_email))