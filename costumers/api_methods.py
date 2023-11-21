

def send_invoices(instance):
    profile = instance.profile
    card = instance.card_info
    xml_items, count = [], 1
    for item in instance.order_items.all():
        xml_items.append({
            'lineNumber': count,
            'quantity': item.qty,
            'measurementUnit': item.unit,
            'netValue': item.total_clean_value,
            'vatCategory': item.taxes_modifier,
            'vatAmount': item.taxes_value,
        })
        count += 1
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    data = {
        'issuer': {
            'vatNumber': card.afm,
            'country': 'GR'.encode('utf-8'),
            'branch': 0,
            'address': {
                'postalCode': card.zipcode.encode('utf-8'),
                'city': card.city.encode('utf-8')
            }
        },
        'counterpart': {
            'vatNumber': profile.afm,
            'country': 'GR',
            'branch': 0,
            'address': {
                'postalCode': card.zipcode,
                'city': profile.destination_city
            }
        },
        'invoiceHeader': {
            'series': instance.series,
            'aa': instance.number,
            'issueDate': instance.date,
            'invoiceType': instance.order_type,
            # 'vehicleNumber': instance.profile.car
            'movePurpose': instance.purpose_of_moving,
            'vehicleNumber': profile.transport,
            'currency': 'EUR'
        },
        'invoiceDetails': xml_items,
        'invoiceSummary': {
            'totalNetValue': instance.clean_value,
            'totalVatAmount': instance.taxes_value,
            'totalWithheldAmount': 0,
            'totalFeesAmount': 0,
            'totalStampDutyamount': 0,
            'totalOtherTaxesAmount': 0,
            'totalDeductionsAmount': 0,
            'totalGrossValue': instance.final_value
        }
    }
    return headers, data

# 30

def send_income_classification(request):
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    data = {
        'invoiceMark': 'Μοναδικός Αριθμός Καταχώρησης Παραστατικού',
        'classificationMark': 'Μοναδικός Αριθμός Καταχώρησης Χαρακτηρισμού',
        'transactionMode': 'Είδος Συναλλαγής choices 1= reject',
        'lineNumber': 'Αριθμός Γραμμής',

    }


def send_expenses_classification(request):
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    data = {
        'invoiceMark': 'Μοναδικός Αριθμός Καταχώρησης Παραστατικού',
        'classificationMark': 'Μοναδικός Αριθμός Καταχώρησης Χαρακτηρισμού',
        'transactionMode': 'Είδος Συναλλαγής choices 1= reject',
        'lineNumber': 'Αριθμός Γραμμής',

    }


def cancel_invoice(request):
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    result = {
        'mark': 'Μοναδικός αριθμός καταχώρησης παραστατικού προς ακύρωση'

    }


def request_docs(request):
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    result = {
        'mark': 'Μοναδικός αριθμός καταχώρηση',
        'nextPartitionKey': '',
        'nextRowKey': ''

    }


def request_transmitted_docs(request):
    headers = {
        # Request headers
        'aade-user-id': 'Zefarak',
        'Ocp-Apim-Subscription-Key': 'fae2cc4901f64e22a16e3319ba9e1947',
    }
    result = {
        'mark': 'Μοναδικός αριθμός καταχώρηση',
        'nextPartitionKey': '',
        'nextRowKey': ''

    }