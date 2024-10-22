import requests
import re
import os

qiscus_app_id = os.environ.get("QISCUS_APP_ID")
qiscus_secret_key = os.environ.get("QISCUS_SECRET_KEY")

def role_finder(user_id):
    if user_id == 'system@daki-fq9mhonubqarcuy6.qiscus.com':
        return 'system'
    if user_id == 'daki-fq9mhonubqarcuy6_admin@qismo.com' or '@honestdocs.co' in user_id:
        return 'assistant'
    else:
        return 'user'

def extract_url(message):
    match = re.search(r'https?://[^\s\]]+', message)
    if match:
        return match.group(0)
    return None

def content_normaliser(comment):
    res = None
    if comment['type'] == 'file_attachment' or '[sticker]' in comment['message']:
        res = {
            'type': 'image_url',
            'image_url': {
                'url': extract_url(comment['message']),
                'detail': 'auto'
            }
        }
    else:
        res = comment['message']
    
    return res

def conversation_normaliser(comments):
    res = []
    try:
        for comment in comments:
            role = role_finder(comment['user']['user_id'])
            if role == 'system':
                continue
            else:
                message_object = {}
                message_object['content'] = content_normaliser(comment)
                message_object['role'] = role
                message_object['timestamp'] = comment['timestamp']
                res.append(message_object)
        return res
    except Exception as e:
        print(f"Unable to normalise conversation : {e}")

def fetch_chat_history(room_id:str, page_number:int):
    url = f"https://api.qiscus.com/api/v2.1/rest/load_comments?room_id={room_id}&limit=100&page={page_number}"
    headers = {
        "QISCUS-SDK-APP-ID": qiscus_app_id,
        "QISCUS-SDK-SECRET": qiscus_secret_key
    }

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        comments = data.get('results').get('comments')
        return comments
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve conversation history for room ID: {room_id} - {str(e)}")
        return None

def get_page_number(room_id:str, page_number:int):
    comments = fetch_chat_history(room_id=room_id, page_number=page_number)

    if comments:
        return get_page_number(room_id=room_id, page_number=page_number+1)
    else:
        return page_number - 1


def get_full_chat_history(room_id:str):
    page_number = get_page_number(room_id=room_id, page_number=1)
    chat_history = []

    for i in range(page_number, 0, -1):
        chats = fetch_chat_history(room_id=room_id, page_number=i)
        chats = conversation_normaliser(chats)
        chat_history.extend(chats)
    
    chat_history.sort(key=lambda chat: chat['timestamp'])
    return chat_history

chat = get_full_chat_history('260996436')

print(chat)




