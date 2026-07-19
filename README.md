# AI-Powered Residential Security Sales Assistant

A production-ready Telegram bot designed for CCTV and residential security integrators in the US market (specifically optimized for Orlando, FL). The bot automates the analysis of property vulnerabilities using Large Language Models (LLMs) and instantly generates high-converting B2B/B2C sales collateral.

## Key Features

*   **Persistent Session Storage:** Utilizes an SQLite database architecture to preserve user context and property states across application reboots.
*   **Vulnerability Analysis:** Leverages OpenAI's `gpt-4o-mini` to perform instantaneous risk assessment based on raw text descriptions of residential properties.
*   **Automated Pitch Mailer:** Generates tailored, high-converting cold outreach emails offering free security audits to homeowners.
*   **Localized Social Selling:** Drafts engaging, neighborly, and expert posts suitable for local US platforms like Nextdoor and Facebook Groups.
*   **Structured Technical Specs:** Produces detailed hardware recommendations specifying camera architectures (dome, bullet, quantities) and motion sensor placement.

## Tech Stack

*   **Language:** Python 3.12+
*   **Framework:** pyTelegramBotAPI (Advanced asynchronous infinity polling architecture)
*   **Database:** SQLite3 (Relational persistence layer with structured query parameters)
*   **AI Integration:** OpenAI API (`gpt-4o-mini` model orchestration)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alexkaa87/ai-cctv-sales-bot.git
   cd ai-cctv-sales-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install pyTelegramBotAPI openai
   ```

3. **Configure environment tokens:**
   Replace the placeholder token inside the script with your official Telegram Bot API key:
   ```python
   TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

4. **Run the application:**
   ```bash
   python day15.py
   ```

## Security & Best Practices

*   **SQL Injection Prevention:** Structured queries utilize parameterized placeholders (`?`) to decouple user inputs from SQL execution logic.
*   **Stateless Secrets Management:** The application configuration blocks are isolated to prevent the exposure of live Telegram and OpenAI API keys within the codebase.
