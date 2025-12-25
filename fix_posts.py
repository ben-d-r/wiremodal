#!/usr/bin/env python3
"""
Script to remove duplicate H1 headings from Jekyll posts
"""
import re
from pathlib import Path

def fix_post(post_path):
    """Remove the first H1 heading if it duplicates the title"""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match frontmatter and body
    match = re.match(r'^(---\s*\n.*?\n---\s*\n)(.*)$', content, re.DOTALL)
    if not match:
        print(f"Warning: No frontmatter found in {post_path}")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # Remove leading newlines
    body = body.lstrip('\n')

    # Check if body starts with an H1
    h1_match = re.match(r'^#\s+(.+?)\s*\n', body)
    if h1_match:
        # Remove the H1 and any following blank lines
        body = re.sub(r'^#\s+.+?\s*\n+', '', body)
        print(f"Removed H1 from {post_path.name}")

    # Write back
    new_content = frontmatter + '\n' + body
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    posts_dir = Path('_posts')
    post_files = list(posts_dir.glob('*.md'))

    print(f"Processing {len(post_files)} posts...")

    for post_file in sorted(post_files):
        fix_post(post_file)

    print("Done!")

if __name__ == '__main__':
    main()
