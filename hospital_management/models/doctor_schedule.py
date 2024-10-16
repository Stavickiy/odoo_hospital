from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DoctorSchedule(models.Model):
    _name = 'hospital_management.doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one('hospital_management.doctor', string='Doctor', required=True)
    start_datetime = fields.Datetime(string='Start work day', required=True)
    stop_datetime = fields.Datetime(string='End work day', required=True)
    color = fields.Integer(string='Color', compute='_compute_color')
    state = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked')
    ], default='available')

    # Метод для открытия окна бронирования визита
    def action_book_visit(self):
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
        for record in self:
            if record.start_datetime.date() != record.stop_datetime.date():
                raise ValidationError('Start and end times must be on the same day.')

    @api.depends('state')
    def _compute_color(self):
        for record in self:
            if record.state == 'booked':
                record.color = 1  # Тусклый цвет для забронированных слотов
            else:
                record.color = 10  # Яркий цвет для доступных слотов

    @api.constrains('doctor_id', 'start_datetime', 'stop_datetime')
    def _check_time_overlap(self):
        for record in self:
            overlapping_schedule = self.env['hospital_management.doctor.schedule'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('id', '!=', record.id),  # Исключить текущую запись
                ('start_datetime', '<', record.stop_datetime),
                ('stop_datetime', '>', record.start_datetime),
            ])
            if overlapping_schedule:
                raise ValidationError("This schedule overlaps with another appointment for the same doctor.")

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_time_validity(self):
        for record in self:
            if record.start_datetime >= record.stop_datetime:
                raise ValidationError("End time must be after start time.")

    @api.depends('doctor_id')
    def _compute_display_name(self):
        for record in self:
            if record.doctor_id and record.start_datetime:
                record.display_name = f"{record.doctor_id.name}"
            else:
                record.display_name = "Unknown Visit"

    def unlink(self):
        for record in self:
            if record.state == 'booked':
                raise ValidationError(_('You cannot delete a booked slot.'))
        return super(DoctorSchedule, self).unlink()
