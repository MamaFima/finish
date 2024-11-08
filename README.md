
# Описание проекта

## FlowerDelivery - сервис доставки цветов и аналитики

FlowerDelivery — это веб-приложение на базе Django для заказа и управления доставкой цветов с интеграцией Telegram-бота для сотрудников. Проект разработан с целью автоматизации обработки заказов, управления статусами и предоставления аналитики.

### Основные функции

1. **Веб-сайт**: 
   - Просмотр каталога букетов, добавление отзывов и оформление заказов.
   - Личный кабинет для пользователей, где отображается история заказов и статусы.
   - Админ-панель для управления товарами и заказами.

2. **Telegram-бот для сотрудников**:
   - Сотрудники могут получать данные о заказах и управлять статусами через бота.
   - Бот предоставляет аналитику, отчеты и экспорт данных о заказах.

### Сценарии использования

1. **Для пользователей**:
   - Пользователи могут зарегистрироваться на сайте, просматривать каталог, оставлять отзывы и делать заказы.
   - Личный кабинет позволяет отслеживать статусы, повторять прошлые заказы и оставлять отзывы.

2. **Для администраторов и сотрудников**:
   - Администраторы управляют каталогом и заказами через админ-панель.
   - Сотрудники используют Telegram-бота для работы с заказами и управления статусами.

3. **Для аналитики**:
   - Бот генерирует отчеты по продажам, популярности букетов и активности за разные периоды.
   - Аналитика экспортируется в Excel и визуализируется в виде графиков.

### Структура проекта

- **Django проект**: основной веб-интерфейс с моделями данных, шаблонами и админ-панелью.
- **Приложение `catalog`**: управление каталогом букетов, отображением и отзывами.
- **Приложение `orders`**: обработка заказов и функциональность Telegram-бота.
- **Приложение `accounts`**: регистрация, аутентификация и личные кабинеты.
- **Telegram-бот**: отдельный скрипт на базе Aiogram для работы с базой заказов и предоставления аналитики.

---

# Project Description

## FlowerDelivery - Flower Delivery and Analytics Service

FlowerDelivery is a Django-based web application for ordering and managing flower delivery, integrated with a Telegram bot for staff operations. The project aims to automate order processing, status management, and provide analytics.

### Key Features

1. **Website**:
   - Browse bouquet catalog, add reviews, and place orders.
   - Personal user accounts to track order history and statuses.
   - Admin panel for managing products and orders.

2. **Telegram Bot for Employees**:
   - Employees receive order data and manage statuses through the bot.
   - The bot provides analytics, reports, and order data export.

### Usage Scenarios

1. **For Customers**:
   - Customers can register, browse the catalog, leave reviews, and place orders.
   - Personal account allows order tracking, reordering, and reviewing.

2. **For Administrators and Employees**:
   - Administrators manage the catalog and orders via the admin panel.
   - Employees use the Telegram bot to access order data and update statuses.

3. **For Analytics**:
   - The bot generates sales reports and bouquet popularity analytics.
   - Analytics are exported to Excel and visualized with charts.

### Project Structure

- **Django Project**: Main web interface with data models, templates, and admin panel.
- **`catalog` app**: Manages bouquet catalog, display, and reviews.
- **`orders` app**: Handles order processing and Telegram bot functionality.
- **`accounts` app**: Manages user registration, authentication, and profiles.
- **Telegram Bot**: A separate Aiogram-based script to interact with the order database and provide analytics.
