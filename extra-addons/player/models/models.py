# -*- coding: utf-8 -*-

from odoo import models, fields

class Player(models.Model):
    _name = 'player'
    _description = 'player model'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    country = fields.Char(string="Country")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')], string="Gender", default="male")
    day_of_birth = fields.Datetime(string="Day of Birth")
    position = fields.Char(string="Position")
    height = fields.Float(string="Height")
    weight = fields.Float(string="Weight")
    wife = fields.One2many('wife', 'player_id', string="Wife")

class PlayerWife(models.Model):
    _name = 'wife'
    _description = 'player wife model'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    country = fields.Char(string="Country")
    day_of_birth = fields.Datetime(string="Day of Birth")
    player_id = fields.Many2one('player', string="Player")

class Team(models.Model):
    _name = 'team'
    _description = 'team model'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    country = fields.Char(string="Country")
    stadium = fields.Char(string="Stadium")
    founded = fields.Date(string="Founded")
    coach = fields.Char(string="Coach")
    captain = fields.Char(string="Captain")
    players = fields.Many2many('player', string="Players")
