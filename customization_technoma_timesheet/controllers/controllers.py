# -*- coding: utf-8 -*-
# from odoo import http


# class CustomizationTechnomaTimesheet(http.Controller):
#     @http.route('/customization_technoma_timesheet/customization_technoma_timesheet', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customization_technoma_timesheet/customization_technoma_timesheet/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customization_technoma_timesheet.listing', {
#             'root': '/customization_technoma_timesheet/customization_technoma_timesheet',
#             'objects': http.request.env['customization_technoma_timesheet.customization_technoma_timesheet'].search([]),
#         })

#     @http.route('/customization_technoma_timesheet/customization_technoma_timesheet/objects/<model("customization_technoma_timesheet.customization_technoma_timesheet"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customization_technoma_timesheet.object', {
#             'object': obj
#         })
