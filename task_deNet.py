from web3 import Web3
import requests
import json
import ast

# RPC-узел сети Polygon (можно заменить на свой)
RPC_URL = "https://polygon-rpc.com"

# Адрес контракта токена
TOKEN_ADDRESS = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"

# ABI ERC-20 (стандартный интерфейс)
ABI_URL = "https://gist.githubusercontent.com/veox/8800debbf56e24718f9f483e1e40c35c/raw/f853187315486225002ba56e5283c1dba0556e6f/erc20.abi.json"

def load_abi_from_github(url):
    response = requests.get(url)
    return json.loads(response.text)

ERC20_ABI = load_abi_from_github(ABI_URL)

# Подключаемся к сети Polygon
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_balance(token_address, user_address ):
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=ERC20_ABI)
    # Получаем баланс
    balance = token_contract.functions.balanceOf(web3.to_checksum_address(user_address)).call()
    print(f"Баланс: {balance} TBY")

def get_balance_batch(token_address, *user_address):
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = [token_contract.functions.balanceOf(web3.to_checksum_address(i)).call() for i in user_address]
    print(balance)


# def get_all_holders():
#     TRANSFER_TOPIC = "0x" + web3.keccak(text="Transfer(address,address,uint256)").hex()
#     """ Получает список всех адресов, участвовавших в переводах токена """
#     # Передаем фильтрацию по topic без указания конкретных адресов
#     logs = web3.eth.get_logs({
#         "fromBlock": "earliest",
#         "toBlock": "latest",
#         "address": web3.to_checksum_address(TOKEN_ADDRESS),  # Преобразуем адрес токена в формат с 0x
#         "topics": [TRANSFER_TOPIC]  # Фильтруем только по теме события Transfer
#     })
#     print(logs)

#     holders = set()
#     for log in logs:
#         # Преобразуем байтовые данные в адрес с префиксом 0x
#         sender = web3.to_checksum_address("0x" + log["topics"][1].hex()[26:])  # 26: для обрезки лишнего
#         receiver = web3.to_checksum_address("0x" + log["topics"][2].hex()[26:])  # 26: для обрезки лишнего
#         holders.add(sender)
#         holders.add(receiver)

#     return list(holders)

# def get_top_balances(n):
#     """ Получает топ N адресов по балансу """
#     holders = get_all_holders()
#     print(holders)

#     contract = web3.eth.contract(address=web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)

#     balances = []
#     for holder in holders:
#         balance = contract.functions.balanceOf(web3.to_checksum_address(holder)).call()
#         if balance > 0:  # Игнорируем нулевые балансы
#             balances.append((holder, balance))

#     balances.sort(key=lambda x: x[1], reverse=True)

#     return balances[:n]


# Главная функция для обработки команд

while True:
    user_input = input("Введите команду: ")

    if user_input.startswith("get_balance_batch"):
        # Пример: get_several_balances 0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d 0x1234567890abcdef1234567890abcdef12345678
        _, addresses_str = user_input.split(' ', 1)
        addresses = ast.literal_eval(addresses_str)  # Преобразуем строку в список
        get_balance_batch(TOKEN_ADDRESS, *addresses)

    elif user_input.startswith("get_balance"):
        # Пример: get_balance 0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d
        _, address = user_input.split(" ", 1)
        address = address.strip('["]')  # Убираем лишние кавычки, если они есть
        get_balance(TOKEN_ADDRESS, address)
