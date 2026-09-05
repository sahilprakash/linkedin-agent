"""
linkedin_agent.py

Generates 5 tailored LinkedIn post ideas for Sahil Prakash (BI & Analytics Engineer)
using Groq AI. Saves them as a daily markdown file in linkedin_ideas/.

Themes (rotated daily):
  - Power BI & DAX tips
  - Microsoft Fabric & Analytics Engineering
  - Copilot Studio & Power Platform
  - Career & job hunt journey

Run: python3 linkedin_agent.py
Output: linkedin_ideas/YYYY-MM-DD.md
"""

import os
import json
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
# Groq retires model IDs; try in order until one is available.
GROQ_MODELS   = [
    os.getenv("GROQ_MODEL", "").strip(),
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]
GROQ_MODELS   = [m for m in GROQ_MODELS if m]
OUTPUT_DIR    = "linkedin_ideas"

IST           = timedelta(hours=5, minutes=30)
NOW_IST       = datetime.now(timezone.utc) + IST
TODAY_STR     = NOW_IST.strftime("%Y-%m-%d")
WEEKDAY       = NOW_IST.strftime("%A")   # Monday, Tuesday …

# Optimal posting times by weekday (IST)
OPTIMAL_TIMES = {
    "Monday":    "8:00 AM IST",
    "Tuesday":   "8:30 AM IST",
    "Wednesday": "9:00 AM IST",
    "Thursday":  "8:30 AM IST",
    "Friday":    "8:00 AM IST",
    "Saturday":  "10:00 AM IST",
    "Sunday":    "11:00 AM IST",
}

PROFILE = """
Name        : Sahil Prakash
Role        : BI & Analytics Engineer
Experience  : 5 years
Core stack  : Power BI, DAX, Microsoft Fabric, Copilot Studio, Power Platform, Power Apps,
              Analytics Engineering, SQL, Azure, Data Modeling
Status      : Actively looking for new opportunities
Audience    : Data professionals, hiring managers, BI leads, Power Platform developers,
              analytics engineers, tech recruiters
"""

SYSTEM_PROMPT = f"""You are a LinkedIn content strategist specializing in data & analytics professionals.
You create scroll-stopping posts that build personal brand and attract recruiters and peers.

About the creator:
{PROFILE}

Post writing rules:
- First line (hook): short, punchy, makes people stop scrolling — no greetings, no "I am excited to share"
- Body: practical value, a story, a tip, or a surprising insight. Use short paragraphs (2-3 lines max).
- End with a question or CTA to drive comments
- 3-5 relevant hashtags at the end
- Tone: confident, human, conversational — not corporate
- Length: 150-250 words ideal
- Never use buzzwords like "leverage", "synergy", "deep dive", "delve"
"""

THEMES = [
    {
        "name": "Power BI & DAX",
        "description": "Power BI tips, DAX patterns, report design, performance tuning, calculated columns vs measures, CALCULATE tricks, context transition"
    },
    {
        "name": "Microsoft Fabric & Analytics Engineering",
        "description": "Microsoft Fabric, Lakehouse, OneLake, dataflows, pipelines, analytics engineering principles, dbt-style thinking, medallion architecture, semantic models"
    },
    {
        "name": "Copilot Studio & Power Platform",
        "description": "Copilot Studio agents, Power Automate flows, Power Apps, AI Builder, integrating Copilot with enterprise data, real-world automation use cases"
    },
    {
        "name": "Career & Job Hunt",
        "description": "Honest reflections on job hunting as a BI professional, interview experiences, skills that actually matter, navigating the market, what companies look for in analytics hires"
    },
]

# Rotate theme based on day of week (Mon=0 … Sun=6)
day_index     = NOW_IST.weekday()
primary_theme = THEMES[day_index % len(THEMES)]
secondary_theme = THEMES[(day_index + 1) % len(THEMES)]


