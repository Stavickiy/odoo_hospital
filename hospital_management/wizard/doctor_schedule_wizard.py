from datetime import datetime, timedelta
from odoo import models, fields, api
import pytz

class DoctorScheduleWizard(models.TransientModel):
    _name = 'hospital_management.doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    even_week_start_time = fields.Float(string='Start time for even weeks', required=True, default=8.0)  # Время в часах
    even_week_end_time = fields.Float(string='End time for even weeks', required=True, default=13.0)
    odd_week_start_time = fields.Float(string='Start time for odd weeks', required=True, default=13.0)
    odd_week_end_time = fields.Float(string='End time for odd weeks', required=True, default=18.0)

    def action_generate_schedule(self):
        # Определение следующей недели
        today = fields.Datetime.today()
        next_week_start = today + timedelta(days=(7 - today.weekday()))
        next_week_number = next_week_start.isocalendar()[1]

        # Четная или нечетная неделя
        is_even_week = next_week_number % 2 == 0

        # Установка времени на основе четности недели
        start_time = self.even_week_start_time if is_even_week else self.odd_week_start_time
        end_time = self.even_week_end_time if is_even_week else self.odd_week_end_time

        # Преобразование времени float в часы и минуты
        start_hour = int(start_time)
        end_hour = int(end_time)

        # Получение текущего часового пояса из настроек Odoo
        local_tz = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.utc

        for day in range(5):  # Рабочие дни с понедельника по пятницу
            current_day = next_week_start + timedelta(days=day)

            # Создание datetime для начала и конца рабочего времени
            start_slot = local_tz.localize(current_day.replace(hour=start_hour, minute=0, second=0))
            end_slot = local_tz.localize(current_day.replace(hour=end_hour, minute=0, second=0))

            # Преобразование в UTC и получение наивного значения
            start_slot_utc = start_slot.astimezone(pytz.utc).replace(tzinfo=None)
            end_slot_utc = end_slot.astimezone(pytz.utc).replace(tzinfo=None)

            # Создание часовых слотов
            while start_slot_utc < end_slot_utc:
                stop_slot = start_slot_utc + timedelta(hours=1)
                self.env['hospital_management.doctor.schedule'].create({
                    'doctor_id': self.doctor_id.id,
                    'start_datetime': start_slot_utc,
                    'stop_datetime': stop_slot.replace(tzinfo=None),  # Убедитесь, что stop_slot тоже наивное
                })
                start_slot_utc = stop_slot