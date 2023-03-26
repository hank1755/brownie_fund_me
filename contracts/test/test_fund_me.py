from scripts.utilities import get_account
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.gotEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # this may be wrong: whatif account.address funds more than once?
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.fund({"from": account})
    tx2.wait(1)
    assert (
        fund_me.addressToAmountFunded(account.address) == 0
    )  # confirm all funds funded were withdrawn
