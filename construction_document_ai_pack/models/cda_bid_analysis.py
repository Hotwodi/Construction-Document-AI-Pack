# -*- coding: utf-8 -*-
from odoo import fields, models


class CdaBidAnalysis(models.Model):
    _name = 'cda.bid.analysis'
    _description = 'Bid Analysis'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default='/',
    )
    job_id = fields.Many2one(
        comodel_name='cda.extraction.job',
        string='Extraction Job',
        required=True,
        ondelete='cascade',
        index=True,
    )
    project_name = fields.Char(string='Project Name', tracking=True)
    bid_amount = fields.Monetary(
        string='Bid Amount',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    bid_breakdown = fields.Html(string='Bid Breakdown')
    ai_completeness_score = fields.Float(
        string='AI Completeness Score',
        digits=(6, 4),
        help='How complete the bid appears (0.0 to 1.0).',
    )
    missing_items = fields.Text(
        string='Missing Items',
        help='Items the AI detected as missing from the bid.',
    )
    risk_flags = fields.Text(
        string='Risk Flags',
        help='Potential risks identified by the AI.',
    )
    recommended_action = fields.Text(
        string='Recommended Action',
        help='AI-suggested next step (e.g. request clarification, accept, reject).',
    )
    active = fields.Boolean(default=True)
