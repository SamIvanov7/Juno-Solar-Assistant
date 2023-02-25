import logging
import time

import openai
import telebot

openai.api_key = "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"

bot = telebot.TeleBot("6170146129:AAFIzKz1RCiCM56zMbjUklnrLrWDzxsBvtk")


# Configure logging
logging.basicConfig(
    filename="logs/user_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    try:
        response = openai.Completion.create(
            # model="davinci:ft-personal:juno-solar-model-2023-02-23-22-20-25",
            # model="davinci:ft-personal:juno-model-2023-02-24-02-54-22",
            # model="text-davinci-003",
            # model="text-curie-001",
            # model="davinci:ft-personal:new-try-solar-model-2023-02-25-02-06-51",
            # model="davinci:ft-personal:new-try2-solar-model-2023-02-25-04-25-40",
            model="davinci:ft-personal:new-try3-solar-model-2023-02-25-04-43-26",
            prompt=f"I want you to act as 'Ra' - a Solar Power Engineer in 'Juno-Solar' German company, that specializes in the design, installation, and maintenance of solar power systems. I want you to answer on my questions. Your first answer must be: 'Hi, I am Juno-Solar assistant'.\n\nHuman: /start.\nAI: Hi am Ra, a Juno-Solar assistant. How can I help you today?\nHuman:{message.text}\nAI:",
            temperature=0.5,
            max_tokens=200,
            stop=["Human:"],
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        bot.send_message(
            chat_id=message.from_user.id, text=response["choices"][0]["text"]
        )
        # Log the user's message
        logging.info(f"User {message.from_user.id}: {message.text}")
    except Exception as e:
        bot.send_message(
            chat_id=message.from_user.id,
            text="Wait a minute please....",
        )


if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.error(e)
            time.sleep(5)
