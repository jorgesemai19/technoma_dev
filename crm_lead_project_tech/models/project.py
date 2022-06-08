from odoo import api, fields, models, _

class Project(models.Model):
    _inherit = 'project.project'

    lead_id = fields.Many2one('crm.lead',string='Oportunidad')

class Task(models.Model):
    _inherit = 'project.task'
    lead_id = fields.Many2one(related='project_id.lead_id', readonly=True)
