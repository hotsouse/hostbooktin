import json
from datetime import datetime
from collections import defaultdict

# Файл для хранения данных об обменах
EXCHANGES_FILE = "real_exchanges.json"

def load_exchanges():
    """Загружает историю обменов из файла"""
    try:
        with open(EXCHANGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_exchange(from_user, to_user, book_given, book_received):
    """Сохраняет новый обмен в файл"""
    exchanges = load_exchanges()
    
    new_exchange = {
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "from_user": from_user,
        "to_user": to_user,
        "book_given": book_given,
        "book_received": book_received,
        "status": "✅ Успешно"
    }
    
    exchanges.append(new_exchange)
    
    with open(EXCHANGES_FILE, "w", encoding="utf-8") as f:
        json.dump(exchanges, f, ensure_ascii=False, indent=2)
    
    return new_exchange

def get_exchange_statistics():
    """Возвращает статистику по обменам"""
    exchanges = load_exchanges()
    
    if not exchanges:
        return {
            "total_exchanges": 0,
            "unique_users": 0,
            "top_books": [],
            "weekly_stats": {}
        }
    
    # Сортируем обмены по дате
    exchanges.sort(key=lambda x: datetime.strptime(x['date'], "%d.%m.%Y %H:%M"))
    
    # Статистика
    stats = {
        "total_exchanges": len(exchanges),
        "unique_users": len(set(
            [ex['from_user'][1] for ex in exchanges if ex['from_user'][1] != "None"] + 
            [ex['to_user'][1] for ex in exchanges if ex['to_user'][1] != "None"]
        )),
        "top_books": [],
        "weekly_stats": defaultdict(int)
    }
    
    # Подсчет популярных книг
    book_counts = defaultdict(int)
    for ex in exchanges:
        book_counts[ex['book_given']] += 1
        book_counts[ex['book_received']] += 1
    
    stats["top_books"] = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Статистика по неделям
    for ex in exchanges:
        date = datetime.strptime(ex['date'], "%d.%m.%Y %H:%M")
        week_num = date.isocalendar()[1]
        stats["weekly_stats"][week_num] += 1
    
    return stats

def print_exchanges():
    """Выводит информацию об обменах в консоль (аналогично вашему примеру)"""
    exchanges = load_exchanges()
    stats = get_exchange_statistics()
    
    print("📚 РЕАЛЬНЫЕ ОБМЕНЫ КНИГАМИ\n")
    
    if not exchanges:
        print("Пока не было совершено ни одного обмена.")
        return
    
    first_date = datetime.strptime(exchanges[0]['date'], "%d.%m.%Y %H:%M")
    last_date = datetime.strptime(exchanges[-1]['date'], "%d.%m.%Y %H:%M")
    
    print(f"📅 Период: {first_date.strftime('%d.%m.%Y')} - {last_date.strftime('%d.%m.%Y')}")
    print(f"📊 Всего обменов: {stats['total_exchanges']}")
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
    
    # Вывод статистики
    print("\n📊 СТАТИСТИКА ОБМЕНОВ")
    print("="*60)
    print(f"• Всего обменов: {stats['total_exchanges']}")
    print(f"• Уникальных участников: {stats['unique_users']}")
    
    if stats['top_books']:
        print("\n🏆 Топ-3 популярных книги:")
        for book, count in stats['top_books']:
            print(f"• {book}: {count} обменов")
    
    if stats['weekly_stats']:
        print("\n📅 Статистика по неделям:")
        for week, count in sorted(stats['weekly_stats'].items()):
            print(f"• Неделя {week}: {count} обменов")
    
    print("="*60)

# Пример использования:
if __name__ == "__main__":
    # Пример добавления нового обмена
    new_exchange = save_exchange(
        from_user=("Иван Иванов", "ivan_reader", "Война и мир, Преступление и наказание"),
        to_user=("Петр Петров", "peter_booklover", "1984, Мастер и Маргарита"),
        book_given="Преступление и наказание",
        book_received="1984"
    )
    
    # Вывод всех обменов и статистики
    print_exchanges()