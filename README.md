# Book Crossing Bot

A Telegram bot for book exchange built with Python, Flask, and PostgreSQL.

## Features

- User registration
- Book management (add, search, view)
- User status tracking
- Admin panel
- Secure database operations

## Requirements

- Python 3.8+
- PostgreSQL database
- Telegram Bot Token
- Render account (for deployment)

## Environment Variables

Create a `.env` file with the following variables:

```
TOKEN=your_telegram_bot_token
WEBHOOK_URL=your_render_app_url
DATABASE_URL=your_postgresql_database_url
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file

3. Run the bot:
```bash
python hosthing.py
```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn hosthing:app`
4. Add environment variables in Render dashboard:
   - `TOKEN`
   - `WEBHOOK_URL`
   - `DATABASE_URL`
5. Deploy the service

## Security Notes

- All database operations are protected with locks
- Secure webhook handling
- Error logging
- Process management with proper cleanup 