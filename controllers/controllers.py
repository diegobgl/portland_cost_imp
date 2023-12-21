# -*- coding: utf-8 -*-
# from odoo import http


# class PortlandCostImp(http.Controller):
#     @http.route('/portland_cost_imp/portland_cost_imp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/portland_cost_imp/portland_cost_imp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('portland_cost_imp.listing', {
#             'root': '/portland_cost_imp/portland_cost_imp',
#             'objects': http.request.env['portland_cost_imp.portland_cost_imp'].search([]),
#         })

#     @http.route('/portland_cost_imp/portland_cost_imp/objects/<model("portland_cost_imp.portland_cost_imp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portland_cost_imp.object', {
#             'object': obj
#         })
