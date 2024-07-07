import json
import urllib
import uuid
import requests
import hmac
import hashlib

# parameters send to MoMo get get payUrl
endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
order_status_endpoint = "https://test-payment.momo.vn/v2/gateway/api/query"
partnerCode = "MOMO"
accessKey = "F8BBA842ECF85"
secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
orderInfo = "pay with MoMo"
redirectUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
# redirectUrl = "https://localhost:5173/thanks-premium"
ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
amount = "50000"
orderId = str(uuid.uuid4())
requestId = str(uuid.uuid4())
requestType = "captureWallet"
extraData = ""  # pass empty value or Encode base64 JsonString

# before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
# &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
# &requestType=$requestType
rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
signature = h.hexdigest()


data = {
    'partnerCode': partnerCode,
    'partnerName': "Test",
    'storeId': "MomoTestStore",
    'requestId': requestId,
    'amount': amount,
    'orderId': orderId,
    'orderInfo': orderInfo,
    'redirectUrl': redirectUrl,
    'ipnUrl': ipnUrl,
    'lang': "vi",
    'extraData': extraData,
    'requestType': requestType,
    'signature': signature
}

data_order_id = {
    'partnerCode': partnerCode,
    'requestId': requestId,
    'orderId': orderId,
    'signature': signature,
    'lang': "vi",
}

clen = len(data)

def gen_momo_payment_url() -> tuple[str, str]:
    print(signature)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)}) 
    response = response.json()
    return response['payUrl'], response['orderId']

def get_order_status(input_order_id:str)->int:
    data_order_id["orderId"] = input_order_id
    response = requests.post(order_status_endpoint, data = data_order_id, headers={'Content-Type': 'application/json'})
    response = response.json()
    result = response.get("resultCode")
    return result
