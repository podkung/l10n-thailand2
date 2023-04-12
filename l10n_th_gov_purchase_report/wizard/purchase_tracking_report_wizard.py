# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseTrackingReportWizard(models.TransientModel):
    _name = "purchase.tracking.report.wizard"
    _inherit = "common.purchase.wizard"
    _description = "Purchase Tracking Report Wizard"

    requested_by = fields.Many2many(
        comodel_name="res.users",
    )

    def _prepare_data_report(self):
        res = super()._prepare_data_report()
        res["requested_by"] = self.requested_by.ids
        return res
