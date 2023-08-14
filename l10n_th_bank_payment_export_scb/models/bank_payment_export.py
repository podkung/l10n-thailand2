# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BankPaymentExport(models.Model):
    _inherit = "bank.payment.export"

    bank = fields.Selection(
        selection_add=[("SICOTHBK", "SCB")],
        ondelete={"SICOTHBK": "cascade"},
    )
    scb_company_id = fields.Char(
        string="SCB Company ID",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    # filter
    scb_is_editable = fields.Boolean(
        compute="_compute_scb_editable",
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
            ("M", "Mail => Send by Registered mail"),
            ("C", "Counter => Send by messenger to Customer"),
            ("P", "Pickup => Receiving pickup at SCB branch"),
            ("S", "SCBBusinessNet => Send back to SCBBusinessNet"),
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
        ondelete={
            "C001": "cascade",
            "C002": "cascade",
            "C003": "cascade",
            "C004": "cascade",
            "C005": "cascade",
            "C006": "cascade",
            "C007": "cascade",
            "C008": "cascade",
            "C009": "cascade",
            "C010": "cascade",
            "C011": "cascade",
            "C012": "cascade",
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
        ondelete={
            "01": "cascade",
            "02": "cascade",
            "03": "cascade",
            "04": "cascade",
            "05": "cascade",
            "06": "cascade",
            "07": "cascade",
            "59": "cascade",
        },
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
        ondelete={
            "00": "cascade",
            "01": "cascade",
            "02": "cascade",
            "03": "cascade",
            "04": "cascade",
            "05": "cascade",
            "06": "cascade",
            "07": "cascade",
            "08": "cascade",
            "09": "cascade",
            "10": "cascade",
            "11": "cascade",
            "12": "cascade",
            "13": "cascade",
            "14": "cascade",
            "15": "cascade",
            "16": "cascade",
            "17": "cascade",
            "18": "cascade",
            "19": "cascade",
            "20": "cascade",
            "21": "cascade",
            "22": "cascade",
            "23": "cascade",
        },
    )
    scb_beneficiary_charge = fields.Boolean(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_invoice_language = fields.Selection(
        selection=[("T", "Thai"), ("E", "English")],
        ondelete={
            "T": "cascade",
            "E": "cascade",
        },
        default="T",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_is_invoice_present = fields.Boolean(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_is_wht_present = fields.Boolean(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_is_credit_advice = fields.Boolean(
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_wht_signatory = fields.Selection(
        selection=[("B", "Bank"), ("C", "Corporate")],
        ondelete={
            "B": "cascade",
            "C": "cascade",
        },
        default="B",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_cheque_ref = fields.Selection(
        selection=[
            ("1", "ใบเสร็จรับเงิน"),
            ("2", "ใบวางบิล"),
            ("3", "ใบเสร็จรับเงินและใบวางบิล"),
            ("4", "ใบเสร็จรับเงินและใบกำกับภาษี"),
            ("5", "ใบวางบิลและใบเสร็จรับเงินและใบกำกับภาษี"),
            ("6", "สำเนาบัตรประชาชน/หนังสือเดินทาง"),
            ("7", "สำเนาบัตรประชาชน/หนังสือเดินทาง + ใบนัดรับของรางวัล"),
            ("8", "สำเนาบัตรประชาชน/หนังสือเดินทาง + ใบสั่งจ้าง"),
            ("9", "สำเนาใบเสร็จรับเงิน"),
            ("A", "เงินในเช็คใบเสร็จไม่เท่ากัน - จ่าย"),
            ("B", "หนังสือรับรองการหักภาษีณ.ที่จ่าย."),
            ("C", "หนังสือกรมศุลกากร"),
            ("D", "ใบกำกับภาษี"),
            (
                "E",
                "หนังสือมอบพร้อมติดอากรแสตมป์ 10 บาท + สำเนาบัตร ปชช.ผู้มอบพร้อมลงนาม "
                "+ สำเนาบัตร ปชช.ผู้รับมอบพร้อมลงนาม",
            ),
            (
                "F",
                "หนังสือมอบจากคณะบุคคลพร้อมติดอากรแสตมป์ 10 บาท + "
                "สำเนาสัญญาจัดตั้งคณะบุคคลพร้อมลงนาม + "
                "สำเนาบัตรผู้เสียภาษีของคณะบุคคลพร้อมลงนาม + "
                "สำเนาบัตร ปชช.ผู้มอบ และผู้รับมอบ พร้อมลงนาม",
            ),
            ("G", "เอกสารยืนยันการโอนเงิน/ออกเช็คผ่านโทรสาร"),
            ("H", "อื่น ๆ"),
            ("I", "สัญญาประนีประนอม"),
            ("J", "ใบเสร็จ/ใบกำกับภาษี + ใบรับรถ"),
            ("K", "หนังสือมอบ + บัตร ปชช.ผู้รับมอบ"),
            ("L", "บัตร ปชช.ผู้มอบ + บัตร ปชช.ผู้รับมอบ"),
            ("M", "ใบรับรถ + เซ็นชื่อใบรับเงิน/สัญญา"),
            ("N", "ใบรถ + น.มอบ + ผู้รับมอบ + เซ็นชื่อ/สัญญา"),
            ("O", "ใบรับเช็ค"),
            ("P", "ใบลดหนี้"),
            ("Q", "ใบเพิ่มหนี้"),
            ("R", "ดูช่อง Invoice Description ใน Advice"),
            ("S", "ขายลดเช็คทันที"),
            ("T", "Email + สำเนาบัตรพนง. + สำเนาบัตรปปช."),
            ("U", "ค่าสาธารณูปโภค"),
            ("V", "ใบเสร็จรับเงินและ หนังสือรับรองหักภาษี ณ ที่จ่าย"),
            ("W", "ใบเสร็จรับเงิน หรือบัตรประชาชน"),
            ("X", "ไม่ใช้เอกสารใด ๆ"),
            ("Y", "ใบวางบิลและใบเสร็จรับเงิน (จำนวนเงินไม่ตรง-จ่าย)"),
            ("Z", "ใบวางบิลและสำเนาบัตรประชาชน"),
        ],
        ondelete={
            "1": "cascade",
            "2": "cascade",
            "3": "cascade",
            "4": "cascade",
            "5": "cascade",
            "6": "cascade",
            "7": "cascade",
            "8": "cascade",
            "9": "cascade",
            "A": "cascade",
            "B": "cascade",
            "C": "cascade",
            "D": "cascade",
            "E": "cascade",
            "F": "cascade",
            "G": "cascade",
            "H": "cascade",
            "I": "cascade",
            "J": "cascade",
            "K": "cascade",
            "L": "cascade",
            "M": "cascade",
            "N": "cascade",
            "O": "cascade",
            "P": "cascade",
            "Q": "cascade",
            "R": "cascade",
            "S": "cascade",
            "T": "cascade",
            "U": "cascade",
            "V": "cascade",
            "W": "cascade",
            "X": "cascade",
            "Y": "cascade",
            "Z": "cascade",
        },
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    scb_payment_type_code = fields.Selection(
        selection=[
            ("CSH", "CSH - Cash"),
            ("BCQ", "BCQ - Branch or other bank chqs"),
            ("HCQ", "HCQ - Home chqs"),
            ("DCA", "DCA - Current A/C"),
            ("DSA", "DSA - Saving A/C"),
            ("BCA", "BCA - Current A/C - other branch"),
            ("BSA", "BSA - Saving A/C - other branch"),
            ("FCA", "FCA - Foreign cur. Current A/C"),
            ("FSA", "FSA - Foreign cur. Saving A/C"),
            ("SPD", "SPD - Suspense debtor"),
            ("SPC", "SPC - Suspense creditor"),
            ("UST", "UST - Unsettled"),
            ("OFA", "OFA - Offline Account"),
            ("FWD", "FWD - Forward Value"),
        ],
        ondelete={
            "CSH": "cascade",
            "BCQ": "cascade",
            "HCQ": "cascade",
            "DCA": "cascade",
            "DSA": "cascade",
            "BCA": "cascade",
            "BSA": "cascade",
            "FCA": "cascade",
            "FSA": "cascade",
            "SPD": "cascade",
            "SPC": "cascade",
            "UST": "cascade",
            "OFA": "cascade",
            "FWD": "cascade",
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
    def _compute_scb_editable(self):
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

    def _get_wht_income_type(self, wht_line):
        wht_income_type = wht_line.wht_cert_income_type.lower()
        if len(wht_income_type) == 4:
            wht_income_type = "{}.{}".format(wht_income_type[:3], wht_income_type[3:])
        return wht_income_type

    def _get_wht_header(self, wht_cert):
        if not self.scb_is_wht_present:
            return "".ljust(40)
        wht_type = "00"
        if wht_cert.income_tax_form == "pnd1":
            wht_type = "01"
        elif wht_cert.income_tax_form == "pnd3":
            wht_type = "03"
        elif wht_cert.income_tax_form == "pnd53":
            wht_type = "53"
        total_wht = self._get_amount_no_decimal(sum(wht_cert.wht_line.mapped("amount")))
        text = "{wht_type}{wht_running_no}{wht_attach_no}{wht_line}{total_wht}".format(
            wht_type=wht_type,
            wht_running_no="".ljust(14),  # NOTE: Bank will generate
            wht_attach_no="0".zfill(6),  # NOTE: Bank will generate
            wht_line=str(len(wht_cert.wht_line)).zfill(2),
            total_wht=total_wht,
        )
        return text

    def _get_wht_header2(self, wht_cert):
        if not self.scb_is_wht_present:
            return "".ljust(49)
        mapping_tax_payer = {
            "withholding": "3",
            "paid_one_time": "1",
        }
        text = "{pay_type}{wht_remark}{wht_deduct_date}".format(
            pay_type=mapping_tax_payer.get(wht_cert.tax_payer),
            wht_remark="".ljust(40),  # NOTE: System is not type 4
            wht_deduct_date=wht_cert.date.strftime("%Y%m%d"),
        )
        return text

    def _get_invoice_header(self, invoices):
        if not self.scb_is_invoice_present:
            return "".ljust(22)
        invoice_total_amount = self._get_amount_no_decimal(
            sum(invoices.mapped("amount_total"))
        )
        text = "{invoice_count}{invoice_total_amount}".format(
            invoice_count=str(len(invoices)).zfill(6),
            invoice_total_amount=invoice_total_amount,
        )
        return text

    def _get_service_type(self):
        if self.scb_product_code == "BNT":
            return self.scb_service_type_bahtnet
        return self.scb_service_type

    def _get_text_header_scb(self):
        self.ensure_one()
        scb_company_id = self.scb_company_id or "**Company ID on SCB is not config**"
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
        if not account_bank_payment:
            account_bank_payment = "-------------------------"
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
                account_type_fee=account_type.zfill(2),
                debit_branch_code_fee=branch_code.zfill(4),
            )
        )
        return text

    def _get_text_credit_detail_scb(
        self, idx, pe_line, line_batch_amount, wht_cert, invoices
    ):
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
            "{pickup_location}{wht_header}{invoice_number}{wht_header2}"
            "{receiver_bank_code}{receiver_bank_name}{receiver_branch_code}"
            "{receiver_branch_name}{wht_signatory}{notification}{customer_ref}"
            "{cheque_ref}{payment_type_code}{service_type}{remark}{charge}\r\n".format(
                idx=str(idx).zfill(6),
                credit_account=receiver_acc_number.ljust(25),
                credit_amount=line_batch_amount,
                internal_ref=self._get_reference().ljust(8),
                wht_present=self.scb_is_wht_present,
                invoice_detail_present=self.scb_is_invoice_present,
                credit_advice_required=self.scb_is_credit_advice,
                delivery_mode=self.scb_delivery_mode,
                pickup_location=(self.scb_pickup_location or "").ljust(4),
                wht_header=self._get_wht_header(wht_cert),  # WHT Form Type - Total WHT
                invoice_number=self._get_invoice_header(invoices),
                wht_header2=self._get_wht_header2(wht_cert),  # Pay Type - Deduct Date
                receiver_bank_code=receiver_bank_code,
                receiver_bank_name=pe_line.payment_partner_bank_id.bank_id.name,
                receiver_branch_code="".zfill(4),  # TODO
                receiver_branch_name="".ljust(35),  # TODO
                wht_signatory=self.scb_wht_signatory,
                notification=self.scb_beneficiary_noti,
                customer_ref="".ljust(20),  # TODO
                cheque_ref=self.scb_cheque_ref or "".ljust(1),
                payment_type_code=self.scb_payment_type_code or "".ljust(3),
                service_type=self._get_service_type() or "".ljust(2),
                remark="".ljust(68),  # NOTE: use in cheque
                charge="B" if self.scb_beneficiary_charge else "C",
            )
        )
        return text

    def _get_text_payee_detail_scb(self, idx, pe_line, line_batch_amount, wht_cert):
        receiver_name = pe_line._get_receiver_information()[0]
        receiver_address1 = " ".join(
            [
                pe_line.payment_partner_id.street,
            ]
        )
        receiver_address2 = " ".join(
            [
                pe_line.payment_partner_id.street2 or "",
                pe_line.payment_partner_id.city or "",
                pe_line.payment_partner_id.zip or "",
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
                payee_tax_id="".ljust(10),  # TODO
                payee_name_eng=self._get_payee_name_eng(pe_line).ljust(70),
                payee_fax=self._get_payee_fax().zfill(10),
                payee_sms=self._get_payee_sms().zfill(10),
                payee_email=self._get_payee_email().ljust(64),
                # TODO
                space="".ljust(310),
            )
        )
        return text

    def _get_text_wht_detail_scb(self, idx, sequence_wht, wht_line):
        wht_amount = self._get_amount_no_decimal(wht_line.amount)
        wht_base_amount = self._get_amount_no_decimal(wht_line.base)
        wht_income_type = self._get_wht_income_type(wht_line)
        text = (
            "005{internal_ref}{idx}{wht_sequence}{wht_amount}"
            "{wht_income_type}{wht_income_description}{wht_deduct_rate}"
            "{wht_base_amount}\r\n".format(
                internal_ref=self._get_reference().ljust(8),
                idx=str(idx).zfill(6),
                wht_sequence=str(sequence_wht).zfill(2),
                wht_amount=wht_amount,
                wht_income_type=wht_income_type.ljust(5),
                wht_income_description=wht_line.wht_cert_income_desc.ljust(80),
                wht_deduct_rate=str(abs(int(wht_line.wht_percent))).zfill(2),
                wht_base_amount=wht_base_amount,
            )
        )
        return text

    def _get_text_invoice_detail_scb(self, idx, sequence_inv, inv):
        inv_amount_untaxed = self._get_amount_no_decimal(inv.amount_untaxed)
        inv_amount_tax = self._get_amount_no_decimal(inv.amount_tax)
        purchase = inv.invoice_line_ids.mapped("purchase_line_id.order_id")
        text = (
            "006{internal_ref}{idx}{inv_sequence}{inv_number}{inv_amount}"
            "{inv_date}{inv_description}{po_number}{vat_amount}{payee_chage_amount}"
            "{wht_amount}{language}\r\n".format(
                internal_ref=self._get_reference().ljust(8),
                idx=str(idx).zfill(6),
                inv_sequence=str(sequence_inv).zfill(6),
                inv_number=inv.name.ljust(15) if inv.name != "/" else ".".ljust(15),
                inv_amount=inv_amount_untaxed,
                inv_date=inv.invoice_date.strftime("%Y%m%d"),
                inv_description="".ljust(70),
                po_number=(purchase.name or "").ljust(15),
                vat_amount=inv_amount_tax,
                payee_chage_amount="0".zfill(16),
                wht_amount="0".zfill(16),  # TODO
                language=self.scb_invoice_language,
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
        # Check module install 'l10n_th_account_tax'
        wht = hasattr(self.env["account.payment"], "wht_cert_ids")
        # Details
        for idx, pe_line in enumerate(payment_lines):
            # This amount related decimal from invoice, Odoo invoice do not rounding.
            payment_net_amount = pe_line._get_payment_net_amount()
            line_batch_amount = pe_line._get_amount_no_decimal(payment_net_amount)
            wht_cert = (
                wht
                and pe_line.payment_id.wht_cert_ids.filtered(
                    lambda l: l.state == "done"
                )
                or False
            )
            invoices = pe_line.payment_id.reconciled_bill_ids
            text += self._get_text_credit_detail_scb(
                idx, pe_line, line_batch_amount, wht_cert, invoices
            )
            text += self._get_text_payee_detail_scb(
                idx, pe_line, line_batch_amount, wht_cert
            )
            # Print WHT from bank
            if self.scb_is_wht_present:
                # Get withholding tax from payment state done only
                for sequence_wht, wht_line in enumerate(wht_cert.wht_line):
                    text += self._get_text_wht_detail_scb(idx, sequence_wht, wht_line)
            # Print Invoices from bank
            if self.scb_is_invoice_present:
                for sequence_inv, inv in enumerate(invoices):
                    text += self._get_text_invoice_detail_scb(idx, sequence_inv, inv)
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

    @api.onchange("scb_delivery_mode")
    def onchange_scb_delivery_mode(self):
        if self.scb_delivery_mode == "S" and self.scb_product_code in [
            "MCP",
            "DDP",
            "CCP",
        ]:
            raise UserError(
                _(
                    "The product codes 'MCP', 'DDP', and 'CCP' are not allowed "
                    "to be used with the 'SCBBusinessNet' delivery mode."
                )
            )

    @api.onchange("scb_product_code")
    def onchange_scb_product_code(self):
        if self.scb_product_code not in ("MCP", "DDP", "CCP"):
            self.scb_cheque_ref = False
        if self.scb_product_code != "BNT":
            self.scb_payment_type_code = False
            self.scb_service_type_bahtnet = False
        if self.scb_product_code not in ("MCL", "PA4", "PA5", "PA6"):
            self.scb_service_type = False

    def _check_constraint_confirm(self):
        res = super()._check_constraint_confirm()
        for rec in self.filtered(lambda l: l.bank == "SICOTHBK"):
            rec.onchange_scb_delivery_mode()
        return res
