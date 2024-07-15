# Funções que criam produtos para teste

def product_data() -> dict[str, any]:
    return {'name': 'Produto', 'quantity': 10, 'price': '8500', 'status': True}

def products_data() -> list[dict[str, any]]:
    return [
        {'name': 'Produto', 'quantity': 10, 'price': '8500', 'status': True},
        {'name': 'Produto2', 'quantity': 1, 'price': '500', 'status': True},
        {'name': 'Produto3', 'quantity': 5, 'price': '100', 'status': True},
        {'name': 'Produto4', 'quantity': 9, 'price': '10', 'status': True},
        {'name': 'Produto5', 'quantity': 0, 'price': '1500', 'status': False}
    ]