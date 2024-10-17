from odoo import models, fields, api


class MedicalTest(models.Model):
    """
    Model for managing medical tests conducted for patients.
    This model stores information about medical tests, including the
    patient, type of test, doctor who ordered it, sample type, conclusions,
    and the date the test was ordered.
    """

    _name = 'hospital_management.medical_test'
    _description = 'Analysis conducted for patients'

    patient_id = fields.Many2one('hospital_management.patient', string='Patient', required=True)
    medical_test_type_id = fields.Many2one('hospital_management.medical_test_type', string='Medical Test Type',
                                           required=True)
    doctor_id = fields.Many2one('hospital_management.doctor', string='Ordered by Doctor', required=True)
    sample_id = fields.Many2one('hospital_management.sample_test_type', string='Sample')
    conclusions = fields.Text(string='Conclusions')
    date_ordered = fields.Date(string='Date Ordered', default=fields.Date.today)

    @api.depends('patient_id', 'medical_test_type_id', 'date_ordered')
    def _compute_display_name(self):
        """
        Compute the display name for the medical test record.
        Sets the display name for the medical test record based on the
        date ordered, patient's name, and the type of medical test.
        """
        for record in self:
            record.display_name = f"{record.date_ordered} - " \
                                  f"{record.patient_id.name} - " \
                                  f"{record.medical_test_type_id.name}"
