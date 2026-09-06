from odoo import models,fields


class MachineType(models.Model):
    _name = "machine.type"

    # FIELDS

    name = fields.Char(string="Name")