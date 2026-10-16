# Profile dashboard: how it works

The profile README is a terminal-style dashboard. The data panels are SVGs that a
GitHub Action draws from **public** GitHub data once a day and publishes to the
`output` branch. Everything else is plain Markdown or static SVG in `assets/`.

```
README.md                         layout and text (projects, stack, links)
assets/prompt-*.svg               "jey@github ~ $ …" section prompts (desktop + -mobile)
assets/btn-*.svg                  link buttons
.github/scripts/dashboard.py      draws the data panels (stdlib + Pillow)
.github/workflows/dashboard.yml   runs it daily, publishes to the output branch
```

## Panels

| panel | shows | data source |
| --- | --- | --- |
| `./contributions.sh` | Contribution heatmap, month and weekday labels, total, legend. The mobile version shows the last 26 weeks. | GraphQL `contributionsCollection.contributionCalendar` (GitHub's own day levels) |
| `whoami` · portrait | Dot-matrix portrait cropped from your avatar, name, role caption | Avatar URL from GraphQL; caption is the `ROLE` setting |
| `whoami` · stats | Current streak, longest streak, contributions, active days, best day, average per active day, contributions per month, then public repos, stars, followers and join date | Same calendar, plus `followers`, public repos and stargazers of public non-fork repos |
| `./languages.sh` | Top six languages by share of bytes | `languages` of public non-fork repos (GitHub Linguist) |

Notes on the numbers:

- Streaks and totals cover the calendar window GitHub returns (the last year), so
  "longest streak" is the longest within that window, not all time.
- Third-party streak cards can show different streaks because they count days and
  windows differently.
- Notebook (`.ipynb`) bytes include cell outputs, which inflates Jupyter's share.
- The workflow uses the built-in `GITHUB_TOKEN`, so only public activity is counted.

## Setup

1. Commit and push this repo to `main`. The push includes the workflow file, which
   triggers its first run.
2. Open **Actions → Profile dashboard** and confirm the run is green. It publishes
   `contributions*.svg`, `whoami*.svg` and `languages*.svg` to the `output` branch.
3. Reload your profile. The panels refresh daily at 00:17 UTC, and you can run the
   workflow manually with **Run workflow**.

No secrets, PATs or external services are needed. The workflow asks for
`contents: write` only so it can push to the `output` branch.

## Manual configuration

- [ ] **Push and run the workflow.** Until the first run, the panel images 404.
- [ ] **GitHub bio is empty.** Profile → Edit profile. Suggested: *ML / AI engineering
      and full-stack. Voice AI, RL environments, 3D data products.*
- [ ] **No pinned repositories.** Suggested pins: dhwani-desk, DataEngEnv, Terrain,
      neuroselect, PRO-TECHT, AI_ENGG.
- [ ] **Empty repo descriptions** on neuroselect, Terrain, DataEngEnv, AI_ENGG and others.
      Descriptions show in search, pins and link previews.
- [ ] **Portrait.** Your avatar is a side-on photo with a bright background, which limits
      any portrait style. For the cleanest result, add a plain-background headshot or a
      cartoon avatar as `assets/portrait.png`, then in `dashboard.py` set
      `PORTRAIT_CROP = (0, 0, 1, 1)`. With a cartoon avatar, also try `PORTRAIT_STYLE = "ascii"`.
      Pushing a portrait re-runs the workflow.
- [ ] **Caption and prompt.** Change `ROLE` and `PROMPT_USER` at the top of `dashboard.py`.
- [ ] **Removed from the old README:** Instagram, the view counter, the snake and the
      typing banner. The Medium link was also removed because the profile has no posts
      yet. Add it back to `./links.sh` when you publish.
- [ ] **Unrelated, but worth a look:** the `product-care-flow` README publishes demo
      login emails and passwords.

## Fallbacks

- **Generation fails** (API outage or rate limit): the workflow republishes the last
  good panels from `output`, so the README never shows a broken image once it has run.
- **Avatar or Pillow unavailable:** the portrait falls back to your initials.
- **Want third-party cards instead?** These were checked on 2026-10-16:
  - Stats and top languages: [`stats-organization/github-readme-stats-action@v2`](https://github.com/stats-organization/github-readme-stats-action).
    It runs in Actions. The public `github-readme-stats.vercel.app` instance is marked
    best-effort, and the original repo is no longer maintained.
  - Streaks: [`DenverCoder1/github-readme-streak-stats@v1`](https://github.com/DenverCoder1/github-readme-streak-stats)
    as an action, or `https://streak-stats.demolab.com/?user=Pranav-0710`.
  - Summary cards: `https://github-profile-summary-cards.vercel.app/api/cards/<card>?username=Pranav-0710`.
    It accepts `title_color`, `text_color`, `bg_color`, `border_color` and `chart_color`.
  - `github-readme-activity-graph.vercel.app` returned HTTP 402 (deployment paused). Avoid it.

## Run locally

```bash
pip install pillow
GITHUB_TOKEN=$(gh auth token) python .github/scripts/dashboard.py Pranav-0710 out/
```

A personal token sees your own private contribution counts, so local output can differ
from what the workflow publishes. Only the workflow's output is public.

## Verification checklist

- [ ] Actions run is green, and the `output` branch holds 6 SVGs.
- [ ] Desktop (dark): heatmap, whoami and languages panels render. No broken-image icons.
- [ ] Light mode: panels appear as dark cards with readable text.
- [ ] Phone (under 600px wide, or the GitHub mobile site): the narrow `-mobile` panels load,
      and the heatmap shows 26 weeks.
- [ ] Numbers match your public profile: contributions in the last year, followers,
      public repos.
- [ ] Every link opens: four project repos, Hugging Face Space and model, Terrain demo,
      LinkedIn, email.
