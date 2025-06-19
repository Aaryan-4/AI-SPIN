import requests
from bs4 import BeautifulSoup
import difflib
import uuid
from datetime import datetime

# In-memory store for content versions
version_store = []

def fetch_content_from_url(url):
    """https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1."""
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request fails
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract paragraphs text
    paragraphs = soup.find_all('p')
    text = '\n'.join(p.get_text(strip=True) for p in paragraphs)
    return text.strip()

def ai_spin(content, style="neutral"):
    """Simulate AI-driven spin (placeholder)."""
    # Replace this with an actual AI API call in production
    spun = f"[AI-{style}]: " + content[::-1]  # simple reversal demo
    return spun

def save_version(content, author="Aaryan", status="draft"):
    """Save a version of the content in memory."""
    version_id = str(uuid.uuid4())
    version = {
        "version_id": version_id,
        "timestamp": datetime.utcnow().isoformat(),
        "author": author,
        "content": content,
        "status": status,
    }
    version_store.append(version)
    print(f"Saved version {version_id} by {author} with status '{status}'")
    return version_id

def diff_versions(old, new):
    """Return a unified diff between two text versions."""
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    diff = difflib.unified_diff(old_lines, new_lines, fromfile='Old Version', tofile='New Version', lineterm='')
    return '\n'.join(diff)

def get_version_by_id(version_id):
    for v in version_store:
        if v["version_id"] == version_id:
            return v
    return None

def run_workflow():
    url = input("Enter the URL to fetch content: ").strip()
    try:
        original = fetch_content_from_url(url)
        print("\n[Original Content Preview]\n", original[:500], "...\n")

        v0_id = save_version(original, author="system", status="fetched")

        style = input("Enter AI spin style (e.g., casual, formal, neutral): ").strip() or "neutral"
        spun = ai_spin(original, style=style)
        print("\n[AI-Spun Content Preview]\n", spun[:500], "...\n")

        v1_id = save_version(spun, author="AI", status="spun")

        print("Edit the spun content below. Type 'no' to skip editing:")
        human_edit = input()
        if human_edit.lower() != "no" and human_edit.strip() != "":
            edited_content = human_edit
        else:
            edited_content = spun

        v2_id = save_version(edited_content, author="editor", status="edited")

        print("\n[Diff Between AI and Human Edit]\n")
        diff = diff_versions(spun, edited_content)
        print(diff or "No differences.")

    except requests.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_workflow()
