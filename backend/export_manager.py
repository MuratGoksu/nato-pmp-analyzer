"""
Export Manager for NATO PMP Analyzer
Handles PDF and Excel export functionality
"""

import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import plotly.graph_objects as go
import plotly.io as pio


class ExportManager:
    """Manages export functionality for reports and data"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))

    def export_to_excel(self, documents: list, filename: str = None) -> BytesIO:
        """
        Export project data to Excel file

        Args:
            documents: List of processed documents
            filename: Optional filename (default: NATO_PMP_Analysis_{timestamp}.xlsx)

        Returns:
            BytesIO object containing Excel file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"NATO_PMP_Analysis_{timestamp}.xlsx"

        # Create BytesIO buffer
        buffer = BytesIO()

        # Create Excel writer
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Sheet 1: Project Overview
            overview_data = []
            for doc in documents:
                if doc.get('success'):
                    metadata = doc.get('metadata', {})
                    overview_data.append({
                        'Project Name': metadata.get('project_name', 'N/A'),
                        'Status': metadata.get('status', 'GREEN'),
                        'Word Count': metadata.get('word_count', 0),
                        'Character Count': metadata.get('char_count', 0),
                        'Budget Found': ', '.join(metadata.get('budget', [])) if metadata.get('budget') else 'N/A',
                        'Stakeholders Count': len(metadata.get('stakeholders', [])),
                        'Dates Found': len(metadata.get('dates', [])),
                        'Processed At': doc.get('processed_at', 'N/A'),
                        'File Name': doc.get('file_name', 'N/A')
                    })

            if overview_data:
                df_overview = pd.DataFrame(overview_data)
                df_overview.to_excel(writer, sheet_name='Project Overview', index=False)

                # Format the worksheet
                workbook = writer.book
                worksheet = writer.sheets['Project Overview']

                # Add formats
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#1f77b4',
                    'font_color': 'white',
                    'border': 1
                })

                # Status color formats
                red_format = workbook.add_format({'bg_color': '#ffcccc'})
                amber_format = workbook.add_format({'bg_color': '#fff4cc'})
                green_format = workbook.add_format({'bg_color': '#ccffcc'})

                # Apply header format
                for col_num, value in enumerate(df_overview.columns.values):
                    worksheet.write(0, col_num, value, header_format)

                # Apply conditional formatting to Status column
                worksheet.conditional_format(1, 1, len(df_overview), 1, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'RED',
                    'format': red_format
                })
                worksheet.conditional_format(1, 1, len(df_overview), 1, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'AMBER',
                    'format': amber_format
                })
                worksheet.conditional_format(1, 1, len(df_overview), 1, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'GREEN',
                    'format': green_format
                })

                # Adjust column widths
                worksheet.set_column('A:A', 30)  # Project Name
                worksheet.set_column('B:B', 12)  # Status
                worksheet.set_column('C:D', 15)  # Word/Char Count
                worksheet.set_column('E:E', 20)  # Budget
                worksheet.set_column('F:H', 18)  # Stakeholders, Dates, Processed
                worksheet.set_column('I:I', 35)  # File Name

            # Sheet 2: Stakeholders
            stakeholder_data = []
            for doc in documents:
                if doc.get('success'):
                    metadata = doc.get('metadata', {})
                    project_name = metadata.get('project_name', doc.get('file_name', 'N/A'))
                    stakeholders = metadata.get('stakeholders', [])

                    for stakeholder in stakeholders:
                        stakeholder_data.append({
                            'Project': project_name,
                            'Stakeholder': stakeholder.strip('_'),
                            'Status': metadata.get('status', 'GREEN')
                        })

            if stakeholder_data:
                df_stakeholders = pd.DataFrame(stakeholder_data)
                df_stakeholders.to_excel(writer, sheet_name='Stakeholders', index=False)

                worksheet = writer.sheets['Stakeholders']
                for col_num, value in enumerate(df_stakeholders.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                worksheet.set_column('A:A', 35)
                worksheet.set_column('B:B', 40)
                worksheet.set_column('C:C', 12)

            # Sheet 3: Statistics Summary
            stats_data = {
                'Metric': [
                    'Total Projects',
                    'Projects at Risk (RED)',
                    'Projects with Warning (AMBER)',
                    'Healthy Projects (GREEN)',
                    'Total Stakeholders',
                    'Average Word Count',
                    'Projects with Budget Info'
                ],
                'Value': [
                    len([d for d in documents if d.get('success')]),
                    len([d for d in documents if d.get('success') and d.get('metadata', {}).get('status') == 'RED']),
                    len([d for d in documents if d.get('success') and d.get('metadata', {}).get('status') == 'AMBER']),
                    len([d for d in documents if d.get('success') and d.get('metadata', {}).get('status') == 'GREEN']),
                    sum(len(d.get('metadata', {}).get('stakeholders', [])) for d in documents if d.get('success')),
                    int(sum(d.get('metadata', {}).get('word_count', 0) for d in documents if d.get('success')) /
                        max(len([d for d in documents if d.get('success')]), 1)),
                    len([d for d in documents if d.get('success') and d.get('metadata', {}).get('budget')])
                ]
            }

            df_stats = pd.DataFrame(stats_data)
            df_stats.to_excel(writer, sheet_name='Summary Statistics', index=False)

            worksheet = writer.sheets['Summary Statistics']
            for col_num, value in enumerate(df_stats.columns.values):
                worksheet.write(0, col_num, value, header_format)
            worksheet.set_column('A:A', 35)
            worksheet.set_column('B:B', 15)

        buffer.seek(0)
        return buffer

    def export_to_pdf(self, documents: list, include_charts: bool = True) -> BytesIO:
        """
        Export analysis report to PDF

        Args:
            documents: List of processed documents
            include_charts: Whether to include visualizations

        Returns:
            BytesIO object containing PDF file
        """
        buffer = BytesIO()
        pdf_doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

        # Container for the 'Flowable' objects
        elements = []

        # Title
        title = Paragraph("NATO PMP Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Date
        date_text = Paragraph(
            f"<para align=center>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</para>",
            self.styles['Normal']
        )
        elements.append(date_text)
        elements.append(Spacer(1, 20))

        # Executive Summary
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))

        successful_docs = [d for d in documents if d.get('success')]
        red_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'RED'])
        amber_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'AMBER'])
        green_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'GREEN'])

        summary_text = f"""
        This report provides an analysis of {len(successful_docs)} Project Management Plan(s) processed
        through the NATO PMP Analyzer system. The analysis includes metadata extraction, stakeholder
        identification, and project health assessment.
        <br/><br/>
        <b>Key Findings:</b><br/>
        • Total Projects Analyzed: {len(successful_docs)}<br/>
        • Projects at Risk (RED): {red_count}<br/>
        • Projects with Warning (AMBER): {amber_count}<br/>
        • Healthy Projects (GREEN): {green_count}<br/>
        • Portfolio Health Score: {(green_count / max(len(successful_docs), 1) * 100):.1f}%
        """

        elements.append(Paragraph(summary_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))

        # Project Overview Table
        elements.append(Paragraph("Project Overview", self.styles['CustomHeading']))

        table_data = [['Project Name', 'Status', 'Words', 'Stakeholders']]

        for document in successful_docs:
            metadata = document.get('metadata', {})
            table_data.append([
                Paragraph(metadata.get('project_name', 'N/A')[:40], self.styles['Normal']),
                metadata.get('status', 'GREEN'),
                str(metadata.get('word_count', 0)),
                str(len(metadata.get('stakeholders', [])))
            ])

        # Create table
        table = Table(table_data, colWidths=[3*inch, 0.8*inch, 0.8*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(table)
        elements.append(PageBreak())

        # Detailed Project Information
        elements.append(Paragraph("Detailed Project Information", self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))

        for document in successful_docs:
            metadata = document.get('metadata', {})
            project_name = metadata.get('project_name', 'N/A')

            # Project header
            elements.append(Paragraph(f"<b>{project_name}</b>", self.styles['Heading3']))

            # Project details
            details = f"""
            <b>File:</b> {document.get('file_name', 'N/A')}<br/>
            <b>Status:</b> {metadata.get('status', 'GREEN')}<br/>
            <b>Word Count:</b> {metadata.get('word_count', 0):,}<br/>
            <b>Stakeholders:</b> {len(metadata.get('stakeholders', []))}<br/>
            <b>Budget Information:</b> {', '.join(metadata.get('budget', [])) if metadata.get('budget') else 'Not found'}<br/>
            <b>Dates Found:</b> {len(metadata.get('dates', []))}
            """

            elements.append(Paragraph(details, self.styles['Normal']))
            elements.append(Spacer(1, 16))

        # Build PDF
        pdf_doc.build(elements)
        buffer.seek(0)

        return buffer

    def create_summary_report_pdf(self, documents: list, analysis_results: dict = None) -> BytesIO:
        """
        Create a comprehensive summary report with AI insights

        Args:
            documents: List of processed documents
            analysis_results: Optional AI analysis results

        Returns:
            BytesIO object containing PDF file
        """
        buffer = BytesIO()
        pdf_doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

        elements = []

        # Title Page
        title = Paragraph("NATO PMP Portfolio Analysis<br/>Comprehensive Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 30))

        # Report metadata
        report_info = f"""
        <para align=center>
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M')}<br/>
        <b>Classification:</b> NATO UNCLASSIFIED<br/>
        <b>System:</b> NATO PMP Analyzer v0.5<br/>
        <b>Documents Analyzed:</b> {len([d for d in documents if d.get('success')])}
        </para>
        """
        elements.append(Paragraph(report_info, self.styles['Normal']))
        elements.append(PageBreak())

        # Table of Contents (simplified)
        elements.append(Paragraph("Table of Contents", self.styles['CustomHeading']))
        toc = """
        1. Executive Summary<br/>
        2. Portfolio Health Dashboard<br/>
        3. Risk Analysis<br/>
        4. Stakeholder Overview<br/>
        5. Project Details<br/>
        6. Recommendations
        """
        elements.append(Paragraph(toc, self.styles['Normal']))
        elements.append(PageBreak())

        # Add AI insights if provided
        if analysis_results:
            elements.append(Paragraph("AI-Generated Insights", self.styles['CustomHeading']))
            elements.append(Paragraph(analysis_results.get('insights', 'No insights available'),
                                    self.styles['Normal']))
            elements.append(Spacer(1, 20))

        # Recommendations section
        elements.append(Paragraph("Recommendations", self.styles['CustomHeading']))

        successful_docs = [d for d in documents if d.get('success')]
        red_projects = [d for d in successful_docs if d.get('metadata', {}).get('status') == 'RED']

        recommendations = f"""
        Based on the analysis of {len(successful_docs)} project(s), the following recommendations are provided:
        <br/><br/>
        """

        if red_projects:
            recommendations += f"""
            <b>1. Immediate Attention Required:</b><br/>
            {len(red_projects)} project(s) are marked as RED status and require immediate management attention
            to address critical risks and issues.
            <br/><br/>
            """

        recommendations += """
        <b>2. Portfolio Management:</b><br/>
        • Conduct regular status reviews for all projects<br/>
        • Ensure stakeholder engagement across all projects<br/>
        • Monitor budget allocations and expenditures<br/>
        • Facilitate knowledge sharing between related projects
        <br/><br/>
        <b>3. Risk Mitigation:</b><br/>
        • Develop mitigation plans for at-risk projects<br/>
        • Establish clear escalation procedures<br/>
        • Regular reporting to steering committee
        """

        elements.append(Paragraph(recommendations, self.styles['Normal']))

        # Build PDF
        pdf_doc.build(elements)
        buffer.seek(0)

        return buffer
