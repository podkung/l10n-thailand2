# Copyright 2023 Ecosoft Co., Ltd (https://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)


from odoo import fields, models


class WithHoldingTaxReport(models.TransientModel):
    _inherit = "withholding.tax.report"

    tax_branch_ids = fields.Many2many(comodel_name="tax.branch.operating.unit")

    def _get_domain_wht(self):
        domain = super()._get_domain_wht()
        if not self.tax_branch_ids:
            return domain
        if len(self.tax_branch_ids) > 1:
            domain.append(("cert_id.tax_branch_id", "in", self.tax_branch_ids.ids))
        else:
            domain.append(("cert_id.tax_branch_id", "=", self.tax_branch_ids.id))
        return domain

    def _get_tax_branch_filter(self, tax_branch=False):
        if not tax_branch:
            tax_branch = self.env["tax.branch.operating.unit"].search([])
        return ", ".join(tax_branch.mapped("name"))
