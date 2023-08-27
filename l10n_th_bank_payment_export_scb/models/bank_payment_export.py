# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base.models.res_bank import sanitize_account_number


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
            ("1", "1 - Next Day"),
            ("2", "2 - Same Day Afternoon"),
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
            ("M", "M - Send by Registered mail"),
            ("C", "C - Send by messenger to Customer"),
            ("P", "P - Receiving pickup at SCB branch"),
            ("S", "S - Send back to SCBBusinessNet"),
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
    scb_pickup_location_cheque = fields.Selection(
        selection=[
            ("C002", "C002 - Ratchayothin (CAREER@SCB)-RCP"),
            ("C003", "C003 - Mab Ta Pud Industrial Estate br.0644"),
            ("C004", "C004 - By Return - รับเช็คที่บริษัท"),
            ("C005", "C005 - Phuket br.0537"),
            ("C006", "C006 - Asok br.0032"),
            ("C007", "C007 - Chachoengsao br.0516"),
            ("C008", "C008 - Phra Ram IV (Sirinrat Building) br.0096"),
            ("C009", "C009 - Thanon Cherd Wutthakat (Don Muang) br.0105"),
            ("C010", "C010 - Laem Chabang br.0807 LAEM CHABANG INDUSTRIAL ESTATE SUB"),
            ("C011", "C011 - By Mailing -ส่งทางไปรษณีย์"),
            ("C012", "C012 - ลาดกระบัง"),
            ("0111", "0111 - Ratchayothin West A"),
            ("5190", "5190 - Energy Complex"),
            ("5453", "5453 - G Tower"),
            ("0870", "0870 - Amata City (Rayong) Sub Br."),
            ("0101", "0101 - Thanon Sathon"),
            ("0527", "0527 - Sri Racha"),
        ],
        ondelete={
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
            "0111": "cascade",
            "5190": "cascade",
            "5453": "cascade",
            "0870": "cascade",
            "0101": "cascade",
            "0527": "cascade",
        },
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
    scb_invoice_language = fields.Selection(
        selection=[("T", "T - Thai"), ("E", "E - English")],
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
        selection=[("B", "B - Bank"), ("C", "C - Corporate")],
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
            ("1", "1 - ใบเสร็จรับเงิน"),
            ("2", "2 - ใบวางบิล"),
            ("3", "3 - ใบเสร็จรับเงินและใบวางบิล"),
            ("4", "4 - ใบเสร็จรับเงินและใบกำกับภาษี"),
            ("5", "5 - ใบวางบิลและใบเสร็จรับเงินและใบกำกับภาษี"),
            ("6", "6 - สำเนาบัตรประชาชน/หนังสือเดินทาง"),
            ("7", "7 - สำเนาบัตรประชาชน/หนังสือเดินทาง + ใบนัดรับของรางวัล"),
            ("8", "8 - สำเนาบัตรประชาชน/หนังสือเดินทาง + ใบสั่งจ้าง"),
            ("9", "9 - สำเนาใบเสร็จรับเงิน"),
            ("A", "A - เงินในเช็คใบเสร็จไม่เท่ากัน - จ่าย"),
            ("B", "B - หนังสือรับรองการหักภาษีณ.ที่จ่าย."),
            ("C", "C - หนังสือกรมศุลกากร"),
            ("D", "D - ใบกำกับภาษี"),
            (
                "E",
                "E - หนังสือมอบพร้อมติดอากรแสตมป์ 10 บาท + สำเนาบัตร ปชช.ผู้มอบพร้อมลงนาม "
                "+ สำเนาบัตร ปชช.ผู้รับมอบพร้อมลงนาม",
            ),
            (
                "F",
                "F - หนังสือมอบจากคณะบุคคลพร้อมติดอากรแสตมป์ 10 บาท + "
                "สำเนาสัญญาจัดตั้งคณะบุคคลพร้อมลงนาม + "
                "สำเนาบัตรผู้เสียภาษีของคณะบุคคลพร้อมลงนาม + "
                "สำเนาบัตร ปชช.ผู้มอบ และผู้รับมอบ พร้อมลงนาม",
            ),
            ("G", "G - เอกสารยืนยันการโอนเงิน/ออกเช็คผ่านโทรสาร"),
            ("H", "H - อื่น ๆ"),
            ("I", "I - สัญญาประนีประนอม"),
            ("J", "J - ใบเสร็จ/ใบกำกับภาษี + ใบรับรถ"),
            ("K", "K - หนังสือมอบ + บัตร ปชช.ผู้รับมอบ"),
            ("L", "L - บัตร ปชช.ผู้มอบ + บัตร ปชช.ผู้รับมอบ"),
            ("M", "M - ใบรับรถ + เซ็นชื่อใบรับเงิน/สัญญา"),
            ("N", "N - ใบรถ + น.มอบ + ผู้รับมอบ + เซ็นชื่อ/สัญญา"),
            ("O", "O - ใบรับเช็ค"),
            ("P", "P - ใบลดหนี้"),
            ("Q", "Q - ใบเพิ่มหนี้"),
            ("R", "R - ดูช่อง Invoice Description ใน Advice"),
            ("S", "S - ขายลดเช็คทันที"),
            ("T", "T - Email + สำเนาบัตรพนง. + สำเนาบัตรปปช."),
            ("U", "U - ค่าสาธารณูปโภค"),
            ("V", "V - ใบเสร็จรับเงินและ หนังสือรับรองหักภาษี ณ ที่จ่าย"),
            ("W", "W - ใบเสร็จรับเงิน หรือบัตรประชาชน"),
            ("X", "X - ไม่ใช้เอกสารใด ๆ"),
            ("Y", "Y - ใบวางบิลและใบเสร็จรับเงิน (จำนวนเงินไม่ตรง-จ่าย)"),
            ("Z", "Z - ใบวางบิลและสำเนาบัตรประชาชน"),
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
    scb_remark = fields.Char(size=50)
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

    def _get_payee_name_eng(self, pe_line, receiver_name=""):
        if self.scb_product_code == "BNT":
            receiver_name = (
                pe_line.payment_partner_bank_id.acc_holder_name_en
                or "**Not found account holder en**"
            )
            return receiver_name
        return receiver_name

    def _get_wht_income_type(self, wht_line):
        wht_income_type = wht_line.wht_cert_income_type.lower()
        if len(wht_income_type) == 4:
            wht_income_type = "{}.{}".format(wht_income_type[:3], wht_income_type[3:])
        return wht_income_type

    def _get_wht_header(self, wht_cert):
        wht_type = "00"
        if not (wht_cert and self.scb_is_wht_present):
            return "{wht_type}{filter}{filter_number}".format(
                wht_type=wht_type,
                filter="".ljust(14),
                filter_number="0".zfill(24),
            )
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
        if not (wht_cert and self.scb_is_wht_present):
            return "0{}".format("".ljust(48))
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
            return "0".zfill(22)
        invoice_total_amount = self._get_amount_no_decimal(
            sum(invoices.mapped("amount_total"))
        )
        text = "{invoice_count}{invoice_total_amount}".format(
            invoice_count=str(len(invoices)).zfill(6),
            invoice_total_amount=invoice_total_amount,
        )
        return text

    def _get_pickup_location(self):
        pickup = ""
        if self.scb_delivery_mode == "C":
            if self.scb_product_code not in ("MCP", "DDP", "CCP"):
                pickup = self.scb_pickup_location
            else:
                pickup = self.scb_pickup_location_cheque
        return pickup.ljust(4)

    def _get_scb_bank_name(self, pe_line):
        # NOTE: Not support thai language
        return pe_line.payment_partner_bank_id.bank_id.name[:35].ljust(35)

    def _get_service_type(self):
        if self.scb_product_code == "BNT":
            return self.scb_service_type_bahtnet
        return self.scb_service_type

    def _get_address(self, pe_line):
        if self.scb_product_code == "BNT":
            receiver_address = (
                pe_line.payment_partner_id.street3 or "**street3 is not data**"
            )
        else:
            receiver_address = " ".join(
                [
                    pe_line.payment_partner_id.street,
                    pe_line.payment_partner_id.street2 or "",
                    pe_line.payment_partner_id.city or "",
                    pe_line.payment_partner_id.zip or "",
                ]
            )

        def split_thai_string(input_string, max_length):
            words = input_string.split()
            result = []
            current_line = ""

            for word in words:
                if len(current_line + word) > max_length:
                    result.append(current_line.strip())
                    current_line = ""

                current_line += word + " "

            if current_line.strip():
                result.append(current_line.strip())

            return result

        def pad_lines(lines, desired_length):
            padded_lines = [line.ljust(desired_length) for line in lines]
            return padded_lines

        def ensure_three_lines(lines, desired_length):
            while len(lines) < 3:
                lines.append("".ljust(desired_length))

        result = split_thai_string(receiver_address, 70)
        padded_result = pad_lines(result, 70)
        ensure_three_lines(padded_result, 70)

        return "".join(padded_result)

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
        sanitize_account_bank_payment = sanitize_account_number(account_bank_payment)
        if not sanitize_account_bank_payment:
            sanitize_account_bank_payment = "-------------------------"
        account_type = "0{}".format(sanitize_account_bank_payment[3])
        branch_code = "0{}".format(sanitize_account_bank_payment[0:3])
        text = (
            "002{product_code}{value_date}{debit_account_no}{account_type_debit_account}"
            "{debit_branch_code}THB{debit_amount}{internal_ref}{no_credit}{fee_debit_account}"
            "{filler}{mcl_type}{account_type_fee}{debit_branch_code_fee}\r\n".format(
                product_code=self.scb_product_code,
                value_date=self.effective_date.strftime("%Y%m%d"),
                debit_account_no=sanitize_account_bank_payment.ljust(25),
                account_type_debit_account=account_type,
                debit_branch_code=branch_code,
                debit_amount=total_batch_amount,
                internal_ref=self._get_reference().ljust(8),
                no_credit=str(self._get_line_count()).zfill(6),
                fee_debit_account=sanitize_account_bank_payment.ljust(15),
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
        if self.scb_product_code in ["MCP", "DDP"]:
            receiver_branch_code = "0111"
        text = (
            "003{idx}{credit_account}{credit_amount}THB{internal_ref}{wht_present}"
            "{invoice_detail_present}{credit_advice_required}{delivery_mode}"
            "{pickup_location}{wht_header}{invoice_number}{wht_header2}"
            "{receiver_bank_code}{receiver_bank_name}{receiver_branch_code}"
            "{receiver_branch_name}{wht_signatory}{notification}{customer_ref}"
            "{cheque_ref}{payment_type_code}{service_type}{remark}"
            "{scb_remark}{charge}\r\n".format(
                idx=str(idx).zfill(6),
                credit_account=receiver_acc_number.ljust(25),
                credit_amount=line_batch_amount,
                internal_ref=self._get_reference().ljust(8),
                wht_present="Y" if self.scb_is_wht_present else "N",
                invoice_detail_present="Y" if self.scb_is_invoice_present else "N",
                credit_advice_required="Y" if self.scb_is_credit_advice else "N",
                delivery_mode=self.scb_delivery_mode,
                pickup_location=self._get_pickup_location(),
                wht_header=self._get_wht_header(wht_cert),  # WHT Form Type - Total WHT
                invoice_number=self._get_invoice_header(invoices),
                wht_header2=self._get_wht_header2(wht_cert),  # Pay Type - Deduct Date
                receiver_bank_code=receiver_bank_code,
                receiver_bank_name=self._get_scb_bank_name(pe_line),
                receiver_branch_code=receiver_branch_code,
                receiver_branch_name=(receiver_branch_code or "").ljust(35),
                wht_signatory=self.scb_wht_signatory,
                notification=pe_line.scb_beneficiary_noti,
                customer_ref=pe_line.payment_id.name.ljust(20),
                cheque_ref=self.scb_cheque_ref or "".ljust(1),
                payment_type_code=self.scb_payment_type_code or "".ljust(3),
                service_type=self._get_service_type() or "".ljust(2),
                remark=(self.scb_remark or "").ljust(50),
                scb_remark="".ljust(18),
                charge="B" if pe_line.scb_beneficiary_charge else " ",
            )
        )
        return text

    def _get_text_payee_detail_scb(self, idx, pe_line, line_batch_amount):
        receiver_name = pe_line._get_receiver_information()[0]
        address = self._get_address(pe_line)
        text = (
            "004{internal_ref}{idx}{payee_idcard}{payee_name}"
            "{payee_address}{payee_tax_id}{payee_name_eng}{payee_fax}{payee_sms}"
            "{payee_email}{space}\r\n".format(
                internal_ref=self._get_reference().ljust(8),
                idx=str(idx).zfill(6),
                payee_idcard=str(pe_line.payment_partner_id.vat).zfill(15),
                payee_name=receiver_name.ljust(100),
                payee_address=address,
                payee_tax_id="".ljust(10),  # TODO
                payee_name_eng=self._get_payee_name_eng(pe_line).ljust(70),
                payee_fax=pe_line._get_payee_fax().zfill(10),
                payee_sms=pe_line._get_payee_sms().zfill(10),
                payee_email=pe_line._get_payee_email().ljust(64),
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
            idx += 1
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
            text += self._get_text_payee_detail_scb(idx, pe_line, line_batch_amount)
            # Print WHT from bank
            if self.scb_is_wht_present and wht_cert:
                # Get withholding tax from payment state done only
                for sequence_wht, wht_line in enumerate(wht_cert.wht_line):
                    sequence_wht += 1
                    text += self._get_text_wht_detail_scb(idx, sequence_wht, wht_line)
            # Print Invoices from bank
            if self.scb_is_invoice_present:
                for sequence_inv, inv in enumerate(invoices):
                    sequence_inv += 1
                    text += self._get_text_invoice_detail_scb(idx, sequence_inv, inv)
        text += self._get_text_footer_scb(payment_lines, total_batch_amount)
        return text

    def _generate_bank_payment_text(self):
        self.ensure_one()
        if self.bank == "SICOTHBK":  # SCB
            return self._format_scb_text()
        return super()._generate_bank_payment_text()

    def _get_view_report_text(self):
        """NOTE: This function can used demo. May be we delete it later"""
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
            self.scb_delivery_mode = False
        if self.scb_product_code != "BNT":
            self.scb_payment_type_code = False
            self.scb_service_type_bahtnet = False
        if self.scb_product_code not in ("MCL", "PA4", "PA5", "PA6"):
            self.scb_service_type = False

    @api.onchange(
        "scb_is_invoice_present", "scb_is_wht_present", "scb_is_credit_advice"
    )
    def onchange_scb_present(self):
        if self.scb_product_code not in ("MCP", "DDP", "CCP") and not (
            self.scb_is_invoice_present
            or self.scb_is_wht_present
            or self.scb_is_credit_advice
        ):
            self.scb_delivery_mode = False

    def _check_constraint_confirm(self):
        res = super()._check_constraint_confirm()
        for rec in self.filtered(lambda l: l.bank == "SICOTHBK"):
            rec.onchange_scb_delivery_mode()
            if rec.scb_product_code in ["MCP", "CCP", "DDP", "PAY", "DCP"] and any(
                line.payment_bank_id.bank_code != "014" for line in rec.export_line_ids
            ):
                raise UserError(
                    _(
                        "'MCP', 'CCP', 'DDP' 'PAY' and 'DCP' codes must only be "
                        "received with SCB bank."
                    )
                )
            if rec.scb_product_code == "DCP" and any(
                len(sanitize_account_number(line.payment_partner_bank_id.acc_number))
                != 10
                for line in rec.export_line_ids
            ):
                raise UserError(_("Account Number must only be 10 digits."))
        return res
