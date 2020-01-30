"""Takes in recipients, a subject, an email body, and a file location 
and uses the COM object library implemented in python to call the outlook 
application and send an email.  

It's important to note that this COM object interaction is not meant for 
automating on an automation server, since COM objects rely upon a session id 
being 1 (meaning that a user is actually logged in), but if a task is scheduled 
through the task scheduler to run whether a user is logged in or not, the session 
id will be 0"""


import win32com.client as win32


EMAIL_RECIPIENTS = ""
EMAIL_SUBJECT = ""
EMAIL_BODY = ""
FILE_LOCATION = ""


def send_email(to, subject, body, attachment=None):
    """
    Sends an email using the COM interface in windows.  An optional
    attachment can be passed if needed.  This will most likely be a
    reference to a file location.

    It is important to note that if you are automating a task via task
    scheduler, and the task is set to run whether the user logs in or not,
    COM objects are not reliable because of the session variable not being
    set to 1.  Microsoft applications need to be run in 'live' environments.

    For more information, go here:
    https://support.microsoft.com/en-us/help/257757/considerations-for-server-side-automation-of-office

    :param to: recipients for the email; for multiple recipients pass in a semi-colon
    delimited string
    :param subject: subject heading
    :param body: email body, which can either be plaintext or html
    :param attachment: optional parameter that is a location of a file
    :return: None
    """
    outlook = win32.Dispatch('outlook.application')
    new_mail = outlook.CreateItem(0)
    new_mail.Subject = subject
    new_mail.HTMLBody = body
    new_mail.To = to

    if attachment:
        new_mail.Attachments.Add(attachment)

    new_mail.Send()


def main():
    send_email(
        EMAIL_RECIPIENTS,
        EMAIL_SUBJECT,
        EMAIL_BODY,
        attachment=FILE_LOCATION
    )


main()
