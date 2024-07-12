# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EStateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area or 0 + record.garden_area or 0

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.expected_price
            for offer in record.offer_ids:
                if offer.price > record.best_price:
                    record.best_price = offer.price

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    def on_status_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError('You cannot cancel a sold property')

    def on_status_sold(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError('You cannot sell a canceled property')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=30))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')],
        default='new', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True)
    seller_id = fields.Many2one('res.users', string='Seller', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id', string='Offers')
    best_price = fields.Float(compute='_compute_best_price')


class EStatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The name of the property type must be unique'),
    ]

    name = fields.Char(required=True)


class EStatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The name of the property type must be unique'),
    ]

    name = fields.Char(required=True)


class EStatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    def on_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

    def on_cancel(self):
        for record in self:
            record.status = 'refused'

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date or fields.Date.today() + timedelta(days=record.validity)

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0.9 * record.property_id.expected_price:
                raise UserError('The price is too low')

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The price must be positive'),
    ]

    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline')
