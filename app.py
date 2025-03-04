import os
from collections import Counter

from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from github import Github, GithubException, RateLimitExceededException
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-for-flash-messages")
g = Github(os.getenv("GITHUB_TOKEN"))

def validate_github_username(username):
    """Validate if the string is a valid GitHub username."""
    # GitHub username rules: alphanumeric with hyphens, no more than 39 characters
    pattern = r'^[a-zA-Z0-9-]{1,39}$'
    return re.match(pattern, username) is not None

def get_user_skills(username):
    try:
        user = g.get_user(username)
        # Test that the user exists by accessing a property
        _ = user.login
        
        # Get repositories, limited to 100 to avoid performance issues
        repos = list(user.get_repos()[:100])
        
        languages = [repo.language for repo in repos if repo.language]
        lang_counter = Counter(languages)
        return [lang for lang, _ in lang_counter.most_common(3)]
    except RateLimitExceededException:
        raise Exception("GitHub API rate limit exceeded. Please try again later.")
    except GithubException as e:
        if e.status == 404:
            raise Exception(f"GitHub user '{username}' not found.")
        else:
            raise Exception(f"GitHub API error: {str(e)}")

def find_good_first_issues(skills, min_stars=50):
    issues = []
    
    if not skills:
        return issues
        
    try:
        for skill in skills:
            # Fix: Added is:issue to the query as required by GitHub API
            query = f'is:issue is:open label:"good first issue" language:{skill}'
            result = g.search_issues(query=query)
            count = 0
            
            for issue in result:
                if count >= 5:  # Limit to 5 issues per skill
                    break
                    
                if issue.repository.stargazers_count >= min_stars:
                    issues.append({
                        'title': issue.title,
                        'html_url': issue.html_url,
                        'repository': {
                            'full_name': issue.repository.full_name,
                            'language': skill,
                            'stars': issue.repository.stargazers_count
                        },
                        'labels': [label.name for label in issue.labels]
                    })
                    count += 1
        
        return issues
    except RateLimitExceededException:
        raise Exception("GitHub API rate limit exceeded. Please try again later.")
    except GithubException as e:
        raise Exception(f"GitHub API error: {str(e)}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find-issues', methods=['POST'])
def find_issues():
    username = request.form.get('username', '').strip()
    
    if not username:
        flash('Please enter a GitHub username', 'error')
        return redirect(url_for('home'))
        
    if not validate_github_username(username):
        flash('Invalid GitHub username format', 'error')
        return redirect(url_for('home'))
    
    try:
        skills = get_user_skills(username)
        
        if not skills:
            flash('No programming languages detected in your public repositories', 'warning')
            return render_template('issues.html', issues=[], skills=[], username=username)
            
        issues = find_good_first_issues(skills, min_stars=50)
        
        return render_template('issues.html', 
                               issues=issues, 
                               skills=skills, 
                               username=username)
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
