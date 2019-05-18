# Migration_Ukraine_Project
Analysis of data on migration in Ukraine. My final year project aimed at learning how to collect and represent data.

Цей проект ставить за мету дати ширшому колу дослідників доступ до порівняльної характеристики даних по Україні у зручному, інтуїтивному форматі. 

Опис дослідження:
================

Розроблений модуль research.py надає можливість провести дослідження на основі даних про міграційні процеси в Україні, отримані з сайту data.gov.ua.

Після запуску модуль дозволяє виконувати через інтерфейс командного рядку такі команди та відповідні операції з даними:

* show_data - вивід у командний рядок даних, з якими ми працюємо у форматі <ім'я стрічки в базі даних> - словник значень, що їй відповідає

* row_names - вивід списку імен доступних стрічок у базі даних

* col_names - вивід списку імен доступних колонок у базі даних

* get_val - вивід значення, що міститься у базі даних у полі з параметрами (назвою стрічки та колонки), введеними через командний рядок

* get_row - вивід значень, що міститься у базі даних у стрічці з назвою, введеною через командний рядок

* get_col - вивід значень, що міститься у базі даних у колонці з назвою, введеною через командний рядок

* cor_ind - вивід матриці корреляції між двома колонками/рядками, назви яких уведені через командний рядок

* plot - вивід графіку, що ілюструє зміну певного параметру (приклад: Число прибулих) з часом у певному рядку(області України)
       Назва рядку та параметр вводить користувач через командний рядок
       
* map - генерація карти, що ілюструє різницю в значенні певного параметру в різних областях України (назва файлу та параметр вводиться через       командний рядок)

* explain - вивід додаткових пояснень до даних

* exit - вихід з програми

Для використання модулю необхідно виконати команду <code>python research.py</code> у командній стрічці та виконувати інструкції, що з'являться на екрані.

Структура проекту
=================

У проекті знаходяться файли:
* research.py - модуль з власне дослідженням. Містить клас UADataResearchCommandLine, що надає користувачу можливість користуватися методами класу UkrainianData безпосередньо через командний рядок
* ukrainian_data_adt.py - модуль, що містить реалізацію абстрактного типу даних UkrainianData, що надає можливість виконувати дослідження
* test_ukrainianData.py - модуль для тестування ukrainian_data_adt.py. Тести покривають 83% файлу ukrainian_data_adt.py
* ukrainian_data_example.py - модуль з прикладами використання UkrainianData
