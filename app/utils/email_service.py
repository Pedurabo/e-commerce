"""
Email service utility for sending transactional emails.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.config import settings


class EmailService:
    """Email service for sending transactional emails."""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send an email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new users."""
        subject = "Welcome to Modern Ecommerce Platform!"
        html_content = f"""
        <html>
            <body>
                <h1>Welcome, {user_name}!</h1>
                <p>Thank you for joining our modern ecommerce platform.</p>
                <p>We're excited to provide you with:</p>
                <ul>
                    <li>AI-powered product recommendations</li>
                    <li>Modern payment methods including cryptocurrency</li>
                    <li>Seamless shopping experience</li>
                </ul>
                <p>Start exploring our products today!</p>
            </body>
        </html>
        """
        
        return await self.send_email(user_email, subject, html_content)
    
    async def send_order_confirmation(
        self,
        user_email: str,
        order_number: str,
        order_total: float,
        items: List[dict]
    ) -> bool:
        """Send order confirmation email."""
        subject = f"Order Confirmation - {order_number}"
        
        items_html = ""
        for item in items:
            items_html += f"<li>{item['name']} - ${item['price']} x {item['quantity']}</li>"
        
        html_content = f"""
        <html>
            <body>
                <h1>Order Confirmation</h1>
                <p>Thank you for your order!</p>
                <p><strong>Order Number:</strong> {order_number}</p>
                <p><strong>Total:</strong> ${order_total:.2f}</p>
                
                <h2>Order Items:</h2>
                <ul>{items_html}</ul>
                
                <p>We'll send you tracking information once your order ships.</p>
            </body>
        </html>
        """
        
        return await self.send_email(user_email, subject, html_content)
    
    async def send_password_reset(
        self,
        user_email: str,
        reset_token: str,
        reset_url: str
    ) -> bool:
        """Send password reset email."""
        subject = "Password Reset Request"
        html_content = f"""
        <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>You requested a password reset for your account.</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}?token={reset_token}">Reset Password</a></p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>This link will expire in 1 hour.</p>
            </body>
        </html>
        """
        
        return await self.send_email(user_email, subject, html_content)


# Global email service instance
email_service = EmailService() 