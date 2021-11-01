# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Thai Localization - VAT and Withholding Tax",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/l10n-thailand",
    "category": "Localization / Accounting",
    "depends": ["account"],
    "data": [
        "data/pit_rate_data.xml",
        "security/account_security.xml",
        "security/ir.model.access.csv",
        "wizard/account_payment_register_views.xml",
        "views/account_view.xml",
        "views/account_move_view.xml",
        "views/withholding_tax_cert.xml",
        "views/account_withholding_tax.xml",
        "views/account_withholding_move.xml",
        "views/product_view.xml",
        "views/account_payment_view.xml",
        "views/personal_income_tax_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["kittiu"],
}
