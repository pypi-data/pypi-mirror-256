from flask import Flask, request, jsonify
from src.bitsidy_sdk import BitsidySDK

app = Flask(__name__)


@app.route('/callback-url', methods=['POST'])
def callback_url():
    encrypted_data = request.json.get('data')

    bitsidy_sdk = BitsidySDK('your_api_key', 'your_store_id')
    try:
        decrypted_data = bitsidy_sdk.get_callback_content(encrypted_data)
    except Exception as error:
        print('Error decrypting data:', error)
        return jsonify(message='Error decrypting data'), 500

    transaction_id = decrypted_data.get('transactionId')
    order_id = decrypted_data.get('orderId')
    invoice_amount = decrypted_data.get('invoiceAmount')
    invoice_amount_usd = decrypted_data.get('invoiceAmountUsd')
    status = decrypted_data.get('status')
    payload = decrypted_data.get('payload')
    custom_string = decrypted_data.get('customString')
    received_amount = decrypted_data.get('receivedAmount')

    print('Transaction ID:', transaction_id)  # A unique identifier for the transaction.
    print('Order ID:', order_id)  # Your local order ID that you passed to the invoice creation method. None if was not passed.
    print('Invoice Amount:', invoice_amount)  # The amount of the created invoice in the specified cryptocurrency.
    print('Invoice Amount USD:', invoice_amount_usd)  # The amount of the created invoice in USD.
    print('Status:', status)  # Current status of the invoice. List of all statuses available here.
    print('Payload:', payload)  # A field for additional information, if any. Usually the same as status.
    print('Custom String:', custom_string)  # The custom string you passed to the invoice creation method. None if was not passed.
    print('Received Amount:', received_amount)  # The amount received for the invoice in the specified cryptocurrency so far.

    return 200


if __name__ == '__main__':
    app.run(port=3000)
