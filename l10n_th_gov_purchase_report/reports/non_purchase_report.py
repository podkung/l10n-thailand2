# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class NonPurchaseReport(models.TransientModel):
    _name = "report.non.purchase.report"
    _description = "Non Purchase Report"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    date_from = fields.Date()
    date_to = fields.Date()

    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name="hr.expense",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _get_expense_purchase_type(self):
        c79_2 = self.env.ref("l10n_th_gov_purchase_request.purchase_type_003")
        w119 = self.env.ref("l10n_th_gov_purchase_request.purchase_type_004")
        return c79_2 + w119

    def _compute_results(self):
        self.ensure_one()
        purchase_type = self._get_expense_purchase_type()
        dom = [
            ("purchase_type_id", "in", purchase_type.ids),
            ("sheet_id.state", "in", ["post", "done"]),
        ]
        # Filter report by accounting date
        if self.date_from:
            dom += [("accounting_date", ">=", self.date_from)]
        if self.date_to:
            dom += [("accounting_date", "<=", self.date_to)]
        self.results = self.env["hr.expense"].search(dom, order="date")

    def _hook_print_report(self):
        raise UserError(
            _(
                "This report support type xlsx only. "
                "you can implement it at function '_hook_print_report'"
            )
        )

    def print_report(self, report_type="xlsx"):
        self.ensure_one()
        if report_type != "xlsx":
            return self._hook_print_report()
        action = self.env.ref(
            "l10n_th_gov_purchase_report.action_non_purchase_report_xlsx"
        )
        return action.report_action(self, config=False)
