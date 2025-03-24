import sqlite3
import os

# Создаем базу данных
DB_FILE = 'users_books.db'

def init_db():
    # Удаляем существующую базу если она есть
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Создаем новое подключение
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создаем таблицу пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        username TEXT,
        full_name TEXT,
        books TEXT,
        started BOOLEAN DEFAULT FALSE
    )
    ''')

    # Список реальных пользователей
    real_users = [
        (1, 'None', 'Серикбай Рамазан', '', False),
        (2, 'vveeqqpprr', 'Элина', 'Потому что я тебя люблю - Гийом Мюссо', False),
        (3, 'LAGMAAAAN', 'Saida', 'Маленькие женщины на англ, Стивен Кинг - доктор сон, Стигмалион - Кристина старк', False),
        (4, 'jarixxaa', 'Adjara', '', False),
        (5, 'wualov', 'Жолдаскан Фируза', '', False),
        (6, 'Tengri_cat', 'Нитар', '7 принципов высоко эффективных людей', False),
        (7, 'Konstanteeeen', 'Константин', 'Омар Хайям', False),
        (8, 'AIKQYWX', 'Saleh Aikyz', '', False),
        (9, 'khandrok', 'Алихан Калыбеков', 'Государь, Преступление и наказание, Белые ночи', False),
        (10, 'None', 'Ермурат Турлибеков', '', False),
        (11, 'aamiovee', 'Элин', 'итальянский с нуля', False),
        (12, 'killstationexxidae', 'Наги', 'Темная башня, дезертир, утраченные иллюзии, ванпанчмен', False),
        (13, 'd2sease', 'Алина', '', False),
        (14, 'nariwaaa', 'Ками', '', False),
        (15, 'alisherthegreat', 'Абас Алишер', '', False),
        (16, 'pow3lnah', 'Users', '', False),
        (17, 'ClayzDart', 'Диас', 'Мать Ученья, Повелитель Тайн', False),
        (18, 'asikoakhmetova', 'Ахметова Асылым', 'Хочу и буду - М.Лабковский', False),
        (19, 'None', 'Заида', '', False),
        (20, 'None', 'Аслан Мирабдулла', 'Икигай, Кемел адам', False),
        (21, 'amillienn', 'амина', 'дневник памяти', False),
        (22, 'bekam1na', 'Амина', '', False),
        (23, 'dulbl4', 'Дулат', '48 законов власти, Метро 2033, Война и мир 4 тома', False),
        (24, 'Kadihdj', 'Төлегенқызы Қадиша', '', False),
        (25, 'thch0l', 'Tsoi', 'Детство, Юность отрочество - толстой, Бедные люди - Достоевский', False),
        (26, 'AyankaD', 'Аяна', 'Двойник с лунной дамбы - содзи симада', False),
        (27, 'ewelyl', 'Шатырбеков Даурен', '', False),
        (28, 'lankikinn', 'Нұрмахан Нұрила', '', False),
        (29, 'qwiiskz', 'Хе Диана', 'лисья нора', False),
        (30, 'glebdmitriyev', 'Дмитриев Глеб', '1.000.000$ в инвестициях на пальцах (Даулет Арманович), О чем я говорю, когда говорю о беге (Харуки Мураками), Кемел Адам (Кайрат Жолдыбайулы), Наедине с собой (Марк Аврелий), Великий Гэтсби (Ф. С. Фицджеральд)', False),
        (31, 'akkayasha', 'мухтарқызы амина', 'бедные люди, униженные и оскорбленные, букварь', False),
        (32, 'diana_rollan', 'Аяна Адам', '', False),
        (33, 'werexx', 'Артемий', 'Часодеи - все части', False),
        (34, 'extrareader', 'Нурай Еркинбек', 'Франц Кафка «Процесс»', False),
        (35, 'tiamolr', 'Акмаржан Амирханова', '', False),
        (36, 'ayashhk', 'Аяжан', '', False),
        (37, 'azrrrra', 'Айзере', '', False),
        (38, 'lanenotpunk', 'Романас', 'Гарри Поттер и Философский камень', False),
        (39, 'OlzhasJKY', 'Ибрагим Олжас Дидарұлы', '', False),
        (40, 'Y_u_zuha', 'Иманберді Көркем', 'Спеший любить - Николос Спаркс', False),
        (41, 'None', 'тлепжан улпан', '', False),
        (42, 'hersonsucks', 'Нуржанова Ажар', '', False),
        (43, 'sakennovnaa', 'Тимахан Аружан', '', False),
        (44, 'xxslslsl', 'Бекатов Санжар', '', False),
        (45, 'chase_atlanticc', 'Черри', '', False),
        (46, 'yadeso', 'Валентин', '', False),
        (47, 'safiollamo', 'Сафиолда Мөлдір', '', False),
        (48, 'None', 'Манарбек Қарақат', '', False),
        (49, 'envityy', 'Хан Диана', '', False),
        (50, 'imyapolzovatelya9999', 'Алмаз', '', False),
        (51, 'roflanslav', 'Рамазан', '', False),
        (52, 'sssshveps', 'Абдраимова София Хабировна', '', False),
        (53, 'Nureke_a', 'Нурым', '', False),
        (54, 'bigazy77', 'Bigazy', '', False),
        (55, 'Zikonai_05', 'Айзира', '', False),
        (56, 'aimaneyrlan', 'Users', '', False),
        (57, 'anelka876', 'Анеля', '', False),
        (58, 'None', 'Сейтбек Коркем', '', False),
        (59, 'maybe_elli', 'Элянора', '', False),
        (60, 'None', 'Аида', '', False),
        (61, 'None', 'Джамшуд', '', False),
        (62, 'kuraiyy', 'рр', '', False),
        (63, 'msaniyae', 'Мейрамбек Сания', '', False),
        (64, 'luamizz', 'Жалгасбаева Азима', '', False),
        (65, 'suiynbay', 'Koblandy Suiynbay', '', False),
        (66, 'hamster_1303', 'Мухтаркызы Мариям', '', False),
        (67, 'None', 'Амангелди асем', '', False),
        (68, 'agentPi314', 'Амир', '', False),
        (69, 'evaneeees', 'Акниет', '', False),
        (70, 'akerk_sw', 'Акерке', '', False),
        (71, 'None', 'Динара', '', False),
        (72, 'None', 'Кадыр Аянат', '', False),
        (73, 'None', 'Сара', '', False),
        (74, 'mioolmm', 'Адана', '', False),
        (75, 'ke_aisa', 'Кенесбек Айсана', '', False),
        (76, 'dnteeng08', 'Диана', '', False),
        (77, 'k_nurt', 'Карина', '', False),
        (78, 'aaaiserr', 'Байдалы Айсер', '', False),
        (79, 'babysati444', 'Сати', '', False),
        (80, 'dredfr', 'Темкенов Жарас', '', False),
        (81, 'ramioshaav', 'Амина', '', False),
        (82, 'None', 'Алеся', '', False),
        (83, 'viicks06', 'Черепкова Виктория', '', False),
        (84, 'justacloudygirl', 'Гумаева Виолетта', '', False),
        (85, 'Wxco1c', 'Улдана Жуманали', '', False),
        (86, 'Mustafarg', 'Мустафа', '', False),
        (87, 'Bilimqyzy', 'Смагулова Аделия', '', False),
        (88, 'nurzzzhhh', 'Ннурка', '', False),
        (89, 'yerkkesh', 'Доступные книги', '', False),
        (90, 'Aimkhgvd', 'Кабдый Айым', '', False),
        (91, 'EASLLK', 'Asyl', '', False),
        (92, 'None', 'Акерке Вайзхума', '', False),
        (93, 'fghsmell', 'сакенов Еркебулан', '', False),
        (94, 'amankeldi_a', 'Алуа', '', False),
        (95, 'ulqquiiorra', 'Амир', '', False),
        (96, 'None', 'Tolegen', '', False),
        (97, 'None', 'Аида', '', False),
        (98, 'None', 'Еділұлы Асылжан', '', False),
        (99, 'aidana_erlankyzy', 'Айдана', '', False),
        (100, 'nspzhn', 'Альнур', '', False),
        (101, 'lim_tn', 'Лим Татьяна', '', False),
        (102, 'None', 'Доступные книги', '', False),
        (103, 'diirra_a', 'Индира Салимжан', '', False),
        (104, 'assiyaastt', 'Анна', '', False),
        (105, 'arushk0', 'Арушка', '', False),
        (106, 'Njckl', 'Аяна Алибек', '', False),
        (107, 'Maksim9160', 'Максим Витола', '', False),
        (108, 'Zhibewsx', 'Абай Жибек', '', False),
        (109, 'sssultikk', 'Негр', '', False),
        (110, 'Sofixqwsq', 'Соня', '', False),
        (111, 'None', 'Назгуль', '', False),
        (112, 'microkosmoos', 'Айгерим', '', False),
    ]

    # Добавляем пользователей
    cursor.executemany('INSERT INTO users (user_id, username, full_name, books, started) VALUES (?, ?, ?, ?, ?)', real_users)
    
    # Сохраняем изменения
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("База данных успешно создана и заполнена реальными пользователями!") 