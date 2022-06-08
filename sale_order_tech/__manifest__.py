{
    'name': 'Sale Order Tech',
    'version': '12.0.1.0.0',
    'summary': 'Agregar monto margen y % de margen en Pedidos de Venta',
    'description': 'Agregar monto margen y % de margen en Pedidos de Venta',
    'category': 'Sales',
    'author': 'Laura Gauto',
    'company': 'Technoma',
    'maintainer': 'Technoma',
    'depends': [
        'base',
        'sale_management',
        'factura'
    ],
    'data': [
        'views/sale_view.xml',
        'views/purchase_order_view_inh.xml',
    ],
    'qweb': [],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
