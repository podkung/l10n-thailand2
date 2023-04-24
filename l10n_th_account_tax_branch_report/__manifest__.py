# Copyright 2023 Ecosoft Co., Ltd (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Thai Localization - Tax Branch Reports",
    "version": "15.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-thailand",
    "license": "AGPL-3",
    "category": "Accounting",
    "depends": [
        "l10n_th_account_tax_branch_operating_unit",
        "l10n_th_account_tax_report",
    ],
    "data": [
        "reports/tax_report.xml",
        "reports/tax_report_rd.xml",
        "reports/report_wht_qweb.xml",
        "reports/report_wht_qweb_rd.xml",
        "wizard/tax_report_wizard_view.xml",
        "wizard/withholding_tax_report_wizard_view.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["Saran440"],
}
