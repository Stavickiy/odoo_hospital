from datetime import datetime, timedelta
from odoo import models, fields, api
import pytz


class DoctorScheduleWizard(models.TransientModel):
    """
    Wizard for generating a doctor's schedule.
    This wizard allows users to set working hours for a doctor
    for the upcoming week, distinguishing between even and odd weeks.
    """

    _name = 'hospital_management.doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    even_week_start_time = fields.Float(string='Start time for even weeks', required=True, default=8.0)
    even_week_end_time = fields.Float(string='End time for even weeks', required=True, default=13.0)
    odd_week_start_time = fields.Float(string='Start time for odd weeks', required=True, default=13.0)
    odd_week_end_time = fields.Float(string='End time for odd weeks', required=True, default=18.0)

    def action_generate_schedule(self):
        """
        Generate the doctor's schedule for the next week based on set working hours.
        This method calculates the start and end times for the doctor's working hours,
        creates time slots for each working day, and stores them in the corresponding model.
        """
        # Determine the start of next week
        today = fields.Datetime.today()
        next_week_start = today + timedelta(days=(7 - today.weekday()))
        next_week_number = next_week_start.isocalendar()[1]

        # Check if the next week is even or odd
        is_even_week = next_week_number % 2 == 0

        # Set working hours based on the week type
        start_time = self.even_week_start_time if is_even_week else self.odd_week_start_time
        end_time = self.even_week_end_time if is_even_week else self.odd_week_end_time

        # Convert float time to hours and minutes
        start_hour = int(start_time)
        end_hour = int(end_time)

        # Get the user's timezone from Odoo settings
        local_tz = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.utc

        # Create schedule for each working day (Monday to Friday)
        for day in range(5):
            current_day = next_week_start + timedelta(days=day)

            # Create datetime objects for the start and end of working hours
            start_slot = local_tz.localize(current_day.replace(hour=start_hour, minute=0, second=0))
            end_slot = local_tz.localize(current_day.replace(hour=end_hour, minute=0, second=0))

            # Convert to UTC and obtain naive datetime objects
            start_slot_utc = start_slot.astimezone(pytz.utc).replace(tzinfo=None)
            end_slot_utc = end_slot.astimezone(pytz.utc).replace(tzinfo=None)

            # Create hourly slots for the schedule
            while start_slot_utc < end_slot_utc:
                stop_slot = start_slot_utc + timedelta(hours=1)
                self.env['hospital_management.doctor.schedule'].create({
                    'doctor_id': self.doctor_id.id,
                    'start_datetime': start_slot_utc,
                    'stop_datetime': stop_slot.replace(tzinfo=None),  # Ensure stop_slot is also naive
                })
                start_slot_utc = stop_slot  # Move to the next time slot
