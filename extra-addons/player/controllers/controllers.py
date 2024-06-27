# -*- coding: utf-8 -*-
# from odoo import http


# class Player(http.Controller):
#     @http.route('/player/player', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/player/player/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('player.listing', {
#             'root': '/player/player',
#             'objects': http.request.env['player.player'].search([]),
#         })

#     @http.route('/player/player/objects/<model("player.player"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('player.object', {
#             'object': obj
#         })

