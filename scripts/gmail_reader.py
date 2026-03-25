#!/usr/bin/env python3
"""
Gmail Reader for Mission Control
Reads scott@adc3k.com inbox via IMAP
Requires GMAIL_APP_PASSWORD in .env
"""
import imaplib
import email
from email.header import decode_header
import os
import json
from datetime import datetime, timedelta

GMAIL_USER = "scott@adc3k.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

def connect():
    """Connect to Gmail IMAP"""
    if not GMAIL_APP_PASSWORD:
        print("ERROR: GMAIL_APP_PASSWORD not set in .env")
        print("Scott needs to create one at: https://myaccount.google.com/apppasswords")
        print("Then add to .env: GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
        return None

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    return mail

def get_recent_emails(hours=24, folder="INBOX", max_results=50):
    """Get emails from the last N hours"""
    mail = connect()
    if not mail:
        return []

    mail.select(folder)

    # Search for recent emails
    since_date = (datetime.now() - timedelta(hours=hours)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE "{since_date}")')

    if status != "OK":
        return []

    email_ids = messages[0].split()
    results = []

    for eid in email_ids[-max_results:]:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])

        subject = decode_header(msg["Subject"])[0]
        if isinstance(subject[0], bytes):
            subject = subject[0].decode(subject[1] or "utf-8")
        else:
            subject = subject[0]

        from_addr = msg["From"]
        date = msg["Date"]

        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        body = str(part.get_payload(decode=True))
                    break
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = str(msg.get_payload(decode=True))

        results.append({
            "subject": subject,
            "from": from_addr,
            "date": date,
            "body": body[:2000],  # Truncate long bodies
        })

    mail.logout()
    return results

def get_registrations(hours=24):
    """Get FormSubmit registration emails"""
    emails = get_recent_emails(hours=hours)
    registrations = [e for e in emails if "FormSubmit" in e.get("from", "") or "Registration" in e.get("subject", "")]
    return registrations

def get_nvidia_emails(hours=72):
    """Get emails from NVIDIA"""
    emails = get_recent_emails(hours=hours)
    nvidia = [e for e in emails if "nvidia" in e.get("from", "").lower()]
    return nvidia

def get_investor_emails(hours=72):
    """Get investor-related emails"""
    emails = get_recent_emails(hours=hours)
    investors = [e for e in emails if "investor" in e.get("subject", "").lower() or "alumni" in e.get("subject", "").lower()]
    return investors

def inbox_summary(hours=24):
    """Full inbox summary for Mission Control"""
    emails = get_recent_emails(hours=hours)

    summary = {
        "total": len(emails),
        "registrations": [],
        "nvidia": [],
        "investors": [],
        "other": [],
    }

    for e in emails:
        subj = e.get("subject", "").lower()
        frm = e.get("from", "").lower()

        if "formsubmit" in frm or "registration" in subj:
            summary["registrations"].append(e)
        elif "nvidia" in frm:
            summary["nvidia"].append(e)
        elif "investor" in subj or "alumni" in subj:
            summary["investors"].append(e)
        else:
            summary["other"].append(e)

    return summary

if __name__ == "__main__":
    print("=== MISSION CONTROL INBOX SUMMARY ===")
    print(f"Account: {GMAIL_USER}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    summary = inbox_summary(hours=24)

    print(f"Total emails (24h): {summary['total']}")
    print(f"Registrations: {len(summary['registrations'])}")
    print(f"NVIDIA: {len(summary['nvidia'])}")
    print(f"Investors: {len(summary['investors'])}")
    print(f"Other: {len(summary['other'])}")

    if summary["registrations"]:
        print("\n--- REGISTRATIONS ---")
        for r in summary["registrations"]:
            print(f"  {r['date']} | {r['subject']}")

    if summary["nvidia"]:
        print("\n--- NVIDIA ---")
        for n in summary["nvidia"]:
            print(f"  {n['date']} | {n['from']} | {n['subject']}")

    if summary["investors"]:
        print("\n--- INVESTORS ---")
        for i in summary["investors"]:
            print(f"  {i['date']} | {i['subject']}")
