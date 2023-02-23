from odoo import fields, models, api


class TeamPandL(models.TransientModel):
    _name = 'team.pandl'
    _description = 'Team Profit and Loss'

    profit_and_loss_date_start = fields.Datetime('Date Start')
    profit_and_loss_date_end = fields.Datetime('Date End')
    connection = fields.One2many('team.pandl.line', 'team_and_l')


class TeamPandLLine(models.TransientModel):
    _name = 'team.pandl.line'
    _description = 'Team Profit and Loss Move Line'

    team_and_l = fields.Many2one('team.pandl')
    analytic_acc = fields.Many2one('account.analytic.account', 'Analytic Account')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    balance = fields.Float('Balance')










