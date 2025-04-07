from database import User, Exchange
from datetime import datetime, timedelta

def print_stats_to_console():
    """Выводит статистику пользователей и обменов в терминал"""
    print("\n📊 СТАТИСТИКА СИСТЕМЫ")
    print("=" * 40)

    # Статистика пользователей
    total_users = User.query.count()
    registered_users = User.query.filter(User.full_name.isnot(None)).count()
    active_users = User.query.filter_by(started=True).count()
    users_with_books = User.query.filter(User.books.isnot(None)).count()

    print("\n👥 ПОЛЬЗОВАТЕЛИ:")
    print(f"• Всего: {total_users}")
    print(f"• Зарегистрированы: {registered_users}")
    print(f"• Нажали 'Старт': {active_users}")
    print(f"• Добавили книги: {users_with_books}")

    # Статистика обменов
    total_exchanges = Exchange.query.count()
    recent_exchanges = Exchange.query.filter(
        Exchange.exchange_date >= (datetime.now() - timedelta(days=7))
    ).count()

    print("\n📚 ОБМЕН КНИГ:")
    print(f"• Всего обменов: {total_exchanges}")
    print(f"• За последние 7 дней: {recent_exchanges}")

    print("\n" + "=" * 40 + "\n")

# Пример вызова
if __name__ == "__main__":
    print_stats_to_console()