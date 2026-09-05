# LinkedIn Daily Ideas Agent

An AI-powered agent that generates 5 tailored LinkedIn post ideas every morning, auto-committed to this repo and ready to copy-paste.

Built for **Sahil Prakash** — BI & Analytics Engineer actively job hunting and building a personal brand in the Power BI / Microsoft Fabric / Copilot Studio space.

---

## What It Does

Every day from **7:00 AM IST**, a GitHub Actions workflow generates the ideas.
Automatic catch-up checks later in the day cover delayed GitHub schedules, while
an IST-date guard ensures it generates at most one ideas file per day.

1. Calls the **Groq API** (current default `openai/gpt-oss-20b`, with fallbacks), then **OpenRouter** if Groq fails, with a structured prompt
2. Generates **5 post ideas** — 3 on the primary theme, 2 on the secondary
3. Saves the output as `linkedin_ideas/YYYY-MM-DD.md`
4. Commits and pushes the file to this repo automatically

Each idea includes:
- A scroll-stopping **hook** (first line)
- A full **post draft** ready to publish
- A **"why it works"** explanation
- The **optimal posting time** for that day of the week

---

## Theme Rotation

Themes rotate daily so content stays varied across the week:

| Theme | Focus |
|---|---|
| Power BI & DAX | Tips, DAX patterns, report design, CALCULATE, context transition |
| Microsoft Fabric & Analytics Engineering | Lakehouse, OneLake, medallion architecture, semantic models |
| Copilot Studio & Power Platform | Agents, Power Automate, Power Apps, AI Builder integrations |
| Career & Job Hunt | Honest reflections, interview experiences, market insights |

Each day picks a **primary** (3 posts) and **secondary** (2 posts) theme based on the day index. Today's primary becomes tomorrow's secondary.

---

## Optimal Posting Times

| Day | Best Time (IST) |
|---|---|
| Monday | 8:00 AM |
| Tuesday | 8:30 AM |
| Wednesday | 9:00 AM |
| Thursday | 8:30 AM |
| Friday | 8:00 AM |
| Saturday | 10:00 AM |
| Sunday | 11:00 AM |

The agent prints the day's optimal time at the top of every generated file.

---

## Output Format

Ideas are saved to `linkedin_ideas/YYYY-MM-DD.md`:

```
# LinkedIn Post Ideas — Sunday, 2026-07-12

> Best time to post today: 11:00 AM IST
> Primary theme: Copilot Studio & Power Platform | Secondary: Career & Job Hunt

---

## Idea 1 — Copilot Studio & Power Platform
**Topic:** Automating repetitive reporting with Power Automate

**Hook:** I saved 4 hours a week. Here's the exact flow I built.

**Full Draft:**
I saved 4 hours a week. Here's the exact flow I built.
...

**Why it works:** Concrete time-saving claim + actionable detail drives saves and comments.

---

## Rebranding Tip of the Day
If your headline doesn't mention Copilot Studio, update it today.
...
```

---

## Project Structure

```
linkedin-agent/
├── linkedin_agent.py          # Main agent script
├── linkedin_ideas/            # Auto-generated daily idea files
│   └── YYYY-MM-DD.md
├── .github/
│   └── workflows/
│       └── linkedin-ideas.yml # Scheduled GitHub Actions workflow
├── .env                       # API keys (gitignored)
└── .gitignore
```

---

## Setup

### Prerequisites

- Python 3.10+
- [Groq API key](https://console.groq.com) or [OpenRouter API key](https://openrouter.ai/keys)
- GitHub repository with Actions enabled

### Local Run

```bash
# Clone and enter the repo
git clone https://github.com/sahilprakash/linkedin-agent.git
cd linkedin-agent

# Install dependencies
pip install requests python-dotenv

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
# Optional second provider:
# echo "OPENROUTER_API_KEY=your_key_here" >> .env

# Run the agent
python3 linkedin_agent.py
```

Output will be written to `linkedin_ideas/YYYY-MM-DD.md`.

### Automated Daily Run (GitHub Actions)

The workflow at `.github/workflows/linkedin-ideas.yml` runs on a GitHub-hosted runner, so it does not depend on this Mac being awake.

**Required GitHub Secret:**

| Secret | Value |
|---|---|
| `GH_PAT` | Personal Access Token with `repo` scope (for git push) |
| `GMAIL_USERNAME` | Gmail address used to send the daily email |
| `GMAIL_APP_PASSWORD` | Gmail App Password for SMTP (not your normal Gmail password) |
| `EMAIL_TO` | Gmail address that should receive the ideas |
| `OPENROUTER_API_KEY` | Optional fallback provider key |

If Groq is unavailable, the agent automatically tries OpenRouter. Set the
optional repository variable `OPENROUTER_MODEL` to choose a model; the default
`openrouter/auto` lets OpenRouter select an available model.

Add it via:
```bash
gh secret set GH_PAT --repo sahilprakash/linkedin-agent
```

To enable the daily email, create a Gmail App Password for the sending account
and add the three Gmail secrets above. The workflow sends the ideas inline as
plain text after successfully pushing the daily file.

The primary cron run is `30 1 * * *` (01:30 UTC = 07:00 AM IST), with later
automatic catch-up runs if that attempt is delayed.

---

## Configuration

All configuration is at the top of `linkedin_agent.py`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Optional override; script falls back if Groq retires an ID |
| `OUTPUT_DIR` | `linkedin_ideas` | Directory for output files |
| `THEMES` | 4 themes | List of theme objects with name + description |
| `OPTIMAL_TIMES` | Per weekday | Best posting time map |
| `PROFILE` | Sahil's bio | Injected into system prompt for personalization |

To adapt for a different person, update `PROFILE` and `THEMES`.

---

## Tech Stack

- **Language:** Python 3
- **AI:** Groq API → OpenRouter → built-in templates
- **Automation:** GitHub Actions (GitHub-hosted runner)
- **Persistence:** Markdown files committed to this repo

---

## Security Notes

- `GROQ_API_KEY` lives in `.env` only — never committed
- `GH_PAT` is stored as a GitHub Secret — never in code
- Secrets are provided only to the GitHub Actions workflow at runtime
