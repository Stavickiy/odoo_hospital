# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import date


class Patient(models.Model):
    _name = 'hospital_management.patient'
    _inherit = 'hospital_management.person'
    _description = 'Patient'

    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    passport_data = fields.Char(string='Passport Data')
    contact_person_id = fields.Many2one('hospital_management.contact.person', string='Contact Person')
    personal_doctor_id = fields.Many2one('hospital_management.doctor', string='Personal Doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = date.today()
                patient.age = today.year - patient.birth_date.year - (
                            (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
            else:
                patient.age = 0

    def __str__(self):
        return self.name

    def write(self, vals):
        old_doctor = self.personal_doctor_id
        result = super(Patient, self).write(vals)

        if 'personal_doctor_id' in vals:
            new_doctor = self.personal_doctor_id
            if old_doctor != new_doctor:
                current_history = self.env['hospital_management.personal_doctor.history'].search([
                    ('patient_id', '=', self.id),
                    ('doctor_id', '=', old_doctor.id),
                    ('end_date', '=', False)  # Проверяем, что запись активна
                ], limit=1)

                if current_history:
                    current_history.sudo().end_date = fields.Datetime.now()

                self.env['hospital_management.personal_doctor.history'].sudo().create({
                    'patient_id': self.id,
                    'doctor_id': new_doctor.id,
                })

        return result
