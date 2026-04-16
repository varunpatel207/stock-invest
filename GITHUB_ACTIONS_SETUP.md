# GitHub Actions Setup Guide

This guide will help you set up the daily portfolio crawler to run via GitHub Actions at 4:40 PM ET.

## Prerequisites

- GitHub account with this repository pushed
- Gmail account (or SMTP server)

## Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Setup GitHub Actions for daily portfolio crawler"
git push origin main
```

## Step 2: Add GitHub Secrets

The workflow needs your email credentials as secrets. GitHub Actions will use these instead of storing them in the code.

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

   - **GMAIL_USER**: Your Gmail address (e.g., xyz@email.com)
   - **GMAIL_PASSWORD**: Your Gmail app password (NOT your regular password)
   - **RECIPIENT_EMAIL**: Where to send the report (e.g., abc@example.com)

### Getting Gmail App Password

If using Gmail:

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already enabled)
3. Go back to Security and find "App passwords"
4. Select Mail and Windows Computer
5. Copy the generated 16-character password
6. Use this as `GMAIL_PASSWORD` secret

## Step 3: Verify Setup

1. Go to **Actions** tab in your GitHub repo
2. You should see "Daily Portfolio Crawler" workflow
3. The workflow runs automatically at **4:40 PM ET** every day

### Test Manually

To test before waiting for the scheduled time:

1. Go to **Actions** → **Daily Portfolio Crawler**
2. Click **Run workflow** → **Run workflow**

## Troubleshooting

**Workflow not running?**
- Check that the `.github/workflows/portfolio-crawler.yml` file is in your repository
- Verify secrets are set correctly in Settings → Secrets

**Email not sending?**
- Check GitHub Actions logs: Actions → Daily Portfolio Crawler → Latest run
- Verify `GMAIL_PASSWORD` is an app password, not your regular password
- Ensure `RECIPIENT_EMAIL` is correct

**Timezone Issues?**
- The cron schedule `40 20 * * *` runs at 8:40 PM UTC (= 4:40 PM ET)
- If you're in a different timezone, adjust the cron expression:
  - CST (Central): `40 18 * * *`
  - MST (Mountain): `40 17 * * *`
  - PST (Pacific): `40 16 * * *`

## How It Works

Every day at 4:40 PM ET, GitHub Actions will:

1. Clone your repository
2. Install Python dependencies from `requirements.txt`
3. Run `python main.py` which:
   - Crawls all investor portfolios from Dataroma
   - Generates an HTML report
   - Sends the report via email to `RECIPIENT_EMAIL`
4. Logs are available in the Actions tab for debugging