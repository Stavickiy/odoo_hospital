from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    """
    Model representing a doctor in the hospital management system.
    This model extends the 'person' model and adds specific fields for doctors,
    including specialization, intern status, and the assignment of mentor doctors for interns.
    """
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
        """
        Constraint method that checks if an intern doctor has an assigned mentor doctor.
        Raises a ValidationError if an intern does not have a mentor.
        """
        for record in self:
            if record.is_intern and not record.mentor_doctor_id:
                raise ValidationError("An intern must have a mentor doctor.")
