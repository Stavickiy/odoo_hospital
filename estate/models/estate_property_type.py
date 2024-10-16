from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate model"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate_property', 'property_type_id')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The name must be unique!')
    ]


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
