# GitHub Issue Finder

A command-line tool that searches GitHub for open issues by language and label, then uses NVIDIA LLM to filter and summarize the ones that best match your coding level and interests. You can ask for more results, and dive deeper into any specific issue for a full, detailed analysis pulled directly from GitHub.

## Requirements

- Python 3.10 or newer
- A free GitHub account (for a personal access token)
- A free NVIDIA Build account (for API access to the LLMs used)

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

## 2. Create and activate a virtual environment

A virtual environment keeps this project's packages separate from anything else on your system.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
If PowerShell blocks the activation script, run this once first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked if your terminal prompt now starts with `(venv)`.

## 3. Install dependencies

```bash
pip install -r git_requirements.txt
```

## 4. Create your `.env` file

In the root of the project folder, create a new file named exactly `.env` (no filename before the dot) and add these two lines:

```
GITHUB_TOKEN=your_github_token_here
NVIDIA_API_KEY=your_nvidia_api_key_here
```

Replace each placeholder with your actual keys (see below for how to get them). Don't add quotes around the values.

**Important:** Never commit your `.env` file to GitHub — it should be listed in `.gitignore`.

### Getting a GitHub token

1. Log in to GitHub and go to **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** (or **Tokens (classic)**).
2. Click **Generate new token**.
3. Give it a name and an expiration date.
4. Under repository access, you can leave it scoped to public repositories only — this project only reads public issue data, it doesn't need write access.
5. Generate the token and copy it immediately — GitHub only shows it to you once.
6. Paste it as the value for `GITHUB_TOKEN` in your `.env` file.

### Getting an NVIDIA API key

1. Go to [build.nvidia.com](https://build.nvidia.com) and sign up for a free account (email and possibly phone verification required).
2. Once logged in, open your account settings (or open any model's page and click **Get API Key**).
3. Click **Generate Key**.
4. Copy the key — it will start with `nvapi-` — and save it somewhere safe, as it's typically only shown once.
5. Paste it as the value for `NVIDIA_API_KEY` in your `.env` file.

NVIDIA's free tier includes a limited number of inference credits and a rate limit, so if you run the tool heavily you may eventually need to check your usage on build.nvidia.com.

## 5. Run the program

With your virtual environment active and your `.env` file in place:

```bash
python git_issue_finder.py
```

Follow the prompts: pick a language, pick an issue label, then tell the AI what kind of issues you're looking for and your current skill level. From there you can ask for more results or dive deeper into any issue the AI mentioned for a full breakdown pulled directly from GitHub.

## Notes

- This tool only reads public GitHub data — it never modifies or writes anything to any repository.
- If you see `GITHUB THREW AN ERROR`, double-check your `GITHUB_TOKEN` is valid and hasn't expired.
- If the AI calls fail, double-check your `NVIDIA_API_KEY` and that you haven't exhausted your credits limit for the day.
