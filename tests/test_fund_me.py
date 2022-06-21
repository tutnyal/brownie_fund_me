from pytest import raises, skip
import pytest
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_NETWORKS, get_accounts
from brownie import accounts, network, exceptions


def test_fund_withdraw():
    account = get_accounts()
    fund_me = deploy_fund_me()
    entranceFee = fund_me.getEntranceFee() + 100
    # print(entranceFee)
    # fund_txn = fund_me.fundMe({"from": account, "value": entranceFee})
    # fund_txn_wait = fund_txn.wait(1)
    # assert fund_me.AddressToFunds(account.address) == entranceFee
    # wdraw_txn = fund_me.withdrawFunds({"from": account})
    # wdraw_txn_wait = wdraw_txn.wait(1)
    # assert fund_me.AddressToFunds(account.address) == 0


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("You are not using a development network")
    fund_me = deploy_fund_me()
    bad_account = accounts.add()
    # wdraw_txn = fund_me.withdrawFunds({"from": bad_account})
    with pytest.raises(exceptions.VirtualMachineError):
        wdraw_txn = fund_me.withdrawFunds({"from": bad_account})
        wdraw_txn_wait = wdraw_txn.wait(1)
