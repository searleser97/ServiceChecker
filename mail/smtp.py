import imaplib, pprint, email, email.parser, time, timeit, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

numer_of_test = 0
mail_user = "losmegas"
mail_pass = "pepechido2"
local_mail = mail_user + "@localhost.pepe"

general_status = None
general_message = None

messages = {
    200 : "(nonstandard success response, see rfc876)",
    211 : "System status, or system help reply",
    214 : "Help message",
    220 : "<domain> Service ready",
    221 : "<domain> Service closing transmission channel",
    250 : "Requested mail action okay, completed",
    251 : "User not local; will forward to <forward-path>",
    252 : "Cannot VRFY user, but will accept message and attempt delivery",
    354 : "Start mail input; end with <CRLF>.<CRLF>",
    421 : "<domain> Service not available, closing transmission channel",
    450 : "Requested mail action not taken: mailbox unavailable",
    451 : "Requested action aborted: local error in processing",
    452 : "Requested action not taken: insufficient system storage",
    500 : "Syntax error, command unrecognised",
    501 : "Syntax error in parameters or arguments",
    502 : "Command not implemented",
    503 : "Bad sequence of commands",
    504 : "Command parameter not implemented",
    521 : "<domain> does not accept mail (see rfc1846)",
    530 : "Access denied ",
    550 : "Requested action not taken: mailbox unavailable",
    551 : "User not local; please try <forward-path>",
    552 : "Requested mail action aborted: exceeded storage allocation",
    553 : "Requested action not taken: mailbox name not allowed",
    554 : "Transaction failed"
}

def getStatusOfSMTPServer(ip):
    return getStatusOfSMTPServerRequest(ip, False)

def getStatusOfSMTPServerMultipleclients(ip):
    start = time.time()
    threads = [threading.Thread(target=getStatusOfSMTPServerRequest, args=(ip, True)) for _ in range(20)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    smtp_response = round(time.time() - start, 2)
    return (" \\begin{itemize}" +
                " \\item status: " + str(general_status) +
                " \\item interpretacion: " + general_message +
                " \\item time response of 20 clients " + str(smtp_response) + " s"
                " \\end{itemize}")

def getStatusOfSMTPServerRequest(ip, isThread):
    global general_status, general_message

    smtp_b_time = time.time()
    try:
        smtp = SMTP(ip, timeout=6)
        status = smtp.noop()[0]
        message = messages[status]
        sendEmail(smtp)
        smtp_e_time = time.time()
        imap_time = imapResponse(ip)
    except:
        status = "-"
        message = "Failed to connect"
        smtp_e_time = time.time()
        imap_time = 0

    general_status = status
    general_message = message
    smtp_response = round(smtp_e_time - smtp_b_time, 2)
    imap_response = round(imap_time,2)
    total_response = round(smtp_response + imap_response, 2)

    if not isThread:
        return (" \\begin{itemize}" +
                " \\item status: " + str(status) +
                " \\item interpretacion: " + message +
                " \\item time response of SMTP server: " + str(smtp_response) + " s"
                " \\item time response of IMAP server: " + str(imap_response) + " s"
                " \\item total response: " + str(total_response) + " s"
                " \\end{itemize}")

def imapResponse(ip):
    imap_host = ip
    imap_user = local_mail
    imap_pass = mail_pass

    imap_b_time = time.time()

    imap = imaplib.IMAP4(imap_host)
    imap.login(imap_user, imap_pass)
    imap.select('Inbox', readonly=True)
    type, data = imap.search(None, 'ALL')

    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email_id = id_list[-1]

    result, msg_data = imap.fetch(latest_email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_parser = email.parser.BytesFeedParser()
            email_parser.feed(response_part[1])
            msg = email_parser.close()
            last_subject = msg['subject']
    imap.close()
    imap_e_time = time.time()
    return imap_e_time - imap_b_time

def sendEmail(connection):
    global numer_of_test
    connection.login(local_mail, mail_pass)
    msg = MIMEMultipart()
    msg['From']= local_mail
    msg['To']= local_mail
    msg['Subject']= str(numer_of_test)
    numer_of_test += 1
    connection.send_message(msg)
