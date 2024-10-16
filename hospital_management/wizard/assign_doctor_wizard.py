from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssignDoctorWizard(models.TransientModel):
    _name = 'hospital_management.assign_doctor_wizard'
    _description = 'Assign Doctor Wizard'

    doctor_id = fields.Many2one('hospital_management.doctor', string='New Doctor', required=True)
    patient_ids = fields.Many2many('hospital_management.patient', string='Patients', relation='assign_doctor_patient_rel')

    @api.model
    def default_get(self, fields):
        res = super(AssignDoctorWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_assign_doctor(self):
        if not self.patient_ids:
            raise ValidationError(_('Please select patients.'))
        for patient in self.patient_ids:
            patient.write({'personal_doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
