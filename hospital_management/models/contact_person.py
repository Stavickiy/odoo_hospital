from odoo import models, fields


class ContactPerson(models.Model):
    _name = 'hospital_management.contact.person'
    _inherit = 'hospital_management.person'
    _description = 'Contact Person'
