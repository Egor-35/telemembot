import telebot
import random
import os

# Токен вашего бота
TOKEN = 'Впишите токен вашего бота'
# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /add
@bot.message_handler(commands=['add'])
def handle_add(message):
    bot.reply_to(message, "Отправьте изображение.")

# Обработчик фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем файл изображения
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Находим номер следующего изображения
    existing_images = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]
    if existing_images:
        # Извлекаем номера изображений и находим максимальный
        image_numbers = [int(f.split('mem')[1].split('.')[0]) for f in existing_images if f.startswith('mem')]
        image_counter = max(image_numbers) + 1  # Увеличиваем на 1
    else:
        image_counter = 1  # Если папка пуста, начинаем с 1

    # Формируем имя файла на основе счетчика
    image_name = f'images/mem{image_counter}.jpg'

    # Сохраняем изображение
    with open(image_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, f"Мем сохранен как {image_name}!")


@bot.message_handler(commands=['mem'])
def send_mem(message):
    # Получаем список изображений из папки 'images'
    images = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]
    
    if images:  # Если есть изображения
        with open(os.path.join('images', random.choice(images)), 'rb') as f:
            bot.send_photo(message.chat.id, f)  # Отправляем изображение
    else:
        bot.send_message(message.chat.id, "Мемов нет.")  # Папка пуста

bot.infinity_polling()
