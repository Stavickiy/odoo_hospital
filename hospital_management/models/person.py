from odoo import models, fields


class Person(models.AbstractModel):
    """
    Abstract model representing a person in the hospital management system.
    This model serves as a base class for all entities that have
    personal details such as name, phone, email, photo, and gender.
    It is intended to be inherited by other models that require these fields.
    """

    _name = 'hospital_management.person'
    _description = 'Abstract Person'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')