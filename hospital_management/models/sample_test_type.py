from odoo import models, fields


class SampleTestType(models.Model):
    """
    Model representing a type of sample test.
    This model defines various types of sample tests that can be conducted
    for patients, along with a description for each type.
    """

    _name = 'hospital_management.sample_test_type'
    _description = 'Sample Test Type'

    name = fields.Char(string='Sample Test Type', required=True)
    description = fields.Text(string='Description')