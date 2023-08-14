# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields

from odoo.addons.l10n_th_bank_payment_export.tests.common import CommonBankPaymentExport


class TestBankPaymentExportSCB(CommonBankPaymentExport):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Search field default
        field_scb_company_id = cls.field_model.search(
            [("name", "=", "scb_company_id"), ("model", "=", "bank.payment.export")]
        )
        field_scb_product_code = cls.field_model.search(
            [("name", "=", "scb_product_code"), ("model", "=", "bank.payment.export")]
        )
        field_scb_service_type = cls.field_model.search(
            [("name", "=", "scb_service_type"), ("model", "=", "bank.payment.export")]
        )
        # setup template
        cls.template1 = cls.bank_payment_template_model.create(
            {
                "name": "Template SCB_MCL",
                "bank": "SICOTHBK",
                "template_config_line": [
                    (
                        0,
                        0,
                        {
                            "field_id": field_scb_company_id.id,
                            "value": "COMPANY01",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "field_id": field_scb_product_code.id,
                            "value": "MCL",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "field_id": field_scb_service_type.id,
                            "value": "04",
                        },
                    ),
                ],
            }
        )

    def test_01_bank_payment_template(self):
        """Test default bank payment template"""
        bank_payment = self.bank_payment_export_model.create(
            {
                "name": "/",
                "bank": "SICOTHBK",
                "template_id": self.template1.id,
            }
        )
        self.assertFalse(bank_payment.scb_company_id)
        self.assertFalse(bank_payment.scb_product_code)
        self.assertFalse(bank_payment.scb_service_type)
        # Add template in bank payment export, it should default
        bank_payment._onchange_template_id()
        self.assertEqual(bank_payment.scb_company_id, "COMPANY01")
        self.assertEqual(bank_payment.scb_product_code, "MCL")
        self.assertEqual(bank_payment.scb_service_type, "04")

    def test_02_scb_export(self):
        bank_payment = self.bank_payment_export_model.create(
            {
                "name": "/",
                "bank": "SICOTHBK",
                "effective_date": fields.Date.today(),
            }
        )
        bank_payment.action_get_all_payments()
        self.assertEqual(len(bank_payment.export_line_ids), 2)
        # Add recipient bank on line
        for line in bank_payment.export_line_ids:
            self.assertEqual(line.payment_id.export_status, "to_export")
            if line.payment_partner_id == self.partner_2:
                # check default recipient bank
                self.assertTrue(line.payment_partner_bank_id)
            else:
                line.payment_partner_bank_id = self.partner1_bank_bnp.id
        bank_payment.action_confirm()
        # Export Excel
        xlsx_data = self.action_bank_export_excel(bank_payment)
        self.assertEqual(xlsx_data[1], "xlsx")
        # Export Text File
        text_list = bank_payment.action_export_text_file()
        self.assertEqual(bank_payment.state, "done")
        self.assertEqual(text_list["report_type"], "qweb-text")
        text_word = bank_payment._export_bank_payment_text_file()
        self.assertNotEqual(
            text_word,
            "Demo Text File. You can inherit function "
            "_generate_bank_payment_text() for customize your format.",
        )
        self.assertEqual(bank_payment.state, "done")
