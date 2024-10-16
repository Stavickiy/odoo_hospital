from odoo import models, fields, api


class MedicalTest(models.Model):
    _name = 'hospital_management.medical_test'
    _description = 'Analysis conducted for patients'

    patient_id = fields.Many2one('hospital_management.patient', string='Patient', required=True)
    medical_test_type_id = fields.Many2one('hospital_management.medical_test_type', string='Medical Test Type', required=True)
    doctor_id = fields.Many2one('hospital_management.doctor', string='Ordered by Doctor', required=True)
    sample_id = fields.Many2one('hospital_management.sample_test_type', string='Sample')
    conclusions = fields.Text(string='Conclusions')
    date_ordered = fields.Date(string='Date Ordered', default=fields.Date.today)

    @api.depends('patient_id', 'medical_test_type_id', 'date_ordered')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.date_ordered} - {record.patient_id.name} - {record.medical_test_type_id.name}"