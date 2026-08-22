import os
import re
import sys
import glob
import json
import hashlib
from datetime import datetime, timezone
import yaml
import requests

# Base URL for canonical post link
BASE_URL = "https://4d4cat.com"

# Velog GraphQL Endpoint
VELOG_GRAPHQL_URL = "https://v2.velog.io/graphql"

# Paths
POSTS_DIR = os.path.join("content", "posts")
SYNC_STATE_FILE = ".velog_sync.json"

WRITE_POST_MUTATION = """
mutation WritePost(
  $title: String,
  $body: String,
  $tags: [String],
  $is_markdown: Boolean,
  $is_temp: Boolean,
  $is_private: Boolean,
  $url_slug: String
) {
  writePost(
    title: $title,
    body: $body,
    tags: $tags,
    is_markdown: $is_markdown,
    is_temp: $is_temp,
    is_private: $is_private,
    url_slug: $url_slug
  ) {
    id
    title
    url_slug
  }
}
"""

EDIT_POST_MUTATION = """
mutation EditPost(
  $id: ID!,
  $title: String,
  $body: String,
  $tags: [String],
  $is_markdown: Boolean,
  $is_temp: Boolean,
  $is_private: Boolean,
  $url_slug: String
) {
  editPost(
    id: $id,
    title: $title,
    body: $body,
    tags: $tags,
    is_markdown: $is_markdown,
    is_temp: $is_temp,
    is_private: $is_private,
    url_slug: $url_slug
  ) {
    id
    title
    url_slug
  }
}
"""


def load_sync_state():
    if os.path.exists(SYNC_STATE_FILE):
        try:
            with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Failed to load sync state file: {e}")
    return {}


def save_sync_state(state):
    try:
        with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"[Info] Saved updated sync state to {SYNC_STATE_FILE}")
    except Exception as e:
        print(f"[Error] Failed to save sync state file: {e}")


