import requests
from pathlib import Path
from datetime import datetime
import os
'''
data_folder = Path("source_data/text_files/")
file_to_open = data_folder / "raw_data.txt"
f = open(file_to_open)
print(f.read())
'''


def create_folder(foldername, filename, data):
    date = datetime.now().strftime("%d-%m-%Y")
    dir = f'/{date}/{foldername}/{filename}'
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    with open(filename, "w") as f:
        f.write(data)


def handle_url(url, filename):
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the file name from the response headers
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = 'downloaded_file.txt'  # Default filename if not provided in headers

        # Open a file in binary write mode
        with open(filename, 'wb') as file:
            # Iterate over the response content in chunks and write to the file
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File '{filename}' downloaded successfully!")
    else:
        print("Failed to download the file.")


BASE_URL = 'http://127.0.0.1:8000/backup/'



def fetch_vendors():
    handle_url(BASE_URL + 'vendors/', 'vendors.xls')
    print('url: ', BASE_URL + 'vendors/')
    handle_url(BASE_URL + 'vendors-notes/', 'vendor_notes.xls')
    handle_url(BASE_URL + 'employers/', 'vendor_employers.xls')
    handle_url(BASE_URL + 'vendor-payments/', 'vendor_payments.xls')
    handle_url(BASE_URL + 'vendor-banking-account/', 'vendor_banking_account.xls')
    handle_url(BASE_URL + 'invoices/', 'invoices.xls')
    print('vendors')


def fetch_products():
    handle_url(BASE_URL + 'products/', 'products.xls')
    handle_url(BASE_URL + 'products-vendor/', 'products_vendor.xls')
    handle_url(BASE_URL + 'product-categories/', 'product_categories.xls')
    print('products')


def fetch_payrolls():
    handle_url(BASE_URL + 'generic-expenses/', 'generic_expenses.xls')
    handle_url(BASE_URL + 'payrolls/', 'payrolls.xls')
    handle_url(BASE_URL + 'occupation/', 'occupation.xls')
    handle_url(BASE_URL + 'bills/', 'bills.xls')
    handle_url(BASE_URL + 'bill-categories/', 'bill_categories.xls')
    handle_url(BASE_URL + 'generic-expenses-category/', 'generic_expenses_category.xls')
    handle_url(BASE_URL + 'persons/', 'persons.xls')


def fetch_orders():
    handle_url(BASE_URL + 'orders/', 'orders.xls')
    handle_url(BASE_URL + 'orders/payment/', 'orders_payment.xls')

    taxes_modifier = ['http://127.0.0.1:8000/backup/taxes-modifier/', 'taxes_modifiers.xls']
    handle_url(taxes_modifier[0], taxes_modifier[1])


def fetch_general():
    handle_url(BASE_URL + 'payments-methods/', 'payment_methods.xls')
    handle_url(BASE_URL + 'incomes/', 'incomes.xls')

def fetch_notebooks():
    handle_url(BASE_URL + 'tags/', 'notebook.xls')
    handle_url(BASE_URL + 'notebooks/', 'tags.xls')


def general_expenses():
    handle_url(BASE_URL + 'folder/general-expenses/', 'general_expenses_folder.xls')
    handle_url(BASE_URL + 'folder/general-expenses-category/', 'general_expenses_category_folder.xls')


def customers():
    customers = ['http://127.0.0.1:8000/backup/invoice-items/', 'invoice_items.xls']
    customers_details = ['http://127.0.0.1:8000/backup/my-cards/', 'my_cards.xls']
    payment_invoices = ['http://127.0.0.1:8000/backup/customers/', 'customers_details.xls']
    payment_items = ['http://127.0.0.1:8000/backup/customers-details/', 'taxes_modifiers.xls']
    my_cars = ['http://127.0.0.1:8000/backup/payment-invoices/', 'payment_invoices.xls']

    handle_url(customers[0], customers[1])
    handle_url(customers_details[0], customers_details[1])
    handle_url(payment_invoices[0], payment_invoices[1])
    handle_url(payment_items[0], payment_items[1])
    handle_url(my_cars[0], my_cars[1])



fetch_vendors()
fetch_products()
customers()
general_expenses()
fetch_notebooks()
fetch_general()
fetch_payrolls()

fetch_orders()


