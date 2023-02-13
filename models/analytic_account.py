from odoo import fields, models, api


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _description = 'Team Accounting Account Analytic Account'

    compute_here = fields.Float(compute='fetch_data_from_function')
    ann_account_debit = fields.Monetary()
    ann_account_credit = fields.Monetary()
    ann_account_balance = fields.Monetary()

    def fetch_data_from_function(self):
        pass_data = self._compute_debit_credit_balance()
        for rec in pass_data:
            print(rec)
        # self.ann_account_credit = pass_data


