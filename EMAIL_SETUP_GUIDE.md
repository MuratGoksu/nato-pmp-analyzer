# 📧 Email Notification Setup Guide

## Quick Configuration Options

### Option 1: Gmail (Most Common)

**Step 1: Get App Password**
1. Go to https://myaccount.google.com/apppasswords
2. Create password for "Mail" → "Other" → "NATO PMP"
3. Copy the 16-character password

**Step 2: Update .env file**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
FROM_EMAIL=yourname@gmail.com
```

---

### Option 2: Outlook / Office 365

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=yourname@outlook.com
SMTP_PASSWORD=your-password
FROM_EMAIL=yourname@outlook.com
```

---

### Option 3: Yahoo Mail

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=yourname@yahoo.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=yourname@yahoo.com
```

**Note:** Yahoo also requires app password. Generate at: https://login.yahoo.com/account/security

---

### Option 4: ProtonMail Bridge

```env
SMTP_SERVER=127.0.0.1
SMTP_PORT=1025
SMTP_USERNAME=yourname@protonmail.com
SMTP_PASSWORD=your-bridge-password
FROM_EMAIL=yourname@protonmail.com
```

**Note:** Requires ProtonMail Bridge installed locally

---

### Option 5: Custom SMTP Server

```env
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587
SMTP_USERNAME=yourname@yourcompany.com
SMTP_PASSWORD=your-password
FROM_EMAIL=yourname@yourcompany.com
```

---

### Option 6: Mailtrap (Testing Only - No Real Emails Sent)

**Perfect for testing without sending real emails!**

1. Sign up at https://mailtrap.io (Free)
2. Get your SMTP credentials from inbox settings

```env
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=your-mailtrap-username
SMTP_PASSWORD=your-mailtrap-password
FROM_EMAIL=test@nato-pmp.local
```

**Benefits:**
- ✅ No real emails sent
- ✅ View all emails in web interface
- ✅ Perfect for testing
- ✅ Free tier available

---

### Option 7: SendGrid (Production Ready)

**For production deployments**

1. Sign up at https://sendgrid.com
2. Create API key
3. Configure:

```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=yourname@yourdomain.com
```

---

## Testing Your Configuration

After updating `.env`:

1. **Restart the app**:
   ```bash
   # Kill running instance and restart
   streamlit run app.py
   ```

2. **Navigate to 📧 Notifications page**

3. **Send Test Email**:
   - Enter your email address
   - Click "Send Test Email"
   - Check for success message

4. **Check your inbox** (or Mailtrap inbox for testing)

---

## Troubleshooting

### Error: "Authentication failed"
- ✅ Double-check username and password
- ✅ For Gmail: Make sure you're using App Password, not regular password
- ✅ Check if 2FA is enabled (required for app passwords)

### Error: "Connection refused"
- ✅ Check SMTP_SERVER address
- ✅ Verify SMTP_PORT (usually 587 for TLS)
- ✅ Check firewall settings

### Error: "Recipient rejected"
- ✅ Verify FROM_EMAIL is valid
- ✅ Check recipient email addresses

### Gmail: "Less secure app access"
- ✅ Don't use this! Use App Passwords instead
- ✅ Enable 2FA first, then create App Password

---

## Recommended Setup for Different Use Cases

### For Development/Testing
→ **Use Mailtrap** (Option 6)
- Safe, no real emails
- Easy to verify
- Free

### For Personal Use
→ **Use Gmail** (Option 1)
- Easy setup
- Reliable
- Free

### For Organization/Production
→ **Use SendGrid** (Option 7) or corporate SMTP
- Professional
- Better deliverability
- Analytics

---

## Security Best Practices

1. **Never commit .env file to git**
   - Already in `.gitignore`
   - Contains sensitive credentials

2. **Use App Passwords**
   - Never use your main account password
   - Easier to revoke if compromised

3. **Rotate Passwords Regularly**
   - Change every 90 days
   - Revoke unused app passwords

4. **Limit Permissions**
   - Use dedicated email accounts for notifications
   - Don't use admin accounts

---

## Quick Start Commands

**Edit .env file:**
```bash
nano /Users/muratgoksu/Desktop/nato-pmp-analyzer/.env
```

**Test configuration:**
```bash
cd /Users/muratgoksu/Desktop/nato-pmp-analyzer
source venv/bin/activate
python3 -c "from backend.notification_manager import NotificationManager; nm = NotificationManager(); print('Configured!' if nm.is_configured() else 'Not configured')"
```

**Restart app:**
```bash
streamlit run app.py
```

---

## Example: Complete Gmail Setup

1. **Go to Google Account Security**
   - https://myaccount.google.com/security

2. **Enable 2-Step Verification**
   - Follow prompts to set up

3. **Generate App Password**
   - https://myaccount.google.com/apppasswords
   - App: Mail
   - Device: Other (custom name)
   - Copy password: e.g., `abcd efgh ijkl mnop`

4. **Edit .env**
   ```bash
   nano .env
   ```

5. **Add configuration** (remove spaces from app password):
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=john.doe@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop
   FROM_EMAIL=john.doe@gmail.com
   ```

6. **Save** (Ctrl+O, Enter, Ctrl+X)

7. **Restart app**

8. **Test** in Notifications page

---

## Support

If you encounter issues:
1. Check the error message in the app
2. Verify credentials in .env
3. Test SMTP connection manually
4. Check provider's SMTP documentation

**Common SMTP Ports:**
- 587: TLS (most common, recommended)
- 465: SSL (legacy)
- 25: Unencrypted (not recommended)

---

**Ready to configure? Choose your email provider above and follow the steps!**
