# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate model"
    _order = "id desc"

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer_price")
    garden_orientation = fields.Selection(selection=[
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")
    ])
    state = fields.Selection(selection=[
        ("new", "New"),
        ("offer received", "Offer Received"),
        ("offer accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], default="new", readonly=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The "Expected price" must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The "Selling price" must be strictly positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer_price(self):
        for record in self:
            offers = record.mapped('offer_ids.price')
            if offers:
                record.best_price = max(offers)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange(self):
        if self.garden:
            self.garden_area = 1000
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold_property(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
                return True
            else:
                raise UserError(_("A canceled property cannot be sold!"))

    def action_cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
                return True
            else:
                raise UserError(_("A sold property cannot be canceled!"))

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) == -1:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price!"
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_user(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(f"Property '{record.state}' can't be deleted!")
