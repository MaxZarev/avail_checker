import os
import time

import requests
from eth_account.messages import encode_defunct
from web3 import Web3

if __name__ == '__main__':
    total = 0
    print("Подписывайся  https://t.me/maxzarev")
    web3 = Web3(Web3.HTTPProvider('https://eth-mainnet.public.blastapi.io'))

    with open('private_keys.txt') as f:
        private_keys = f.read().splitlines()

    for private_key in private_keys:
        account = web3.eth.account.from_key(private_key)
        timestamp = int(time.time())

        message_text = f'Greetings from Avail!\n\nSign this message to check your eligibility. This signature will not cost you any fees.\n\nTimestamp: {timestamp}'
        text_hex = "0x" + message_text.encode('utf-8').hex()  # Преобразуем текст в hex
        text_encoded = encode_defunct(hexstr=text_hex)  # Кодируем текст
        signed_message = web3.eth.account.sign_message(text_encoded, private_key=account.key)  # Подписываем сообщение
        signature = signed_message.signature  # Получаем подпись
        signature = signature.hex()

        post_url = "https://claim-api.availproject.org/check-rewards"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "account": account.address.lower(),
            "type": "ETHEREUM",
            "timestamp": timestamp,
            "signedMessage": signature,

        }
        response = requests.post(post_url, headers=headers, json=data)
        if response.json()['message'] == "Not Eligible":
            print(f'{account.address} Not Eligible')

        elif response.json()['message'] == "Claim":
            total += response.json()['data']['reward_amount_avail']
            print(f'{account.address} Claim {response.json()["data"]["reward_amount_avail"]}, Total: {total}')
    print(f'Total: {total}')
