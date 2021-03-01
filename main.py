import requests
import csv

from thenewboston.constants.network import MAX_POINT_VALUE, VERIFY_KEY_LENGTH
from thenewboston.utils.network import fetch

PRIMARY_VALIDATOR_IP = '157.230.75.212'

ACCOUNTS_TO_SKIP = [
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

# returns the list of all core team members
def core_team_account_number_list():
    team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Payment-Processor/master/csvs/teams.csv'

    team_data = requests.get(team_url).text

    contributor_account_number_list = []

    with open('data_files/contributors.csv', 'w') as file:
        file.write(team_data)

    with open('data_files/contributors.csv', 'r') as file:
        reader = csv.reader(file)

        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row[10]) == VERIFY_KEY_LENGTH:
                    contributor_account_number_list.append(row[10])

    return contributor_account_number_list


# Returns total balance of the core team of thenewboston 
def core_team():

    total_coins_supplied = 0

    data = fetch_account_data()

    contributor_account_number_list = core_team_account_number_list()

    for account in data:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins in core team: " + str(total_coins_supplied))
    return total_coins_supplied

# returns the list of all project team members
def project_team_account_number_list():
    team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Project-Proposals/master/CSVs/project-teams.csv'

    team_data = requests.get(team_url).text

    contributor_account_number_list = []

    with open('data_files/contributors.csv', 'w') as file:
        file.write(team_data)

    with open('data_files/contributors.csv', 'r') as file:
        reader = csv.reader(file)

        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row[10]) == VERIFY_KEY_LENGTH:
                    contributor_account_number_list.append(row[10])

    return contributor_account_number_list


# Returns total balance of the project team members of thenewboston 
def project_team():

    total_coins_supplied = 0
    
    data = fetch_account_data()

    contributor_account_number_list = project_team_account_number_list()

    for account in data:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])
        
    print("Total coins with project teams: " + str(total_coins_supplied))
    return total_coins_supplied


# returns the account number of all the contributors
def all_contributor_account_number_list():
    team_url = 'https://raw.githubusercontent.com/thenewboston-developers/Payment-Processor/master/csvs/contributors.csv'

    team_data = requests.get(team_url).text

    contributor_account_number_list = []

    with open('data_files/contributors.csv', 'w') as file:
        file.write(team_data)

    with open('data_files/contributors.csv', 'r') as file:
        reader = csv.reader(file)

        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row[2]) == VERIFY_KEY_LENGTH:
                    contributor_account_number_list.append(row[2])
    return contributor_account_number_list


# Returns total balance of the all the contributors of thenewboston 
def all_contributors():

    total_coins_supplied = 0
    
    data = fetch_account_data()

    contributor_account_number_list = all_contributor_account_number_list()

    for account in data:
        if str(account['account_number']) in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins with all the contributors: " + str(total_coins_supplied))
    return total_coins_supplied


# Returns total balance of contributors that are not part of weekly payment in thenewboston 
def contributors_not_in_team():

    total_coins_supplied = 0

    data = fetch_account_data()

    contributor_account_number_list = all_contributor_account_number_list()

    for account in data:
        if str(account['account_number']) not in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("Total coins with contributors that are not part of team: " + str(total_coins_supplied))
    return total_coins_supplied


# Coins in normal wallets
def normal_wallets():

    total_coins_supplied = 0

    contributor_account_number_list = all_contributor_account_number_list()
    
    data = fetch_account_data()

    for account in data:
        if str(account['account_number']) not in contributor_account_number_list:
            if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
                total_coins_supplied += int(account['balance'])

    print("total coins in normal wallets: " + str(total_coins_supplied))
    return total_coins_supplied


# returns the total supply of coin
def coins_supply():
    total_coins_supplied = 0
    
    data = fetch_account_data()

    for account in data:
        if str(account['account_number']) not in ACCOUNTS_TO_SKIP:
            total_coins_supplied += int(account['balance'])
    print("total supply of coin: " + str(total_coins_supplied))
    return total_coins_supplied


coins_supply()              # Returns the supply of the coin
core_team()                 # Returns total balance of the core team of thenewboston
project_team()              # Returns total balance of the project team members of thenewboston
all_contributors()          # Returns total balance of the all the contributors of thenewboston
contributors_not_in_team()  # Returns total balance of contributors that are not part of weekly payment in thenewboston
normal_wallets()            # Returns the total amount of coins in the regular wallets
