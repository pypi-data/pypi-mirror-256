#!/usr/bin/env python3
import win32com.client as win32


def create_outlook_message(body, subject, to, cc='', bcc='', attachments=[], auto_send=False):
    try:
        outlook = win32.GetActiveObject('Outlook.Application')
    except:
        outlook = win32.DispatchEx('Outlook.Application')

    message = outlook.CreateItem(0)
    message.To = to
    if cc:
        message.CC = cc
    if bcc:
        message.BCC = bcc
    message.Subject = subject
    message.Body = body
    message.Recipients.ResolveAll()

    if attachments:
        for a in attachments:
            message.Attachments.Add(a)

    if auto_send:
        message.Send()
    else:
        message.Display(False)


if __name__ == '__main__':
    pass