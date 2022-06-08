# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BookBankXlsx(models.AbstractModel):
    _name = 'report.left_hours_by_project.custom_partner_report_name'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        domain = [('id', 'in', data['form_data'])]
        obj = self.env['res.partner'].search([('is_company', '=', True)])
        print(len(obj))
        report_name = 'REPORTE PERSONALIZADO DE CONTACTOS'
        # One sheet by partner
        sheet = workbook.add_worksheet(report_name[:31])
        green = workbook.add_format({'bold': True, 'bg_color': 'green', 'align': 'center', 'num_format': 'dd/mm/yy'})
        bold = workbook.add_format({'bold': True})
        cell_format = workbook.add_format()
        cell_format.set_align('left')
        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        format3 = workbook.add_format({'num_format': '[h]:mm'})
        sheet.merge_range(0, 0, 0, 5, report_name, green)
        sheet.set_column(0, 0, 7, cell_format, {'collapsed': 1})
        sheet.set_column(1, 1, 10, cell_format, {'collapsed': 1})
        sheet.set_column(2, 5, 40, cell_format, {'collapsed': 1})
        sheet.write(1, 0, 'Nro', green)
        sheet.write(1, 1, 'Tipo', green)
        sheet.write(1, 2, 'Cuenta / entidad', green)
        sheet.write(1, 3, 'Contactos', green)
        sheet.write(1, 4, 'Email', green)
        sheet.write(1, 5, 'Negocios', green)
        row = 2
        cont = 0
        for o in obj:
            column = 0
            cont += 1
            sheet.write(row, column, cont)
            column += 1
            if len(o.category_id) > 1:
                column += 1
                print(o.name)
                pass
            else:
                sheet.write(row, column, o.category_id.name)
                column += 1
            sheet.write(row, column, o.name)
            column += 1
            column += 1
            sheet.write(row, column, o.email)
            column -= 1
            for contacts in o.child_ids:
                row += 1
                sheet.write(row, column, contacts.name)
                column += 1
                sheet.write(row, column, contacts.email)
                column -= 1
            row += 1