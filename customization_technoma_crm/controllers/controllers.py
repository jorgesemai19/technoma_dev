# -*- coding: utf-8 -*-
# from odoo import http


# class CustomizationTechnomaCrm(http.Controller):
#     @http.route('/customization_technoma_crm/customization_technoma_crm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customization_technoma_crm/customization_technoma_crm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customization_technoma_crm.listing', {
#             'root': '/customization_technoma_crm/customization_technoma_crm',
#             'objects': http.request.env['customization_technoma_crm.customization_technoma_crm'].search([]),
#         })

#     @http.route('/customization_technoma_crm/customization_technoma_crm/objects/<model("customization_technoma_crm.customization_technoma_crm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customization_technoma_crm.object', {
#             'object': obj
#         })
