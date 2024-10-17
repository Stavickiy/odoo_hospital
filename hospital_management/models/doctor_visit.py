from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class DoctorVisit(models.Model):
    """Model to manage doctor visits in the hospital management system."""

    _name = 'hospital_management.doctor.visit'
    _description = 'Doctor Visit'
    _order = 'start_datetime'

    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital_management.patient', string='Patient', required=True)
    diagnosis_id = fields.Many2one('hospital_management.diagnosis', string='Diagnosis')
    start_datetime = fields.Datetime(string='Visit start Date and Time', required=True)
    stop_datetime = fields.Datetime(string='Visit stop Date and Time', required=True)
    medical_test_ids = fields.Many2many('hospital_management.medical_test', string='Medical Tests',
                                        relation='doctor_visit_medical_test_rel')
    recommendations = fields.Text(string='Recommendations')
    state = fields.Selection(selection=[
        ('planed', 'Planed'),
        ('completed', 'Completed'),
    ], default='planed')
    color = fields.Integer(string='Color', compute='_compute_color')

    @api.depends('doctor_id')
    def _compute_color(self):
        """Compute the color for the visit based on the doctor's ID.

        This method sets the color attribute of the visit record based on
        the doctor's ID, ensuring a unique color representation for each doctor.
        """
        for record in self:
            record.color = record.doctor_id.id % 10

    @api.model
    def create(self, vals):
        """
        Create a new doctor visit record and update the schedule status to 'booked'.
        """
        visit = super(DoctorVisit, self).create(vals)
        # Update the schedule status to 'booked' for the relevant time slot
        schedule = self.env['hospital_management.doctor.schedule'].search([
            ('doctor_id', '=', visit.doctor_id.id),
            ('start_datetime', '=', visit.start_datetime),
            ('stop_datetime', '=', visit.stop_datetime),
            ('state', '=', 'available')
        ])
        if schedule:
            schedule.state = 'booked'
        return visit

    @api.depends('patient_id')
    def _compute_display_name(self):
        """
        Compute the display name for the visit record.

        Sets the display name of the visit record based on the associated
        patient's name if available. Defaults to 'Unknown Visit' if not.
        """
        for record in self:
            if record.patient_id and record.start_datetime:
                record.display_name = record.patient_id.name
            else:
                record.display_name = "Unknown Visit"

    @api.constrains('doctor_id', 'start_datetime', 'stop_datetime')
    def _check_double_booking(self):
        """
        Ensure no overlapping bookings for the same doctor.
        """
        for visit in self:
            overlapping_visit = self.env['hospital_management.doctor.visit'].search([
                ('doctor_id', '=', visit.doctor_id.id),
                ('start_datetime', '<', visit.stop_datetime),
                ('stop_datetime', '>', visit.start_datetime),
                ('id', '!=', visit.id)  # Exclude the current visit record
            ])
            if overlapping_visit:
                raise ValidationError("The doctor is already booked for this time slot.")

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_doctor_schedule(self):
        """
        Ensure that the visit is within the doctor's working hours.
        """
        for visit in self:
            schedules = self.env['hospital_management.doctor.schedule'].search([
                ('doctor_id', '=', visit.doctor_id.id),
                ('start_datetime', '<=', visit.start_datetime),
                ('stop_datetime', '>=', visit.stop_datetime)
            ])
            if not schedules:
                raise ValidationError(
                    _("The visit time does not fit into the doctor's working schedule. Check out the doctor's schedule!"))

    def action_visit_completed(self):
        """
        Mark the visit as completed.
        """
        for record in self:
            if record.state == "planed":
                record.state = "completed"
                return True
            else:
                raise UserError(_("Visit is already completed!"))

    @api.constrains('patient_id', 'diagnosis_id')
    def _check_patient_diagnosis(self):
        """
        Ensure that diagnosis patient is the same as the visit patient.
        """
        for visit in self:
            if visit.patient_id and visit.diagnosis_id.patient_id and \
                    visit.patient_id != visit.diagnosis_id.patient_id:
                raise ValidationError(_("Visit patient and diagnosis patient must be the same."))

    def write(self, vals):
        """
        Prevent modification of doctor or time if the visit is completed.
        """
        for record in self:
            if record.state == 'completed':
                if any(key in vals for key in ['start_datetime', 'stop_datetime', 'doctor_id']):
                    raise ValidationError(_("You cannot modify the date, time, or doctor for a completed visit."))
        return super(DoctorVisit, self).write(vals)

    def unlink(self):
        """
        Prevent deletion of visits with a diagnosis.
        """
        for record in self:
            if record.diagnosis_id:
                raise ValidationError(_("You cannot delete a visit that has a diagnosis."))

            # Restore the schedule state to 'available' if it was booked
            old_schedule = self.env['hospital_management.doctor.schedule'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('start_datetime', '=', record.start_datetime),
                ('stop_datetime', '=', record.stop_datetime),
                ('state', '=', 'booked')
            ])
            if old_schedule:
                old_schedule.state = 'available'
        return super(DoctorVisit, self).unlink()

    def action_open_move_visit_wizard(self):
        """
        Open the wizard to move the visit to a different time or doctor.
        """
        return {
            'name': _('Move visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital_management.move_doctor_visit_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_doctor_visit_id': self.id,
            }
        }
