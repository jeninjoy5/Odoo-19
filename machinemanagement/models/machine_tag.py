from odoo import models,fields


class MachineType(models.Model):
    _name = "machine.tag"

    # FIELDS

    name = fields.Char(string="Name")