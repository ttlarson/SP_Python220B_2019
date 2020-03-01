import csv
import names
from random_word import RandomWords
from random import randint, random, choice, uniform
from pathlib import Path

ENTRY_SIZE = 1000

PRODUCT_IDS = []
CUSTOMER_IDS = []

PRODUCT_FILE_NAME = "./sample_csv_files/products.csv"
CUSTOMER_FILE_NAME = "./sample_csv_files/customers.csv"
RENTAL_FILE_NAME = "./sample_csv_files/rentals.csv"

RW = RandomWords()

def generate_products():
    """
    Generate Product CSV file.

    Using random words, generate a list of products, IDs, etc and save into
    a CSV file called "products.csv"
    """
    print("Generating Products")
    product = {
            'product_id':[],
            'description': [],
            'market_price':[],
            'rental_price':[],
            'product_type':[],
            'brand':[],
            'voltage':[],
            'material':[],
            'size':[],
            'quantity_available':[]
        }
    header = list(product.keys())
    with open(Path(PRODUCT_FILE_NAME), 'w') as f:
        csv_file = csv.DictWriter(f, header, lineterminator='\n')
        csv_file.writeheader()
        for idx in range(ENTRY_SIZE):
            product = {
                'product_id':[],
                'description': [],
                'market_price':[],
                'rental_price':[],
                'product_type':[],
                'brand':[],
                'voltage':[],
                'material':[],
                'size':[],
                'quantity_available':[]
            }
            product['product_type'] = choice(['Furniture','Electric'])
            product['quantity_available'] = randint(0,99)
            product['market_price'] = round(uniform(0.01, 2500.00),2)
            product['rental_price'] = round(product['market_price'] * random() / 365, 2)
            if product['product_type'] == 'Furniture':
                product['product_id'] = f"F{randint(0,999999):06}"
                product['material'] = choice(['Maple','Oak', 'Walnut', 'Tile', 'Granite', 'Formica'])
                product['size'] = choice(['x-small','small','medium', 'large', 'extra-large', 'lawn orniment'])
                try:
                    word = RW.get_random_word(includePartOfSpeech="noun").capitalize() 
                except:
                    word = "Standard"
                product['description'] = word + ' ' + choice(['Table', 'Chair', 'Stool','Mirror', 'Fixture', 'Desk'])
            else:
                product['product_id'] = f"E{randint(0,999999):06}"
                product['voltage'] = choice(['110VAC','220VAC','440VAC', '12VDC', '10kV'])
                try:
                    product['brand'] =  RW.get_random_word(hasDictionaryDef="true",includePartOfSpeech="noun").capitalize()
                except:
                    product['brand'] = choice(['Acme', 'Suck-n-cut', 'ComputerDiluter', 'Freebird', 'Nowayout'])

                try:
                    word = RW.get_random_word(includePartOfSpeech="noun").capitalize() 
                except:
                    word = "Standard"
                product['description'] = word + ' ' + choice(['Fan', 'Coffee Maker', 'Washing Machine', 'Microwave', 'Kettle', 'Toothbrush'])

            PRODUCT_IDS.append(product['product_id'])
            csv_file.writerow(product)
            # print(product)

def generate_customers():
    """
    Generate Product CSV file.

    Using random words, generate a list of products, IDs, etc and save into
    a CSV file called "customers.csv"

    customer_id,name,last_name,address,phone_number,email_address,status,credit_limit
    """
    print("Generating Customers")
    customer = {
            'customer_id':[],
            'name': [],
            'last_name':[],
            'address':[],
            'phone_number':[],
            'email_address':[],
            'status':[],
            'credit_limit':[],
            }
    header = list(customer.keys())
    with open(Path(CUSTOMER_FILE_NAME), 'w') as f:
        csv_file = csv.DictWriter(f, header, lineterminator='\n')
        csv_file.writeheader()
        for idx in range(ENTRY_SIZE):
            customer['customer_id'] = f'C{randint(0,999999):06}'
            customer['name'] = names.get_first_name()
            customer['last_name'] = names.get_last_name()

            try:
                address =  RW.get_random_word(hasDictionaryDef="true",includePartOfSpeech="noun").capitalize()
            except:
                address = choice(['Rarotonga', 'Tuvalu', 'Samoa'])
            customer['address'] = address
            customer['phone_number'] = f"{randint(0,999):3}-{randint(0,999):3}-{randint(0,9999):3}"
            try:
                randurl = RW.get_random_word()
            except:
                randurl = 'gmail'
            customer['email_address'] = customer['name'].lower() + '.' + customer['last_name'].lower() + '@' + randurl + choice(['.com', '.net', '.io', '.org'])
            customer['status'] = choice([True, False])
            customer['credit_limit'] = round(uniform(0.0, 100000.00),2)

            CUSTOMER_IDS.append(customer['customer_id'])
            csv_file.writerow(customer)
            # print(customer)

def generate_rentals():
    """
    Generate Rental CSV file.

    Using random words, generate a list of rentals, IDs, etc and save into
    a CSV file called "customers.csv"

    customer_id,name,last_name,address,phone_number,email_address,status,credit_limit
    """
    print("Generating Rentals")
    rentals = {
            'customer_id':[],
            'product_id': [],
            }
    header = list(rentals.keys())
    with open(Path(RENTAL_FILE_NAME), 'w') as f:
        csv_file = csv.DictWriter(f, header, lineterminator='\n')
        csv_file.writeheader()
        for idx in range(ENTRY_SIZE):
            rentals['customer_id'] = CUSTOMER_IDS[randint(0,ENTRY_SIZE-1)]
            rentals['product_id'] = PRODUCT_IDS[randint(0, ENTRY_SIZE-1)]

            # print(rentals)
            csv_file.writerow(rentals)
if __name__ == "__main__":
    generate_products()
    generate_customers()    
    generate_rentals()