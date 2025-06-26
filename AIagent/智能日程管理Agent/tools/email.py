import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_email(to_email, subject, content):
    try:
        # 创建邮件对象
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header(EMAIL_USER)
        message['To'] = Header(to_email)
        message['Subject'] = Header(subject)
        
        # 连接SMTP服务器并发送
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server: #  使用SMTP服务器发送邮件
            server.starttls() #  启动TLS加密
            server.login(EMAIL_USER, EMAIL_PASSWORD) #  登录SMTP服务器
            server.sendmail(EMAIL_USER, [to_email], message.as_string()) #  发送邮件
        
        return f"📧 邮件已成功发送至 {to_email}"
    except Exception as e:
        return f"❌ 邮件发送失败: {str(e)}"

def email_tool(query):
    if query.startswith("发送邮件"):
        try:
            _, params = query.split("发送邮件", 1)
            to_email, subject, content = [p.strip() for p in params.split("|")]
            return send_email(to_email, subject, content)
        except Exception as e:
            return f"❌ 格式错误: {str(e)}。请使用'发送邮件 [收件人]|[主题]|[内容]'"
    else:
        return "❌ 不支持的命令。支持：发送邮件 [收件人]|[主题]|[内容]"