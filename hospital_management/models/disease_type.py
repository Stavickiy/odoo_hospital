from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DiseaseType(models.Model):
    _name = 'hospital_management.disease.type'
    _description = 'Disease Type'
    _parent_store = True
    _parent_name = 'parent_id'

    name = fields.Char(string='Disease Type', required=True)
    parent_id = fields.Many2one('hospital_management.disease.type', string='Parent Type', index=True,
                                ondelete='cascade')
    child_ids = fields.One2many('hospital_management.disease.type', 'parent_id', string='Child Types')
    parent_path = fields.Char(index=True, unaccent=False)
    disease_ids = fields.One2many('hospital_management.disease.directory', 'type_id')
    exist_relation_disease = fields.Boolean(compute='_compute_exist_relation_disease')

    @api.depends('disease_ids')
    def _compute_exist_relation_disease(self):
        for record in self:
            record.exist_relation_disease = bool(record.disease_ids)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError("You cannot assign a parent that would cause a recursive loop.")

    def action_show_related_diseases(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Diseases',
            'view_mode': 'tree,form',
            'res_model': 'hospital_management.disease.directory',
            'domain': [('type_id', '=', self.id)],
            'context': dict(self.env.context),
            'views': [(self.env.ref('hospital_management.view_specific_disease_directory_tree').id, 'tree')],
        }
