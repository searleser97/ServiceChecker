from mail.smtp import getStatusOfSMTPServer

mail_server = "192.168.1.69"

mail_latex_response = getStatusOfSMTPServer(mail_server)

print(mail_latex_response)