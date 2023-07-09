# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models


class BankPaymentExport(models.Model):
    _inherit = "bank.payment.export"

    bank = fields.Selection(
        selection_add=[("SICOTHBK", "SCB")],
        ondelete={"SICOTHBK": "cascade"},
    )
    # # Configuration
    config_scb_company_id = fields.Many2one(
        comodel_name="bank.payment.config",
        string="SCB Company ID",
        default=lambda self: self._default_common_config("config_scb_company_id"),
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="""
            You can config this field from menu
            Invoicing > Configuration > Payments > Bank Payment Configuration
        """,
    )
    # config_ktb_sender_name = fields.Many2one(
    #     comodel_name="bank.payment.config",
    #     string="KTB Sender Name",
    #     default=lambda self: self._default_common_config("config_ktb_sender_name"),
    #     readonly=True,
    #     states={"draft": [("readonly", False)]},
    #     help="""
    #         You can config this field from menu
    #         Invoicing > Configuration > Payments > Bank Payment Configuration
    #     """,
    # )
    # # filter
    scb_is_editable = fields.Boolean(
        compute="_compute_ktb_editable",
        string="SCB Editable",
    )
    scb_bank_type = fields.Selection(
        selection=[
            ("1", "Next Day"),
            ("2", "Same Day Afternoon"),
        ],
        default="1",
        tracking=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_product_code = fields.Selection(
        selection=[
            ("BNT", "Bahtnet"),
            ("DCP", "Direct Credit"),
            ("MCL", "Media Clearing"),
            ("PAY", "Payroll"),
            ("PA2", "Payroll 2"),
            ("PA3", "Payroll 3"),
            ("PA4", "MediaClearing Payroll"),
            ("PA5", "MediaClearing Payroll 2"),
            ("PA6", "MediaClearing Payroll 3"),
            ("MCP", "MCheque"),
            ("CCP", "Corporate Cheque"),
            ("DDP", "Demand Draft"),
            ("XMQ", "Express Manager Cheque"),
            ("XDQ", "Express Demand Draft"),
        ],
        ondelete={
            "BNT": "cascade",
            "DCP": "cascade",
            "MCL": "cascade",
            "PAY": "cascade",
            "PA2": "cascade",
            "PA3": "cascade",
            "PA4": "cascade",
            "PA5": "cascade",
            "PA6": "cascade",
            "MCP": "cascade",
            "CCP": "cascade",
            "DDP": "cascade",
            "XMQ": "cascade",
            "XDQ": "cascade",
        },
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    # ktb_service_type_direct = fields.Selection(
    #     selection=[
    #         ("02", "รายการเข้าบัญชีเงินเดือน (Salary)"),
    #         ("04", "รายการชำระดอกเบี้ย (Bond Interest)"),
    #         ("09", "รายการชำระเบี้ยประกัน (Insurance Premium)"),
    #         ("10", "รายการชำระค่าโทรศัพท์ (Telephone Payment)"),
    #         ("11", "รายการชำระค่าไฟฟ้า (Electricity Payment)"),
    #         ("12", "รายการชำระค่าน้ำประปา (Water Payment)"),
    #         ("14", "รายการชำระค่าสินค้าและบริการ (Purchase & Service)"),
    #         ("15", "รายการชำระเงินของธนาคารอาคารสงเคราะห์ (GSB)"),
    #         ("21", "รายการชำระราคาหลักทรัพย์ (Securities)"),
    #         ("25", "รายการชำระ Clearing Bank"),
    #         ("27", "รายการชำระค่าประกันสังคม (SSO)"),
    #         ("28", "รายการชำระของกองสลากฯ (Lottery)"),
    #         ("37", "รายการชำระด้วยบัตรอิเลคทรอนิคส์ (Electronic Card)"),
    #         ("46", "รายการจ่ายเงินบำนาญ (Pension Fund)"),
    #     ],
    #     ondelete={
    #         "02": "cascade",
    #         "04": "cascade",
    #         "09": "cascade",
    #         "10": "cascade",
    #         "11": "cascade",
    #         "12": "cascade",
    #         "14": "cascade",
    #         "15": "cascade",
    #         "21": "cascade",
    #         "25": "cascade",
    #         "27": "cascade",
    #         "28": "cascade",
    #         "37": "cascade",
    #         "46": "cascade",
    #     },
    #     readonly=True,
    #     states={"draft": [("readonly", False)]},
    # )

    @api.depends("bank")
    def _compute_required_effective_date(self):
        res = super()._compute_required_effective_date()
        for rec in self.filtered(lambda l: l.bank == "SICOTHBK"):
            rec.is_required_effective_date = True
        return res

    @api.depends("bank")
    def _compute_ktb_editable(self):
        for export in self:
            export.scb_is_editable = True if export.bank == "SICOTHBK" else False

    # def _get_ktb_sender_name(self):
    #     return self.config_ktb_sender_name.value or self.env.company.display_name

    # def _get_ktb_receiver_info(self, pe_line):
    #     return "".ljust(8)

    # def _get_ktb_receiver_id(self, pe_line):
    #     return "0".zfill(10)

    # def _get_ktb_other_info1(self, pe_line):
    #     return "".ljust(40)

    # def _get_ktb_other_info2(self, pe_line):
    #     return "".ljust(20)

    # def _get_ktb_ddr_ref1(self, pe_line):
    #     return "".ljust(18)

    # def _get_ktb_ddr_ref2(self, pe_line):
    #     return pe_line.payment_id.name.ljust(18)

    # def _get_ktb_email(self, pe_line):
    #     return (
    #         pe_line.payment_partner_id.email
    #         and pe_line.payment_partner_id.email[:40].ljust(40)
    #         or "".ljust(40)
    #     )

    # def _get_ktb_sms(self, pe_line):
    #     return (
    #         pe_line.payment_partner_id.phone
    #         and pe_line.payment_partner_id.phone[:20].ljust(20)
    #         or "".ljust(20)
    #     )

    # def _get_ktb_receiver_sub_branch_code(self, pe_line):
    #     return "0".zfill(4)

    def _get_text_header_scb(self):
        self.ensure_one()
        scb_company_id = (
            self.config_scb_company_id.value or "**Company ID on SCB is not config**"
        )
        today = fields.Datetime.context_timestamp(self.env.user, datetime.now())
        file_date = today.strftime("%Y%m%d")
        file_time = today.strftime("%H%M%S")
        text = (
            "001{scb_company}{customer_ref}{file_date}{file_time}BCM"
            "{batch_reference}\r\n".format(
                scb_company=scb_company_id.ljust(12),
                customer_ref="".ljust(32),  # TODO
                file_date=file_date,
                file_time=file_time,
                batch_reference="".ljust(32),  # TODO
            )
        )
        return text

    def _get_text_company_detail_scb(self, payment_lines):
        self.ensure_one()
        # NOTE: Can pay with 1 account
        account_bank_payment = self.export_line_ids[
            0
        ].payment_journal_id.bank_account_id.acc_number
        account_type = "0{}".format(account_bank_payment[3])
        branch_code = "0{}".format(account_bank_payment[0:3])
        output_map = {
            "1": " ",
            "2": "2",
        }
        text = (
            "002{product_code}{value_date}{debit_account_no}{account_type_debit_account}"
            "{debit_branch_code}THB{debit_amount}{internal_ref}{no_credit}{fee_debit_account}"
            "{filler}{bank_type}{account_type_fee}{debit_branch_code_fee}\r\n".format(
                product_code=self.scb_product_code,
                value_date=self.effective_date.strftime("%Y%m%d"),
                debit_account_no=account_bank_payment.ljust(25),
                account_type_debit_account=account_type,
                debit_branch_code=branch_code,
                debit_amount="",
                internal_ref="",
                no_credit="",
                fee_debit_account="",
                filler="".ljust(9),
                bank_type=output_map.get(self.scb_bank_type),
                account_type_fee="",
                debit_branch_code_fee="",
            )
        )
        return text

    def _get_text_credit_detail_scb(self, idx, pe_line, payment_net_amount_bank):
        # Receiver
        (
            receiver_name,
            receiver_bank_code,
            receiver_branch_code,
            receiver_acc_number,
        ) = pe_line._get_receiver_information()
        text = (
            "003{idx}{credit_account}{credit_amount}THB{internal_ref}{wht_present}"
            "{invoice_detail_present}{credit_advice_required}{delivery_mode}"
            "{pickup_location}\r\n".format(
                idx=str(idx).zfill(6),
                credit_account=receiver_acc_number.ljust(25),
                credit_amount=payment_net_amount_bank
                and str(payment_net_amount_bank)[:17].zfill(16)
                or "0".zfill(16),
                internal_ref="",
                wht_present="",
                invoice_detail_present="",
                credit_advice_required="",
                delivery_mode="",
                pickup_location="",
            )
        )
        return text

    def _get_text_payee_detail_scb(self, idx, pe_line, payment_net_amount_bank):
        text = (
            "004{internal_ref}{credit_sequence}{payee_idcard}{payee_name}"
            "{payee_address}{payee_tax_id}\r\n".format(
                internal_ref="",
                credit_sequence="",
                payee_idcard="",
                payee_name="",
                payee_address="",
                payee_tax_id="",
            )
        )
        return text

    def _get_text_footer_scb(self, payment_lines):
        text = "999{total_debit}{total_credit}{total_amount}\r\n".format(
            total_debit="1".zfill(6),
            total_credit=str(len(payment_lines)).zfill(6),
            total_amount="0000000000000000",  # TODO
        )
        return text

    def _format_scb_text(self):
        self.ensure_one()
        total_amount = 0
        payment_lines = self.export_line_ids
        # total_amount =
        # Header
        text = self._get_text_header_scb()
        text += self._get_text_company_detail_scb(payment_lines)
        # Details
        for idx, pe_line in enumerate(payment_lines):
            # This amount related decimal from invoice, Odoo invoice do not rounding.
            payment_net_amount = pe_line._get_payment_net_amount()
            payment_net_amount_bank = pe_line._get_amount_no_decimal(payment_net_amount)
            text += self._get_text_credit_detail_scb(
                idx, pe_line, payment_net_amount_bank
            )
            text += self._get_text_payee_detail_scb(
                idx, pe_line, payment_net_amount_bank
            )
            # text += self._get_text_wht_detail_scb(idx, pe_line, payment_net_amount_bank)
            total_amount += payment_net_amount_bank
        text += self._get_text_footer_scb(payment_lines)
        return text

    def _generate_bank_payment_text(self):
        self.ensure_one()
        if self.bank == "SICOTHBK":  # SCB
            return self._format_scb_text()
        return super()._generate_bank_payment_text()

    def _get_view_report_text(self):
        """TODO: This function can used demo. May be we delete it later"""
        if self.bank == "SICOTHBK":
            return "l10n_th_bank_payment_export_scb.action_payment_scb_txt"
        return super()._get_view_report_text()

    # def _check_constraint_confirm(self):
    #     res = super()._check_constraint_confirm()
    #     for rec in self.filtered(lambda l: l.bank == "KRTHTHBK"):
    #         if not rec.ktb_bank_type:
    #             raise UserError(_("You need to add 'Bank Type' before confirm."))
    #         if rec.ktb_bank_type == "direct" and any(
    #             line.payment_bank_id.bic != rec.bank for line in rec.export_line_ids
    #         ):
    #             raise UserError(
    #                 _("Bank type '{}' can not export payment to other bank.").format(
    #                     dict(self._fields["ktb_bank_type"].selection).get(
    #                         self.ktb_bank_type
    #                     )
    #                 )
    #             )
    #         if rec.ktb_bank_type == "standard" and any(
    #             line.payment_bank_id.bic == rec.bank for line in rec.export_line_ids
    #         ):
    #             raise UserError(
    #                 _("Bank type '{}' can not export payment to the same bank.").format(
    #                     dict(self._fields["ktb_bank_type"].selection).get(
    #                         self.ktb_bank_type
    #                     )
    #                 )
    #             )
    #     return res

    # def _get_context_create_bank_payment_export(self, payments):
    #     ctx = super()._get_context_create_bank_payment_export(payments)
    #     partner_bic_bank = list(set(payments.mapped("partner_bank_id.bank_id.bic")))
    #     # KTB Bank
    #     if partner_bic_bank and ctx["default_bank"] == "KRTHTHBK":
    #         # Same bank
    #         if len(partner_bic_bank) == 1 and partner_bic_bank[0] == "KRTHTHBK":
    #             ctx.update({"default_ktb_bank_type": "direct"})
    #         # Other bank
    #         elif "KRTHTHBK" not in partner_bic_bank:
    #             ctx.update({"default_ktb_bank_type": "standard"})
    #     return ctx

    # def _check_constraint_create_bank_payment_export(self, payments):
    #     res = super()._check_constraint_create_bank_payment_export(payments)
    #     payment_bic_bank = list(set(payments.mapped("journal_id.bank_id.bic")))
    #     payment_bank = len(payment_bic_bank) == 1 and payment_bic_bank[0] or ""
    #     # Check case KTB must have 1 journal / 1 PE
    #     if payment_bank == "KRTHTHBK" and len(payments.mapped("journal_id")) > 1:
    #         raise UserError(
    #             _("KTB can create bank payment export 1 Journal / 1 Payment Export.")
    #         )
    #     return res
