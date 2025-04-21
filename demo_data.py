from datetime import datetime

# Список смоделированных обменов с датами с 15 по 20 апреля
exchanges = [
    {
        "date": "15.04.2025 11:00",
        "from_user": ("Айгерим", "microkosmoos", "Скотный двор, Мастер и Маргарита"),
        "to_user": ("Диас", "ClayzDart", "451 градус по Фаренгейту"),
        "book_given": "Скотный двор",
        "book_received": "451 градус по Фаренгейту",
        "status": "✅ Успешно"
    },
    {
        "date": "16.04.2025 14:45",
        "from_user": ("Саида", "LAGMAAAAN", "Дюна, Маленькие женщины на англ"),
        "to_user": ("Аяна", "AyankaD", "Мемуары гейши"),
        "book_given": "Дюна",
        "book_received": "Мемуары гейши",
        "status": "✅ Успешно"
    },
    {
        "date": "17.04.2025 09:30",
        "from_user": ("Алихан Калыбеков", "khandrok", "Государь, Кандид, Преступление и наказание"),
        "to_user": ("Ахметова Асылым", "asikoakhmetova", "Маленький принц, Виноваты звезды"),
        "book_given": "Кандид",
        "book_received": "Маленький принц",
        "status": "✅ Успешно"
    },
    {
        "date": "17.04.2025 17:20",
        "from_user": ("Tsoi", "thch0l", "Детство, Бедные люди - Достоевский"),
        "to_user": ("Глеб Дмитриев", "glebdmitriyev", "Наедине с собой"),
        "book_given": "Детство",
        "book_received": "Наедине с собой",
        "status": "✅ Успешно"
    },
    {
        "date": "18.04.2025 13:15",
        "from_user": ("Нурай Еркинбек", "extrareader", "Портрет Дориана Грея"),
        "to_user": ("Наги", "killstationexxidae", "Утраченные иллюзии"),
        "book_given": "Портрет Дориана Грея",
        "book_received": "Утраченные иллюзии",
        "status": "✅ Успешно"
    },
    {
        "date": "19.04.2025 16:00",
        "from_user": ("Гумаева Виолетта", "justacloudygirl", "Анна Каренина"),
        "to_user": ("Алуа", "amankeldi_a", "Спеши любить"),
        "book_given": "Анна Каренина",
        "book_received": "Спеши любить",
        "status": "✅ Успешно"
    },
    {
        "date": "20.04.2025 10:30",
        "from_user": ("Лим Татьяна", "lim_tn", "Художественная литература"),
        "to_user": ("Кабдый Айым", "Aimkhgvd", "Книги по саморазвитию"),
        "book_given": "Художественная литература",
        "book_received": "Книги по саморазвитию",
        "status": "✅ Успешно"
    }
]

# Сортировка по дате
exchanges.sort(key=lambda x: datetime.strptime(x['date'], "%d.%m.%Y %H:%M"))

# Вывод обменов
print("📚 ОБМЕНЫ КНИГАМИ \n")
print(f"📅 Период: 15.04.2025 - 20.04.2025")
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

# Статистика
print("\n📊 СТАТИСТИКА ОБМЕНОВ")
print("="*60)
total_exchanges = len(exchanges)
unique_users = len(set([ex['from_user'][1] for ex in exchanges] + [ex['to_user'][1] for ex in exchanges]))
print(f"• Всего обменов: {total_exchanges}")
print(f"• Уникальных участников: {unique_users}")

# Подсчёт популярных книг
book_counts = {}
for ex in exchanges:
    book_counts[ex['book_given']] = book_counts.get(ex['book_given'], 0) + 1
    book_counts[ex['book_received']] = book_counts.get(ex['book_received'], 0) + 1

top_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:3]
print("\n🏆 Топ-3 популярных книги:")
for book, count in top_books:
    print(f"• {book}: {count} обменов")

print("="*60)

# Статистика по неделям
print("\n📅 Статистика по неделям:")
weeks = {}
for ex in exchanges:
    date = datetime.strptime(ex['date'], "%d.%m.%Y %H:%M")
    week_num = date.isocalendar()[1]
    weeks[week_num] = weeks.get(week_num, 0) + 1

for week, count in sorted(weeks.items()):
    print(f"• Неделя {week}: {count} обменов")

print("="*60)
