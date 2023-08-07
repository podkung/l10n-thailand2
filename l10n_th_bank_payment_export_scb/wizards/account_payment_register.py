# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    scb_product_code = fields.Selection(
        selection=[
            ("BNT", "BNT - Bahtnet"),
            ("DCP", "DCP - Direct Credit"),
            ("MCL", "MCL - Media Clearing"),
            ("PAY", "PAY - Payroll"),
            ("PA2", "PA2 - Payroll 2"),
            ("PA3", "PA3 - Payroll 3"),
            ("PA4", "PA4 - MediaClearing Payroll"),
            ("PA5", "PA5 - MediaClearing Payroll 2"),
            ("PA6", "PA6 - MediaClearing Payroll 3"),
            ("MCP", "MCP - MCheque"),
            ("CCP", "CCP - Corporate Cheque"),
            ("DDP", "DDP - Demand Draft"),
            ("XMQ", "XMQ - Express Manager Cheque"),
            ("XDQ", "XDQ - Express Demand Draft"),
        ],
        string="Product Code",
    )
    scb_service_type = fields.Selection(
        selection=[
            ("01", "01 - เงินเดือน, ค่าจ้าง, บำเหน็จ, บำนาญ"),
            ("02", "02 - เงินปันผล"),
            ("03", "03 - ดอกเบี้ย"),
            ("04", "04 - ค่าสินค้า, บริการ"),
            ("05", "05 - ขายหลักทรัพย์"),
            ("06", "06 - คืนภาษี"),
            ("07", "07 - เงินกู้"),
            ("59", "59 - อื่น ๆ"),
        ],
        string="Service Type",
    )
    scb_service_type_bahtnet = fields.Selection(
        selection=[
            ("00", "00 - Other"),
            ("01", "01 - Freight"),
            ("02", "02 - Insurance Premium"),
            ("03", "03 - Trasportation Cost"),
            ("04", "04 - Travelling Expenses (Thai)"),
            ("05", "05 - Forign Tourist Expenses"),
            ("06", "06 - Interest Paid"),
            ("07", "07 - Dividened"),
            ("08", "08 - Education"),
            ("09", "09 - Royalty Fee"),
            ("10", "10 - Agency Expenses"),
            ("11", "11 - Advertising Fee"),
            ("12", "12 - Communication Cost"),
            ("13", "13 - Personal Remittance / Family Support"),
            ("14", "14 - Money Transfer for Government"),
            ("15", "15 - Embassy / Military / Government Expenses"),
            ("16", "16 - Thai Lobour Money Transfer"),
            ("17", "17 - Salary"),
            ("18", "18 - Commission Fee"),
            ("19", "19 - Loan"),
            ("20", "20 - Direct Investment"),
            ("21", "21 - Portfolio Investment"),
            ("22", "22 - Trade Transaction"),
            ("23", "23 - Fixed Asset Investment"),
        ],
        string="Service Type (BahtNet)",
    )

    scb_delivery_mode = fields.Selection(
        selection=[
            ("M", "Mail"),
            ("C", "Counter"),
            ("P", "Pickup"),
            ("S", "SCBBusinessNet"),
        ],
        string="Delivery Mode",
    )
    scb_pickup_location = fields.Selection(
        selection=[
            ("C001", "C001 - รัชโยธิน"),
            ("C002", "C002 - ชิดลม"),
            ("C003", "C003 - มาบตาพุด"),
            ("C004", "C004 - ลาดกระบัง"),
            ("C005", "C005 - ท่าแพ"),
            ("C006", "C006 - อโศก"),
            ("C007", "C007 - พัทยา สาย2"),
            ("C008", "C008 - พระราม 4"),
            ("C009", "C009 - ถนนเชิดวุฒากาศ"),
            ("C010", "C010 - แหลมฉบัง"),
            ("C011", "C011 - ไอทีสแควร์ (หลักสี่)"),
            ("C012", "C012 - สุวรรณภูมิ"),
        ],
        string="Pickup Location",
    )

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        payment_vals["scb_product_code"] = self.scb_product_code
        payment_vals["scb_service_type"] = self.scb_service_type
        payment_vals["scb_service_type_bahtnet"] = self.scb_service_type_bahtnet
        payment_vals["scb_delivery_mode"] = self.scb_delivery_mode
        payment_vals["scb_pickup_location"] = self.scb_pickup_location
        return payment_vals

    def _create_payment_vals_from_batch(self, batch_result):
        payment_vals = super()._create_payment_vals_from_batch(batch_result)
        payment_vals["scb_product_code"] = self.scb_product_code
        payment_vals["scb_service_type"] = self.scb_service_type
        payment_vals["scb_service_type_bahtnet"] = self.scb_service_type_bahtnet
        payment_vals["scb_delivery_mode"] = self.scb_delivery_mode
        payment_vals["scb_pickup_location"] = self.scb_pickup_location
        return payment_vals

    @api.onchange("scb_product_code")
    def _onchange_scb_product_code(self):
        if self.scb_product_code not in ["MCL", "PA4", "PA5", "PA6"]:
            self.scb_service_type = False
        if self.scb_product_code != "BNT":
            self.scb_service_type_bahtnet = False
        if self.scb_product_code not in ["MCP", "DDP", "CCP"]:
            self.scb_delivery_mode = False

    def action_create_payments(self):
        # Not allow select difference bank SCB
        if (
            self.scb_product_code in ["MCP", "CCP", "DDP", "PAY", "DCP"]
            and self.partner_bank_id.bank_id.bic != "SICOTHBK"
        ):
            raise UserError(
                _(
                    "Product Code 'MCP', 'CCP', 'DDP', 'PAY' and 'DCP' "
                    "must only be associated with the recipient bank account of 'SCB'."
                )
            )
        return super().action_create_payments()
