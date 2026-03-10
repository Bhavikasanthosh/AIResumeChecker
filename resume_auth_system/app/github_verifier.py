import requests

def extract_username(github_url):
    if github_url == "Not found" or not github_url:
        return None
    # Handles both 'github.com/user' and 'https://github.com/user'
    return github_url.rstrip("/").split("/")[-1]

def fetch_repositories(username):
    if not username:
        return []

    # Fetches all public repositories for the user
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        repos = response.json()
        detailed_repos = []
        
        for r in repos:
            detailed_repos.append({
                "name": r.get("name"),
                "description": r.get("description") or "",
                "language": r.get("language") or "Unknown",
                "topics": r.get("topics", []), # GitHub topics are great for skill matching
                "html_url": r.get("html_url"),
                "stars": r.get("stargazers_count", 0)
            })
        return detailed_repos
    except Exception:
        return []