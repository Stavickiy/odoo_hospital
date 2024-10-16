from odoo import models, fields

class SampleTestType(models.Model):
    _name = 'hospital_management.sample_test_type'
    _description = 'Sample Test Type'

    name = fields.Char(string='Sample Test Type', required=True)
    description = fields.Text(string='Description')
