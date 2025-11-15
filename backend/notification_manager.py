"""
Notification Manager for NATO PMP Analyzer
Handles email notifications and alerts
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Dict
import os


class NotificationManager:
    """Manages email notifications for project alerts"""

    def __init__(self, smtp_server: str = None, smtp_port: int = None,
                 smtp_username: str = None, smtp_password: str = None):
        """
        Initialize notification manager

        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port (default: 587 for TLS)
            smtp_username: SMTP username
            smtp_password: SMTP password
        """
        # Get from environment variables if not provided
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = smtp_username or os.getenv('SMTP_USERNAME', '')
        self.smtp_password = smtp_password or os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)

    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return bool(self.smtp_username and self.smtp_password and self.smtp_server)

    def send_alert_notification(self, to_emails: List[str], projects: List[Dict],
                               alert_type: str = "RED") -> bool:
        """
        Send alert notification for at-risk projects

        Args:
            to_emails: List of recipient email addresses
            projects: List of project dictionaries with metadata
            alert_type: Type of alert (RED, AMBER, or CUSTOM)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.is_configured():
            raise ValueError("Email notifications not configured. Please set SMTP credentials.")

        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_emails)

        if alert_type == "RED":
            msg['Subject'] = f"🔴 NATO PMP Alert: {len(projects)} Critical Project(s) Require Attention"
            alert_emoji = "🔴"
            alert_color = "#dc3545"
        elif alert_type == "AMBER":
            msg['Subject'] = f"🟡 NATO PMP Alert: {len(projects)} Project(s) Need Review"
            alert_emoji = "🟡"
            alert_color = "#ffc107"
        else:
            msg['Subject'] = f"NATO PMP Notification: {len(projects)} Project Update(s)"
            alert_emoji = "📊"
            alert_color = "#1f77b4"

        # Create HTML body
        html = self._create_alert_html(projects, alert_type, alert_emoji, alert_color)

        # Attach HTML
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def _create_alert_html(self, projects: List[Dict], alert_type: str,
                          alert_emoji: str, alert_color: str) -> str:
        """Create HTML email body for alerts"""

        project_rows = ""
        for project in projects:
            metadata = project.get('metadata', {})
            project_name = metadata.get('project_name', 'Unknown')
            status = metadata.get('status', 'N/A')
            word_count = metadata.get('word_count', 0)
            stakeholders = len(metadata.get('stakeholders', []))

            project_rows += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{project_name}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{status}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{word_count:,}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{stakeholders}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

                <!-- Header -->
                <div style="text-align: center; padding-bottom: 20px; border-bottom: 3px solid {alert_color};">
                    <h1 style="color: {alert_color}; margin: 0;">
                        {alert_emoji} NATO PMP Alert
                    </h1>
                    <p style="color: #666; margin: 10px 0 0 0;">
                        Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}
                    </p>
                </div>

                <!-- Summary -->
                <div style="margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-left: 4px solid {alert_color};">
                    <h2 style="margin-top: 0; color: #333;">Alert Summary</h2>
                    <p style="font-size: 16px; line-height: 1.6; color: #555;">
                        <strong>{len(projects)}</strong> project(s) with <strong>{alert_type}</strong> status
                        require management attention. Please review the details below and take appropriate action.
                    </p>
                </div>

                <!-- Projects Table -->
                <div style="margin: 30px 0;">
                    <h2 style="color: #333;">Project Details</h2>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                        <thead>
                            <tr style="background-color: {alert_color}; color: white;">
                                <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">Project Name</th>
                                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Status</th>
                                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Words</th>
                                <th style="padding: 12px; border: 1px solid #ddd; text-align: center;">Stakeholders</th>
                            </tr>
                        </thead>
                        <tbody>
                            {project_rows}
                        </tbody>
                    </table>
                </div>

                <!-- Action Required -->
                <div style="margin: 30px 0; padding: 20px; background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 5px;">
                    <h3 style="margin-top: 0; color: #856404;">⚠️ Action Required</h3>
                    <ul style="color: #856404; line-height: 1.8;">
                        <li>Review project status and identify root causes</li>
                        <li>Engage with project managers and stakeholders</li>
                        <li>Develop mitigation plans for identified risks</li>
                        <li>Schedule follow-up reviews</li>
                    </ul>
                </div>

                <!-- Footer -->
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #999; font-size: 12px;">
                    <p>
                        This is an automated notification from the NATO PMP Analyzer system.<br/>
                        For questions or support, please contact your system administrator.
                    </p>
                    <p style="margin-top: 10px;">
                        🛡️ NATO PMP Analyzer v0.4 | Classification: NATO UNCLASSIFIED
                    </p>
                </div>

            </div>
        </body>
        </html>
        """

        return html

    def send_summary_report(self, to_emails: List[str], documents: List[Dict],
                           attachment: bytes = None, attachment_name: str = None) -> bool:
        """
        Send portfolio summary report

        Args:
            to_emails: List of recipient email addresses
            documents: List of all processed documents
            attachment: Optional PDF/Excel file as bytes
            attachment_name: Name for the attachment

        Returns:
            bool: True if sent successfully
        """
        if not self.is_configured():
            raise ValueError("Email notifications not configured.")

        # Calculate statistics
        successful_docs = [d for d in documents if d.get('success')]
        red_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'RED'])
        amber_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'AMBER'])
        green_count = len([d for d in successful_docs if d.get('metadata', {}).get('status') == 'GREEN'])

        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = f"NATO PMP Portfolio Report - {datetime.now().strftime('%B %d, %Y')}"

        # Create HTML body
        html = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #1f77b4;">📊 NATO PMP Portfolio Report</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>

            <h2>Executive Summary</h2>
            <table style="border-collapse: collapse; margin: 20px 0;">
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>Total Projects</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{len(successful_docs)}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>🟢 GREEN (Healthy)</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{green_count}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>🟡 AMBER (Warning)</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{amber_count}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd; background-color: #f8f9fa;"><strong>🔴 RED (Critical)</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{red_count}</td>
                </tr>
            </table>

            <p>Please see the attached report for detailed analysis.</p>

            <p style="color: #666; font-size: 12px; margin-top: 40px; border-top: 1px solid #ddd; padding-top: 20px;">
                🛡️ NATO PMP Analyzer | NATO UNCLASSIFIED
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        # Attach file if provided
        if attachment and attachment_name:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_name}')
            msg.attach(part)

        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_test_email(self, to_email: str) -> bool:
        """
        Send test email to verify configuration

        Args:
            to_email: Test recipient email address

        Returns:
            bool: True if sent successfully
        """
        if not self.is_configured():
            return False

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = "NATO PMP Analyzer - Test Email"

        html = """
        <html>
        <body>
            <h2>✅ Test Email Successful</h2>
            <p>This is a test email from the NATO PMP Analyzer notification system.</p>
            <p>If you received this, your email configuration is working correctly!</p>
            <p style="color: #666; font-size: 12px; margin-top: 20px;">
                🛡️ NATO PMP Analyzer v0.4
            </p>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending test email: {str(e)}")
            return False
