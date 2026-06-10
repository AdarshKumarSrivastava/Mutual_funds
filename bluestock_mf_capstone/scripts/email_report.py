import sqlite3
import pandas as pd
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Setup Path
db_path = Path(__file__).resolve().parent.parent / "data" / "db" / "bluestock_mf.db"

def generate_html_report():
    conn = sqlite3.connect(str(db_path))
    # Top 5 funds by 1yr return
    top_5 = pd.read_sql_query("SELECT scheme_name, category, return_1yr_pct FROM scheme_performance ORDER BY return_1yr_pct DESC LIMIT 5", conn)
    conn.close()
    
    html = f"""
    <html>
      <head></head>
      <body>
        <h2>Bluestock Weekly Mutual Fund Performance Report</h2>
        <p>Report Date: {datetime.now().strftime('%Y-%m-%d')}</p>
        <h3>Top 5 Performing Funds (1-Year Return)</h3>
        {top_5.to_html(index=False, border=1)}
        <p>Please check the full dashboard for more detailed insights.</p>
        <p>Regards,<br>Bluestock MF Capstone Bot</p>
      </body>
    </html>
    """
    return html

def send_email():
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient@gmail.com"
    password = "your_app_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Bluestock MF Weekly Report - {datetime.now().strftime('%Y-%m-%d')}"
    message["From"] = sender_email
    message["To"] = receiver_email

    html_content = generate_html_report()
    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        # Create secure connection with server and send email
        # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # server.login(sender_email, password)
        # server.sendmail(sender_email, receiver_email, message.as_string())
        # server.quit()
        print("HTML Email successfully generated! (Sending disabled locally without valid credentials)")
        print(html_content)
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_email()
