from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DoctorSchedule(models.Model):
    """
    Model representing a doctor's work schedule. It defines the start and end times for each working day,
    as well as the status (available or booked) of the schedule. It includes validation to ensure that schedules
    do not overlap and that start and end times are valid.
    """
    _name = 'hospital_management.doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one(
        'hospital_management.doctor',
        string='Doctor',
        required=True
    )

    start_datetime = fields.Datetime(
        string='Start work day',
        required=True
    )

    stop_datetime = fields.Datetime(
        string='End work day',
        required=True
    )

    color = fields.Integer(
        string='Color',
        compute='_compute_color'
    )

    state = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked')
    ], default='available')

    def action_book_visit(self):
        """
        Action to open the window for booking a visit for the selected time slot.
        Pre-fills the doctor and time information in the booking form.
        """
        return {
            'name': _('Book Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hospital_management.doctor.visit',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.doctor_id.id,
                'default_start_datetime': self.start_datetime,
                'default_stop_datetime': self.stop_datetime,
                'from_book_visit': True,
            }
        }

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_same_day(self):
        """
        Constraint to ensure that the start and end times of the schedule are on the same day.
        Raises a ValidationError if they are not.
        """
        for record in self:
            if record.start_datetime.date() != record.stop_datetime.date():
                raise ValidationError('Start and end times must be on the same day.')

    @api.depends('state')
    def _compute_color(self):
        """
        Computes the color field based on the state of the schedule.
        Booked slots get a dim color, while available slots get a bright color.
        """
        for record in self:
            if record.state == 'booked':
                record.color = 1  # Dim color for booked slots
            else:
                record.color = 10  # Bright color for available slots

    @api.constrains('doctor_id', 'start_datetime', 'stop_datetime')
    def _check_time_overlap(self):
        """
        Constraint to prevent overlapping schedules for the same doctor.
        Raises a ValidationError if there is an overlapping schedule for the doctor.
        """
        for record in self:
            overlapping_schedule = self.env['hospital_management.doctor.schedule'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('id', '!=', record.id),  # Exclude the current record
                ('start_datetime', '<', record.stop_datetime),
                ('stop_datetime', '>', record.start_datetime),
            ])
            if overlapping_schedule:
                raise ValidationError("This schedule overlaps with another appointment for the same doctor.")

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_time_validity(self):
        """
        Constraint to ensure that the end time is after the start time.
        Raises a ValidationError if the end time is earlier or equal to the start time.
        """
        for record in self:
            if record.start_datetime >= record.stop_datetime:
                raise ValidationError("End time must be after start time.")

    @api.depends('doctor_id')
    def _compute_display_name(self):
        """
        Computes the display name for the schedule. If the doctor and start time are set,
        it uses the doctor's name for the display. Otherwise, it defaults to 'Unknown Visit'.
        """
        for record in self:
            if record.doctor_id and record.start_datetime:
                record.display_name = f"{record.doctor_id.name}"
            else:
                record.display_name = "Unknown Visit"

    def unlink(self):
        """
        Overrides the unlink method to prevent deletion of a booked schedule slot.
        Raises a ValidationError if the slot is booked.
        """
        for record in self:
            if record.state == 'booked':
                raise ValidationError(_('You cannot delete a booked slot.'))
        return super(DoctorSchedule, self).unlink()
