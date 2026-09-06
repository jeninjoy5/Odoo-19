# -*- coding: utf-8 -*-


{
    'name': "Machine Management",
    'version': '1.0',
    'application': True,
    'sequence':-10,
    'summary': 'Manage Machines',
    'depends': ['mail','product'],
    'data': ['security/ir.model.access.csv',

             'data/machine_type_demo.xml',
             'data/sequence_data.xml',

             'views/machine_service_views.xml',
             'views/res_partner_views.xml',
             'views/machine_tags_views.xml',
             'views/machine_transfer_views.xml',
             'views/machine_type_views.xml',
             'views/machine_management_views.xml',
             'views/machine_management_menu.xml'
    ]
}