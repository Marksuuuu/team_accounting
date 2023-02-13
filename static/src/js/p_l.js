odoo.define('client_act.sale_cust', function (require) {
   'use strict';
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var rpc = require('web.rpc');
   var FormController = require('web.FormController');
   var QWeb = core.qweb;
   var SaleCustom = AbstractAction.extend({

   template: 'SaleCust',
       events: {
            'click #pdf': 'print_pdf',
            'click #xlsx': 'print_xlsx',
            'click .gl-line': 'show_drop_down',
       },
       init: function(parent, action) {
           this._super(parent, action);
       },

       print_pdf: function(e){
            console.log('Test...')
            e.preventDefault();
            var self = this;
            var action_title = self._title
            self._rpc({
                model: 'account.move',
                method: 'view_report',
                args: [
                    [self.wizard_id], action_title
                ],
            }).then(function(data) {
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name': 'team_accounting.new_debit_credit_memo_report_id',
                    'report_file': 'team_accounting.new_debit_credit_memo_report_id',
                    'data': {
                        'report_data': data
                    },
                    'context': {
//                        'active_model': 'account.general.ledger',
//                        'landscape': 1,
//                        'trial_pdf_report': true
                    },
                    'display_name': action_title,
                };
                return self.do_action(action);
            });
       },
       show_drop_down: function(event) {
            event.preventDefault();
            var self = this;
            var account_id = $(event.currentTarget).data('account-id');
            var offset = 0;
            var td = $(event.currentTarget).next('tr').find('td');
            if (td.length == 1) {
                    var action_title = self._title
                    self._rpc({
                        model: 'account.general.ledger',
                        method: 'view_report',
                        args: [
                            [self.wizard_id], action_title
                        ],
                    }).then(function(data) {
                    _.each(data['report_lines'], function(rep_lines) {
                            _.each(rep_lines['move_lines'], function(move_line) {

                             move_line.debit = self.format_currency(data['currency'],move_line.debit);
                             move_line.credit = self.format_currency(data['currency'],move_line.credit);
                             move_line.balance = self.format_currency(data['currency'],move_line.balance);


                             });
                             });

                    for (var i = 0; i < data['report_lines'].length; i++) {

                    if (account_id == data['report_lines'][i]['id'] ){

                    $(event.currentTarget).next('tr').find('td .gl-table-div').remove();
                    $(event.currentTarget).next('tr').find('td ul').after(
                        QWeb.render('SubSection', {
                            account_data: data['report_lines'][i]['move_lines'],
                            currency_symbol : data.currency[0],
                            currency_position : data.currency[1],

                        }))
                    $(event.currentTarget).next('tr').find('td ul li:first a').css({
                        'background-color': '#00ede8',
                        'font-weight': 'bold',
                    });
                     }
                    }

                    });
            }
        },



       start: function() {
           var self = this;
//           alert("Hello")
           self.load_data();
       },
       load_data: function () {
           var self = this;
                   var self = this;
                   self._rpc({
                       model: 'account.custom',
                       method: 'get_sale_order',
                       args: [],
                   }).then(function(datas) {
                   console.log("dataaaaaa", datas)
                       self.$('.table_view').html(QWeb.render('SaleTable', {
                                  report_lines : datas,
                       }));
                   });
           },
    //PRINTING PDF HERE//
   });
   core.action_registry.add("sale_cust", SaleCustom);
   return SaleCustom;
});