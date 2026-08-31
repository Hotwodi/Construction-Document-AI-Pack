# -*- coding: utf-8 -*-
from odoo import fields, models


class CdaExtractedField(models.Model):
    _name = 'cda.extracted.field'
    _description = 'Extracted Field'
    _order = 'job_id, id'

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
    field_name = fields.Char(
        string='Field Name',
        required=True,
        help='The label/key of the field as detected by the AI engine.',
    )
    field_value = fields.Text(string='Field Value')
    confidence = fields.Float(
        string='Confidence',
        digits=(6, 4),
        help='Per-field AI confidence score (0.0 to 1.0).',
    )
    verified = fields.Boolean(
        string='Verified',
        default=False,
        help='Set to True once a human reviewer has confirmed the value.',
    )
    corrected_value = fields.Text(
        string='Corrected Value',
        help='The human-corrected value, if the AI value was wrong.',
    )
    field_type = fields.Selection(
        selection=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('date', 'Date'),
            ('currency', 'Currency'),
            ('reference', 'Reference'),
        ],
        string='Field Type',
        default='text',
        required=True,
    )
    active = fields.Boolean(default=True)

    def action_verify(self):
        for rec in self:
            rec.verified = True

    def action_apply_correction(self):
        """Apply the corrected value to the main field_value and mark verified."""
        for rec in self:
            if rec.corrected_value:
                rec.field_value = rec.corrected_value
            rec.verified = True
