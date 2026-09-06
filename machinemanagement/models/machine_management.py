from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError
from odoo.orm.decorators import readonly


class MachineManagement(models.Model):
    _name = 'machine.management'
    _description = 'Machine'
    _inherit = ['mail.thread']
    _rec_name = 'machine_name'

    # FIELDS

    name = fields.Char(string='Reference',
                       required=True, copy=False,
                       readonly=True,
                       default=lambda self: 'New')
    machine_name = fields.Char(string='Name',
                               required = True,
                               help="Name of the Machine")
    date_of_purchase = fields.Date(string='Date of purchase',
                                 help="Date of purchase")
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
    purchase_value = fields.Monetary(string='Purchase Value',
                                     tracking=True,
                                     help="Purchase Value")
    customer_id = fields.Many2one(comodel_name='res.partner',
                                  string='Customer',
                                  tracking=True,
                                  help="Name of the Customer")
    serial_number = fields.Char('Serial Number',
                                help="Unique Serial Number for the Machine",
                                required=True)
    machine_type_id=fields.Many2one(comodel_name='machine.type',
                                    string='Machine Type',
                                    help="Type of the Machine")
    state = fields.Selection([('active', 'Active'),
                              ('in_service', 'In Service')],
                             string="Status",
                             default='active')
    image = fields.Image(string='Image')
    is_warranty = fields.Boolean(string='Is Warranty',
                                 default=False,
                                 tracking=True,
                                 help="Is the Machine has Warranty or not")
    machine_tag_ids=fields.Many2many(comodel_name='machine.tag',
                                   string='Tags')
    description = fields.Text(string='Description')
    instructions = fields.Html(string='Instructions')
    machine_transfer_count = fields.Integer(string='Transfers',
                                    compute='compute_machine_transfer_count')
    order_line_ids = fields.One2many(comodel_name='machine.order.line',
                                     inverse_name='order_id',
                                     string="Order Lines",copy=True)
    machine_age = fields.Integer(string='Machine Age',
                                 compute='_compute_machine_age')
    machine_service_count = fields.Integer(string='Services',
                                    compute='_compute_machine_service_count')
    active = fields.Boolean(default=True)


    @api.model_create_multi
    def create(self, vals_l):
        '''Creating sequence number'''
        for vals in vals_l:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'machine.management') or 'New'
        return super(MachineManagement, self).create(vals_l)


    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        '''Validating purchase value'''
        for rec in self:
            if rec.purchase_value<=0:
                raise ValidationError("Purchase Value must be greater than 0")


    @api.constrains('serial_number')
    def _check_serial_number(self):
        '''Checking serial number whether unique or not'''
        for rec in self:
            domain = [('serial_number', '=', rec.serial_number)]
            count = rec.search_count(domain)
        if count > 1:
            raise ValidationError(("The Serial Number should be unique"))


    def action_view_machine_transfer(self):
        '''Smart button for transfer history'''
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.transfer",
            "name": ("Machine Transfers"),
            "view_mode": "list,form",
            "domain": [('machine_name_id', '=', self.id)],
            'context': "{'create': False}"
        }


    def compute_machine_transfer_count(self):
        '''Counting transfers'''
        for transfer in self:
            transfer.machine_transfer_count = self.env[
                'machine.transfer'].search_count([
                ('machine_name_id', '=', self.id)])


    def action_machine_transfer_form_view(self):
        '''Action for button in machine management form'''
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.transfer",
            "view_mode": "form",
            "context": {'default_machine_name_id': self.id,
                        'default_transfer_type':'install'}

        }

    @api.depends('date_of_purchase')
    def _compute_machine_age(self):
        """Calculate machine age from purchase date"""
        for record in self:
            if record.date_of_purchase:
                today = fields.Date.today()
                purchase = record.date_of_purchase
                record.machine_age = today.year - purchase.year - (
                        (today.month, today.day) < (purchase.month, purchase.day))
            else:
                record.machine_age = 0

    def action_service_form_view(self):
        return {
                "type": "ir.actions.act_window",
                "res_model": "machine.service",
                "view_mode": "form",
                "context": {'default_machine_name_id': self.id}
        }

    def action_view_machine_service(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "machine.services",
            "name": ("Machine Services"),
            "view_mode": "list,form",
            "domain": [('machine_name_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _compute_machine_service_count(self):
        for service in self:
            service.machine_service_count = self.env[
                'machine.service'].search_count([
                ('machine_name_id', '=', self.id)])

    def unlink(self):
        for machine in self:
            if machine.state == 'in_service':
                raise UserError("You cannot delete this machine because it is"
                                " already transferred")
        return super().unlink()





    # @api.depends('name', 'machine_name')
    # def _compute_display_name(self):
    #     for record in self:
    #         name = record.name or ''
    #         if record.machine_name:
    #             name = f'[{record.machine_name}] {name}'
    #         record.display_name = name










