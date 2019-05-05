from mail.smtp import getStatusOfSMTPServer, getStatusOfSMTPServerMultipleclients

mail_server = "192.168.1.69"

print(getStatusOfSMTPServer(mail_server))
print(getStatusOfSMTPServerMultipleclients(mail_server))