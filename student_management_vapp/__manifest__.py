{
    'name': 'Student Management',
    'version': '1.0',
    'summary': 'Comprehensive Student Management System for Schools',
    'description': """
Manage student profiles,
fee calculations,
and payments seamlessly.
""",
    'author': 'Digimonk Technologies',
    'website': 'https://www.digimonk.in',
    'category': 'Education',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/student_views.xml',
        'views/payment_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/student_management_vapp/static/description/icon.png',
}