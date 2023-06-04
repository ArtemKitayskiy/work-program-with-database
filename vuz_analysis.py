import os, sqlite3
os.chdir('D:\\Kitaysky\\NIR\\Part3')

def select_cmd(sql):
    """Запись содержимого таблицы в переменную"""
    with con:
        data = cur.execute(sql).fetchall()
    return (data)

def oper_choice():
    """Ввод пользователем номера операции"""
    oper = input("""\n\tМеню
1: Отображение содержимого БД в виде таблицы
2: Отображение перечня полных наименований вузов, расположенных в выбранном городе
3: Отображение в виде таблице порядкового номера, федерального округа, количество преподавателей,
количества преподавателей с учеными степенями доктора наук в вузах данного федерального округа,
процентное отношение преподавателей со степенью доктора наук к общему числу преподавателей.
4: Выход
Введите номер оцерации: """)
    return oper

def disp_cont(table):
    """Отображение содержимого таблицы"""
    sql = 'SELECT * FROM {}'.format(table)
    data = select_cmd(sql)
    print('\nБаза данных:', db_name, '\nТаблица:', table)
    for i in range(len(data)):
        print(data[i])
    cur.close()
    con.close()

def p1():
    """Отображение перечня полных наименований вузов, расположенных в выбранном городе"""
    sql = 'SELECT city FROM vuzkart'
    data_cities = select_cmd(sql)
    list_cities = []
    for i in range(len(data_cities)):
        if data_cities[i][0] not in list_cities:
            list_cities.append(data_cities[i][0]) # Заполняем список неповторяющимися городами
    list_cities.sort()
    # Редактируем строку с городами
    for i in range(len(list_cities)):
        list_cities[i] = list_cities[i].strip()
    str_cities = ', '.join(list_cities)
    print(f'\nСписок городов:\n{str_cities}')
    interest_city = input('\nВведите интересующий город из списка: ')
    while True:
        if interest_city not in str_cities:
            interest_city = input('Введите интересующий город повторно: ')
        else:
            break
    while (len(interest_city) < 20):
        interest_city += ' ' # Заполняем строку с интересующим городом пробелами
    sql = 'SELECT z1,city FROM {} WHERE city = "{}"'.format(table_name1, interest_city)
    data_names_cities = select_cmd(sql)
    print('\nПеречень полных наименований вузов в этом городе: ')
    for i in range(len(data_names_cities)):
        print(data_names_cities[i][0]) # Выводим перечень всех вузов в выбранном городе
    cur.close()
    con.close()

def p2():
    """Отображение в виде таблице порядкового номера, федерального округа, количество преподавателей,
    количества преподавателей с учеными степенями доктора наук в вузах данного федерального округа,
    отношение преподавателей со степенью доктора наук к общему числу преподавателей.
    Нижняя строка таблицы содержит суммарное значение количества преподавателей и количество "остепененных"
    преподавателей, а также общее процентное ошношение этих значений."""
    sql = 'SELECT DISTINCT region FROM vuzkart'
    data_region = select_cmd(sql)
    list_region = []
    for i in range(len(data_region)):
        sql = 'SElECT x.region, sum(y.PPS), sum(y.DN) ' \
              'FROM {} x JOIN {} y ON x.codvuz = y.codvuz ' \
              'WHERE x.region = "{}"'.format(
            table_name1, table_name2, data_region[i][0])
        one_list = select_cmd(sql)
        list_region.append(list(one_list[0])) # Заполняем список списками, которые состоят из федерального округа, количества преподавателей и количества преподавателей с учеными степенями
    all_teach = 0 # Создаем переменную для общего колечества преподавателей
    all_teach_degree = 0 # Создаем переменную для общего количества преподавателей с учеными степенями
    print('\n№;', 'Фед. округ;', 'Кол-во преподавателей;', 'Наличие ученой степени;', 'Процентное отношение')
    for i in range(len(list_region)):
        list_region[i].insert(0, i + 1) # Добавляем к i списку порядковый номер
        percent = round((list_region[i][3] / list_region[i][2]) * 100, 1)
        list_region[i].append(percent) # Добавляем к i списку процентное отношение
        print(list_region[i])
        all_teach += list_region[i][2] # Подсчитываем общее колчество преподавателей
        all_teach_degree += list_region[i][3] # Подсчитываем общее количество преподавателей с учеными степенями
    all_percent = round((all_teach_degree / all_teach) * 100, 1)
    sum_list = [len(list_region) + 1, 'All              ', all_teach, all_teach_degree, all_percent]
    print(sum_list) # Выводим нижнюю строку
    cur.close()
    con.close()

while True:
    db_name = 'VUZ.sqlite'
    table_name1 = 'vuzkart'
    table_name2 = 'vuzstat'
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    num = oper_choice()
    if num == '1':
        table_oper = input("""
1: vuzkart
2: vuzstat
Введите номер таблицы для отображения: """)
        if table_oper == '1':
            disp_cont(table_name1)
        if table_oper == '2':
            disp_cont(table_name2)
    if num == '2':
        p1()
    if num == '3':
        p2()
    if num == '4':
        cur.close()
        con.close()
        break
