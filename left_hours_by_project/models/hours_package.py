from odoo import fields, models, api


class HoursPackage(models.Model):
    _name = 'hours.package'
    _description = 'This module handles the hours package crated in the CRM module to have control about' \
                   'the hours consumed in timesheet in relation to budget'
    _order = 'approval_date desc'

    name = fields.Char(string='Description')
    hours_from_budget = fields.Float(
        string='Hours from budget',
        required=False)
    package_type_ids = fields.Many2many(
        comodel_name='hours.package.type',
        string='Hours package types')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=False)
    crm_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Origin',
        required=False,
        readonly=True)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('approved', 'Approved'),
                   ('cancel', 'Cancel'),
                   ('consumed', 'Consumed')],
        required=False,
        default='draft')
    available_hours = fields.Float(
        string='Hours Available',
        required=False,
        compute='compute_hours_used_and_available')
    hours_used = fields.Float(
        string='Hours used',
        required=False,
        compute='compute_hours_used_and_available')
    integer_hours = fields.Boolean(
        string='Integer hours',
        required=False)
    active = fields.Boolean(
        string='Active',
        required=False,
        default='True',)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        index=True,
        default=lambda self: self.env.user.company_id.id)
    approval_date = fields.Date(
        string='Approval date',
        required=False)
    analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line',
        inverse_name='hours_package_id',
        string='Analytic lines ',
        required=False)

    def has_decimals(self, number):
        var_to_string = str(number)
        decimal_string = var_to_string.split('.')
        if int(decimal_string[1]) > 0:
            return True
        else:
            return False

    @api.depends('analytic_line_ids', 'integer_hours')
    def compute_hours_used_and_available(self):
        for rec in self:
            var = 0
            for lines in rec.analytic_line_ids.mapped('unit_amount'):
                if rec.integer_hours:
                    if lines > 0:
                        if lines <= 1:
                            var += 1
                        else:
                            if rec.has_decimals(lines):
                                var += int(lines) + 1
                            else:
                                var += int(lines)
                else:
                    var += lines
            rec.hours_used = var
            rec.available_hours = rec.hours_from_budget - var

    @api.multi
    def get_hours_used_and_available(self):
        for rec in self:
            var = 0
            timesheet = rec.env['account.analytic.line'].search([('hours_package_id', '=', rec.id)])
            if rec.state == 'approved':
                if len(timesheet) > 0:
                    for t in timesheet:
                        if rec.integer_hours:
                            if t.unit_amount > 0:
                                if t.unit_amount <= 1:
                                    var += 1
                                else:
                                    if rec.has_decimals(t.unit_amount):
                                        var += int(t.unit_amount) + 1
                                    else:
                                        var += int(t.unit_amount)
                        else:
                            var += t.unit_amount
                    rec.hours_used = var
                    rec.available_hours = rec.hours_from_budget - rec.hours_used
                    if rec.available_hours <= 0:
                        rec.state = 'consumed'

    @api.multi
    def update_all_package_hours(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        update = self.env['hours.package'].browse(active_ids)
        for p in update:
            p.get_hours_used_and_available()
