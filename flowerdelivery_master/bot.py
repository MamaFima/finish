import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowerdelivery_master.settings')  # Замените на правильный путь к settings
django.setup()

import asyncio
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command
from config import TELEGRAM_BOT_TOKEN
from django.utils import timezone
import xlsxwriter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from django.conf import settings
from asgiref.sync import sync_to_async
from django.db.models import F, Sum, Count
from aiogram.types import InputFile
from aiogram.types import FSInputFile
import matplotlib as plt
import pandas as pd
from datetime import timedelta, date
from orders.models import Order, Product  # Импортируем необходимые модели
from io import BytesIO



# Импортируем нужные модели после настройки Django
from orders.models import Order

# Настройка бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()  # Создаем экземпляр Router отдельно
dp.include_router(router)  # Подключаем router к диспетчеру




# Команда /start с приветствием
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать в бот магазина FlowerDelivery! 🌸\n\n"
        "Я помогу вам управлять заказами и просматривать аналитику продаж.\n"
        "Для списка доступных команд отправьте /help."
    )

# Команда /help с описанием всех функций
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "Вот список доступных команд:\n\n"
        "/start - Приветственное сообщение и информация о боте\n"
        "/help - Описание всех доступных команд\n"
        "/orders - Показать все заказы и их статусы\n"
        "/take_order - Взять заказ в работу\n"
        "/sales_report - Получить расширенный текстовый отчет по продажам\n"
        "/sales_chart - Показать график популярности букетов\n\n"
        "Если у вас есть вопросы, просто выберите нужную команду и следуйте инструкциям."
    )




# Функция для получения заказов с асинхронным доступом
@dp.message(Command("orders"))
async def list_orders(message: Message):
    orders = await sync_to_async(list)(Order.objects.select_related('product').all())
    if not orders:
        await message.answer("Нет активных заказов.")
        return

    response = "Активные заказы:\n\n"
    for order in orders:
        product_name = await sync_to_async(lambda: order.product.name)()
        response += (
            f"Заказ №{order.id}\nПродукт: {product_name}\n"
            f"Получатель: {order.recipient_name}\nТелефон: {order.recipient_phone}\n"
            f"Адрес доставки: {order.delivery_address}\n"
            f"Дата доставки: {order.delivery_date} Время: {order.delivery_time}\n"
            f"Статус: {order.get_status_display()}\n\n"
        )
    await message.answer(response)


# Команда для выбора заказа
@dp.message(Command("update_order"))
async def choose_order_for_update(message: types.Message):
    orders = await sync_to_async(list)(Order.objects.filter(status="ordered"))
    if not orders:
        await message.answer("Нет заказов для обновления статуса.")
        return

    # Создаем клавиатуру с кнопками заказов
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for order in orders:
        button = InlineKeyboardButton(text=f"Заказ №{order.id}", callback_data=f"select_order:{order.id}")
        keyboard.inline_keyboard.append([button])

    await message.answer("Выберите заказ для обновления статуса:", reply_markup=keyboard)

# Обработчик для команды выбора заказа
@router.callback_query(lambda c: c.data and c.data.startswith("select_order"))
async def select_order_callback(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(":")[1]
    order = await sync_to_async(Order.objects.get)(id=order_id)

    # Создаем клавиатуру для изменения статуса заказа
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="На доставке", callback_data=f"update_status:delivery:{order_id}")],
            [InlineKeyboardButton(text="Выполнен", callback_data=f"update_status:completed:{order_id}")]
        ]
    )

    await callback_query.message.answer(
        f"Вы выбрали заказ №{order.id}.\nТекущий статус: {order.get_status_display()}.\nВыберите новый статус:",
        reply_markup=keyboard
    )

# Обработчик для обновления статуса заказа
@router.callback_query(lambda c: c.data and c.data.startswith("update_status"))
async def update_order_status_callback(callback_query: types.CallbackQuery):
    _, new_status, order_id = callback_query.data.split(":")
    order = await sync_to_async(Order.objects.get)(id=order_id)

    # Обновляем статус заказа
    order.status = new_status
    await sync_to_async(order.save)()

    # Отправляем подтверждение
    await callback_query.message.answer(f"Статус заказа №{order.id} обновлен на: {order.get_status_display()}.")