def parse_hugo_post(file_path):
    """
    Parses Hugo Markdown file to extract frontmatter and body.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Frontmatter regex split (--- ... ---)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None

    frontmatter_raw, body = match.group(1), match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_raw) or {}
    except Exception as e:
        print(f"[Warning] YAML parse error in {file_path}: {e}")
        return None

    # Check draft status
    if frontmatter.get("draft", False):
        return None

    title = frontmatter.get("title")
    if not title:
        # Fallback to filename without extension
        title = os.path.splitext(os.path.basename(file_path))[0]

    # Tags handling
    raw_tags = frontmatter.get("tags", [])
    if isinstance(raw_tags, str):
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
    elif isinstance(raw_tags, list):
        tags = [str(t).strip() for t in raw_tags if str(t).strip()]
    else:
        tags = []

    # Clean body: convert relative URLs for images and links to absolute using BASE_URL
    def to_absolute_url(url):
        if not url:
            return url
        if url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("data:") or url.startswith("#") or url.startswith("mailto:"):
            return url
        cleaned = re.sub(r'^\.?\/+', '', url)
        return f"{BASE_URL}/{cleaned}"

    def replace_md_image_or_link(m):
        prefix = m.group(1)
        label = m.group(2)
        url = m.group(3).strip()
        abs_url = to_absolute_url(url)
        return f"{prefix}{label}]({abs_url})"

    # Replace Markdown image/link syntax: ![alt](url) and [label](url)
    body_cleaned = re.sub(r'(!?\[)(.*?)\]\((.*?)\)', replace_md_image_or_link, body)

    # Replace HTML <img src="..."> tags
    def replace_html_img_src(m):
        attr_name = m.group(1)
        quote = m.group(2)
        url = m.group(3)
        abs_url = to_absolute_url(url)
        return f'{attr_name}{quote}{abs_url}{quote}'

    body_cleaned = re.sub(r'(src=)(["\'])(.*?)\2', replace_html_img_src, body_cleaned)

    # Remove Hugo shortcodes (e.g. {{< ... >}} or {{% ... %}})
    body_cleaned = re.sub(r'\{\{<.*?>\}\}', '', body_cleaned)
    body_cleaned = re.sub(r'\{\{%.*?%\}\}', '', body_cleaned)

    # Generate canonical URL
    rel_path = os.path.relpath(file_path, "content")
    path_without_ext = os.path.splitext(rel_path)[0].replace("\\", "/")
    canonical_url = f"{BASE_URL}/{path_without_ext}/"

    # Append source link footer
    body_with_footer = body_cleaned.strip() + f"\n\n---\n> 📌 *이 포스트는 [{BASE_URL.replace('https://', '')}]({canonical_url})에 원본이 게시된 글입니다.*"

    # Slug for Velog
    filename_slug = os.path.splitext(os.path.basename(file_path))[0]
    url_slug = frontmatter.get("slug", filename_slug)
    # Sanitize url_slug for Velog (allow lowercase, numbers, hyphens, korean chars)
    url_slug = re.sub(r'[^a-zA-Z0-9\-가-힣]', '-', url_slug).strip('-')

    return {
        "file_path": file_path,
        "title": str(title),
        "tags": tags,
        "body": body_with_footer,
        "canonical_url": canonical_url,
        "url_slug": url_slug
    }


def compute_content_hash(parsed_post):
    data = f"{parsed_post['title']}|{','.join(parsed_post['tags'])}|{parsed_post['body']}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def send_graphql_request(query, variables, token, refresh_token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": f"access_token={token}" + (f"; refreshToken={refresh_token}" if refresh_token else ""),
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "query": query,
        "variables": variables
    }

    res = requests.post(VELOG_GRAPHQL_URL, json=payload, headers=headers, timeout=15)
    res.raise_for_status()
    return res.json()


def sync_to_velog(parsed_post, existing_state, token, refresh_token=None, dry_run=False):
    file_path = parsed_post["file_path"]
    content_hash = compute_content_hash(parsed_post)
    prev_state = existing_state.get(file_path, {})

    if not dry_run and prev_state.get("content_hash") == content_hash and prev_state.get("velog_id"):
        print(f"[Skip] Unchanged: {file_path}")
        return prev_state

    is_update = bool(prev_state.get("velog_id"))

    variables = {
        "title": parsed_post["title"],
        "body": parsed_post["body"],
        "tags": parsed_post["tags"],
        "is_markdown": True,
        "is_temp": False,
        "is_private": False,
        "url_slug": parsed_post["url_slug"]
    }

    if is_update:
        variables["id"] = prev_state["velog_id"]
        mutation = EDIT_POST_MUTATION
        action_name = "Update"
    else:
        mutation = WRITE_POST_MUTATION
        action_name = "Publish"

    print(f"[{action_name}] {parsed_post['title']} ({file_path})")

    if dry_run:
        print(f"  [Dry Run] Would execute {action_name} for slug: {parsed_post['url_slug']}")
        return {
            "velog_id": prev_state.get("velog_id", "dry-run-id"),
            "velog_url_slug": parsed_post["url_slug"],
            "content_hash": content_hash,
            "synced_at": datetime.now(timezone.utc).isoformat()
        }

    try:
        res = send_graphql_request(mutation, variables, token, refresh_token)

        if "errors" in res:
            print(f"  [Error] Velog API error for {file_path}: {res['errors']}")
            return prev_state

        data = res.get("data", {})
        post_data = data.get("editPost") if is_update else data.get("writePost")

        if not post_data or not post_data.get("id"):
            print(f"  [Error] Velog returned null post response: {res}")
            return prev_state

        velog_id = post_data["id"]
        url_slug = post_data.get("url_slug", parsed_post["url_slug"])
        print(f"  [Success] Velog post ID: {velog_id}, slug: {url_slug}")

        return {
            "velog_id": velog_id,
            "velog_url_slug": url_slug,
            "content_hash": content_hash,
            "synced_at": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        print(f"  [Exception] Failed to sync {file_path}: {e}")
        return prev_state


def main():
    token = os.environ.get("VELOG_ACCESS_TOKEN")
    refresh_token = os.environ.get("VELOG_REFRESH_TOKEN")
    dry_run_env = os.environ.get("DRY_RUN", "false").lower() in ("true", "1", "yes")
    force_sync = os.environ.get("FORCE_SYNC", "false").lower() in ("true", "1", "yes")

    if not token and not dry_run_env:
        print("[Error] VELOG_ACCESS_TOKEN environment variable is missing.")
        sys.exit(1)

    sync_state = load_sync_state()
    if force_sync:
        print("[Info] FORCE_SYNC enabled. Will re-evaluate all posts.")

    # Find all post files
    pattern = os.path.join(POSTS_DIR, "**", "*.md")
    files = glob.glob(pattern, recursive=True)

    print(f"[Info] Found {len(files)} markdown post files in {POSTS_DIR}")

    updated_count = 0
    state_changed = False

    for file_path in sorted(files):
        # Normalizing path separators
        file_path_normalized = file_path.replace("\\", "/")
        parsed = parse_hugo_post(file_path)
        if not parsed:
            continue

        if force_sync and file_path_normalized in sync_state:
            # Clear stored hash to force update
            sync_state[file_path_normalized]["content_hash"] = ""

        new_post_state = sync_to_velog(parsed, sync_state, token, refresh_token, dry_run=dry_run_env)

        if new_post_state and new_post_state != sync_state.get(file_path_normalized):
            sync_state[file_path_normalized] = new_post_state
            state_changed = True
            updated_count += 1

    if state_changed and not dry_run_env:
        save_sync_state(sync_state)

    print(f"[Complete] Processed {len(files)} files. Updated/Synced: {updated_count}")


if __name__ == "__main__":
    main()
