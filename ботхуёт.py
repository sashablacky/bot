import vk_api 
import time
import random
import json
import apiai
import bs4
import requests
import os

token = "a04d1f272b7cb3ab841fbe2d1fcbe704e37fbc6dc2b36b3f99466ad05f7ece43b275c8e242fa95f8f4e78"
dlg_fl='a83553effdcb4a549dcc5fef916ba3c6'
vk = vk_api.VkApi(token=token)
vk._auth_token('a04d1f272b7cb3ab841fbe2d1fcbe704e37fbc6dc2b36b3f99466ad05f7ece43b275c8e242fa95f8f4e78')
upload = vk_api.upload.VkUpload(vk)

value = { 
"offset" : 0, 
"count": 20, 
"filter": "unanswered" 
}
'''
                img=
                msg = vk.method("messages.getConversations", value)
                user_id = msg['items'][0]['last_message']['from_id']
                img = upload.photo_messages('toster.jpg')[0]
                msg = vk.method("messages.getConversations", value)
                user_id = msg['items'][0]['last_message']['from_id']
                img = upload.photo_messages('toster.jpg')[0]                     
                photo = 'photo'+str(img['owner_id'])+'_'+str(img['id'])      
                vk.method('messages.send', {'peer_id': user_id,'random_id':random.randint(100000, 999999),'attachment':photo})
'''
'''
    a=0
    img=None
    while a<5:
        
        msg = vk.method("messages.getConversations", value)
        user_id = msg['items'][0]['last_message']['from_id']
        img = upload.photo_messages('toster.jpg')[0]                    
        a=+1
    photo = 'photo'+str(img['owner_id'])+'_'+str(img['id'])    
    vk.method('messages.send', {'peer_id': user_id,'random_id':random.randint(100000, 999999),'attachment':photo})
'''
def photo_messages(imgfile,user_id):
    msg = vk.method("messages.getConversations", value)
    user_id = msg['items'][0]['last_message']['from_id']
    img=None
    while not (img and img['owner_id'] and img['id']):
        upload_result = upload.photo_messages('toster.jpg')
        print("Результат загрузки: %s\n" % upload_result)
        img = upload_result[0]
    photo = 'photo'+str(img['owner_id'])+'_'+str(img['id'])    
    vk.method('messages.send', {'peer_id': user_id,'random_id':random.randint(100000, 999999),'attachment':photo})
  
def images(user_id):
    '''
    vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message':'прости, мои разработчики слишком тупые, чтобы я отправлял тебе картинки.НО.они оставили ссылку на реддит'+' https://www.reddit.com/r/memes/'})
    '''
    mas=[]  
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127 (Edition Campaign 76)'}
    img=requests.get('https://www.reddit.com/r/memes/', headers=headers)
    soup=bs4.BeautifulSoup(img.text,'html.parser')
    mas = soup.select('img')
    filename='toster.jpg'
    response=requests.get(mas[random.randint(1,15)]['src'])
    print(mas[random.randint(1,15)]['src'])
    
    if response.status_code==200:
        with open(filename,'w+b') as imgfile:
            imgfile.write(response.content)
        photo_messages(imgfile,user_id)
    #open(filename,'w')
    os.remove(filename)

    
def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": False,
    "buttons": [
 
    [get_button(label="весело", color="positive")],
    [get_button(label="активно", color="positive")],
    [get_button(label="грустно", color="primary")],
    [get_button(label="негативно", color="negative")],   
    [get_button(label="всё", color="default")],
 
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard2 = {
    "one_time": False,
    "buttons": [
 
    [get_button(label="Отправь картиночек", color="positive")],
    [get_button(label="Послушать музыку", color="positive")],
    [get_button(label="Отстань", color="negative")],
 
    ]
}

keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))
while True:
    messages = vk.method("messages.getConversations", value)
    print(messages)
    if messages['count'] >= 1: 
        user_id = messages['items'][0]['last_message']['from_id']
        
        print(user_id)
        for chat in messages['items']:
             msg = chat['last_message']
        request = apiai.ApiAI(dlg_fl).text_request()        
        request.lang='ru'
        request.session_id='123'
        request.query=msg['text']       
        responseJson=json.loads(request.getresponse().read().decode('utf-8'))
        response=responseJson['result']['fulfillment']['speech']
        text=response[1:].lower()
        music_id = 0
        if (response and response[0]!='&'):
            answer = response
            vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message': response})
            continue
                  
        if (response[1] == '+'):
            music_id = response[2:]
            vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message': 'Послушай ', 'attachment' : music_id})
            continue
        
        if (response[1] == '$'):
            music_id = response[2:]
            vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message': 'Послушай ', 'attachment' : music_id})
            continue
        
        if (response[1] == '*'):
            music_id = response[2:]
            vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message': 'Послушай ', 'attachment' : music_id})
            continue
        if (response[1] == '['):
            music_id = response[2:]
            vk.method('messages.send', {'peer_id':user_id, 'random_id':random.randint(100000, 999999), 'message': 'Послушай ', 'attachment' : music_id})
            continue
        
        elif text.lower() == "клавиатура":
                vk.method("messages.send", {"peer_id": user_id, "message": "Выбери кнопку!", "keyboard": keyboard2, "random_id": random.randint(1, 2147483647)})
        elif text.lower() == "послушать музыку":
                vk.method("messages.send", {"peer_id": user_id, "message": "какую пожелаете?", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        elif text.lower() == "отстань":
                vk.method("messages.send", {"peer_id": user_id, "message": "Хорошо...\nНо если ты не в духе, послушай музыку", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        elif text.lower() == "всё":
                vk.method("messages.send", {"peer_id": user_id, "message": "оке", "keyboard": keyboard2, "random_id": random.randint(1, 2147483647)})
        elif text.lower()=='отправь картиночек':
                images(user_id)
                

        time.sleep(1)
 
