# Copyright 2018-2020 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
import html


class Report(models.AbstractModel):
    #_name = 'report.hr_timesheet_report.report_timeformat'
    _inherit = 'report.hr_timesheet_report.report'

    @api.model
    def _render_value_cell(self, row, col, sheet, formats, entry, field):
        raw_value = entry.any_line_id[field.field_name]
        value = entry.render_value(field.field_name)
        if not raw_value:
            sheet.write(
                row,
                col,
                html.unescape(value),
                formats['cell_generic']
            )
        else:
            if field.field_type == 'datetime':
                sheet.write_datetime(
                    row,
                    col,
                    raw_value,
                    formats['cell_datetime']
                )
            elif field.field_type == 'date':
                sheet.write_datetime(
                    row,
                    col,
                    raw_value,
                    formats['cell_date']
                )
            # Se anhade formato de time a campos time_start y time_stop
            elif field.field_type == 'float' and field.field_name in ('time_start', 'time_stop'):
                sheet.write(
                    row,
                    col,
                    self._convert_amount_num_format(entry.group_id.report_id, raw_value),
                    formats['entry_total']
                )
            else:
                sheet.write(
                    row,
                    col,
                    html.unescape(value),
                    formats['cell_generic']
                )
