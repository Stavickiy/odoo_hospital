# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, Command


class InheritedEstateProperty(models.Model):
    _inherit = "estate_property"

    def action_sold_property(self):
        res = super(InheritedEstateProperty, self).action_sold_property()
        for property in self:
            values = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                "line_ids": [
                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        'price_unit': property.selling_price * 0.06
                    }),
                    Command.create({
                        "name": 'Administrative fees',
                        "quantity": 1,
                        'price_unit': 100
                    })
                ],
            }
            self.env['account.move'].create(values)
        return res
