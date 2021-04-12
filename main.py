import requests
import csv

PRIMARY_VALIDATOR_IP = '54.219.183.128'
MAX_POINT_VALUE = 281474976710656
VERIFY_KEY_LENGTH = 64

ACCOUNTS_TO_SKIP = [
    "0000000000000000000000000000000000000000000000000000000000000000", # Coin Burnt in this account
    "7658a980ecc4458bad84be5bb239968cf7be96fa18a1197bef3d62f9b93e5410", # Faucet wallet (new)
    "23676c35fce177aef2412e3ab12d22bf521ed423c6f55b8922c336500a1a27c5", # TREASURY (new)
    "6ad6deef2a65642a130fb081dacc2010c7521678986ed44b53a845bc00dd3924", # TREASURY
    "9bfa37627e2dba0ae48165b219e76ceaba036b3db8e84108af73a1cce01fad35", # TREASURY (old)
    "f0fe0fdff41db888a0938882502ee809f6874c015aa09e11e38c8452d4175535", # Payments (Taiwo Odetola)
    "addf211d203c077bc5c6b78f41ddc68481804539de4bd3fd736fa853514551c0", # Payments (Rajput Usman)
    "c536b7717f4c3e3b864e384c2156a44f952223326bc0eab4f2f8be1a34bc2e6d", # Payments (Nikhil Taneja)
    "9cb647da9ea1445c361e6d734a6ee0fce4896230392947713686697dd586495b", # Payments (Tawanda Makunike)
    "0d304450eae6b5094240cc58b008066316d9f641878d9af9dd70885f065913a0", # Held lot of value in past, now has 0
    "ca85c141c945866dd32af37ad669855458eb3f9e5d1a4530d852c3c745de11a7", # Held lot of value in past, now has 0
    "a7381dce0249efc26130dd226ecc0df3154009a0210adc4cac869e4a2cb92d65", # Held lot of value in past, now has 0
    "0c9e43fd6630e213a088bf816425c294248ae496129dadb03137c151a2a22ff6", # Held lot of value in past, now has 0
    "67077b2397f99fb6c63185af25cdf49d43736b22b7ea5dd68089a04cd4dbf8cf"  # Held lot of value in past, now has 0
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

# returns the list of all members
def account_number_list(team):
    team_url = ''
    account_number_position = 0
    file_name = ''
    if team == 'team':
        file_name = 'data_files/teams.csv'
        team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Payment-Processor/master/csvs/teams.csv'
        account_number_position = 10
    elif team == 'project':
        file_name = 'data_files/project-teams.csv'
        account_number_position = 10
        team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Project-Proposals/master/CSVs/project-teams.csv'
    elif team == 'contributor':
        file_name = 'data_files/contributors.csv'
        account_number_position = 2
        team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Payment-Processor/master/csvs/contributors.csv'
    elif team == 'task':
        file_name = 'data_files/tasks.csv'
        team_url = 'https://raw.githubusercontent.com/tomijaga/tnb-supply/master/src/csvs/input/tasks.csv'
        account_number_position = 7
    else:
        Exception("This is not good brruuhh")
    team_data = requests.get(team_url).text

    contributor_account_number_list = []

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(team_data)

    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                try:
                    if len(row[account_number_position]) == VERIFY_KEY_LENGTH:
                        contributor_account_number_list.append(row[account_number_position])
                except:
                    pass

    return contributor_account_number_list


# Returns total balance of the core team of thenewboston
def core_team():

    total_coins_supplied = 0

    contributor_account_number_list = account_number_list('team')

    for account in account_data_results:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins with core team: " + str(total_coins_supplied) + " | " + \
     str(int(total_coins_supplied/global_coin_supply*10000)/100) + "% of total supply")
    return total_coins_supplied

# Returns total balance of the project team members of thenewboston
def project_team():

    total_coins_supplied = 0

    contributor_account_number_list = account_number_list('project')

    for account in account_data_results:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins with project teams: " + str(total_coins_supplied) + " | " + \
    str(int(total_coins_supplied/global_coin_supply*10000)/100) + "% of total supply")
    return total_coins_supplied

# Returns total balance not in core team
def not_in_core_team():

    total_coins_supplied = 0

    contributor_account_number_list = account_number_list('team')

    for account in account_data_results:
        if str(account['account_number']) not in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins in all normal wallets: " + str(total_coins_supplied)+ " | " + \
    str(int((total_coins_supplied/global_coin_supply)*10000)/100) + "% of total supply")
    return total_coins_supplied


# Returns total balance of contributors that are not part of weekly payment in thenewboston
def contributors_not_in_team():

    total_coins_supplied = 0

    team_project_account_number_list = account_number_list('team') + account_number_list('project')

    contributor_account_number_list = account_number_list('contributor')

    for account in account_data_results:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in team_project_account_number_list:
                if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                    total_coins_supplied += int(account['balance'])

    print("Total coins with contributors that are not part of any team: " + str(total_coins_supplied)+ " | " + \
    str(int(total_coins_supplied/global_coin_supply*10000)/100) + "% of total supply")
    return total_coins_supplied


# Coins in normal wallets
def normal_wallets():

    total_coins_supplied = 0

    contributor_account_number_list = account_number_list('team') + account_number_list('contributor') \
         + account_number_list('project')
    for account in account_data_results:
        if str(account['account_number']) not in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins in normal wallets: " + str(total_coins_supplied)+ " | " + \
    str(int(total_coins_supplied/global_coin_supply*10000)/100) + "% of total supply")
    return total_coins_supplied

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
core_team()                 # total coins of the core team of thenewboston
not_in_core_team()          # Returns total balance of the only the contributors of
print("---------------------------")
project_team()              # total coins of the project team members of thenewboston
contributors_not_in_team()  # total coins of contributors that are not part of weekly payment in thenewboston
normal_wallets()            # Total coins not in core, project or the contributor list
print("---------------------------")
wallet_data()
