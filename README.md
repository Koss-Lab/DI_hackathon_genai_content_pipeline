# 🎉 **README – DI GenAI Content Pipeline**

*Your complete beginner-friendly guide to running a text-generation pipeline, CLI tool, and Telegram bot powered by OpenAI.*

---

# 🚀 What is this project?

**DI GenAI Content Pipeline** is a full end-to-end content generator built for students, beginners, hackathons, and anyone who wants to experiment with AI text generation.

It includes:

* ✅ A **CLI app** to generate AI content
* ✅ A **Telegram bot** that runs 24/7 (via Railway)
* ✅ A **content filter** (to detect unsafe text)
* ✅ A **batch processor** for CSV files
* ✅ A **local JSON history** saving system
* ✅ Easy deployment and zero-config setup

This pipeline uses **OpenAI GPT-4o-mini** for AI generation.

---

# 📦 Features

### ✅ **1. CLI Tool**

* Run default prompts
* Enter your own custom prompt
* Run a full CSV batch
* View past results
* Everything saved in `last_results.json`

### ✅ **2. Telegram Bot**

* Friendly menu with buttons
* Generates text on demand
* Processes multiple prompts
* Returns long messages safely
* Has “Back to Menu” navigation
* Deployed on Railway (runs 24/7)

### ✅ **3. Content Filtering**

Automatically flags:

* violence
* hate speech
* self-harm
* dangerous content

### ✅ **4. Beginner-friendly**

No ML knowledge needed.
Just plug your API key + Telegram bot token and everything works.

---

# 🧱 Project Structure

```
DI_hackathon_genai_content_pipeline/
│
├── automation/
│   ├── scheduler.py
│   └── telegram_bot.py      ← Telegram bot runner
│
├── src/
│   ├── pipeline.py          ← Core logic
│   ├── api_generator.py     ← OpenAI generator
│   ├── content_filter.py
│   ├── ethical_filter.py
│   ├── summarizer.py        ← (Optional – disabled on Railway)
│   ├── generator.py
│   ├── utils.py
│
├── data/
│   ├── prompts.csv          ← For batch mode
│   ├── prompts.json
│   ├── flagged.json
│   └── results/
│
├── cli.py                   ← Command-line interface
├── main.py
├── Procfile                 ← Railway runner
├── runtime.txt              ← Python version
├── requirements.txt
└── README.md
```

---

# 🛠️ Installation (Local)

## 1️⃣ Clone the repository

```bash
git clone https://github.com/Koss-Lab/DI_hackathon_genai_content_pipeline
cd DI_hackathon_genai_content_pipeline
```

## 2️⃣ Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setting your `.env` file

Create a file named **`.env`** at the root of the project:

```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
USE_OPENAI_API=true

TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

Both are required.

---

# 🤖 Creating your Telegram Bot (Beginner-Friendly Guide)

1. Open Telegram
2. Search for **@BotFather**
3. Send: `/start`
4. Send: `/newbot`
5. BotFather asks for:

   * name → choose anything
   * username → must end in **_bot**
6. BotFather gives you a token:

```
1234567890:ABCdefGHIjkLMNOP-123456789
```

👉 Put this token inside your `.env` file.

7. Your bot URL becomes:

```
https://t.me/your_bot_name
```

---

# 🧪 Running the CLI

Start the CLI:

```bash
python3 cli.py
```

You will see:

```
1) Run pipeline on default prompts
2) Enter a custom prompt
3) Run batch on CSV file
4) View last results
5) Quit
```

Everything saves automatically to:

* `last_results.json`


---

# 🤖 Running the Telegram Bot Locally

Make sure your `.env` is set correctly.

Run:

```bash
python3 automation/telegram_bot.py
```

You should see:

```
🤖 Telegram bot running (clean event loop)…
```

Then open Telegram → talk to your bot.

---

# 🌐 Deploying on Railway (24/7 Hosting)

### ✔️ Railway automatically runs:

```
python3 automation/telegram_bot.py
```

### 1️⃣ Create a new Railway project

Go to: [https://railway.app](https://railway.app)

### 2️⃣ Choose “Deploy from GitHub”

Select your repository:

```
https://github.com/username/your_repo
```

### 3️⃣ Add Environment Variables

In Railway → Project → **Variables**

Add:

```
OPENAI_API_KEY=your_key
MODEL_NAME=gpt-4o-mini
USE_OPENAI_API=true
TELEGRAM_BOT_TOKEN=your_bot_token
```

### 4️⃣ Deploy

Railway builds your project and starts your bot.

### 5️⃣ Check logs

Under **Deployments → Logs**

If it says:

```
🤖 Telegram bot running (clean event loop)…
```

🎉 Your bot is now live 24/7.

---

# 🔎 Troubleshooting

### ❌ Bot says “TELEGRAM_BOT_TOKEN not found”

You forgot to add variables in Railway → *Variables*.

### ❌ “ModuleNotFoundError: src”

Your folder structure is wrong, or you didn’t push the `.env` or imports.

### ❌ Transformers missing on Railway

Normal – summarizer auto-disables itself.

### ❌ CLI works but bot fails

Always rerun:

```bash
git add .
git commit -m "Fix"
git push
```

Railway redeploys automatically.

---

# ⭐ Credits

Created by **Koss-Lab**
Telegram bot: [https://t.me/kossmagic_gpt_bot](https://t.me/kossmagic_gpt_bot)
Repo: [https://github.com/Koss-Lab/DI_hackathon_genai_content_pipeline](https://github.com/Koss-Lab/DI_hackathon_genai_content_pipeline)

---

# 🎤 Want to Improve the Project?

You can extend the pipeline by adding:

* new filters
* new models
* new Telegram features
* logging and analytics
* databases
* full conversations
* admin panel

Just ask the bot for help, we upgrade together.

