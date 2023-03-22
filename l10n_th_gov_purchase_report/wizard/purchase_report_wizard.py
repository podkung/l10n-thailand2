# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseReportWizard(models.TransientModel):
    _name = "purchase.report.wizard"
    _description = "Purchase Report Wizard"

    date_range_id = fields.Many2one(
        comodel_name="date.range",
    )
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
        index=True,
    )

    @api.onchange("date_range_id")
    def _onchange_date_range(self):
        for rec in self:
            if rec.date_range_id:
                rec.date_from = rec.date_range_id.date_start
                rec.date_to = rec.date_range_id.date_end

    def button_export_xlsx(self):
        self.ensure_one()
        report_type = "xlsx"
        return self._export(report_type)

    def _prepare_purchase_report(self):
        self.ensure_one()
        return {
            "date_from": self.date_from,
            "date_to": self.date_to,
            "company_id": self.company_id.id,
        }

    def _export(self, report_type):
        model = self.env["report.purchase.report"]
        report = model.create(self._prepare_purchase_report())
        return report.print_report(report_type)
