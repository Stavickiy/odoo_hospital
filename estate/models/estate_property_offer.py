# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "id desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one('res.partner', string='Partners', required=True)
    property_id = fields.Many2one('estate_property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)
    create_date = fields.Date(copy=False, default=fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline_date', inverse='_inverse_validity_days')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The "Price" must be strictly positive.'),
    ]

    @api.model
    def create(self, vals):
        property = self.env['estate_property'].browse(vals["property_id"])
        property.state = "offer received"

        if property.offer_ids:
            max_price = max([offer.price for offer in property.offer_ids])
            if max_price > vals['price']:
                raise UserError(f"The offer price must be higher than {max_price}")
        return super().create(vals)


    @api.depends('validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.validity and (record.create_date + relativedelta(days=record.validity)) != record.date_deadline:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)


    def _inverse_validity_days(self):
        for record in self:
            if record.date_deadline and (record.date_deadline - record.create_date).days != record.validity:
                record.validity = (record.date_deadline - record.create_date).days


    def action_confirm_offer(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("A refused offer cannot be accepted!")
            elif record.property_id.state == 'sold':
                raise UserError("The property has already been sold!")
            else:
                for offer in record.property_id.offer_ids:
                    if record != offer:
                        offer.status = "refused"
                record.status = "accepted"
                record.property_id.state = "offer accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                return True


    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("A accepted offer cannot be refused!")
            elif record.status == "refused":
                raise UserError("The offer has already been refused!")
            else:
                record.status = "refused"
                return True
