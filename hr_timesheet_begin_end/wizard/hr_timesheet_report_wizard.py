# Copyright 2018-2020 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class HrTimesheetReportWizardField(models.AbstractModel):
    _inherit = 'hr.timesheet.report.wizard.field'

    @api.model
    def _selection_field_name(self):
        fields = self.env['account.analytic.line'].fields_get()
        fields.pop('unit_amount')
        fields = fields.items()
        if fields:
            print('prueba')
        #fields = self.env['account.analytic.line'].fields_get().items()
        return [
            (f, d.get('string')) for f, d in fields if self._field_selectable(
                f, d)
        ]