def fallback_ideas() -> list[dict]:
    """Return useful posts even when the external AI provider is unavailable."""
    return [
        {
            "theme": primary_theme["name"],
            "title": "Build a reliable Fabric data foundation",
            "hook": "A beautiful dashboard cannot rescue unreliable data.",
            "draft": (
                "A beautiful dashboard cannot rescue unreliable data.\n\n"
                "The strongest analytics teams start with a clear data foundation: "
                "defined owners, consistent naming, documented transformations, and "
                "a semantic model people can trust.\n\n"
                "In Microsoft Fabric, small improvements to ingestion and modeling "
                "often create more value than another layer of visual polish.\n\n"
                "What is the first thing you improve when a reporting project becomes unreliable?\n\n"
                "#MicrosoftFabric #AnalyticsEngineering #DataModeling"
            ),
            "why_it_works": "It connects a practical engineering lesson with a question that invites experience-based replies.",
        },
        {
            "theme": primary_theme["name"],
            "title": "Treat analytics models like products",
            "hook": "Your semantic model is a product, not just a database layer.",
            "draft": (
                "Your semantic model is a product, not just a database layer.\n\n"
                "It has users, quality expectations, release changes, and support needs. "
                "When analysts understand the model, adoption improves. When definitions "
                "change without communication, trust disappears.\n\n"
                "A simple product mindset means documenting business definitions, testing "
                "important measures, and giving users a clear way to report issues.\n\n"
                "How does your team manage changes to shared metrics?\n\n"
                "#AnalyticsEngineering #PowerBI #DataCulture"
            ),
            "why_it_works": "It reframes a familiar technical topic in a memorable, practical way.",
        },
        {
            "theme": primary_theme["name"],
            "title": "Choose measures over calculated columns",
            "hook": "One DAX decision can make your model easier to maintain.",
            "draft": (
                "One DAX decision can make your model easier to maintain.\n\n"
                "If a value depends on filter context, start by asking whether it belongs "
                "as a measure instead of a calculated column. Measures keep logic flexible "
                "and can reduce unnecessary model size.\n\n"
                "The right choice still depends on the use case, but making the decision "
                "explicit prevents many performance and maintenance problems later.\n\n"
                "What DAX modeling rule has saved you the most rework?\n\n"
                "#PowerBI #DAX #BusinessIntelligence"
            ),
            "why_it_works": "It offers a concise technical takeaway that Power BI practitioners can immediately apply.",
        },
        {
            "theme": secondary_theme["name"],
            "title": "Start small with Copilot automation",
            "hook": "The best Copilot automation usually starts with one boring task.",
            "draft": (
                "The best Copilot automation usually starts with one boring task.\n\n"
                "Instead of trying to automate an entire business process, find one step "
                "that is repetitive, well understood, and easy to measure. Then add the "
                "right approvals and exception handling.\n\n"
                "Small wins create confidence—and reveal the real process gaps that need "
                "attention before scaling.\n\n"
                "Which repetitive task would you automate first?\n\n"
                "#CopilotStudio #PowerPlatform #Automation"
            ),
            "why_it_works": "It makes AI adoption feel practical and lowers the barrier to starting.",
        },
        {
            "theme": secondary_theme["name"],
            "title": "Make automation observable and safe",
            "hook": "Automation without monitoring is just invisible risk.",
            "draft": (
                "Automation without monitoring is just invisible risk.\n\n"
                "Every production flow should make it easy to answer three questions: "
                "Did it run? Did it complete? If not, what needs attention?\n\n"
                "Add clear failure notifications, meaningful logs, and an owner who can "
                "act on exceptions. Reliable automation is not only about saving clicks; "
                "it is about making outcomes predictable.\n\n"
                "What signal do you monitor most closely in your Power Platform flows?\n\n"
                "#PowerAutomate #PowerPlatform #DigitalTransformation"
            ),
            "why_it_works": "It addresses a common operational blind spot with a clear checklist and discussion prompt.",
        },
    ]


