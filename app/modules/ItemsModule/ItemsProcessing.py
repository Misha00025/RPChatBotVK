import re
from app.core.User import User
from .Inventory import Inventory
from app.core import alias_management as am 


def parse_message(message: str):
    message = message.strip()
    match = re.search(r'(\d+)$', message)
    if match is not None:
        quantity = int(match.group(1))
        item_name = message[:match.start()].strip()
    else:
        item_name = message
        quantity = 1
    return item_name, quantity


def get_wallet(inventory: Inventory, params):
    ok, item = inventory.get_item(params)
    if item is None or item.amount is None:
        amount = 0
    else:
        amount = item.amount 
    return f"Деньги на счету {am.get_alias(inventory.owner_id)}: {amount}"


def show_items(user: User, params):
    inv = Inventory(user.get_user_id())
    name, _ = parse_message(params)
    if name == "деньги":
        return get_wallet(inv, name)
    ok, items = inv.get_items()
    message, i = "", 0
    if not ok:
        return f"Не получилось посмотреть инвентарь игрока {am.get_alias(user.get_user_id())}"
    for item in items:
        i += 1
        amount = item.amount
        if amount is None: amount = 0
        message += f"\n{i}. {item.name}: {amount}"
    return f"Инвентарь игрока {am.get_alias(user.get_user_id())}: {message}\n"


def add_item(user: User, params):
    name, amount = parse_message(params)
    if name == "":
        return "Невозможно добавить предмет без названия"
    if amount <= 0:
        return "Количество предмета должно быть больше 0"
    inv = Inventory(user.get_user_id())
    ok, res = inv.add_item(name, amount)
    if not ok:
        print(res)
        return f"Не удалось добавить предмет '{name}' пользователю {am.get_alias(user.get_user_id())}"
    ok, item = inv.get_item(name)
    return (f"Предмет {name} в количестве {amount} шт. добавлен в инвентарь пользователя {am.get_alias(user.get_user_id())}\n"
            f"Сейчас в инвентаре: {item.amount}")

def remove_item(user: User, params):
    name, amount = parse_message(params)
    if name == "":
        return "Невозможно удалить предмет без названия"
    if amount <= 0:
        return "Количество предмета должно быть больше 0"
    inv = Inventory(user.get_user_id())
    ok, _ = inv.remove_item(name, amount)
    if not ok:
        return f"Невозможно удалить предмет '{name}' из инвентаря игрока {am.get_alias(user.get_user_id())}"
    have, item = inv.get_item(name)
    if not have:
        return f"Предмет '{name}' был полностью удалён из инвентаря пользователя {am.get_alias(user.get_user_id())}"
    return f"Количество предмета {name} в инвентаре игрока {am.get_alias(user.get_user_id())} уменьшено.\nОсталось: {item.amount}"