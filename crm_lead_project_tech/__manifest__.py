# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'CRM lead-project',
    'version': '12.0.1.0.0',
    'category': 'Customer Relationship Management',
    'license': 'LGPL-3',
    'summary': 'Modulo que integra los modulos de proyecto y Crm a traves de la accion Generar Proyecto en la '
               'vista de formulario de oportunidades',
    'author': "Laura Gauto",
    'depends': ['crm', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/project_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