@dp.message(Command("sales_report"))
async def sales_report(message: types.Message):
    now = timezone.now()

    # Получение заказов за разные периоды и удаление таймзоны у дат
    async def get_orders_without_timezone(period):
        orders = await sync_to_async(list)(
            Order.objects.filter(created_at__gte=now - timezone.timedelta(days=period))
            .values('id', 'created_at', 'product__name', 'product__price')
        )
        for order in orders:
            order['created_at'] = order['created_at'].replace(tzinfo=None)  # Убираем таймзону
        return orders

    # Данные для отчетов за неделю, месяц и год
    orders_week = await get_orders_without_timezone(7)
    orders_month = await get_orders_without_timezone(30)
    orders_year = await get_orders_without_timezone(365)

    # Создаем текстовый отчет
    week_text, week_revenue = await format_order_details(orders_week)
    month_text, month_revenue = await format_order_details(orders_month)
    year_text, year_revenue = await format_order_details(orders_year)

    report_text = (
        f"Отчет по продажам:\n\n"
        f"За последнюю неделю:\n{week_text}\nОбщая сумма: {week_revenue} руб\n\n"
        f"За последний месяц:\n{month_text}\nОбщая сумма: {month_revenue} руб\n\n"
        f"За последний год:\n{year_text}\nОбщая сумма: {year_revenue} руб"
    )
    await message.answer(report_text)

async def format_order_details(orders):
    orders_text = ""
    total_revenue = 0
    order_count = 0  # Счетчик заказов

    for order in orders:
        order_total = order['product__price']  # Считаем общую стоимость
        total_revenue += order_total
        order_count += 1
        orders_text += (
            f"ID заказа: {order['id']}\n"
            f"Дата: {order['created_at']:%Y-%m-%d %H:%M}\n"
            f"Товар: {order['product__name']}\n"
            f"Стоимость: {order_total} руб\n\n"
        )

    summary_text = f"Количество заказов: {order_count}, на общую сумму: {total_revenue} руб\n\n"
    return summary_text + orders_text, total_revenue


# Функция для построения графика популярности букетов
import matplotlib.pyplot as plt
from io import BytesIO
from aiogram.types import BufferedInputFile


@dp.message(Command("sales_chart"))
async def sales_chart(message: types.Message):
    # Подсчитываем популярность букетов
    async def get_product_counts(period):
        orders = await sync_to_async(list)(
            Order.objects.filter(created_at__gte=now - timezone.timedelta(days=period))
            .values('product__name')
        )
        product_counts = {}
        for order in orders:
            product_name = order['product__name']
            if product_name in product_counts:
                product_counts[product_name] += 1
            else:
                product_counts[product_name] = 1
        return product_counts

    now = timezone.now()
    week_counts = await get_product_counts(7)
    month_counts = await get_product_counts(30)
    year_counts = await get_product_counts(365)

    # Получаем уникальные имена букетов для упорядочения данных
    product_names = set(week_counts.keys()).union(month_counts.keys(), year_counts.keys())

    # Упорядочиваем данные для графика
    week_values = [week_counts.get(name, 0) for name in product_names]
    month_values = [month_counts.get(name, 0) for name in product_names]
    year_values = [year_counts.get(name, 0) for name in product_names]

    # Создаем график
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    x = range(len(product_names))

    # Отображаем данные с цветовой дифференциацией
    ax.bar([i - bar_width for i in x], week_values, width=bar_width, label="Неделя", color="blue")
    ax.bar(x, month_values, width=bar_width, label="Месяц", color="orange")
    ax.bar([i + bar_width for i in x], year_values, width=bar_width, label="Год", color="green")

    # Настройка графика
    ax.set_xticks(x)
    ax.set_xticklabels(product_names, rotation=45, ha="right")
    ax.set_title("Популярность букетов")
    ax.set_xlabel("Название букета")
    ax.set_ylabel("Количество заказов")
    ax.legend()

    # Сохранение графика в буфер
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Отправляем график как фото
    await message.answer_photo(photo=BufferedInputFile(buf.getvalue(), filename="popularity_chart.png"),
                               caption="График популярности букетов за неделю, месяц и год")


# Основная функция запуска бота
async def main():
    try:
        print("Бот запущен...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
