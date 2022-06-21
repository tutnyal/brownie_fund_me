from brownie import FundMeContrc
from scripts.helpful_scripts import get_accounts


def fund():
    fund_me = FundMeContrc[-1]
    account = get_accounts()
    get_entrance_fee = fund_me.getEntranceFee()
    print(get_entrance_fee)
    fund_me.fundMe({"from": account, "value": get_entrance_fee})


def withdraw():
    withdraw = FundMeContrc[-1]
    account = get_accounts()
    withdraw.withdrawFunds({"from": account})


def main():
    fund()
    withdraw()
