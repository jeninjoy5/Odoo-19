from odoo import models,fields,api


class MachineOrderLine(models.Model):
    _name = 'machine.order.line'

    order_id = fields.Many2one('machine.management',
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
    parts_uom_id = fields.Many2one(comodel_name='uom.uom',
                                   string="Unit")




