import openai
import logging
import os
from dotenv import load_dotenv, find_dotenv
import telebot

ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE)

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_api_key = str(os.getenv("TELEGRAM_API_KEY"))

bot = telebot.TeleBot(telegram_api_key)

start_chat_log = [
    {
        "role": "system",
        "content": """

          ### prompt message ###

          
                     """,
    }
]

chat_log = None
completion = openai.ChatCompletion()



def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(  # type: ignore
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]  # type: ignore
    return answer


def append_interaction_to_chat_log(question, answer, chat_log):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    return chat_log + prompt2 + answer


def handle_message(text):
    try:
        global chat_log
        question = f"{text}"
        response = ask(question, chat_log)
        chat_log = append_interaction_to_chat_log(question, response, chat_log)

        logging.info(f"\n\nUser {text}\n**********AI: {response}")

        return response[0].content

    except Exception as e:
        chat_log = start_chat_log
        return f"Wait a minute please....{e}"


def get_chat_bot_response(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-4",
    )
    answer = [response.choices[0].message]  # type: ignore
    return answer

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = handle_message(message.text)
    bot.reply_to(message, response)

bot.polling()