from odoo import models, fields


class MedicakTestType(models.Model):
    _name = 'hospital_management.medical_test_type'
    _description = 'Hierarchical Medical Test Types'

    name = fields.Char(string='Type Name', required=True)
    parent_id = fields.Many2one('hospital_management.medical_test_type',
                                string='Parent Medical Test Type',
                                ondelete='cascade')
    child_ids = fields.One2many('hospital_management.medical_test_type', 'parent_id', string='Subtypes')
    parent_path = fields.Char(index=True, unaccent=False)
