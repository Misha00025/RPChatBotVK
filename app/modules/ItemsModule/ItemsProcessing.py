

def show_items(user, params):
    if params == "деньги ":
        return f"{params}: Показываем кошель"
    return f"{params}: Показываем инвентарь"


def add_item(user, params):
    return "Добавляем предметы"


def remove_item(user, params):
    return "Удаляем предметы"