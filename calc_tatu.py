hour_price = 300
prices = {
    "small": hour_price*3,
    "medium": hour_price*6,
    "large": hour_price*9,
    "sketch_design": 2500,
    "realistic_style": 5000,
    "geometric_style": 7500,
    "minimalist_style": 5000,
    "intim_placement": 4000,
    "diff_placement": 4000,
    "forearm_placement": 4000,
    "back_placement": 4000,
    "chest_placement": 4000,
    "leg_placement": 4000,
    "several": 3000,
    "null": 0
}

# Функция для подсчета стоимости татуировки
def calculate_tattoo_cost(size, design, style, placement):
    total_cost = prices[size] + prices[design] + prices[style] + prices[placement]
    return total_cost

# Пример использования функции
# print('Выбери размер(small, medium, large)')
# size = input()
# print('Есть ли эскиз(sketch_design, null)')
# design = input()
# print('Стиль(realistic_style, geometric_style, minimalist_style)')
# style = input()
# print('Место(forearm_placement, back_placement, chest_placement, leg_placement')
# placement = input()

# cost = calculate_tattoo_cost(size, design, style, placement)
# print(f"Приблизительная стоимость тату: ${cost}")