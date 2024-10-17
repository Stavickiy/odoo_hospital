from odoo import models, fields


class DiseaseDirectory(models.Model):
    """
    Model representing the directory of diseases in the hospital management system.
    It stores information about different diseases and their types, including
    hierarchical relationships between disease types.
    """
    _name = 'hospital_management.disease.directory'
    _description = 'Disease Directory'

    name = fields.Char(string='Disease Name', required=True)
    type_id = fields.Many2one('hospital_management.disease.type', string='Disease Type', required=True)
    parent_type_id = fields.Many2one(related='type_id.parent_id', string="Parent Type", store=True)
