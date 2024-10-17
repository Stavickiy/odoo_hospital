from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AssignDoctorWizard(models.TransientModel):
    """
    Wizard for assigning a new doctor to selected patients.
    This wizard allows the user to select multiple patients and
    assign a new doctor to them. It validates the selection before
    making the changes.
    """

    _name = 'hospital_management.assign_doctor_wizard'
    _description = 'Assign Doctor Wizard'

    doctor_id = fields.Many2one('hospital_management.doctor', string='New Doctor', required=True)
    patient_ids = fields.Many2many('hospital_management.patient', string='Patients',
                                   relation='assign_doctor_patient_rel')

    @api.model
    def default_get(self, fields):
        """
        Get default values for the wizard.
        This method populates the patient_ids field with the active
        patient records from the context when the wizard is opened.
        """
        res = super(AssignDoctorWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_assign_doctor(self):
        """
        Assign the selected doctor to the chosen patients.
        This method checks if any patients have been selected. If not,
        it raises a ValidationError. If patients are selected, it updates
        each patient's personal doctor ID with the new doctor's ID and
        closes the wizard.
        """
        if not self.patient_ids:
            raise ValidationError(_('Please select patients.'))
        for patient in self.patient_ids:
            patient.write({'personal_doctor_id': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
