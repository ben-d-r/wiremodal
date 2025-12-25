#!/usr/bin/env python3
"""
Fix tag format in posts from ['tag1', 'tag2'] to [tag1, tag2]
"""
import re
from pathlib import Path

def fix_tags_in_post(post_path):
    """Fix tag format in a post"""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match frontmatter and body
    match = re.match(r'^(---\s*\n)(.*?)(\n---\s*\n)(.*)$', content, re.DOTALL)
    if not match:
        return False

    before = match.group(1)
    frontmatter = match.group(2)
    after_fm = match.group(3)
    body = match.group(4)

    # Fix tags line - remove quotes from list items
    # From: tags: ['AI', 'ideas']
    # To: tags: [AI, ideas]
    frontmatter = re.sub(
        r"tags:\s*\[([^\]]+)\]",
        lambda m: "tags: [" + re.sub(r"'([^']+)'", r"\1", m.group(1)) + "]",
        frontmatter
    )

    new_content = before + frontmatter + after_fm + body

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    posts_dir = Path('_posts')
    post_files = list(posts_dir.glob('*.md'))

    print(f"Processing {len(post_files)} posts...")

    for post_file in sorted(post_files):
        if fix_tags_in_post(post_file):
            print(f"Fixed tags in {post_file.name}")

    print("Done!")

if __name__ == '__main__':
    main()
