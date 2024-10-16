# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital manegment',
    'description': 'Hospital manegment system',
    'category': 'Services',
    'depends': ['base', 'calendar', 'web'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_management_patient_view.xml',
        'views/hospital_management_doctor_view.xml',
        'views/hospital_management_disease_directory_view.xml',
        'views/hospital_management_disease_type_view.xml',
        'views/hospital_management_contact_person_view.xml',
        'wizard/move_doctor_visit_wizard.xml',
        'views/hospital_doсtor_visit_view.xml',
        'views/hospital_management_personal_doctot_history.xml',
        'views/hospital_management_diagnosis_view.xml',
        'views/hospital_medical_test_view.xml',
        'views/hospital_medical_test_type_view.xml',
        'views/hospital_sample_test_type.xml',
        'wizard/hospital_doctor_schedule_wizard.xml',
        'views/hospital_doctor_schedule.xml',
        'wizard/hospital_assign_doctor_wizard.xml',
        'wizard/desease_report_wizard.xml',
        'views/hospital_management_menus.xml',
    ],

}
