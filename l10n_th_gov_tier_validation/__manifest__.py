# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Thai Localization - Government Tier Validation",
    "version": "15.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-thailand",
    "license": "AGPL-3",
    "category": "Localization / Tools",
    "depends": [
        "base_tier_validation_formula",
        "hr_expense_advance_clearing",
        "hr_expense_tier_validation",
        "purchase_request_tier_validation",
    ],
    "data": [
        "data/hr_expense_tier_definition.xml",
        "data/purchase_request_tier_definition.xml",
        "security/l10n_th_gov_tier_validation_security.xml",
        "security/ir.model.access.csv",
        "templates/tier_validation_templates.xml",
        "views/hr_department_views.xml",
        "views/tier_level_views.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["ps-tubtim"],
}
