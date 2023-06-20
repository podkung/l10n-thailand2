# Copyright 2023 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class WithHoldingTaxReportWizard(models.TransientModel):
    _inherit = "withholding.tax.report.wizard"

    branch_ids = fields.Many2many(
        comodel_name="res.branch",
    )

    def _prepare_wht_report(self):
        res = super()._prepare_wht_report()
        res["branch_ids"] = self.branch_ids.ids
        return res
