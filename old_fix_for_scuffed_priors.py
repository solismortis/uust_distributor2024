# Fix bug with scuffed priorities
# for abit_key, abit_value in abits.items():
#     prios = []
#     mx = 0
#     c = 0
#     for prio_key, prio_value in abit_value.items():
#         prios.append(prio_key)
#         mx = max(prio_key, mx)
#         c += 1
#     if len(abit_value.values()) != mx:
#         prios.sort()
#         for n in range(1, c+1):
#             abit_value[n] = abit_value.pop(prios[n-1])
# TODO: Bug: Надо также изменить приоритеты в самих таблицах. Вот только для этого надо бы
# list из таблиц превратить в dict для быстрого доступа. Или можно изменить алго проверки того,
# можно ли юзать прио