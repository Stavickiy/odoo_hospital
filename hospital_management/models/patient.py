from odoo import models, fields, api
from datetime import date


class Patient(models.Model):
    """
    Model representing a patient in the hospital management system.
    This model inherits from the 'hospital_management.person' class
    and includes additional fields and methods specific to patients,
    such as birth date, age, and personal doctor.
    """

    _name = 'hospital_management.patient'
    _inherit = 'hospital_management.person'
    _description = 'Patient'

    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    passport_data = fields.Char(string='Passport Data')
    contact_person_id = fields.Many2one('hospital_management.contact.person', string='Contact Person')
    personal_doctor_id = fields.Many2one('hospital_management.doctor', string='Personal Doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        """Compute the age of the patient based on their birth date."""
        for patient in self:
            if patient.birth_date:
                today = date.today()
                # Calculate age considering if the birthday has occurred this year
                patient.age = today.year - patient.birth_date.year - (
                        (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
            else:
                patient.age = 0  # Default age if no birth date is provided

    def __str__(self):
        """String representation of the patient, returning their name."""
        return self.name

    def write(self, vals):
        """
        Override the write method to manage the history of personal doctors.
        If the personal doctor is changed, the current doctor's record
        will be updated with the end date, and a new history record
        will be created for the new personal doctor.
        """
        old_doctor = self.personal_doctor_id
        result = super(Patient, self).write(vals)

        # Check if the personal doctor has been changed
        if 'personal_doctor_id' in vals:
            new_doctor = self.personal_doctor_id
            if old_doctor != new_doctor:
                current_history = self.env['hospital_management.personal_doctor.history'].search([
                    ('patient_id', '=', self.id),
                    ('doctor_id', '=', old_doctor.id),
                    ('end_date', '=', False)  # Check that the record is active
                ], limit=1)

                if current_history:
                    # Set the end date for the current personal doctor
                    current_history.sudo().end_date = fields.Datetime.now()

                # Create a new record for the new personal doctor
                self.env['hospital_management.personal_doctor.history'].sudo().create({
                    'patient_id': self.id,
                    'doctor_id': new_doctor.id,
                })

        return result
