from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 1365157 # Replace this with your own api_id
api_hash = '0187ea10ecb1e79c7c7e3a5e0cddbb46' # Replace this with your own api_hash
phone = '+13127246350' # Your phone number goes here with the area code and + 
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)


for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
print('Parsing the following groups:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

def get(chat_num):
    #print(chat_num)
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
     
    result = client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash = 0
             ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    g_index = chat_num
    target_group=groups[int(g_index)]
    filename = target_group.title 
    print('Fetching Members from {} ...'.format(filename))
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving In file...')
    #print(target_group.title)
    filename = target_group.title 
    with open(("{}.csv".format(filename)),"w",encoding='UTF-8') as f:

        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print('Members scraped successfully from {} .'.format(filename))

chat_list_index = list(range(len(chats)))

for x in chat_list_index:
    try: 
        get(x)
    except:
        print("No more groups.", end = " ")
print("Done")
