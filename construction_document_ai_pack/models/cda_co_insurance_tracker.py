# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CdaCoInsuranceTracker(models.Model):
    _name = 'cda.co.insurance.tracker'
    _description = 'Certificate of Insurance Tracker'
    _inherit = ['mail.thread']
    _order = 'expiry_date asc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default='/',
    )
    vendor_name = fields.Char(string='Vendor Name', required=True, tracking=True)
    policy_number = fields.Char(string='Policy Number')
    insurance_type = fields.Selection(
        selection=[
            ('general_liability', 'General Liability'),
            ('workers_comp', 'Workers Compensation'),
            ('auto_liability', 'Auto Liability'),
            ('umbrella', 'Umbrella / Excess'),
            ('professional', 'Professional Liability'),
            ('property', 'Property'),
        ],
        string='Insurance Type',
        default='general_liability',
        required=True,
    )
    coverage_amount = fields.Monetary(
        string='Coverage Amount',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    effective_date = fields.Date(string='Effective Date')
    expiry_date = fields.Date(string='Expiry Date', tracking=True)
    ai_days_until_expiry = fields.Integer(
        string='Days Until Expiry',
        compute='_compute_ai_days_until_expiry',
        store=True,
    )
    state = fields.Selection(
        selection=[
            ('valid', 'Valid'),
            ('expiring_soon', 'Expiring Soon'),
            ('expired', 'Expired'),
        ],
        string='Status',
        default='valid',
        required=True,
        tracking=True,
    )
    alert_sent = fields.Boolean(
        string='Alert Sent',
        default=False,
        help='Whether an expiry alert has been sent for this certificate.',
    )
    active = fields.Boolean(default=True)

    @api.depends('expiry_date')
    def _compute_ai_days_until_expiry(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.expiry_date:
                rec.ai_days_until_expiry = (rec.expiry_date - today).days
            else:
                rec.ai_days_until_expiry = 0

    @api.onchange('expiry_date')
    def _onchange_expiry_date(self):
        """Auto-update the state based on the expiry date."""
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.expiry_date:
                rec.state = 'valid'
                continue
            days = (rec.expiry_date - today).days
            if days < 0:
                rec.state = 'expired'
            elif days <= 30:
                rec.state = 'expiring_soon'
            else:
                rec.state = 'valid'

    def write(self, vals):
        """Keep state in sync when expiry_date changes via write."""
        res = super().write(vals)
        if 'expiry_date' in vals:
            today = fields.Date.context_today(self)
            for rec in self:
                if not rec.expiry_date:
                    rec.state = 'valid'
                    continue
                days = (rec.expiry_date - today).days
                if days < 0:
                    rec.state = 'expired'
                elif days <= 30:
                    rec.state = 'expiring_soon'
                else:
                    rec.state = 'valid'
        return res

    def action_send_alert(self):
        """Send an expiry alert to the vendor's contact (placeholder)."""
        for rec in self:
            if rec.state == 'valid':
                raise UserError(_('This certificate is still valid; no alert needed.'))
            rec.alert_sent = True
        return True

    def action_refresh_state(self):
        """Recompute the state for all selected records based on today's date."""
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.expiry_date:
                rec.state = 'valid'
                continue
            days = (rec.expiry_date - today).days
            if days < 0:
                rec.state = 'expired'
            elif days <= 30:
                rec.state = 'expiring_soon'
            else:
                rec.state = 'valid'
