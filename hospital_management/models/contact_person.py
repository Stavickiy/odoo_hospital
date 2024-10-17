from odoo import models, fields


class ContactPerson(models.Model):
    """
    Model representing a contact person associated with a patient or other individuals
    in the hospital management system. This model inherits from the 'hospital_management.person'
    model to reuse basic person-related fields and functionality.
    """
    _name = 'hospital_management.contact.person'
    _inherit = 'hospital_management.person'
    _description = 'Contact Person'
