from odoo import models


class BookBankXlsx(models.AbstractModel):
    _name = 'report.left_hours_by_project.report_hours_package_name'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        domain = [('id', 'in', data['form_data'])]
        obj = self.env['hours.package'].search(domain).sorted(key=lambda r: r.approval_date)
        date_from = data['date_from']
        date_to = data['date_to']
        if data['state'] == 'approved':
            state = 'APROBADOS'
        elif data['state'] == 'cancel':
            state = 'CANCELADOS'
        elif data['state'] == 'consumed':
            state = 'CONSUMIDOS'
        else:
            state = 'TODOS'
        partner_id = data['partner_id']
        partner = self.env['res.partner'].search([('id', '=', partner_id)])
        integer_hours = data['integer_hours']
        report_name = 'REPORTE DE PAQUETES DE HORAS'
        # One sheet by partner
        sheet = workbook.add_worksheet(report_name[:31])
        green = workbook.add_format({'bold': True, 'bg_color': 'green', 'align': 'center', 'num_format': 'dd/mm/yy'})
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format()
        cell_format.set_align('left')
        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        format3 = workbook.add_format({'num_format': '[h]:mm'})
        sheet.merge_range(0, 0, 0, 5, report_name, green)
        sheet.set_column(0, 0, 35, cell_format, {'collapsed': 1})
        sheet.set_column(1, 1, 40, cell_format, {'collapsed': 1})
        sheet.set_column(2, 6, 25, cell_format, {'collapsed': 1})
        sheet.write(1, 0, 'FECHA DESDE', bold)
        sheet.write(1, 1, date_from, bold)
        sheet.write(1, 3, 'FECHA HASTA:', bold)
        sheet.write(1, 4, date_to, bold)
        sheet.write(2, 0, 'ESTADO:', bold)
        sheet.write(2, 1, state, bold)
        sheet.write(2, 3, 'EMPRESA', bold)
        sheet.write(2, 4, partner.name, bold)
        sheet.write(3, 0, 'HORAS ENTERAS?', bold)
        sheet.write(3, 1, integer_hours, bold)
        sheet.write(4, 0, 'DESCRIPCION', green)
        sheet.write(4, 1, 'EMPRESA', green)
        sheet.write(4, 2, 'HORAS PRESUPUESTADAS', green)
        sheet.write(4, 3, 'HORAS UTILIZADAS', green)
        sheet.write(4, 4, 'HORAS DISPONIBLES', green)
        sheet.write(4, 5, 'FECHA DE APROBACION', green)
        row = 5
        for o in obj:
            column = 0
            sheet.write(row, column, o.name, bold)
            column += 1
            sheet.write(row, column, o.partner_id.name)
            column += 1
            sheet.write(row, column, o.hours_from_budget / 24, format3)
            column += 1
            sheet.write(row, column, o.hours_used / 24, format3)
            column += 1
            sheet.write(row, column, o.available_hours / 24, format3)
            column += 1
            sheet.write(row, column, o.approval_date, format2)
            column += 1
            row += 2
            # if len(o.analytic_line_ids) > 0:
            #     sheet.write(row, 3, "Detalle de horas", bold)
            #     sheet.merge_range(row, 0, row, 5, "Detalle de horas", bold)
            #     row += 1
            #     for lines in o.analytic_line_ids:
            #         column = 0
            #         sheet.write(row, column, lines.date, format2)
            #         column += 1
            #         sheet.write(row, column, lines.employee_id.name)
            #         column += 1
            #         sheet.write(row, column, lines.name)
            #         column += 1
            #         sheet.write(row, column, lines.time_start / 24, format3)
            #         column += 1
            #         sheet.write(row, column, lines.time_stop / 24, format3)
            #         column += 1
            #         sheet.write(row, column, lines.unit_amount / 24, format3)
            #         row += 1
            #     row += 1

