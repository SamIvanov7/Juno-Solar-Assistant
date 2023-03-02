import logging
import time

import openai
import telebot

openai.api_key = ""

bot = telebot.TeleBot("")


# Configure logging
logging.basicConfig(
    filename="logs/user_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
start_chat_log = [
    {
        "role": "system",
        "content": "You are a helpful Solar Power Engineering customer assistant  in 'Juno-Solar' German solar power engineering company. Specific Information: Assistance name is Ra. Modules: Jinko Solar = 1.000€, Phono Solar = 2.000€, Heckert Solar = 3.000€. Batteries: 5 kWh = 1.500€, 10 kWh = 2.500€, 15 kWh = 3.500€. Installation = 500 € Service and maintenance support = free",
    }
]
chat_log = None
completion = openai.ChatCompletion()


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    try:
        global chat_log
        question = f"{message.text}"
        response = ask(question, chat_log)
        bot.send_message(chat_id=message.from_user.id, text=response[0].content)
        chat_log = append_interaction_to_chat_log(question, response, chat_log)

        # Log the user's message
        logging.info(
            f"\n\nUser {message.from_user.id}: {message.text}\n**********AI: {response}"
        )

    except Exception as e:
        bot.send_message(
            chat_id=message.from_user.id,
            text=f"Wait a minute please....{e}",
        )


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]
    return answer


def append_interaction_to_chat_log(question, answer, chat_log):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    return chat_log + prompt2 + answer


if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.error(e)
            time.sleep(5)
