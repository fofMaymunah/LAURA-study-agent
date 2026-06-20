import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> list:
    """Search the web for a query and return results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                }
                for r in results
            ]
    except Exception as e:
        return [{"title": "search failed", "url": "", "snippet": str(e)}]


def read_webpage(url: str) -> str:
    """Read and extract text from webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in text.splitlines() if len(line.strip()) > 40]
        return "\n".join(lines[:100])

    except Exception as e:
        return f"Could not read page: {str(e)}"


def create_study_plan(subject: str, duration: str, level: str, resources: list) -> str:
    """Format a structured study plan from gathered resources."""
    plan = f"""
LAURA STUDY PLAN
================
Subject: {subject}
Duration: {duration}
Level: {level}

TOP RESOURCES FOUND:
"""
    for i, r in enumerate(resources, 1):
        plan += f"\n{i}. {r['title']}\n   {r['url']}\n   {r['snippet'][:200]}...\n"

    return plan

def is_relevant(subject: str, resource: dict) -> bool:
    """Quick check if a search result is actually related to the subject."""
    subject_words = [w.lower() for w in subject.split() if len(w) > 3]
    text_to_check = (resource.get("title", "") + " " + resource.get("snippet", "")).lower()
    return any(word in text_to_check for word in subject_words)