import requests
import csv

PRIMARY_VALIDATOR_IP = '54.219.183.128'
MAX_POINT_VALUE = 281474976710656
VERIFY_KEY_LENGTH = 64

ACCOUNTS_TO_SKIP = [
    "0000000000000000000000000000000000000000000000000000000000000000", # Coin Burnt in this account
    "7658a980ecc4458bad84be5bb239968cf7be96fa18a1197bef3d62f9b93e5410", # Faucet wallet (new)
    "23676c35fce177aef2412e3ab12d22bf521ed423c6f55b8922c336500a1a27c5", # TREASURY (new)
]

# imported from thenewboston-python repo
def validate_response(response):
    """
    Validate status code
    Return response as Python object
    """
    if response.status_code >= 400:
        err = f'status_code:{response.status_code} - {response.text}'
        raise NetworkException(err)

    return response.json()

# imported from thenewboston-python repo
def fetch(*, url, headers):
    """Send a GET request and return response as Python object"""
    response = requests.get(url, headers=headers)
    return validate_response(response)

def fetch_account_data():
    """
    Fetch all account data from primary validator
    Return list of accounts
    """
    results = []

    next_url = f'http://{PRIMARY_VALIDATOR_IP}/accounts'

    while next_url:
        print(next_url)
        data = fetch(url=next_url, headers={})
        accounts = data['results']
        results += accounts
        next_url = data['next']

    return results

account_data_results = fetch_account_data()

# returns the total supply of coin
def coins_supply():
    total_coins_supplied = 0

    for account in account_data_results:
        if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
            total_coins_supplied += int(account['balance'])
    return total_coins_supplied

global_coin_supply = coins_supply()

def wallet_data():
    more_than_zero = 0
    more_than_1000 = 0
    more_than_10000 = 0
    more_than_100000 = 0
    more_than_200000 = 0
    more_than_300000 = 0
    more_than_400000 = 0
    more_than_500000 = 0
    no_balance = 0

    for account in account_data_results:
        if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
            if int(account['balance']) > 500000:
                more_than_500000 += 1
            elif int(account['balance']) > 400000 and int(account['balance']) < 500000:
                more_than_400000 += 1
            elif int(account['balance']) > 300000 and int(account['balance']) < 400000:
                more_than_300000 += 1
            elif int(account['balance']) > 200000 and int(account['balance']) < 300000:
                more_than_200000 += 1
            elif int(account['balance']) > 100000 and int(account['balance']) < 200000:
                more_than_100000 += 1
            elif int(account['balance']) > 10000 and int(account['balance']) < 100000:
                more_than_10000 += 1
            elif int(account['balance']) > 1000 and int(account['balance']) < 10000:
                more_than_1000 += 1
            elif int(account['balance']) > 0 and int(account['balance']) < 1000:
                more_than_zero += 1
            else:
                no_balance += 1

    print(f"Total Accounts: {len(account_data_results)}")
    print(f"Accounts with more than 500,000 coins: {more_than_500000}")
    print(f"Accounts between 400,000 - 500,000 coins: {more_than_400000}")
    print(f"Accounts between 300,000 - 400,000 coins: {more_than_300000}")
    print(f"Accounts between 200,000 - 300,000 coins: {more_than_200000}")
    print(f"Accounts between 100,000 - 200,000 coins: {more_than_100000}")
    print(f"Accounts between 10,000 - 100,000 coins: {more_than_10000}")
    print(f"Accounts between 1,000 - 10,000 coins: {more_than_1000}")
    print(f"Accounts between 0 - 1,000 coins: {more_than_zero}")
    print(f"Accounts with no coins: {no_balance}")

print()
print(f"Total coins in circulation: {global_coin_supply}")
print("---------------------------")
wallet_data()
