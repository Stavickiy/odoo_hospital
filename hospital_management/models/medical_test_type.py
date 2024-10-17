from odoo import models, fields


class MedicalTestType(models.Model):
    """
    Model for managing hierarchical medical test types.
    This model allows for the categorization of medical tests into
    types and subtypes, enabling a structured representation of
    different test categories. Each type can have a parent type,
    forming a hierarchical relationship among medical test types.
    """

    _name = 'hospital_management.medical_test_type'
    _description = 'Hierarchical Medical Test Types'

    name = fields.Char(string='Type Name', required=True)
    parent_id = fields.Many2one('hospital_management.medical_test_type',
                                string='Parent Medical Test Type',
                                ondelete='cascade')
    child_ids = fields.One2many('hospital_management.medical_test_type',
                                'parent_id',
                                string='Subtypes')
    parent_path = fields.Char(index=True, unaccent=False)