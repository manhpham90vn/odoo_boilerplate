# -*- coding: utf-8 -*-
from odoo import http
import json


class Player(http.Controller):

    IGNORE_FIELDS = ['image', 'day_of_birth', 'create_date',
                     'write_date', 'create_uid', 'write_uid']

    def _filter_fields(self, model_obj):
        fields_to_read = [field for field in model_obj.fields_get(
        ) if field not in self.IGNORE_FIELDS]
        return model_obj.read(fields=fields_to_read)

    @http.route('/player', auth='public', type='http')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/player/login', auth='public')
    def login(self, **kw):
        return http.request.render("web.login")

    @http.route('/player/all', auth='public')
    def all(self, **kw):
        players = http.request.env['player'].search([])
        players_filtered = self._filter_fields(players)
        return json.dumps(players_filtered)

    @http.route('/player/<int:player_id>', auth='public')
    def get_player(self, player_id):
        players = http.request.env['player'].search([('id', '=', player_id)])
        players_filtered = self._filter_fields(players)
        player = players_filtered[0] if players_filtered else None
        if player:
            return json.dumps(player)
        else:
            return json.dumps({})
