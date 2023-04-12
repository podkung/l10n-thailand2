# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class NonPurchaseReportWizard(models.TransientModel):
    _name = "non.purchase.report.wizard"
    _inherit = "common.purchase.wizard"
    _description = "Non Purchase Report Wizard"
