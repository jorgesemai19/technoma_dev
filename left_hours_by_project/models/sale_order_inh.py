from odoo import fields, models, api


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrderInh, self).action_confirm()
        for rec in self:
            if rec.opportunity_id:
                if rec.opportunity_id.hours_package:
                    for h in rec.opportunity_id.hours_package_ids:
                        if h.state in 'draft':
                            h.state = 'approved'
                            h.approval_date = fields.Date.today()
            return res

    @api.multi
    def action_cancel(self):
        res = super(SaleOrderInh, self).action_cancel()
        for rec in self:
            if rec.opportunity_id:
                if rec.opportunity_id.hours_package:
                    for h in rec.opportunity_id.hours_package_ids:
                        if h.state in 'approved':
                            h.state = 'cancel'
            return res

    @api.multi
    def action_draft(self):
        res = super(SaleOrderInh, self).action_draft()
        for rec in self:
            if rec.opportunity_id:
                if rec.opportunity_id.hours_package:
                    for h in rec.opportunity_id.hours_package_ids:
                        if h.state in 'cancel':
                            h.state = 'draft'
                            h.approval_date = None
            return res
