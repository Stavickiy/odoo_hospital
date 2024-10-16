from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _name = 'hospital_management.doctor'
    _inherit = 'hospital_management.person'
    _description = 'Doctor'

    specialization = fields.Char(string='Specialization', required=True)
    is_intern = fields.Boolean(string='Is Intern', default=False)
    mentor_doctor_id = fields.Many2one('hospital_management.doctor',
                                       string='Mentor Doctor',
                                       domain="[('is_intern', '=', False), ('id', '!=', id)]"
                                       )

    @api.constrains('is_intern', 'mentor_doctor_id')
    def _check_mentor_doctor(self):
        for record in self:
            if record.is_intern and not record.mentor_doctor_id:
                raise ValidationError("An intern must have a mentor doctor.")
