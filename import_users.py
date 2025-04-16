from database import db, app, User

# Ваши данные пользователей
real_users = [
    (1, 'None', 'Серикбай Рамазан', '', False),
    (2, 'vveeqqpprr', 'Элина', 'Потому что я тебя люблю - Гийом Мюссо', False),
    (3, 'LAGMAAAAN', 'Saida','Маленькие женщины на англ, Стивен Кинг - доктор сон, Стигмалион - Кристина старк', False),
    (4, 'jarixxaa', 'Adjara', '', False),
    (5, 'wualov', 'Жолдаскан Фируза', '', False),
    (6, 'Tengri_cat', 'Нитар', '7 принципов высоко эффективных людей', False),
    (7, 'Konstanteeeen', 'Константин', 'Омар Хайям', False),
    (8, 'AIKQYWX', 'Saleh Aikyz', '', False),
    (9, 'khandrok', 'Алихан Калыбеков','Государь, Преступление и наказание, Белые ночи', False),
    (10, 'None', 'Ермурат Турлибеков', '', False),
    (11, 'aamiovee', 'Элин', 'итальянский с нуля', False),
    (12, 'killstationexxidae', 'Наги','Темная башня, дезертир, утраченные иллюзии, ванпанчмен', False),
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
    (25, 'thch0l', 'Tsoi','Детство, Юность отрочество - толстой, Бедные люди - Достоевский', False),
    (26, 'AyankaD', 'Аяна', 'Двойник с лунной дамбы - содзи симада', False),
    (27, 'ewelyl', 'Шатырбеков Даурен', '', False),
    (28, 'lankikinn', 'Нұрмахан Нұрила', '', False),
    (29, 'qwiiskz', 'Хе Диана', 'лисья нора', False),
    (30, 'glebdmitriyev', 'Дмитриев Глеб', '1.000.000$ в инвестициях на пальцах (Даулет Арманович), О чем я говорю, когда говорю о беге (Харуки Мураками), Кемел Адам (Кайрат Жолдыбайулы), Наедине с собой (Марк Аврелий), Великий Гэтсби (Ф. С. Фицджеральд)', False),
    (31, 'akkayasha', 'мухтарқызы амина','бедные люди, униженные и оскорбленные, букварь', False),
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
    (113, 'bookwanderer1', 'Жания', '451 градус по Фаренгейту – Рэй Брэдбери', False),
    (114, 'azamatreader', 'Азамат', 'Казахское ханство – Олжас Сулейменов', False),
    (115, 'gulimlover', 'Гулим Айгеримовна', 'Унесённые ветром – Маргарет Митчелл', False),
    (116, 'sayat_001', 'Саят', 'Над пропастью во ржи – Дж. Д. Сэлинджер', False),
    (117, 'liiliyaa', 'Лилия Исмаилова', 'Анна Каренина – Лев Толстой', False),
    (118, 'batyrbekovvv', 'Батырбек Батыр', 'Мудрость веков – Восточная философия', False),
    (119, 'dostykfriend', 'Достык', 'Дюна – Фрэнк Герберт', False),
    (120, 'alua_reader', 'Алуа Ахметова', 'Ешь, молись, люби – Элизабет Гилберт', False),
    (121, 'temirtau_boy', 'Мади', 'Песнь льда и пламени – Джордж Р.Р. Мартин', False),
    (122, 'aidai_books', 'Айдай', 'Сила настоящего – Экхарт Толле', False),
    (123, 'timurbekov', 'Тимур Беков', 'Игра престолов – Джордж Мартин', False),
    (124, 'dariya_blossom', 'Дария', 'Вино из одуванчиков – Рэй Брэдбери', False),
    (125, 'kairat_reader', 'Кайрат', 'Цель – Элияху Голдратт', False),
    (126, 'nargiza_dust', 'Наргиза', 'Триумфальная арка – Эрих Мария Ремарк', False),
    (127, 'askarovv', 'Аскар', 'Ревизор – Николай Гоголь', False),
    (128, 'esbolov', 'Есбол', 'Мальчик в полосатой пижаме – Джон Бойн', False),
    (129, 'zhanara_books', 'Жанара', 'Гордость и предубеждение – Джейн Остин', False),
    (130, 'serikzhan_91', 'Серикжан', 'Наруто. Том 1 – Масаси Кишимото', False),
    (131, 'zhaneli_lovebooks', 'Жанель', 'Маленький принц – Антуан де Сент-Экзюпери', False),
    (132, 'rakhim_writer', 'Рахим', 'Алгоритмы для жизни – Брайан Кристиан', False),
    (133, 'daneliya_kz', 'Даниялия', 'Преступление и наказание – Фёдор Достоевский', False),
    (134, 'arman_dreamer', 'Арман', 'Великий Гэтсби – Ф. Скотт Фицджеральд', False),
    (135, 'kamshat_21', 'Камшат', 'Сто лет одиночества – Габриэль Гарсиа Маркес', False),
    (136, 'azhar_bibliophile', 'Ажар', 'Старик и море – Эрнест Хемингуэй', False),
    (137, 'riza_kz', 'Риза', 'Мемуары гейши – Артур Голден', False),
    (138, 'dinara_mind', 'Динара', 'Краткая история времени – Стивен Хокинг', False),
    (139, 'erbol_scholar', 'Ербол', 'О дивный новый мир – Олдос Хаксли', False),
    (140, 'nurgul_classic', 'Нургуль', 'Тихий Дон – Михаил Шолохов', False),
    (141, 'yernar_readz', 'Ернар', 'Человек в поисках смысла – Виктор Франкл', False),
    (142, 'aliya_blossom', 'Алия', 'Великий инквизитор – Ф.М. Достоевский', False)
]



def import_users():
    with app.app_context():
        try:
            print("🔄 Начало импорта пользователей...")

            for user_data in real_users:
                user = User(
                    user_id=str(user_data[0]),  # Конвертируем ID в строку
                    username=user_data[1] if user_data[1] != 'None' else None,
                    full_name=user_data[2],
                    books=user_data[3] if user_data[3] else None,
                    started=user_data[4]
                )
                db.session.merge(user)  # Добавляем или обновляем пользователя

            db.session.commit()
            print("✅ Данные пользователей успешно импортированы!")
            print(f"Всего обработано: {len(real_users)} записей")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка импорта: {e}")
            raise  # Повторно поднимаем исключение для логирования


if __name__ == "__main__":
    try:
        import_users()

        # Дополнительная проверка
        with app.app_context():
            count = User.query.count()
            print(f"Проверка: в базе теперь {count} пользователей")

            # Выводим первые 3 записи для проверки
            sample_users = User.query.limit(3).all()
            for user in sample_users:
                print(
                    f"ID: {user.user_id}, Name: {user.full_name}, Books: {user.books}")

    except Exception as e:
        print(f"🔴 Критическая ошибка: {e}")
