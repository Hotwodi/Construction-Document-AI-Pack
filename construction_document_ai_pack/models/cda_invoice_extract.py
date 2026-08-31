# -*- coding: utf-8 -*-
from odoo import fields, models


class CdaInvoiceExtract(models.Model):
    _name = 'cda.invoice.extract'
    _description = 'Invoice Extract'
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
    vendor_name = fields.Char(string='Vendor Name', tracking=True)
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    line_items = fields.Html(string='Line Items')
    subtotal = fields.Monetary(
        string='Subtotal',
        currency_field='currency_id',
    )
    tax = fields.Monetary(
        string='Tax',
        currency_field='currency_id',
    )
    total = fields.Monetary(
        string='Total',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    ai_match_confidence = fields.Float(
        string='AI Match Confidence',
        digits=(6, 4),
        help='Confidence that this invoice matches a purchase order (0.0 to 1.0).',
    )
    matched_po = fields.Char(
        string='Matched PO',
        help='Purchase order number the invoice was matched to, if any.',
    )
    active = fields.Boolean(default=True)
