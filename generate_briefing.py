"""
Generates the daily medtech briefing by calling the Anthropic API with
web search enabled, and writes the result to briefing.json.

Run daily by the GitHub Actions workflow in .github/workflows/daily-briefing.yml.
Requires the ANTHROPIC_API_KEY environment variable to be set.
"""

import json
import os
import re
import sys
from datetime import date, datetime, timezone

import anthropic

MODEL = "claude-sonnet-4-6"

PROMPT = """You are a medical technology news curator. Search for and return \
today's ({today}) most important medtech articles that feature ACTUAL \
IMPLEMENTATION RESULTS -- meaning real-world deployments, clinical trial \
outcomes, hospital rollouts, patient outcomes, or measurable efficacy data. \
Exclude pure research announcements or speculative pieces with no results yet.

Return ONLY a JSON object (no markdown fences, no preamble, no commentary) \
with this exact structure:

{{
  "date": "{today}",
  "feature": {{
    "title": "compelling headline summarizing today's biggest medtech story",
    "summary": "3-4 sentence editorial summary of today's medtech landscape \
and biggest themes",
    "highlights": [
      {{"label": "Biggest story", "text": "one sentence"}},
      {{"label": "Key trend", "text": "one sentence"}},
      {{"label": "To watch", "text": "one sentence"}}
    ]
  }},
  "articles": [
    {{
      "title": "article title",
      "source": "publication name",
      "category": "one of: AI & Machine Learning | Diagnostics & Imaging | \
Digital Health | Robotics & Surgery | Wearables & Monitoring | Genomics & \
Precision Medicine | Drug Delivery & Therapeutics | Other",
      "snippet": "2 sentence summary focusing on the implementation result \
or outcome",
      "result": "key measurable result or outcome in under 10 words",
      "url": "actual source URL"
    }}
  ]
}}

Include 8-12 articles, each with a real, working source URL from the search \
results. Focus on: FDA approvals with real deployment, hospital AI rollouts, \
clinical trial results, surgical robot outcomes, wearable validation \
studies, digital therapeutic approvals. Categories must match one of the \
options exactly."""


def extract_json(text: str) -> dict:
    cleaned = re.sub(r"```json|```", "", text).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model response")
    return json.loads(cleaned[start : end + 1])


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    today = date.today().isoformat()

    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": PROMPT.format(today=today)}],
    )

    text_blocks = [block.text for block in response.content if block.type == "text"]
    full_text = "\n".join(text_blocks)

    briefing = extract_json(full_text)
    briefing["generated_at"] = datetime.now(timezone.utc).isoformat()

    with open("briefing.json", "w", encoding="utf-8") as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)

    print(f"Wrote briefing.json with {len(briefing.get('articles', []))} articles")


if __name__ == "__main__":
    main()
