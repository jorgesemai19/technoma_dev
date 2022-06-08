# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Modulo de Tipificacion de Proyectos de Ventas ganados en Odoo",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Laura Gauto",
    "license": "AGPL-3",
    "depends": [
        "crm",
        'mail',
        'sale_crm',
    ],
    "data": [
        'security/ir.model.access.csv',
        "views/crm_modelo_tipificacion_proyecto_view.xml",
        "views/crm_lead_view.xml",
        "views/sales_order_view.xml"
    ],
    'installable': True,
    # "pre_init_hook": "create_code_equal_to_id",
    # "post_init_hook": "assign_old_sequences",
}
