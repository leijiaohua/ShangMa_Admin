import smtplib  # smtplib这个模块是管发邮件
import email.mime.text
from email.mime.multipart import MIMEMultipart  # 发带附件的邮件用的
from common.openpyxl_xls import ReadData

r = ReadData()


class SendMail(object):

    def __init__(self, file=None):
        self.data = r.read_yaml('Email')

        self.username = self.data['username']
        self.passwd = self.data['passwd']
        self.recv = self.data['recv']
        self.title = self.data['title']
        self.content = self.data['content']
        self.file = file
        self.email_host = self.data['email_host']
        self.port = self.data['port']

    def send_mail(self):
        # 发送内容的对象
        msg = MIMEMultipart()

        # 处理附件
        if self.file:
            att = email.mime.text.MIMEText(open(self.file, encoding='utf-8').read())
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % self.file
            msg.attach(att)

        msg.attach(email.mime.text.MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = self.recv  # 接收者账号列表
        smtp = smtplib.SMTP(self.email_host, port=self.port)  # 发送邮件服务器的对象
        smtp.login(self.username, self.passwd)

        try:
            smtp.sendmail(self.username, self.recv, msg.as_string())
        except Exception as e:
            print('出错了。。', e)
        else:
            print('发送成功！')

        smtp.quit()