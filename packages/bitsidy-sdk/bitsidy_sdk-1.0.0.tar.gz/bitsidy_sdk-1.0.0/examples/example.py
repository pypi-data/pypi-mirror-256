import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.bitsidy_sdk import BitsidySDK

bitsidy_sdk = BitsidySDK('your_api_key', 'your_store_id')
invoice_data = {
    'currency': 'BTC',  # Required: Cryptocurrency code, e.g., 'BTC' for Bitcoin. Find all available currencies "here."
    'amount': 10,  # Required: Amount in USD.
    'email': 'payer@example.com',  # Required: Email of the payer.
    'callbackNotify': 'https://yourdomain.com/callback.php',  # Required: Your callback URL.
    'customString': 'Payment for Product XYZ',  # Optional: Custom string for the invoice, displayed on the payment page.
    'orderId': 'order123'  # Optional: Your local order ID for future invoice retrieval. If an existing invoice with this orderId is found, a new invoice will not be created; instead, the existing one will be returned.

}


def create_invoice():
    try:
        response = bitsidy_sdk.create_invoice(invoice_data)

        if not response:
            print('Error creating invoice. Check the console for more details.')
            return

        transaction_id = response.get('transactionId')
        payment_link = response.get('paymentLink')
        status = response.get('status')
        amount = response.get('amount')
        custom_string = response.get('customString')
        email = response.get('email')
        order_id = response.get('orderId')

        print('Transaction ID:', transaction_id)  # A unique identifier for the transaction.
        print('Payment Link:', payment_link)  # Payment link to redirect your clients to.
        print('Status:', status)  # Invoice status, will be 'wait' if the invoice has just been created. List of all statuses available here.
        print('Amount:', amount)  # The amount of the created invoice in the specified cryptocurrency.
        print('Custom String:', custom_string)  # The custom string you passed to the invoice creation method.
        print('Email:', email)  # The customer's email you passed to the invoice creation method.
        print('Order ID:', order_id)  # Your local order ID that you passed to the invoice creation method.

    except Exception as error:
        print('Error creating invoice:', error)


if __name__ == '__main__':
    create_invoice()
