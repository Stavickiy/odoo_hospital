from odoo import models, fields, api

class DiseaseReportLine(models.TransientModel):
    _name = 'hospital_management.disease.report.line'
    _description = 'Disease Report Line'

    disease_id = fields.Many2one('hospital_management.disease.directory', string="Хвороба")
    diagnosis_count = fields.Integer(string="Кількість діагнозів")
    wizard_id = fields.Many2one('hospital_management.disease.report.wizard', string="Wizard")

class DiseaseReportWizard(models.TransientModel):
    _name = 'hospital_management.disease.report.wizard'
    _description = 'Wizard to generate disease report'

    year = fields.Selection(
        [(str(num), str(num)) for num in range((fields.Date.today().year), 2000, - 1)],
        default=str(fields.Date.today().year),
        string='Year', required=True)
    month = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
         ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
         ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        default=str(fields.Date.today().month),
        string='Month', required=True)

    report_lines_ids = fields.One2many('hospital_management.disease.report.line', 'wizard_id', string="Report Lines", store=True)

    def action_generate_report(self):
        # Удаляем предыдущие данные
        self.env['hospital_management.disease.report.line'].search([]).unlink()

        # Получаем диагнозы за выбранный месяц и год
        domain = [
            ('date_diagnosis', '>=', f'{self.year}-{self.month}-01'),
            ('date_diagnosis', '<', f'{self.year}-{int(self.month) + 1}-01')
        ]
        diagnoses = self.env['hospital_management.diagnosis'].search(domain)

        # Группируем диагнозы по болезням
        report_data = {}
        for diagnosis in diagnoses:
            disease = diagnosis.disease_id
            if disease not in report_data:
                report_data[disease] = 0
            report_data[disease] += 1

        # Создаем записи в временной модели
        report_lines = []
        for disease, count in report_data.items():
            report_lines.append((0, 0, {
                'disease_id': disease.id,
                'diagnosis_count': count
            }))

        self.write({'report_lines_ids': report_lines})

        # Открываем отчет на экране
        return self.env.ref('hospital_management.report_disease_report_pdf').report_action(self)
