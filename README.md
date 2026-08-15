# Medtech Daily

A daily-updating website that summarizes medtech innovation news featuring
real-world implementation results, categorized by innovation type.

Every day, a GitHub Actions workflow calls the Anthropic API (with web
search) to research the day's medtech news, writes the result to
`briefing.json`, and publishes the site via GitHub Pages.

## One-time setup

### 1. Create the repository
- Create a new **public** repository on GitHub (e.g. `medtech-daily`).
  (Public is required for free GitHub Pages, unless you have GitHub Pro.)
- Upload all files from this folder, preserving the folder structure
  (the `.github/workflows/daily-briefing.yml` file must stay in that exact
  path).

### 2. Add your API key as a secret
- In the repository: **Settings → Secrets and variables → Actions**
- Click **New repository secret**
- Name: `ANTHROPIC_API_KEY`
- Value: paste your Anthropic API key
- Save

Your key is never exposed to site visitors or stored in the code — GitHub
injects it only at workflow run time.

### 3. Enable GitHub Pages
- **Settings → Pages**
- Under "Build and deployment", set **Source** to **GitHub Actions**

### 4. Run the workflow once manually
- Go to the **Actions** tab → select **"Generate daily medtech briefing"**
- Click **Run workflow** → **Run workflow**
- Wait ~1-2 minutes for it to finish (green checkmark)

### 5. Visit your site
Your site will be live at:

```
https://<your-github-username>.github.io/<repository-name>/
```

## How it stays updated

The workflow runs automatically every day at 06:00 UTC (edit the `cron`
line in `.github/workflows/daily-briefing.yml` to change the time — times
are always in UTC). You can also trigger it manually any time from the
Actions tab.

## Costs

- GitHub repository, Actions minutes, and Pages hosting: free for public
  repositories.
- Anthropic API usage: pay-as-you-go. One run (one web-search-enabled
  request) costs a small fraction of a dollar. Running once a day, monthly
  cost should be well under $1-2. Set a spending limit in the Anthropic
  Console as a safety net (Settings → Billing → Usage limits).

## Customizing

- **Categories or article count**: edit the prompt in
  `generate_briefing.py`.
- **Schedule**: edit the `cron` line in the workflow file.
- **Look and feel**: edit `index.html` (plain HTML/CSS, no build step).
