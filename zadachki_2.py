# 1) Реализуйте chunks(lst, n) — генератор чанков длины n.
def chunks(lst: list, chunk_size: int):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


# example_chunks = chunks(list(range(50)), 8)
# for chunk in example_chunks:
# print(chunk)
# Вывод:[0, 1, 2, 3, 4, 5, 6, 7]
# [8, 9, 10, 11, 12, 13, 14, 15]
# [16, 17, 18, 19, 20, 21, 22, 23]
# [24, 25, 26, 27, 28, 29, 30, 31]
# [32, 33, 34, 35, 36, 37, 38, 39]
# [40, 41, 42, 43, 44, 45, 46, 47]
# [48, 49]

# 2) Реализуйте flatten(nested) — итеративно.
# Если встречаем список, то с помощью extend забираем содержимое в обратном порядке(так как берем с конца - надо сохранить порядок).Встретили элемент, а не список - добавляем в результат
def flatten(nested: list):
    stack = [nested]
    result = []
    while stack:
        element = stack.pop()
        if type(element) is list:
            stack.extend(reversed(element))
        else:
            result.append(element)
    return result


# print(flatten([1,[2,3,[5,6],7,8],9,10]))
# Вывод: [1, 2, 3, 5, 6, 7, 8, 9, 10]

# 3) Объясните и исправьте [[None]*3]*3 проблему.
# [[None]*3]*3 создает три ссылки на один и тот же объект
l_err = [[None] * 3] * 3
# Демонстрация: кажется, что меняем только первый элемент первого списка, но меняются первые элементы всех список, что и демонстрирует ошибку
l_err[0][0] = 1
# print(l_err)
# Вывод: [[1, None, None], [1, None, None], [1, None, None]]
# Один из вариантов исправления: можем использовать генераторы, чтобы создать три разных объекта
l_fixed = [[None] * 3 for i in range(3)]
# Проверка: меняем первый элемент первого списка и ожидаем, что поменяется только он
l_fixed[0][0] = 1


# print(l_fixed)
# Вывод: [[1, None, None], [None, None, None], [None, None, None]]

# 4) Реализуйте unique_preserve_order(iterable).
#Идея: заведем список seen, куда будем добавлять элементы, которые уже встретили.
# При проходе смотрим, есть ли элемент в seen, если есть, то пропускаем, так как уже встречали, если нет, то добавляем в результат и в seen.
def unique_preserve_order(lst: list):
    seen = []
    result = []
    for item in lst:
        if item not in seen:
            seen.append(item)
            result.append(item)
    return result


example_list = [1, 2, 3, 5, 5, 8, 11, 45, 1, 3, 45, 8]
# print(unique_preserve_order(example_list))
# Вывод: [1, 2, 3, 5, 8, 11, 45]
