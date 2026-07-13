# AI-Powered Lead Conversion & Tech Assistant for CCTV Business

An interactive Telegram bot built with **Python** and **OpenAI API (GPT-4o-mini)** designed to automate outbound lead generation, vulnerability analysis, and personalized sales communication for residential security (CCTV) installation businesses.

## 🚀 Business Value & Impact
* **Speed to Lead:** Reduces the time required to analyze property vulnerabilities and generate a highly personalized pitch from **40 minutes to 3 seconds**.
* **Localization:** Instantly crafts native, highly empathetic responses tailored for US neighborhood platforms (Nextdoor, Facebook Groups) to convert worried homeowners into paying clients without sounding salesy.
* **Technical Onboarding:** Streamlines internal workflows by generating instant hardware recommendations (camera types, placement zones) directly on a smartphone.

## 🛠️ Tech Stack & Architecture
* **Backend:** Python 3
* **LLM Integration:** OpenAI API (`gpt-4o-mini`) using dynamic structured prompts and context preservation.
* **UI/UX:** `pyTelegramBotAPI` (Telegram Bot API wrapper) utilizing an interactive inline keyboard interface (`InlineKeyboardMarkup`) for state management and seamless user experience.

## 📦 Features & UI Flow
1. **Context Retention:** The bot securely maps the original property description to the user's chat session.
2. **Interactive Inline Menu:**
   * 📧 **Generate Pitch Email:** Creates an American-style, professional cold email focused on the specific property's risks.
   * 🏡 **Nextdoor/Facebook Reply:** Generates a friendly, non-formal, high-converting neighborly response for local community boards.
   * 🛠️ **Tech Specs:** Outputs structured hardware suggestions and optimal camera placement zones.

## 🔧 Installation & Setup



1. Clone the repository:
   ```bash
   git clone [https://github.com/alexkaa87/ai-cctv-sales-bot.git](https://github.com/alexkaa87/ai-cctv-sales-bot.git)
