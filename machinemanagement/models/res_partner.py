from odoo import models,fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    machine_count = fields.Integer(
        string="Machine Count",
        compute='_compute_machine_count'
    )
    active = fields.Boolean(default=True)

    def action_view_machines(self):
        '''Smart button for transfer history'''
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.management",
            "name": ("Machines"),
            "view_mode": "list,form",
            "domain": [('customer_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_machine_count(self):
        '''Counting machines'''
        for machine in self:
            machine.machine_count = self.env[
                'machine.management'].search_count([
                ('customer_id', '=', self.id)])

    def write(self,vals):
        if 'active' in vals and not vals['active']:
            self.env['machine.management'].search(
                [('customer_id', 'in', self.ids)]).active = False
        res = super(ResPartner, self).write(vals)
        return res



        # self.machine_count = 0
        #
        # all_partners = self.with_context(active_test=False).search_fetch(
        #     [('id', 'child_of', self.ids)],
        #     ['parent_id'],
        # )
        # machine_groups = self.env['machine.management']._read_group(
        #     domain=[('partner_id', 'in', all_partners.ids)],
        #     groupby=['partner_id'], aggregates=['__count'],
        # )
        # self_ids = set(self._ids)
        #
        # for partner, count in machine_groups:
        #     while partner:
        #         if partner.id in self_ids:
        #             partner.purchase_order_count += count
        #         partner = partner.parent_id


