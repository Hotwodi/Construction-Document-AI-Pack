# -*- coding: utf-8 -*-
import base64
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CdaExtractionJob(models.Model):
    _name = 'cda.extraction.job'
    _description = 'Document Extraction Job'
    _inherit = ['mail.thread']
    _order = 'created_date desc, id desc'

    name = fields.Char(
        string='Job Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    document_type = fields.Selection(
        selection=[
            ('bid', 'Bid'),
            ('change_order', 'Change Order'),
            ('invoice', 'Invoice'),
            ('co_insurance', 'Certificate of Insurance'),
            ('delivery_ticket', 'Delivery Ticket'),
            ('subcontract', 'Subcontract'),
        ],
        string='Document Type',
        required=True,
        tracking=True,
    )
    file_name = fields.Char(string='File Name')
    file_data = fields.Binary(string='Document File', attachment=True)
    state = fields.Selection(
        selection=[
            ('uploaded', 'Uploaded'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('reviewed', 'Reviewed'),
        ],
        string='Status',
        default='uploaded',
        required=True,
        tracking=True,
        copy=False,
    )
    ai_confidence = fields.Float(
        string='AI Confidence',
        digits=(6, 4),
        help='Overall AI confidence score for the extraction (0.0 to 1.0).',
    )
    extracted_fields_count = fields.Integer(
        string='Extracted Fields Count',
        compute='_compute_extracted_fields_count',
        store=True,
    )
    created_by = fields.Many2one(
        comodel_name='res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    created_date = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    extracted_field_ids = fields.One2many(
        comodel_name='cda.extracted.field',
        inverse_name='job_id',
        string='Extracted Fields',
    )
    bid_analysis_id = fields.One2many(
        comodel_name='cda.bid.analysis',
        inverse_name='job_id',
        string='Bid Analysis',
    )
    change_order_extract_id = fields.One2many(
        comodel_name='cda.change.order.extract',
        inverse_name='job_id',
        string='Change Order Extract',
    )
    invoice_extract_id = fields.One2many(
        comodel_name='cda.invoice.extract',
        inverse_name='job_id',
        string='Invoice Extract',
    )
    active = fields.Boolean(default=True)

    @api.depends('extracted_field_ids')
    def _compute_extracted_fields_count(self):
        for job in self:
            job.extracted_fields_count = len(job.extracted_field_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'cda.extraction.job'
                ) or _('New')
        return super().create(vals_list)

    def action_start_processing(self):
        """Mark the job as processing and simulate AI extraction."""
        for job in self:
            if not job.file_data:
                raise UserError(_('Please upload a document file before processing.'))
            job.state = 'processing'
        self._run_ai_extraction()

    def _run_ai_extraction(self):
        """Hook for actual AI extraction logic.

        This placeholder simulates a successful extraction by moving each
        job to the ``completed`` state with a sample confidence score.
        Override this method to integrate a real AI/OCR backend.
        """
        for job in self:
            try:
                # Placeholder: real implementation would call an external
                # AI/OCR service, parse the response, and create
                # cda.extracted.field records.
                job.ai_confidence = 0.85
                job.state = 'completed'
            except Exception as exc:  # noqa: BLE001
                _logger.exception('AI extraction failed for job %s: %s', job.name, exc)
                job.state = 'failed'

    def action_mark_reviewed(self):
        for job in self:
            job.state = 'reviewed'

    def action_reset_to_uploaded(self):
        for job in self:
            job.state = 'uploaded'
