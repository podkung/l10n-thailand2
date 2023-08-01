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
    # Configuration
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
    # filter
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
    scb_delivery_mode = fields.Selection(
        selection=[
            ("M", "Mail"),
            ("C", "Counter"),
            ("P", "Pickup"),
            ("S", "SCBBusinessNet"),
        ],
        ondelete={
            "M": "cascade",
            "C": "cascade",
            "P": "cascade",
            "S": "cascade",
        },
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_beneficiary_noti = fields.Selection(
        selection=[
            ("N", "None"),
            ("F", "Fax"),
            ("S", "SMS"),
            ("E", "Email"),
        ],
        ondelete={
            "N": "cascade",
            "F": "cascade",
            "S": "cascade",
            "E": "cascade",
        },
        default="N",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_beneficiary_phone = fields.Char(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_beneficiary_email = fields.Char(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_beneficiary_charge = fields.Selection(
        selection=[("B", "Beneficiary Charge"), ("C", "Customer Charge")],
        ondelete={
            "B": "cascade",
            "C": "cascade",
        },
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

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

    @api.onchange("scb_beneficiary_noti")
    def _onchange_scb_beneficiary_noti(self):
        if self.scb_beneficiary_noti != "E":
            self.scb_beneficiary_email = False
        elif self.scb_beneficiary_noti not in ("F", "S"):
            self.scb_beneficiary_phone = False

    def _get_amount_no_decimal(self, amount):
        if self.bank == "SICOTHBK":
            return str(int(amount * 1000)).zfill(16)
        return super()._get_amount_no_decimal(amount)

    def _get_reference(self):
        return self.name

    def _get_line_count(self):
        return len(self.export_line_ids)

    def _get_mcl_type(self):
        if self.scb_product_code == "MCL" and self.scb_bank_type == "2":
            return "2"
        return " "

    def _get_payee_name_eng(self, pe_line):
        if self.scb_product_code == "BNT":
            receiver_name = (
                pe_line.payment_partner_bank_id.acc_holder_name_en
                or "**Not found account holder en**"
            )
            return receiver_name
        return ""

    def _get_payee_fax(self):
        return self.scb_beneficiary_phone if self.scb_beneficiary_noti == "F" else ""

    def _get_payee_sms(self):
        return self.scb_beneficiary_phone if self.scb_beneficiary_noti == "S" else ""

    def _get_payee_email(self):
        return self.scb_beneficiary_email if self.scb_beneficiary_noti == "E" else ""

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
                customer_ref=self._get_reference().ljust(32),
                file_date=file_date,
                file_time=file_time,
                batch_reference=self._get_reference().ljust(32),
            )
        )
        return text

    def _get_text_company_detail_scb(self, payment_lines, total_batch_amount):
        self.ensure_one()
        # NOTE: Can pay with 1 account
        account_bank_payment = self.export_line_ids[
            0
        ].payment_journal_id.bank_account_id.acc_number
        account_type = "0{}".format(account_bank_payment[3])
        branch_code = "0{}".format(account_bank_payment[0:3])
        text = (
            "002{product_code}{value_date}{debit_account_no}{account_type_debit_account}"
            "{debit_branch_code}THB{debit_amount}{internal_ref}{no_credit}{fee_debit_account}"
            "{filler}{mcl_type}{account_type_fee}{debit_branch_code_fee}\r\n".format(
                product_code=self.scb_product_code,
                value_date=self.effective_date.strftime("%Y%m%d"),
                debit_account_no=account_bank_payment.ljust(25),
                account_type_debit_account=account_type,
                debit_branch_code=branch_code,
                debit_amount=total_batch_amount,
                internal_ref=self._get_reference().ljust(8),
                no_credit=str(self._get_line_count()).zfill(6),
                fee_debit_account=account_bank_payment.ljust(15),
                filler="".ljust(9),
                mcl_type=self._get_mcl_type(),
                account_type_fee=account_type,
                debit_branch_code_fee=branch_code,
            )
        )
        return text

    def _get_text_credit_detail_scb(self, idx, pe_line, line_batch_amount):
        # Receiver
        (
            receiver_name,
            receiver_bank_code,
            receiver_branch_code,
            receiver_acc_number,
        ) = pe_line._get_receiver_information()
        mapping_charge = {
            "B": "B",
            "C": " ",
        }
        text = (
            "003{idx}{credit_account}{credit_amount}THB{internal_ref}{wht_present}"
            "{invoice_detail_present}{credit_advice_required}{delivery_mode}"
            "{pickup_location}{notification}{charge}\r\n".format(
                idx=str(idx).zfill(6),
                credit_account=receiver_acc_number.ljust(25),
                credit_amount=line_batch_amount,
                internal_ref=self._get_reference().ljust(8),
                wht_present="N",
                invoice_detail_present="N",
                credit_advice_required="Y",
                delivery_mode=self.scb_delivery_mode,
                pickup_location="",  # TODO
                # TODO: many field is not do
                notification=self.scb_beneficiary_noti,
                # TODO: many field is not do
                charge=mapping_charge.get(self.scb_beneficiary_charge),
            )
        )
        return text

    def _get_text_payee_detail_scb(self, idx, pe_line, line_batch_amount):
        receiver_name = pe_line._get_receiver_information()[0]
        receiver_address1 = " ".join(
            [
                pe_line.payment_partner_id.street,
            ]
        )
        receiver_address2 = " ".join(
            [
                pe_line.payment_partner_id.street2,
                pe_line.payment_partner_id.city,
                pe_line.payment_partner_id.zip,
            ]
        )
        text = (
            "004{internal_ref}{idx}{payee_idcard}{payee_name}"
            "{payee_address1}{payee_address2}{payee_address3}{payee_tax_id}"
            "{payee_name_eng}{payee_fax}{payee_sms}{payee_email}{space}\r\n".format(
                internal_ref=self._get_reference().ljust(8),
                idx=str(idx).zfill(6),
                payee_idcard=str(pe_line.payment_partner_id.vat).zfill(15),
                payee_name=receiver_name.ljust(100),
                payee_address1=receiver_address1.ljust(70),
                payee_address2=receiver_address2.ljust(70),
                payee_address3="".ljust(70),
                payee_tax_id="".ljust(10),
                payee_name_eng=self._get_payee_name_eng(pe_line).ljust(70),
                payee_fax=self._get_payee_fax(),  # TODO: why numeric?
                payee_sms=self._get_payee_sms(),  # TODO: why numeric?
                payee_email=self._get_payee_email().ljust(64),
                # TODO
                space="".ljust(310),
            )
        )
        return text

    def _get_text_footer_scb(self, payment_lines, total_batch_amount):
        text = "999{total_debit}{total_credit}{total_amount}\r\n".format(
            total_debit="1".zfill(6),
            total_credit=str(len(payment_lines)).zfill(6),
            total_amount=total_batch_amount,
        )
        return text

    def _format_scb_text(self):
        self.ensure_one()
        payment_lines = self.export_line_ids
        # Header
        text = self._get_text_header_scb()
        total_batch_amount = self._get_amount_no_decimal(self.total_amount)
        text += self._get_text_company_detail_scb(payment_lines, total_batch_amount)
        # Details
        for idx, pe_line in enumerate(payment_lines):
            # This amount related decimal from invoice, Odoo invoice do not rounding.
            payment_net_amount = pe_line._get_payment_net_amount()
            line_batch_amount = pe_line._get_amount_no_decimal(payment_net_amount)
            text += self._get_text_credit_detail_scb(idx, pe_line, line_batch_amount)
            text += self._get_text_payee_detail_scb(idx, pe_line, line_batch_amount)
            # text += self._get_text_wht_detail_scb(idx, pe_line, line_batch_amount)
        text += self._get_text_footer_scb(payment_lines, total_batch_amount)
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
    #     for rec in self.filtered(lambda l: l.bank == "SICOTHBK"):
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
