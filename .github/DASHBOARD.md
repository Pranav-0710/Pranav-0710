# Profile dashboard: how it works

The profile README is a terminal-style dashboard. The data panels are SVGs that a
GitHub Action draws from **public** GitHub data once a day and publishes to the
`output` branch. The hero, the four project panels, the prompts and the buttons are static
SVGs in `assets/`.

```
README.md                         layout, links and the "more projects" fold-out
assets/hero*.svg                  animated intro panel: name, role, pitch, stack summary (desktop + -mobile)
assets/project-*.svg              one wide panel per featured project: animated scene, three numbers, stack
assets/card-*.svg                 small looping illustrations used in the "more projects" fold-out
assets/footer*.svg                closing prompt over flowing wave lines
assets/prompt-*.svg               "jey@github ~ $ …" section prompts (desktop + -mobile)
assets/btn-*.svg                  link buttons
.github/scripts/static_assets.py  draws every SVG in assets/ except the buttons (stdlib only)
.github/scripts/dashboard.py      draws the data panels (stdlib + Pillow)
.github/workflows/dashboard.yml   runs dashboard.py daily, publishes to the output branch
```

## Data panels (rebuilt daily)

| panel | shows | data source |
| --- | --- | --- |
| `whoami` · portrait | Halftone portrait cropped from your avatar, name, role caption. It fades in and out on a 7 s loop. | Avatar URL from GraphQL; caption is the `ROLE` setting |
| `whoami` · stats | Current streak, longest streak, contributions, active days, best day, average per active day, contributions per month, then public repos, stars, followers and join date | `contributionsCollection.contributionCalendar`, plus `followers`, public repos and stargazers of public non-fork repos |
| `git log --since='30 days'` | Your latest 8 commits across public repos (repo, message, age), plus the five most active repos over 30 days with commit counts | `/users/<you>/repos`, then each repo's commits by you |
| `./contributions.sh` | 3D skyline, one bar per day, with the peak day labelled. The mobile version shows the last 26 weeks. | The same contribution calendar (GitHub's own day levels) |
| `./languages.sh` | Top six languages by share of bytes | `languages` of public non-fork repos (GitHub Linguist) |

Notes on the numbers:

- Streaks and totals cover the calendar window GitHub returns (the last year), so
  "longest streak" is the longest within that window, not all time.
- Skyline heights use a square-root scale, so one 100+ day does not flatten the other bars.
- The activity feed lists commits authored by your GitHub user in your own public, non-fork
  repos (the profile repo itself is skipped). Merge commits are left out, and a trailing
  `(#123)` is trimmed from messages.
- Third-party streak cards can show different streaks because they count days and
  windows differently.
- Notebook (`.ipynb`) bytes include cell outputs, which inflates Jupyter's share.
- The workflow uses the built-in `GITHUB_TOKEN`, so only public activity is counted.

## Project panels (static, edited by hand)

The four featured projects are drawn by `static_assets.py` from the `PROJECTS` list: DataEngEnv,
dhwani-desk, Terrain, neuroselect. Each entry holds the pill, one-sentence pitch, three numbers and
the stack chips. **Every number comes from that project's own README**, so update an entry when the
repo's numbers change, run `python .github/scripts/static_assets.py`, and commit the changed files in
`assets/`.

Current numbers and where they come from:

| project | numbers on the panel | source |
| --- | --- | --- |
| DataEngEnv | 4 stages · reward 0.25 → 0.38 · live Space | README: pipeline stages, "Training Results" (25-step GRPO run: first 5 steps vs last 5) |
| dhwani-desk | 30/34 hazards caught · department F1 0.71 · 1.5 s first reply | README "At a glance" table |
| Terrain | 3D globe · GDELT + RSS · 30-day scenario sim | README feature list |
| neuroselect | 306 MEG channels · 8 real trials · 50 Hz | README "Real subset" |

neuroselect's panel says "no benchmark claimed" because its README says no real-data CER/WER has been
reported yet. If that changes, update the panel.

## Setup

1. Commit and push this repo to `main`. The push includes the workflow file, which
   triggers its first run.
2. Open **Actions → Profile dashboard** and confirm the run is green. It publishes
   `contributions*.svg`, `whoami*.svg`, `pulse*.svg` and `languages*.svg` to the `output` branch.
3. Reload your profile. The panels refresh daily at 00:17 UTC, and you can run the
   workflow manually with **Run workflow**.

No secrets, PATs or external services are needed. The workflow asks for
`contents: write` only so it can push to the `output` branch.

## Manual configuration

- [ ] **Push and run the workflow.** Until the first run, the data panels 404.
- [ ] **GitHub bio is empty.** Profile → Edit profile. Suggested: *ML / AI engineering.
      Voice AI, LLM agents, RL environments, brain-to-text research.*
- [ ] **No pinned repositories.** Suggested pins: DataEngEnv, dhwani-desk, Terrain, neuroselect.
- [ ] **Empty repo descriptions** on DataEngEnv, Terrain, neuroselect and others. Descriptions show
      in search, pins and link previews.
- [ ] **Portrait.** Your avatar is a side-on photo with a bright background, so the halftone reads
      as a stylised head and hand at the mic. For the cleanest result, add a plain-background
      headshot as `assets/portrait.png` and set `PORTRAIT_CROP = (0, 0, 1, 1)` in `dashboard.py`.
      With a cartoon avatar, also try `PORTRAIT_STYLE = "ascii"`. Pushing a portrait re-runs the workflow.
- [ ] **Caption and prompt.** Change `ROLE` and `PROMPT_USER` at the top of `dashboard.py`.
- [ ] **Hero and prompts.** Drawn by `static_assets.py`; edit the text settings at the top and rerun it.
- [ ] **Animations.** GitHub removes scripts and CSS from READMEs, so all motion is CSS
      keyframes inside the SVGs. Visitors with "reduce motion" switched on keep the fades but
      lose the movement (scan line, bar grow-in, scene motion).
- [ ] **Activity feed shows public commit messages.** Anything you would not want read in a public
      commit message will appear there too, so keep commit messages tidy.
- [ ] **Removed from the old README:** Instagram, the view counter, the snake, the typing banner and
      the shields.io stack table (the hero already lists the stack). The Medium link was removed
      because the profile has no posts yet.
- [ ] **Unrelated, but worth a look:** the `product-care-flow` README publishes demo
      login emails and passwords.

## Fallbacks

- **Generation fails** (API outage or rate limit): the workflow republishes the last
  good panels from `output`, so the README never shows a broken image once it has run.
- **Activity feed fails but the rest works:** the other panels are published and the previous
  `pulse*.svg` stays in place.
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
python .github/scripts/static_assets.py     # rewrites assets/
```

A personal token sees your own private contribution counts, so local output can differ
from what the workflow publishes. Only the workflow's output is public.

## Verification checklist

- [ ] Actions run is green, and the `output` branch holds 8 SVGs.
- [ ] Desktop (dark): hero, whoami, four project panels, activity feed, skyline and languages render.
      No broken-image icons.
- [ ] Light mode: panels appear as dark cards with readable text.
- [ ] Phone (under 600px wide, or the GitHub mobile site): the narrow `-mobile` panels load,
      the project panels stack with the scene on top, and the skyline shows 26 weeks.
- [ ] Numbers match your public profile: contributions in the last year, followers, public repos.
- [ ] Project panel numbers still match each project's README.
- [ ] Every link opens: the four repos, Hugging Face Space, trained adapter and dataset, dhwani-desk
      demo video and pitch, Terrain demo, reliefroute, signal-hunters, planet-hunters, Krama,
      LinkedIn, email.
