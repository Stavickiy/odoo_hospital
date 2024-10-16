from odoo import models, fields

class PersonalDoctorHistory(models.Model):
    _name = 'hospital_management.personal_doctor.history'
    _description = 'Personal Doctor History'

    patient_id = fields.Many2one('hospital_management.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date')
