"""
    database.py
    Contains interactions for the HP Norton Mongodb database.

    Functionality:
        HP Norton customer: see a list of all products available for rent
        HP Norton salesperson: see a list of all of the different products, showing product ID,
            description, product type and quantity available.
        HP Norton salesperson: see a list of the names and contact details
            (address, phone number and email) of all customers who have rented a certain product.
"""
import logging
import csv
from pymongo import MongoClient

# File logging setup
LOG_FILE = 'HP.log'
FILE_LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FILE_FORMATTER = logging.Formatter(FILE_LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FILE_FORMATTER)

# Console logging setup
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
     This function takes a directory name three csv files as input, one with product data, one with
    customer data and the third one with rentals data and creates and populates a new MongoDB
    database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors
    that occurred, in the same order.

    :return: tuple1, record count of the # of products, customers, rentals added
             tuple2, count of any errors that occurred, in the same order
    """
    count_list = []
    error_list = []

    # Open connection
    logging.info('Importing datafiles in %s', directory_name)
    logging.info('Opening connection to mongodb.')
    mongo = MongoDBConnection()
    logging.info('Connection open.')

    with mongo:
        # Create connection to database
        logging.info('Attempting to connect to mongodb: HPNortonDatabase in local')
        db = mongo.connection.HPNortonDatabase
        logging.info('Connected HPNortonDatabase.')

        # create/connect to collections
        logging.info('Connecting to collections...')
        product_data = db['product_data']
        logging.info('*connected to collection: product_data')
        customer_data = db['customer_data']
        logging.info('*connected to collection: customer_data')
        rental_data = db['rental_data']
        logging.info('*connected to collection: rental_data')

        # load product data
        logging.info('Attempting to open: %s', product_file)
        with open(directory_name + '/' + product_file) as prod_file:
            logging.info('File opened.')
            reader = csv.DictReader(prod_file)
            logging.debug('Created reader to process file.')
            data = []
            for row in reader:
                logging.debug('Adding to data list %s', row)
                data.append({'product_id': row['product_id'],
                             'description': row['description'],
                             'product_type': row['product_type'],
                             'quantity_available': row['quantity_available']})
                logging.debug('Data added to list.')

        try:
            product_data.insert_many(data)
            count_list.append(data.__len__())
            logging.info('File data loaded.')
        except TypeError as e: # may need to figure out how to accommodate more errors...
            logging.info('Error %s: ', e)
            error_list.append(e)

        # load customer data
        logging.info('Attempting to open %s', customer_file)
        with open(directory_name + '/' + customer_file) as cust_file:
            logging.info('File opened.')
            reader = csv.DictReader(cust_file)
            logging.info('Created reader to process file.')
            data = []
            for row in reader:
                logging.info('Adding to data list %s', row)
                data.append({'customer_id': row['customer_id'],
                             'name': row['name'],
                             'address': row['address'],
                             'phone_number': row['phone_number'],
                             'email': row['email']})
                logging.debug('Data added to list.')

        try:
            customer_data.insert_many(data)
            count_list.append(data.__len__())
            logging.info('File data loaded.')
        except TypeError as e:
            logging.info('Error %s', e)
            error_list.append(e)

        # load rental data
        logging.info('Attempting to open %s', rentals_file)
        with open(directory_name + '/' + rentals_file) as rent_file:
            logging.info('File opened.')
            reader = csv.DictReader(rent_file)
            logging.info('Created reader to process file.')
            data = []
            for row in reader:
                logging.info('Adding to data list %s:', row)
                data.append({'rental_id': row['rental_id'],
                              'customer_id': row['customer_id'],
                              'product_id': row['product_id']})
                logging.debug('Data added to list.')

        try:
            rental_data.insert_many(data)
            count_list.append(data.__len__())
            logging.info('File data loaded.')
        except TypeError as e:
            logging.info('Error %s:', e)
            error_list.append(e)

    # Place holders
    tuple1 = tuple(count_list)
    tuple2 = tuple(error_list)
    return tuple1, tuple2


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
        product_id
        description
        product_type
        quantity_available
    """
    pass


def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information from users that have rented
    products matching product_id:
        user_id
        name
        address
        phone_number
        email
    """
    pass


def main():
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson05/data_files'
    tup1, tup2 = import_data(directory_path, 'product_data.csv',
                                      'customer_data.csv', 'rental_data.csv')

    print(tup1)
    print(tup2)


if __name__ == "__main__":
    main()
