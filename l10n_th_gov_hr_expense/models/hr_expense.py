# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    purchase_type_id = fields.Many2one(
        string="Purchase Type",
        comodel_name="purchase.type",
        compute="_compute_purchase_type_id",
        domain=[("to_create", "=", "expense")],
        store=True,
        readonly=False,
        index=True,
        ondelete="restrict",
    )

    @api.depends("sheet_id.purchase_request_id")
    def _compute_purchase_type_id(self):
        for expense in self:
            if expense.sheet_id.purchase_request_id:
                expense.purchase_type_id = (
                    expense.sheet_id.purchase_request_id.purchase_type_id
                )


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    purchase_request_id = fields.Many2one(
        comodel_name="purchase.request",
        string="Purchase Request",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