def generate_ideas() -> list[dict]:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    prompt = f"""
Today is {WEEKDAY}, {TODAY_STR}.

Generate 5 LinkedIn post ideas for Sahil Prakash. Mix the following two themes for today:
- Primary theme (3 posts): {primary_theme['name']} — {primary_theme['description']}
- Secondary theme (2 posts): {secondary_theme['name']} — {secondary_theme['description']}

For each post, return a JSON object with:
  - "theme": the theme name
  - "title": a 5-7 word description of the post topic
  - "hook": the first line only (the scroll-stopper, max 12 words)
  - "draft": the full post draft including hook, body, CTA, and hashtags
  - "why_it_works": one sentence on why this post will perform well

Return a JSON array of exactly 5 objects. No markdown fences, just raw JSON.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    last_error = None
    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            "temperature": 0.85,
            "max_tokens": 3000,
        }

        for attempt in range(2):
            try:
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers, json=payload, timeout=60
                )
                if res.status_code == 429:
                    if attempt == 0:
                        import time; time.sleep(20)
                        continue
                    last_error = RuntimeError("Groq rate limited after retry")
                    break
                if res.status_code in (400, 404):
                    last_error = RuntimeError(f"Groq error {res.status_code} for {model}: {res.text[:200]}")
                    break
                if res.status_code != 200:
                    last_error = RuntimeError(f"Groq error {res.status_code}: {res.text[:200]}")
                    if attempt == 0:
                        import time; time.sleep(5)
                        continue
                    break

                try:
                    content = res.json()["choices"][0]["message"]["content"].strip()
                except (KeyError, IndexError, TypeError, ValueError) as e:
                    raise RuntimeError(f"Unexpected Groq response for {model}: {e}") from e
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                ideas = json.loads(content)
                print(f"Using Groq model: {model}")
                return ideas

            except (requests.exceptions.ConnectionError, json.JSONDecodeError) as e:
                last_error = RuntimeError(f"Failed to generate ideas with {model}: {e}")
                if attempt == 0:
                    import time; time.sleep(5)
                    continue

    if last_error:
        raise last_error
    return []


def save_markdown(ideas: list[dict]) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{TODAY_STR}.md")
    optimal  = OPTIMAL_TIMES.get(WEEKDAY, "8:30 AM IST")

    lines = [
        f"# LinkedIn Post Ideas — {WEEKDAY}, {TODAY_STR}",
        "",
        f"> **Best time to post today:** {optimal}",
        f"> **Primary theme:** {primary_theme['name']}  |  **Secondary:** {secondary_theme['name']}",
        "",
        "---",
        "",
    ]

    for i, idea in enumerate(ideas, 1):
        lines += [
            f"## Idea {i} — {idea.get('theme', '')}",
            f"**Topic:** {idea.get('title', '')}",
            "",
            f"**Hook:** {idea.get('hook', '')}",
            "",
            "**Full Draft:**",
            "",
            idea.get("draft", ""),
            "",
            f"**Why it works:** _{idea.get('why_it_works', '')}_",
            "",
            "---",
            "",
        ]

    lines += [
        "## Rebranding Tip of the Day",
        "",
        "_Profile keyword to add or strengthen today:_",
        f"If your headline doesn't mention **{primary_theme['name'].split('&')[0].strip()}**, update it today.",
        "Recruiters search by skill keywords — your headline is indexed by LinkedIn search.",
        "",
        "**Suggested headline format:**",
        "> BI & Analytics Engineer | Power BI · Microsoft Fabric · Copilot Studio | Open to Opportunities",
        "",
    ]

    content = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    print(f"LinkedIn Agent — {WEEKDAY}, {TODAY_STR}")
    print(f"Theme: {primary_theme['name']} (primary) + {secondary_theme['name']} (secondary)")
    print("Generating ideas via Groq...")

    try:
        ideas = generate_ideas()
    except Exception as exc:
        print(f"AI generation failed ({exc}); using built-in fallback ideas.")
        ideas = fallback_ideas()

    if not ideas:
        print("ERROR: No ideas generated.")
        return

    filepath = save_markdown(ideas)
    print(f"\nSaved {len(ideas)} ideas → {filepath}")
    print(f"Best time to post: {OPTIMAL_TIMES.get(WEEKDAY, '8:30 AM IST')}")
    print("\nPost Hooks:")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. [{idea.get('theme','')}] {idea.get('hook','')}")


if __name__ == "__main__":
    main()
