# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class UserInheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate_property',
        'salesman_id',
        domain=[('state', 'not in', ['sold', 'canceled'])])
