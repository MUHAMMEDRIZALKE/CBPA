# CBPA - Chat Based Privet Assistant

CBPA (Chat Based Privet Assistant) is an intelligent, chat-first personal assistant. It currently focuses on expense tracking and financial management through a Telegram bot, and is evolving into a fully fledged assistant with reminders, integrations, and multi-platform support (including a future app frontend). Powered by advanced Large Language Models (LLMs) like OpenAI and Google GenAI, CBPA understands natural language commands, making interacting with your assistant as simple as chatting with a friend.

> **Note**: CBPA is a work in progress. Features and APIs are actively evolving.

## 🚀 Features (Current)

- **Natural Language Expense Logging**: Simply type "Spent $15 on lunch" and the assistant automatically categorizes and logs the transaction.
- **General Q&A**: Ask normal questions and get intelligent answers powered by LLMs - CBPA can help with general knowledge, explanations, and conversations beyond just expense tracking.
- **Multi-Currency Support**: Handle expenses in various currencies with ease. Set your default currency and log transactions in any other currency.
- **Interactive Chat Interface**: A user-friendly chat experience (currently via Telegram) powered by `python-telegram-bot`.
- **Robust Data Management**: Built on PostgreSQL with TimescaleDB for efficient handling of time-series data.
- **Dockerized Deployment**: easy to deploy and scale using Docker and Docker Compose.
- **Modern Python Stack**: Built with Python 3.13+, using `uv` for fast package management.

## 🧭 Roadmap & Vision

CBPA is planned to grow beyond a Telegram-only, finance-focused bot into a general-purpose, chat-based personal assistant, including:

- **Reminders & Scheduling**: Create, manage, and receive reminders and notifications.
- **3rd-Party Integrations**: Connect with external apps and services for richer workflows.
- **Multi-Platform Frontends**: In addition to Telegram, provide an app frontend (and potentially other clients).
- **Broader Personal Assistant Capabilities**: Go beyond expense tracking to support everyday tasks and productivity.

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Bot Framework**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **Database**: PostgreSQL (TimescaleDB), SQLAlchemy (ORM), Alembic (Migrations)
- **AI/LLM**: OpenAI API / Google GenAI
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Containerization**: Docker, Docker Compose

## 📋 Prerequisites

Before you begin, ensure you have the following requirements:

- **Docker** and **Docker Compose** installed on your machine.
- A **Telegram Bot Token** (obtained from [@BotFather](https://t.me/BotFather)).
- An **OpenAI API Key** or **Google GenAI API Key**.
- (Optional) **Python 3.13+** and **uv** installed for local development.

## ⚙️ Installation & Setup

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/tpa.git
    cd tpa
    ```

2.  **Environment Configuration**

    Create a `.env` file in the root directory based on the following template:

    ```ini
    # Database Configuration
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_DB=tpa_db
    DATABASE_URL=postgresql+psycopg2://your_db_user:your_db_password@db:5432/tpa_db

    # Bot Configuration
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token

    # AI Configuration (Choose one or both depending on setup)
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key

    # System
    BACKEND_SYSTEM_PORT=8000
    ```

3.  **Run with Docker (Recommended)**

    Build and start the services using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    The bot will start, run database migrations automatically, and be ready to accept messages.

4.  **Run Locally (Development)**

    If you prefer to run the bot locally without Docker (requires a running Postgres instance):

    ```bash
    # Install dependencies
    uv sync

    # Run migrations
    uv run alembic upgrade head

    # Start the bot
    uv run app/main.py
    ```

## 📖 Usage

1.  Open your bot in Telegram.
2.  Send the `/start` command to initiate the session.
3.  **Set your currency**:
    ```text
    /set_currency USD
    ```
4.  **Log an expense** naturally:
    ```text
    I spent 50 EUR on groceries today.
    ```
5.  **Ask general questions**:
    ```text
    How do large language models work?
    What's the difference between AI and machine learning?
    ```
6.  **View Help**:
    ```text
    /help
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

[MIT License](LICENSE)
