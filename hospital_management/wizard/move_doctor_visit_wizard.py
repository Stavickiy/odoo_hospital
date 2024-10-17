from odoo import models, fields, api, _


class MoveDoctorVisitWizard(models.TransientModel):
    """Wizard for moving a doctor's visit to a new doctor and updating schedules."""

    _name = 'hospital_management.move_doctor_visit_wizard'
    _description = 'Move doctor visit'

    doctor_visit_id = fields.Many2one(
        'hospital_management.doctor.visit',
        relation='doctor_visit_move_doctor_visit_rel',
        string='Doctor Visit',
        required=True
    )

    new_doctor_id = fields.Many2one(
        'hospital_management.doctor',
        string='New Doctor',
        required=True
    )

    available_slot_id = fields.Many2one(
        'hospital_management.doctor.schedule',
        string='Available Slot',
        domain="[('doctor_id', '=', new_doctor_id), ('state', '=', 'available')]",
        required=True
    )

    def move_doctor_visit(self):
        """Move the doctor visit to a new doctor and update the schedules."""
        self.ensure_one()  # Ensure the wizard is called for a single record
        visit = self.doctor_visit_id

        # Find and mark the old schedule as available
        old_schedule = self.env['hospital_management.doctor.schedule'].search([
            ('doctor_id', '=', visit.doctor_id.id),
            ('start_datetime', '=', visit.start_datetime),
            ('stop_datetime', '=', visit.stop_datetime),
            ('state', '=', 'booked')
        ])
        if old_schedule:
            old_schedule.state = 'available'

        # Update the visit details with the new doctor and time slot
        visit.write({
            'doctor_id': self.new_doctor_id.id,
            'start_datetime': self.available_slot_id.start_datetime or visit.start_datetime,
            'stop_datetime': self.available_slot_id.stop_datetime or visit.stop_datetime,
        })

        # Mark the new schedule as booked
        new_schedule = self.env['hospital_management.doctor.schedule'].search([
            ('doctor_id', '=', self.new_doctor_id.id),
            ('start_datetime', '=', self.available_slot_id.start_datetime),
            ('stop_datetime', '=', self.available_slot_id.stop_datetime),
            ('state', '=', 'available')
        ])
        if new_schedule:
            new_schedule.state = 'booked'

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',  # Reload the view to reflect changes
        }
