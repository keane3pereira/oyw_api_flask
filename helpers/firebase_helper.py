from models import Registers, Redemptions, Passes
from settings import environment
from firebase_db import db


def update_total_values():

    total_days = 0; total_ends = 0; total_weeks = 0
    redeemed = { 'd': 0, 'e': 0}

    all_pass_register_logs = Registers.find_all_pass_registers()
    for log in all_pass_register_logs:
        total_days += log.days
        total_ends += log.ends
        total_weeks += log.weeks

    all_pass_redemption_logs = Redemptions.find_all_pass_redemptions()
    for log in all_pass_redemption_logs:
        if log.type in ['d','e']:
            redeemed[log.type] += log.qty

    total_weekscanned = Passes.get_total_weekscanned()

    doc_ref = db.collection(environment).document('total_purchased')

    data = doc_ref.set({
        u'weekdays': total_days,
        u'weekends': total_ends,
        u'week': total_weeks,
        u'redeemed_weekdays': redeemed['d'],
        u'redeemed_weekends': redeemed['e'],
        u'redeemed_weeks': total_weekscanned
    })

