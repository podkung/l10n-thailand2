# Copyright 2023 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class WithHoldingTaxReportWizard(models.TransientModel):
    _inherit = "withholding.tax.report.wizard"

    tax_branch_ids = fields.Many2many(
        comodel_name="tax.branch.operating.unit",
    )

    def _prepare_wht_report(self):
        res = super()._prepare_wht_report()
        res["tax_branch_ids"] = self.tax_branch_ids.ids
        return res
