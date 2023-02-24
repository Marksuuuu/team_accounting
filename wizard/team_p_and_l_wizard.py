from odoo import fields, models, api


class TeamPandL(models.TransientModel):
    _name = 'team.pandl'
    _description = 'Team Profit and Loss'

    name = fields.Char(string="Profit and Loss", readonly=True, copy=False, default='New')
    state = fields.Selection(selection=[
        ('post', 'Post'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled'),
        ('draft', 'Draft'),
    ], string='Status', readonly=True, copy=False, tracking=True, default='draft')

    profit_and_loss_date_start = fields.Datetime('Date Start')
    profit_and_loss_date_end = fields.Datetime('Date End')
    connection = fields.One2many('team.pandl.line', 'team_and_l')
    fetch_analytic_line_data = fields.Float(compute='fetch_analytic_line_data_func')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'team.pandl') or 'New'
        result = super(TeamPandL, self).create(vals)
        return result

    def post_but(self):
        for rec in self:
            rec.state = 'post'

    def confirm_but(self):
        for rec in self:
            rec.state = 'confirm'

    def cancel_but(self):
        for rec in self:
            rec.state = 'cancel'

    def fetch_analytic_line_data_func(self):
        self.fetch_analytic_line_data = 0
        my_function_get = self.connection
        for rec in my_function_get:
            # print(rec.analytic_acc.id)
            fetch_id = rec.analytic_acc.id
            query = "SELECT name,date,amount,unit_amount,account_id FROM public.account_analytic_line WHERE account_id = %s" % fetch_id
            self.env.cr.execute(query)
            data_here = self.env.cr.dictfetchone()
            fetched_data_extracted = list(data_here.values())

            list_data = []
            for data in fetched_data_extracted:
                list_data = data + list_data
                print(list_data)

            # for record in self.connection:
            #     record.write({
            #         'name': fetched_data_extracted[0],
            #         'date_data': fetched_data_extracted[1],
            #         'unit_amm': fetched_data_extracted[2],
            #         'amount': fetched_data_extracted[3],
            #         'acc_id': fetched_data_extracted[4],
            #     })
            #     return record
            # data_fetched = ' '.join([str(rec) for rec in fetched_data_extracted])

            # print(fetched_data_extracted)


class TeamPandLLine(models.TransientModel):
    _name = 'team.pandl.line'
    _description = 'Team Profit and Loss Move Line'

    team_and_l = fields.Many2one('team.pandl')
    test = fields.Many2one('account.analytic.line')
    analytic_acc = fields.Many2one('account.analytic.account', 'Analytic Account')
    debit_line_team = fields.Float('Debit', related='analytic_acc.ann_account_debit', stored=True)
    credit_line_team = fields.Float('Credit', related='analytic_acc.ann_account_credit', stored=True)
    balance_line_team = fields.Float('Balance', related='analytic_acc.ann_account_balance', stored=True)

    name = fields.Char('Name')
    date_data = fields.Datetime('Date')
    amount = fields.Float('Amount')
    unit_amm = fields.Float('Unit Amount')
    acc_id = fields.Integer('Account Id')




    # def _view_data_from_analytic_acc(self):
    #     view_data_from_ann_line = self.env['account.analytic.line']
    #     for rec in view_data_from_ann_line:
    #         view_data = rec.search(
    #             [(view_data_from_ann_line, '=', self.analytic_acc)]
    #         )
    #         print(view_data)
    # def fetch_analytic_line_data_func(self):
    #     my_function_get = self.connection
    #     for rec in my_function_get:
    #         # print(rec.analytic_acc.id)
    #         fetch_id = rec.analytic_acc.id
    #
    #         query = "SELECT name,date,amount,unit_amount,account_id FROM public.account_analytic_line WHERE account_id = %s" % fetch_id
    #         self.env.cr.execute(query)
    #         data_here = self.env.cr.dictfetchone()
    #         fetched_data_extracted = list(data_here.values())
    #         # print(fetched_data_extracted)
    #
    #         qw = "INSERT INTO team_pandl_line (amount) VALUES (30.0) "
    #         self.env.cr.execute(qw)
            # for fetched in fetched_data_extracted:
            #     print(fetched)
                # query = "INSENT INTO name,date,amount,unit_amount,account_id FROM public.account_analytic_line WHERE account_id = %s" % fetch_id
                # self.env.cr.execute(query)
                # save_in_name = rec.name[fetched[0]]
                # save_in_date_data = rec.name[fetched[1]]
                # save_in_amount = rec.name[fetched[2]]
                # save_in_unit_amm = rec.name[fetched[3]]
                # save_in_acc_id = rec.name[fetched[4]]
                #
                # return save_in_name, save_in_date_data, save_in_amount, save_in_unit_amm, save_in_acc_id

            # fetched_data_extracted_var = fetched_data_extracted + fetched_data_extracted_var
            # print(fetched_data_extracted_var)






















