<!--
  Profile dashboard for github.com/Pranav-0710
  - output branch ........... panels rebuilt daily by .github/workflows/dashboard.yml (script: .github/scripts/dashboard.py)
  - assets/ ................. static hero panel, prompt lines and link buttons
  - .github/DASHBOARD.md .... how it works, setup, fallbacks, checklist
-->

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/hero-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/hero.svg" alt="jey@github ~ $ cat README.md: Jey Pranav, software developer working across ML / AI engineering and full-stack. I build software where models meet real users: voice AI, LLM agents, RL environments, 3D data products and brain-to-text research. Open to internships and collaborations." />
</picture>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/whoami-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/whoami.svg" alt="jey@github ~ $ whoami: dot-matrix portrait of Jey Pranav next to current and longest streak, contributions, active days, best day, average per active day, and contributions per month" />
</picture>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-now-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-now.svg" alt="jey@github ~ $ cat ~/now.md" />
</picture>

<table>
<tr>
<td width="33%" valign="top">

**building**<br />
[Krama](https://github.com/Pranav-0710/Krama): a small coding model that plans first, then codes, then explains why. LoRA fine-tune of Qwen2.5-Coder-1.5B for Python and FastAPI, with the test tasks and scoring rules fixed before training.

</td>
<td width="33%" valign="top">

**in development**<br />
[dhwani-desk](https://github.com/Pranav-0710/dhwani-desk): a Kannada-first voice helpline for civic complaints, for the Great Indian AI Internship Challenge (Gnani AI).

</td>
<td width="33%" valign="top">

**open to**<br />
Internships and collaborations in software engineering, ML / AI engineering and full-stack. [Email](mailto:pranavkanth07@gmail.com) or [LinkedIn](https://www.linkedin.com/in/jey-pranav-783761278/).

</td>
</tr>
</table>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-projects-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-projects.svg" alt="jey@github ~ $ ls ~/projects --featured" />
</picture>

<table>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/reliefroute"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-reliefroute.svg" alt="Animation: a truck's route is redrawn around a flooded road" /></a>

#### [reliefroute](https://github.com/Pranav-0710/reliefroute)
<sub>Agent Wars · GDG DevFest 2026</sub>

Flood-relief logistics agent for Chennai. It reads field reports as text, photos or voice notes in English, Tamil, Tanglish or Hindi, plans truck routes on real road distances around reported floods, replans when a road is blocked mid-delivery, and learns from each run. Also exposed as an MCP server.

`Python` `FastAPI` `Gemini` `PyTorch` `OpenEnv` `MCP` `Docker`

<sub>[live app](https://reliefroute.vercel.app)</sub>

</td>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/dhwani-desk"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-dhwani-desk.svg" alt="Animation: a caller's voice passes through transcribe, decide and speak stages" /></a>

#### [dhwani-desk](https://github.com/Pranav-0710/dhwani-desk)
<sub>`status: in development` · Great Indian AI Internship Challenge (Gnani AI)</sub>

Kannada-first voice helpline for civic complaints. Gnani Prisma transcribes the caller, the Laya engine decides department, ward, urgency and when a human must step in (locally, no LLM in the call path), and Gnani Timbre speaks the reply. A supervisor console lets an officer take over a call.

`Python` `FastAPI` `React` `TypeScript` `Vite` `Laya`

<sub>my part: voice pipeline and serving</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/DataEngEnv"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-dataengenv.svg" alt="Animation: four failing pipeline stages turn green as a reward bar fills" /></a>

#### [DataEngEnv · PipelineOps Arena](https://github.com/Pranav-0710/DataEngEnv)
<sub>Meta AI × Hugging Face OpenEnv Hackathon 2026</sub>

A four-stage OpenEnv environment where an LLM agent repairs a broken ML pipeline: schema drift, unscaled features, data leakage, then a fairness gate. Rewards come from actually running the fixed script, not from an LLM judge.

`Python` `FastAPI` `Docker` `OpenEnv` `Unsloth` `LoRA` `GRPO`

<sub>[live Space](https://huggingface.co/spaces/CoBeDigger/DataEngEnv) · [trained adapter](https://huggingface.co/CoBeDigger/pipelineops-arena-llama3-grpo)</sub>

</td>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/signal-hunters"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-signal-hunters.svg" alt="Animation: a drifting line appears only in the ON panels of a radio-telescope cadence" /></a>

#### [signal-hunters](https://github.com/Pranav-0710/signal-hunters)
<sub>Hack4Hack ML Challenge 2026, Round 2 · Team Cyclops</sub>

Classifies SETI ON/OFF radio-telescope cadences into 9 classes when the training data comes from one telescope and the test set from another. A stack of 11 models (LightGBM on hand-built features, CNNs and EfficientNets) took public macro-F1 from 0.7884 to 0.9088.

`Python` `LightGBM` `PyTorch` `timm` `scikit-learn`

<sub>Round 1: [planet-hunters](https://github.com/Pranav-0710/planet-hunters) · 0.7564 public macro-F1 on TESS-like light curves</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/Terrain"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-terrain.svg" alt="Animation: a rotating globe feeds a list comparing how outlets frame one story" /></a>

#### [Terrain](https://github.com/Pranav-0710/Terrain)
<sub>built for an OpenAI hackathon</sub>

News-intelligence platform that maps live events onto a 3D WebGL globe and compares how outlets around the world frame the same story, with LLM-based consensus and contradiction analysis over GDELT and RSS feeds.

`Next.js` `React` `Three.js` `FastAPI` `Supabase` `PostGIS`

<sub>[live demo](https://terrain-green.vercel.app)</sub>

</td>
<td width="50%" valign="top">

<a href="https://github.com/Pranav-0710/neuroselect"><img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/card-neuroselect.svg" alt="Animation: scrolling MEG traces feed character slots scanned one at a time" /></a>

#### [neuroselect](https://github.com/Pranav-0710/neuroselect)
<sub>`status: baseline stage` · research codebase</sub>

Reproducible groundwork for non-invasive brain-to-text decoding: a character-level CTC baseline on public SpanishBCBL MEG recordings, with documented label-mapping, alignment and CTC-geometry audits. No benchmark claimed yet.

`Python` `PyTorch` `MNE` `NumPy` `SciPy` `pytest`

</td>
</tr>
</table>

<details>
<summary><b>more in ~/projects</b></summary>
<br />

| repo | what it is | stack |
| --- | --- | --- |
| [PRO-TECHT](https://github.com/Pranav-0710/PRO-TECHT) | Service-center portal: job tracking, warranties, customer chat, reports, role-based views | React · TypeScript · shadcn/ui · Supabase |
| [AI_ENGG](https://github.com/Pranav-0710/AI_ENGG) | AI engineering roadmap (15 projects, 5 phases) with Claude Code hooks that block AI edits to core logic | Bash · Python |
| [ChurnPrediction-](https://github.com/Pranav-0710/ChurnPrediction-) | Telco churn classifier with a Streamlit app and a Power BI report | scikit-learn · Streamlit · Power BI |
| [SalesPrediction](https://github.com/Pranav-0710/SalesPrediction) | 24-month retail sales forecast with confidence intervals | pandas · Prophet · Power BI |
| [f1-MODEL](https://github.com/Pranav-0710/f1-MODEL) | My first ML project: Formula 1 prediction notebook | pandas · scikit-learn |

</details>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/contributions-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/contributions.svg" alt="jey@github ~ $ ./contributions.sh: contribution heatmap for the last year, one green square per day" />
</picture>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/languages-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/output/languages.svg" alt="jey@github ~ $ ./languages.sh: share of code by language across public repositories" />
</picture>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-stack-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-stack.svg" alt="jey@github ~ $ cat ~/.stack" />
</picture>

| layer | tools |
| --- | --- |
| `languages` | <img src="https://img.shields.io/badge/Python-161b22?style=flat-square&logo=python&logoColor=39d353" alt="Python" /> <img src="https://img.shields.io/badge/TypeScript-161b22?style=flat-square&logo=typescript&logoColor=39d353" alt="TypeScript" /> <img src="https://img.shields.io/badge/JavaScript-161b22?style=flat-square&logo=javascript&logoColor=39d353" alt="JavaScript" /> <img src="https://img.shields.io/badge/SQL-161b22?style=flat-square&logo=postgresql&logoColor=39d353" alt="SQL" /> <img src="https://img.shields.io/badge/Bash-161b22?style=flat-square&logo=gnubash&logoColor=39d353" alt="Bash" /> |
| `ml · data` | <img src="https://img.shields.io/badge/PyTorch-161b22?style=flat-square&logo=pytorch&logoColor=39d353" alt="PyTorch" /> <img src="https://img.shields.io/badge/scikit--learn-161b22?style=flat-square&logo=scikitlearn&logoColor=39d353" alt="scikit-learn" /> <img src="https://img.shields.io/badge/pandas-161b22?style=flat-square&logo=pandas&logoColor=39d353" alt="pandas" /> <img src="https://img.shields.io/badge/NumPy-161b22?style=flat-square&logo=numpy&logoColor=39d353" alt="NumPy" /> <img src="https://img.shields.io/badge/Jupyter-161b22?style=flat-square&logo=jupyter&logoColor=39d353" alt="Jupyter" /><br /><sub>also: LightGBM · timm · Prophet · MNE · Matplotlib · Seaborn</sub> |
| `llm · agents` | <img src="https://img.shields.io/badge/Hugging%20Face-161b22?style=flat-square&logo=huggingface&logoColor=39d353" alt="Hugging Face" /> <img src="https://img.shields.io/badge/Claude%20Code-161b22?style=flat-square&logo=claude&logoColor=39d353" alt="Claude Code" /><br /><sub>also: Unsloth · LoRA / GRPO fine-tuning · OpenEnv · MCP · Gemini, Groq and OpenAI APIs</sub> |
| `backend` | <img src="https://img.shields.io/badge/FastAPI-161b22?style=flat-square&logo=fastapi&logoColor=39d353" alt="FastAPI" /> <img src="https://img.shields.io/badge/PostgreSQL-161b22?style=flat-square&logo=postgresql&logoColor=39d353" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Supabase-161b22?style=flat-square&logo=supabase&logoColor=39d353" alt="Supabase" /><br /><sub>also: Pydantic · PostGIS · Uvicorn</sub> |
| `frontend` | <img src="https://img.shields.io/badge/React-161b22?style=flat-square&logo=react&logoColor=39d353" alt="React" /> <img src="https://img.shields.io/badge/Next.js-161b22?style=flat-square&logo=nextdotjs&logoColor=39d353" alt="Next.js" /> <img src="https://img.shields.io/badge/Vite-161b22?style=flat-square&logo=vite&logoColor=39d353" alt="Vite" /> <img src="https://img.shields.io/badge/Tailwind%20CSS-161b22?style=flat-square&logo=tailwindcss&logoColor=39d353" alt="Tailwind CSS" /> <img src="https://img.shields.io/badge/Three.js-161b22?style=flat-square&logo=threedotjs&logoColor=39d353" alt="Three.js" /><br /><sub>also: shadcn/ui · Framer Motion</sub> |
| `ship · test` | <img src="https://img.shields.io/badge/Docker-161b22?style=flat-square&logo=docker&logoColor=39d353" alt="Docker" /> <img src="https://img.shields.io/badge/GitHub%20Actions-161b22?style=flat-square&logo=githubactions&logoColor=39d353" alt="GitHub Actions" /> <img src="https://img.shields.io/badge/Vercel-161b22?style=flat-square&logo=vercel&logoColor=39d353" alt="Vercel" /> <img src="https://img.shields.io/badge/pytest-161b22?style=flat-square&logo=pytest&logoColor=39d353" alt="pytest" /><br /><sub>also: Vitest · Hugging Face Spaces · Render · Git</sub> |
| `analytics` | <img src="https://img.shields.io/badge/Streamlit-161b22?style=flat-square&logo=streamlit&logoColor=39d353" alt="Streamlit" /><br /><sub>also: Power BI</sub> |

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-links-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/prompt-links.svg" alt="jey@github ~ $ ./links.sh" />
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/jey-pranav-783761278/"><img src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/btn-linkedin.svg" height="36" alt="LinkedIn: linkedin.com/in/jey-pranav-783761278" /></a>
  &nbsp;
  <a href="mailto:pranavkanth07@gmail.com"><img src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/btn-email.svg" height="36" alt="Email: pranavkanth07@gmail.com" /></a>
</p>

<p align="center"><sub>linkedin.com/in/jey-pranav-783761278 · pranavkanth07@gmail.com</sub></p>

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/footer-mobile.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Pranav-0710/Pranav-0710/main/assets/footer.svg" alt="jey@github ~ $ echo &quot;thanks for stopping by&quot;" />
</picture>
