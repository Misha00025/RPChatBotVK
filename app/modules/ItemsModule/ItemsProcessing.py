import re
from app.core.User import User
from .Inventory import Inventory


def parse_message(message: str):
    message = message.strip()
    match = re.search(r'(\d+)$', message)
    if match:
        quantity = int(match.group(1))
        item_name = message[:match.start()].strip()
    else:
        item_name = message
        quantity = 1
    return item_name, quantity


def get_wallet(inventory: Inventory, name):
    ok, item = inventory.get_item(name)
    if item is None or item.amount is None:
        amount = 0
    else:
        amount = item.amount 
    return f"Деньги на счету: {amount}"


def show_items(user: User, params):
    inv = Inventory(user.get_user_id())
    name, _ = parse_message(params)
    if name == "деньги":
        return get_wallet(inv, name)
    ok, items = inv.get_items()
    message, i = "", 0
    for item in items:
        i += 1
        amount = item.amount
        if amount is None: amount = 0
        message += f"\n{i}. {item.name}: {amount}"
    return f"Показываем инвентарь: {message}\n"


def add_item(user, params):
    return "Добавляем предметы"


def remove_item(user, params):
    return "Удаляем предметы"