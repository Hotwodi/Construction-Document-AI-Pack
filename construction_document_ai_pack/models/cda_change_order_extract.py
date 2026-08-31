# -*- coding: utf-8 -*-
from odoo import fields, models


class CdaChangeOrderExtract(models.Model):
    _name = 'cda.change.order.extract'
    _description = 'Change Order Extract'
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
    co_number = fields.Char(string='Change Order Number', tracking=True)
    description = fields.Text(string='Description')
    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    impact_schedule_days = fields.Integer(
        string='Schedule Impact (Days)',
        help='Number of days the change order impacts the project schedule.',
    )
    ai_approval_recommendation = fields.Selection(
        selection=[
            ('approve', 'Approve'),
            ('review', 'Needs Review'),
            ('reject', 'Reject'),
        ],
        string='AI Approval Recommendation',
    )
    linked_project = fields.Char(
        string='Linked Project',
        help='Project identifier or name the change order is tied to.',
    )
    active = fields.Boolean(default=True)
