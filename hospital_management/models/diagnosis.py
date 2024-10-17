from odoo import models, fields, api
from datetime import date


class Diagnosis(models.Model):
    _name = 'hospital_management.diagnosis'
    _description = 'Diagnosis in hospital management'

    disease_id = fields.Many2one('hospital_management.disease.directory', string='Disease', required=True, )
    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital_management.patient', string='Patient', required=True)
    medical_test_ids = fields.Many2many('hospital_management.medical_test', relation='diagnosis_medical_test_rel' ,string='Medical Tests')
    treatment = fields.Text(string='Prescribed treatment')
    date_diagnosis = fields.Date(string='Date of Diagnosis', default=date.today(), required=True)
    mentor_comment = fields.Text(string='Mentor comment')
    mentor_comment_needed = fields.Boolean(string='Mentor comment needed',
                                           compute='_compute_mentor_comment_needed',
                                           store=True,
                                           readonly=True)

    @api.depends('patient_id')
    def _compute_display_name(self):
        for record in self:
            if record.disease_id:
                record.display_name = f"{record.disease_id.name}"
            else:
                record.display_name = "Unknown disease"

    @api.depends('doctor_id', 'mentor_comment')
    def _compute_mentor_comment_needed(self):
        for record in self:
            record.mentor_comment_needed = record.doctor_id.is_intern and not record.mentor_comment
