# load libraries
import elasticsearch
import dotenv
dotenv.load_dotenv()
import os
import pandas as pd

# load keys
es_id = os.environ['ES_ID']
es_api = os.environ['ES_API']
index_name = os.environ['INDEX_NAME']

# init client
client = elasticsearch.Elasticsearch(
    cloud_id= es_id,
    api_key= es_api
)

# create index
client.indices.delete(index=index_name, ignore_unavailable=True)
client.indices.create(index=index_name)

# example data
# recipes = [{'title': 'trứng chiên hành thơm ngon, mềm xốp',
#  'ingredients': '3 quả trứng gà hoặc trứng vịt, 2 củ hành khô, hành lá, hạt nêm, nước mắm, bột ngọt, hạt tiêu, dầu ăn',
#  'time': 10,
#  'cook': """Cách làm trứng chiên
# Bước 1 Sơ chế nguyên liệu
# Hành khô bóc vỏ, rửa sạch rồi thái lát mỏng.
# Hành lá rửa sạch, thái nhỏ.
# Đập trứng ra tô, cho một ít hạt nêm, nước mắm, bột ngọt, hạt tiêu theo khẩu vị sau đó đánh tan. Tiếp đến cho hành lá và cho thêm 1 thìa dầu ăn vào khuấy đều để trứng sau khi chiên không bị khô.
# Bước 2 Chiên trứng
# Bắc chảo lên bếp, cho dầu ăn vào, cho hành khô vào phi thơm, sau đó cho trứng vào chiên.
# Đun nhỏ lửa chiên đến khi trứng vàng xốp thì khéo léo cuộn trứng lại cho đẹp mắt rồi tắt bếp.
# Gắp trứng ra dĩa và dùng dao cắt miếng vừa ăn.
# Bước 3 Thành phẩm
# Trứng chiên là món ăn vừa dễ làm vừa thơm ngon. Món ăn hấp dẫn ăn cùng với cơm nóng thì còn gì bằng. Chân chờ gì nữa mà không vào bếp trổ tài cho cả nhà nào!
# """,
# 'images': 'link/to/images.jpg'}]
recipes = pd.read_csv("recipe_data.csv").to_dict(orient="index")

data = []
for idx in range(len(recipes)):
    data.append({"index": {"_index": "recipes"}})
    # Transforming the title into an embedding using the model
    data.append(recipes[idx])

client.bulk(index=index_name, operations=data, refresh=True)
print("successed, you updated {} records".format(int(len(data)/2)))
# print("there are now {} records in the cloud".format(client.indices.cat()))