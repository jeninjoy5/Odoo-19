from email.policy import default
from functools import total_ordering

from odoo import models,fields,api
from odoo.cli import Command
from odoo.orm.decorators import readonly


class MachineService(models.Model):
    _name = 'machine.service'
    _description = 'Machine Service'
    _rec_name = 'machine_name_id'
    _inherit = ['mail.thread']

    machine_name_id = fields.Many2one('machine.management',
                                      string="Machine Name",
                                      required=True)
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  tracking=True)
    service_date = fields.Datetime(string='Date',
                                   tracking=True)
    description = fields.Text(string='Description')
    internal_notes = fields.Html('Internal Notes')
    service_state = fields.Selection([('open', 'Open'),
                                       ('started', 'Started'),
                                      ('done', 'Done'),
                                      ('cancelled', 'Cancelled')],
                                      string="Status",
                                      default='open')
    company_id = fields.Many2one('res.company',
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    service_order_line_ids = fields.One2many(comodel_name='service.order.line',
                                     inverse_name='order_id',
                                     string="Order Lines", copy=True)
    user_ids = fields.Many2many('res.users',
                                string='Tech Person',
                                tracking=True)


    def action_service_start(self):
        self.write({'service_state': 'started'})

    def action_service_close(self):
        self.write({'service_state': 'done'})

    def action_create_invoice(self):
        for service in self:
            for record in service.service_order_line_ids:
                invoice=self.env['account.move'].create([{
                        'move_type' : 'out_invoice',
                        'partner_id' : self.customer_id.id,
                        'invoice_line_ids' : [fields.Command.create({
                            'product_id' : record.parts_id.id,
                            'quantity' : record.parts_qty,
                            'price_subtotal' : record.price_total

                        })]
                    }])
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id
        }



    #
    # @api.onchange('machine_name_id')
    # def _onchange_machine_name_id(self):
    #     if self.machine_name_id:
    #         parts=self.env['machine.management'].search([('machine_name_id','=',self.machine_name_id)])



class ServiceOrderLine(models.Model):
    _name = 'service.order.line'

    order_id = fields.Many2one('machine.service',
                               string='Order',
                               required=True,
                               ondelete='cascade',
                               index=True,
                               copy=False)
    parts_id = fields.Many2one(string="Parts",
                               comodel_name='product.template',
                               required=True)
    parts_qty = fields.Float(string="Quantity",
                             digits='Product Unit',
                             default=1.0,
                             required=True)
    price_unit = fields.Float(string="Unit Price",
                              related = "parts_id.list_price",
                              readonly=False)
    company_id = fields.Many2one('res.company',
                                 store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self:
                                  self.env.user.company_id.currency_id.id)
    price_total = fields.Monetary(string="Total",
                                  readonly=False,
                                  compute="_compute_price_total")



    @api.depends('parts_id','parts_qty','price_unit')
    def _compute_price_total(self):
        self.price_total=self.parts_qty*float(self.price_unit)


