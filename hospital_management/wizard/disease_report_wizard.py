from odoo import models, fields, api


class DiseaseReportLine(models.TransientModel):
    """
    Line item for the disease report.
    This model holds the information about each disease and the number
    of diagnoses associated with it for a specific report.
    """

    _name = 'hospital_management.disease.report.line'
    _description = 'Disease Report Line'

    disease_id = fields.Many2one('hospital_management.disease.directory', string="Disease")
    diagnosis_count = fields.Integer(string="Diagnosis count")
    wizard_id = fields.Many2one('hospital_management.disease.report.wizard', string="Wizard")


class DiseaseReportWizard(models.TransientModel):
    """
    Wizard for generating a disease report.
    This wizard allows users to select a year and month, and then generates
    a report summarizing the number of diagnoses for each disease in that
    time period.
    """

    _name = 'hospital_management.disease.report.wizard'
    _description = 'Wizard to generate disease report'

    # Year selection for the report
    year = fields.Selection(
        [(str(num), str(num)) for num in range((fields.Date.today().year), 2000, -1)],
        default=str(fields.Date.today().year),
        string='Year', required=True)

    # Month selection for the report
    month = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
         ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
         ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        default=str(fields.Date.today().month),
        string='Month', required=True)

    # Lines of the report, linked to the wizard
    report_lines_ids = fields.One2many('hospital_management.disease.report.line', 'wizard_id', string="Report Lines",
                                       store=True)

    def action_generate_report(self):
        """
        Generate the disease report based on the selected year and month.
        This method removes any previous report line entries, retrieves
        diagnoses within the specified date range, groups them by disease,
        and creates corresponding report line entries. Finally, it opens
        the generated report.
        """
        self.env['hospital_management.disease.report.line'].search([]).unlink()

        domain = [
            ('date_diagnosis', '>=', f'{self.year}-{self.month}-01'),
            ('date_diagnosis', '<', f'{self.year}-{int(self.month) + 1}-01')
        ]
        diagnoses = self.env['hospital_management.diagnosis'].search(domain)

        report_data = {}
        for diagnosis in diagnoses:
            disease = diagnosis.disease_id
            if disease not in report_data:
                report_data[disease] = 0
            report_data[disease] += 1

        report_lines = []
        for disease, count in report_data.items():
            report_lines.append((0, 0, {
                'disease_id': disease.id,
                'diagnosis_count': count
            }))

        self.write({'report_lines_ids': report_lines})

        return self.env.ref('hospital_management.report_disease_report_pdf').report_action(self)
