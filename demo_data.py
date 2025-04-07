from datetime import datetime

# Список смоделированных обменов с фиксированными датами
exchanges = [
    {
        "date": "10.03.2025 14:30",
        "from_user": ("Алихан Калыбеков", "khandrok", "Государь, Преступление и наказание, Белые ночи"),
        "to_user": ("Саида", "LAGMAAAAN", "Маленькие женщины на англ, Стивен Кинг - доктор сон, Стигмалион - Кристина старк"),
        "book_given": "Преступление и наказание",
        "book_received": "Стивен Кинг - доктор сон",
        "status": "✅ Успешно"
    },
    {
        "date": "12.03.2025 10:15",
        "from_user": ("Диас", "ClayzDart", "Мать Ученья, Повелитель Тайн"),
        "to_user": ("Айгерим", "microkosmoos", ""),
        "book_given": "Повелитель Тайн",
        "book_received": "Доступные книги",
        "status": "✅ Успешно"
    },
    {
        "date": "12.03.2025 18:45",
        "from_user": ("Глеб Дмитриев", "glebdmitriyev", "1.000.000$ в инвестициях на пальцах, О чем я говорю, когда говорю о беге, Кемел Адам, Наедине с собой, Великий Гэтсби"),
        "to_user": ("Артемий", "werexx", "Часодеи - все части"),
        "book_given": "Великий Гэтсби",
        "book_received": "Часодеи - все части",
        "status": "✅ Успешно"
    },
    {
        "date": "18.03.2025 11:20",
        "from_user": ("Наги", "killstationexxidae", "Темная башня, дезертир, утраченные иллюзии, ванпанчмен"),
        "to_user": ("Константин", "Konstanteeeen", "Омар Хайям"),
        "book_given": "Темная башня",
        "book_received": "Омар Хайям",
        "status": "✅ Успешно"
    },
    {
        "date": "20.03.2025 16:10",
        "from_user": ("Ахметова Асылым", "asikoakhmetova", "Хочу и буду - М.Лабковский"),
        "to_user": ("амина", "amillienn", "дневник памяти"),
        "book_given": "Хочу и буду - М.Лабковский",
        "book_received": "дневник памяти",
        "status": "✅ Успешно"
    },
    {
        "date": "22.03.2025 09:30",
        "from_user": ("Дулат", "dulbl4", "48 законов власти, Метро 2033, Война и мир 4 тома"),
        "to_user": ("Tsoi", "thch0l", "Детство, Юность отрочество - толстой, Бедные люди - Достоевский"),
        "book_given": "48 законов власти",
        "book_received": "Бедные люди - Достоевский",
        "status": "✅ Успешно"
    },
    {
        "date": "25.03.2025 13:45",
        "from_user": ("Аяна", "AyankaD", "Двойник с лунной дамбы - содзи симада"),
        "to_user": ("Нурай Еркинбек", "extrareader", "Франц Кафка «Процесс»"),
        "book_given": "Двойник с лунной дамбы",
        "book_received": "Франц Кафка «Процесс»",
        "status": "✅ Успешно"
    },
    {
        "date": "28.03.2025 17:00",
        "from_user": ("Романас", "lanenotpunk", "Гарри Поттер и Философский камень"),
        "to_user": ("Мухтаркызы Мариям", "hamster_1303", ""),
        "book_given": "Гарри Поттер и Философский камень",
        "book_received": "Книги по запросу",
        "status": "✅ Успешно"
    },
    {
        "date": "30.03.2025 12:25",
        "from_user": ("Иманберді Көркем", "Y_u_zuha", "Спеший любить - Николос Спаркс"),
        "to_user": ("Алуа", "amankeldi_a", ""),
        "book_given": "Спеший любить - Николос Спаркс",
        "book_received": "Рекомендации бота",
        "status": "✅ Успешно"
    },
    {
        "date": "01.04.2025 15:40",
        "from_user": ("Айсер", "aaaiserr", ""),
        "to_user": ("Гумаева Виолетта", "justacloudygirl", ""),
        "book_given": "Личные рекомендации",
        "book_received": "Классическая литература",
        "status": "✅ Успешно"
    },
    {
        "date": "01.04.2025 10:50",
        "from_user": ("Смагулова Аделия", "Bilimqyzy", ""),
        "to_user": ("Еділұлы Асылжан", "None", ""),
        "book_given": "Научные книги",
        "book_received": "Деловая литература",
        "status": "✅ Успешно"
    },
    {
        "date": "04.04.2025 19:15",
        "from_user": ("Кабдый Айым", "Aimkhgvd", ""),
        "to_user": ("Лим Татьяна", "lim_tn", ""),
        "book_given": "Книги по инвестициям",
        "book_received": "Художественная литература",
        "status": "✅ Успешно"
    }
]

# Сортируем обмены по дате
exchanges.sort(key=lambda x: datetime.strptime(x['date'], "%d.%m.%Y %H:%M"))

# Вывод информации об обменах
print("📚 ОБМЕНЫ КНИГАМИ \n")
print(f"📅 Период: 10.03.2025 - 04.04.2025")
print("="*60)
for i, exchange in enumerate(exchanges, 1):
    print(f"\n🔄 Обмен #{i}")
    print(f"📅 Дата: {exchange['date']}")
    print(f"👤 Отправитель: {exchange['from_user'][0]} (@{exchange['from_user'][1]})")
    print(f"   📖 Книги: {exchange['from_user'][2]}")
    print(f"👤 Получатель: {exchange['to_user'][0]} (@{exchange['to_user'][1]})")
    print(f"   📖 Книги: {exchange['to_user'][2]}")
    print(f"📤 Отдал: {exchange['book_given']}")
    print(f"📥 Получил: {exchange['book_received']}")
    print(f"🟢 Статус: {exchange['status']}")
    print("="*60)

# Генерация статистики
print("\n📊 СТАТИСТИКА ОБМЕНОВ")
print("="*60)
total_exchanges = len(exchanges)
unique_users = len(set([ex['from_user'][1] for ex in exchanges] + [ex['to_user'][1] for ex in exchanges]))
print(f"• Всего обменов: {total_exchanges}")
print(f"• Уникальных участников: {unique_users}")

# Подсчет популярных книг
book_counts = {}
for ex in exchanges:
    book_counts[ex['book_given']] = book_counts.get(ex['book_given'], 0) + 1
    book_counts[ex['book_received']] = book_counts.get(ex['book_received'], 0) + 1

top_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:3]
print("\n🏆 Топ-3 популярных книги:")
for book, count in top_books:
    print(f"• {book}: {count} обменов")

print("="*60)

# Дополнительно: статистика по неделям
print("\n📅 Статистика по неделям:")
weeks = {}
for ex in exchanges:
    date = datetime.strptime(ex['date'], "%d.%m.%Y %H:%M")
    week_num = date.isocalendar()[1]
    weeks[week_num] = weeks.get(week_num, 0) + 1

for week, count in sorted(weeks.items()):
    print(f"• Неделя {week}: {count} обменов")

print("="*60)