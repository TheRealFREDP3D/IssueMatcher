# IssueMatcher v0.1 - Prototype

IssueMatcher is a tool that helps developers find "good first issues" on GitHub based on their programming language skills. It analyzes your GitHub repositories to determine your primary programming languages and recommends issues that match your abilities.

## Features

- Automatic skill detection based on your GitHub repository languages
- Smart filtering of "good first issues" matching your programming skills
- Repository star count filtering to surface issues from established projects
- Simple web interface built with Flask
- GitHub API integration using PyGithub

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- GitHub account
- GitHub personal access token (optional, but recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/TheRealFREDP3D/IssueMatcher
cd issuematcher
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask pygithub
```

## Configuration

To avoid GitHub API rate limits, it's recommended to use a personal access token:

1. Create a token at https://github.com/settings/tokens
2. Required scope: `public_repo`
3. Set your token in `app.py`:
```python
github_token = "your_token_here"
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://127.0.0.1:5000`
3. Enter your GitHub username
4. View recommended issues based on your programming skills

## How It Works

1. Analyzes your public GitHub repositories
2. Identifies your primary programming languages
3. Searches for "good first issues" in repositories using those languages
4. Filters issues from repositories with significant star counts
5. Presents a curated list of issues matching your skills

## Additional Features (TODO)

Here are some ideas I have on my todo list:

**User Preferences:** Add form fields for users to specify interests (e.g., "I prefer documentation tasks" or "I want web development issues").
**Implementation:** Modify the search query to include keywords like "documentation".

**Skill Weighting:** Beyond language frequency, weigh skills by repository size or commit count for accuracy.
**Implementation:** Use repo.size or fetch commit data with repo.get_commits().

**Caching:** Store API results temporarily to speed up repeated searches.
**Implementation:** Use Flask-Caching (pip install flask-caching).

**GitHub Login:** Allow users to authenticate with GitHub for private repo access.
**Implementation:** Integrate Flask-Dance for OAuth.

**Issue Details:** Display more info (e.g., issue description, comment count).
**Implementation:** Pass additional attributes like issue.body to the template.

## Final Thoughts

This Flask prototype demonstrates a functional "Good First Issue" finder:
It identifies user skills from their GitHub repositories.

It finds relevant beginner-friendly issues based on those skills.

It includes error handling and a simple UI.

## Media

Podcast by NotebookLM

<audio controls src="assets/issue-matcher-podcast.wav" title="Title"></audio>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT] - See LICENSE file for details