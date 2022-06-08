# -*- coding: utf-8 -*-
from odoo import http

# class LeftHoursByProject(http.Controller):
#     @http.route('/left_hours_by_project/left_hours_by_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/left_hours_by_project/left_hours_by_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('left_hours_by_project.listing', {
#             'root': '/left_hours_by_project/left_hours_by_project',
#             'objects': http.request.env['left_hours_by_project.left_hours_by_project'].search([]),
#         })

#     @http.route('/left_hours_by_project/left_hours_by_project/objects/<model("left_hours_by_project.left_hours_by_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('left_hours_by_project.object', {
#             'object': obj
#         })