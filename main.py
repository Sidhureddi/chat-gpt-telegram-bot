import telebot
import openai
import json

from keys import *

bot = telebot.TeleBot(telegram_token)
openai.api_key = openai_api_key

chats = {}


def chat(text, messages):
    messages.append({"role": "user", "content": text})
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )


@bot.message_handler(content_types=["text"])
def handle_text(user_input):
    chat_id = user_input.chat.id
    bot.send_chat_action(chat_id, "typing")
    if chat_id not in chats.keys():
        chats[chat_id] = [
            {"role": "system", "content": "Hello"},
        ]
    response = chat(user_input.text, chats[chat_id])
    result = response.choices[0]['message']
    chats[chat_id].append(result)
    bot.send_message(user_input.chat.id, result['content'], parse_mode="Markdown")


bot.polling()
