import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import os


class EmailSender:
    """
    电子邮件发送类，用于发送包含各种字段的邮件
    """

    def __init__(self, smtp_user, smtp_password,smtp_server):
        """
        初始化邮件发送器

        参数:
        smtp_server (str): SMTP服务器地址
        smtp_port (int): SMTP服务器端口
        smtp_user (str): SMTP用户名
        smtp_password (str): SMTP密码
        use_tls (bool): 是否使用TLS加密，默认为True
        """
        self.smtp_server = smtp_server
        self.smtp_port = 25
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.use_tls = False

    @staticmethod
    def create_message(sender, recipients, cc=None, bcc=None, subject='', body='',
                       attachments=None, html_body=None):
        """
        创建邮件消息对象

        参数:
        sender (str): 发件人邮箱
        recipients (list): 收件人邮箱列表
        cc (list, optional): 抄送人邮箱列表
        bcc (list, optional): 密送人邮箱列表
        subject (str, optional): 邮件主题
        body (str, optional): 邮件正文(纯文本)
        attachments (list, optional): 附件路径列表
        html_body (str, optional): 邮件正文(HTML格式)

        返回:
        tuple: (邮件对象, 所有收件人列表)
        """
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = Header(subject, 'utf-8')

        # 添加抄送人
        if cc:
            msg['Cc'] = ', '.join(cc)
            all_recipients = recipients + cc
        else:
            all_recipients = recipients

        # 添加密送人
        if bcc:
            all_recipients += bcc

        # 添加正文(纯文本)
        if body:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 添加正文(HTML)
        if html_body:
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        # 添加附件
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                else:
                    print(f"附件文件不存在: {file_path}")

        return msg, all_recipients

    def send_email(self, sender, recipients, cc=None, bcc=None, subject='', body='',
                   attachments=None, html_body=None):
        """
        发送电子邮件

        参数:
        sender (str): 发件人邮箱
        recipients (list): 收件人邮箱列表
        cc (list, optional): 抄送人邮箱列表
        bcc (list, optional): 密送人邮箱列表
        subject (str, optional): 邮件主题
        body (str, optional): 邮件正文(纯文本)
        attachments (list, optional): 附件路径列表
        html_body (str, optional): 邮件正文(HTML格式)

        返回:
        bool: 发送成功返回True，失败返回False
        """
        # 创建邮件对象和获取所有收件人
        msg, all_recipients = self.create_message(
            sender, recipients, cc, bcc, subject, body, attachments, html_body
        )

        try:
            # 连接SMTP服务器
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()  # 启用TLS加密
            server.login(self.smtp_user, self.smtp_password)

            # 发送邮件
            server.sendmail(sender, all_recipients, msg.as_string())
            server.quit()
            print("邮件发送成功!")
            return True
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            return False
