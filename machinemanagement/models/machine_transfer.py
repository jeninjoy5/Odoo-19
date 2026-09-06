from odoo import models,fields,api
from odoo.addons.test_convert.tests.test_env import data
from odoo.cli import Command


class MachineTransfer(models.Model):
    _name = 'machine.transfer'
    _description = 'Transfer'
    _rec_name = 'machine_name_id'
    _inherit = ['mail.thread']


    # FIELDS

    machine_name_id = fields.Many2one('machine.management',
                           string="Machine Name",
                           required=True,
                           domain="[('id','in',allowed_machine_ids)]")
    serial_number = fields.Char(string='Serial Number',
                                related="machine_name_id.serial_number")
    transfer_date = fields.Date(string="Transfer Date")
    transfer_type = fields.Selection([('install','Install'),
                                      ('remove','Remove')],
                                     string="Transfer Type")
    customer_id = fields.Many2one('res.partner',
                                  string="Customer",
                                  tracking=True)
    internal_notes = fields.Html('Internal Notes')
    allowed_machine_ids=fields.Many2many('machine.management')
    transfer_state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')],
                             string="Status",
                             default='draft')



    def action_machine_form_view(self):
        '''Adding customer and changing state'''
        self.machine_name_id.write({'state':"in_service"})
        self.machine_name_id.write({'customer_id':self.customer_id})
        self.write({'transfer_state':'done'})
        # return {
        #     "type": "ir.actions.act_window",
        #     "res_model": "machine.management",
        #     "view_mode": "form",
        #     "res_id": self.machine_name_id.id
        # }


    @api.onchange('transfer_type')
    def _onchange_transfer_type(self):
        '''Showing active and in service machines according to the transfer
        type selected'''
        if self.transfer_type == "install":
            machines=self.env['machine.management'].search([
                ('state', '=', 'active')])
            # self.update({'allowed_machine_ids':[(fields.Command.set(
            #     machines.ids))]})
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
            for rec in machines:
                self.update({'allowed_machine_ids': [(fields.Command.link(
                    rec.id))]})
            if self.machine_name_id and self.machine_name_id.state!='active':
                self.write({'machine_name_id': False})
        elif self.transfer_type == "remove":
            machines=self.env['machine.management'].search([
                ('state', '=', 'in_service')])
            # self.update({'allowed_machine_ids':[(fields.Command.set(
            #     machines.ids))]})
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
            for rec in machines:
                self.update({'allowed_machine_ids': [(fields.Command.link(
                    rec.id))]})
            if (self.machine_name_id and self.machine_name_id.state
                    !='in_service'):
                self.write({'machine_name_id': False})
        else:
            self.update({'allowed_machine_ids':[(fields.Command.clear())]})
















    # @api.model
    # def name_search(self, name='', domain=None, operator='ilike', limit=100):
    #     domain = domain or []
    #     if name:
    #         records = self.search(
    #             ['|',
    #              ('purchase_value', operator, name)] + domain,
    #             limit=limit
    #         )
    #         return records.name_get()
    #     return super().name_search(
    #         name=name, domain=domain, operator=operator, limit=limit
    #     )




