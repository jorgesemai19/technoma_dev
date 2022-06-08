{
    "name": "Licitaciones ",
    "version": "1.0",
    "author": 'Laura Gauto',
    "description": """
    Modulo de Proyectos customizado para la gestion de Licitaciones
    """,
    "depends": ['base', 'project'],
    "data": [
        'security/ir.model.access.csv',
        'wizard/motivo_perdida_licitacion_views.xml',
        'views/motivo_perdida_menu_views.xml',
        'views/project_views.xml',
        'views/estados_licitacion.xml',
        'views/tipo_procedimiento_views.xml',
        'views/modalidad_procedimiento_views.xml',
        'views/licitaciones_task_report.xml'
    ],
    "application": True,
    'category': 'Uncategorized',
    "installable": True,
}
