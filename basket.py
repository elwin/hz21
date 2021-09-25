import pandas as pd  # only needed to load example shopping cart


def get_product_details(product_id):
    # dummy function for leon to fill in the DB query.
    pass


def compare_with_similar(product):
    """
    Adds price per base unit entry for the product, and calculates price
    per base unit for all related products with the same unit. 
    """
    unit = product['price']['base']['unit']
    product['price']['base_per_unit'] = product['price']['base'][
        'price'] / product['price']['base']['quantity']
    for similar_product_id in product['related_products'][
            'purchase_recommendations']['product_ids']:
        similar_product = get_product_details(similar_product_id)
        if unit == similar_product['price']['base'][
                'unit']:  # make sure we're comparing the same units
            similar_product['price'][
                'base_per_unit'] = similar_product['price']['base'][
                    'price'] / similar_product['price']['base']['quantity']
        else:
            product['related_products']['purchase_recommendations'][
                'product_ids'].pop(similar_product_id)
    return product
    # TODO: more lol


def calculate_basket(cart):
    """
    Calculates average m_check rating for basket, weighted by amount/Menge.
    """
    cart = get_product_details(cart)
    n_products = 0
    m_check = 0
    for product_id in cart:
        product = get_product_details(product_id)
        m_check += product['m_check2']['carbon_footprint'][
            'ground_and_sea_cargo']['rating'] * cart[product_id]['Menge']
        n_products += cart[product_id]['Menge']
    m_check_avg = m_check / n_products
    return cart, m_check_avg


def load_example_cart_csv(path):
    # loads the example cart (Abverkaufdaten_trx_202001.csv)
    with open(path) as f:
        cart = pd.read_csv(f)
    cart = cart[cart['KundeID'] == 100688]
    cart = cart[cart['WarenkorbID'] == 1]
    cart = cart[['ArtikelID',
                 'Menge']].set_index('ArtikelID').to_dict(orient='index')
    # {
    #   507085300000: {'Menge': 1.0},
    #   220622085000: {'Menge': 0.853},
    #   ...
    # }
    return cart


if __name__ == '__main__':
    cart = load_example_cart_csv('example_cart.csv')
    print(cart)