# -*- coding: utf-8 -*-
{
    'name': 'Construction Document AI Pack: Bid, Change Order & Invoice Extraction',
    'version': '18.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-powered extraction for construction bids, change orders, invoices, '
               'certificates of insurance, delivery tickets, and subcontract documents.',
    'description': """
Construction Document AI Pack
=============================
Extract, verify, and manage construction documents with AI.

* Bid analysis with completeness scoring and risk flags
* Change order extraction with schedule impact and approval recommendations
* Invoice extraction with line-item matching to POs
* Certificate of insurance tracking with expiry alerts
* Delivery ticket and subcontract document support
* Per-field confidence scoring and human-in-the-loop review
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'application': True,
    'price': 399.99,
    'currency': 'USD',
    'data': [
        'security/ir.model.access.csv',
        'views/cda_extraction_job_views.xml',
        'views/cda_extracted_field_views.xml',
        'views/cda_bid_analysis_views.xml',
        'views/cda_change_order_extract_views.xml',
        'views/cda_invoice_extract_views.xml',
        'views/cda_co_insurance_tracker_views.xml',
        'views/cda_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
}
