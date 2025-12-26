#!/usr/bin/env python3
"""
Script to migrate blog posts from weblog/ structure to Jekyll _posts/ structure
"""
import os
import re
from pathlib import Path
from datetime import datetime

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = match.group(2)

    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body

def convert_post(source_path):
    """Convert a single post to Jekyll format"""
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    # Extract date
    date_str = frontmatter.get('Date') or frontmatter.get('date', '')
    # Handle different date formats
    if ' ' in date_str:
        date_str = date_str.split(' ')[0]  # Take just the date part

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print(f"Warning: Could not parse date for {source_path}, skipping...")
        return None

    # Extract title from first # heading in body
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else source_path.stem

    # Get tags
    tags_str = frontmatter.get('Tags') or frontmatter.get('tags', '')
    tags = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

    # Get slug
    slug = frontmatter.get('Slug') or frontmatter.get('slug', '')
    if slug.startswith('/'):
        slug = slug[1:]

    # Create new Jekyll frontmatter
    new_frontmatter = f"""---
layout: post
title: "{title}"
date: {date_obj.strftime('%Y-%m-%d')}
"""

    if tags:
        new_frontmatter += f"tags: {tags}\n"

    new_frontmatter += "---\n"

    # Create Jekyll filename: YYYY-MM-DD-title.md
    if slug:
        filename = f"{date_obj.strftime('%Y-%m-%d')}-{slug}.md"
    else:
        # Create slug from title
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        filename = f"{date_obj.strftime('%Y-%m-%d')}-{slug}.md"

    new_content = new_frontmatter + "\n" + body

    return filename, new_content

def main():
    """Main migration function"""
    weblog_dir = Path('weblog')
    posts_dir = Path('_posts')
    posts_dir.mkdir(exist_ok=True)

    # Find all markdown files in year directories
    post_files = []
    for year_dir in weblog_dir.glob('[0-9][0-9][0-9][0-9]'):
        if year_dir.is_dir():
            post_files.extend(year_dir.glob('*.md'))

    print(f"Found {len(post_files)} posts to migrate")

    for post_file in sorted(post_files):
        result = convert_post(post_file)
        if result:
            filename, content = result
            output_path = posts_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Migrated: {post_file} -> {output_path}")
        else:
            print(f"Skipped: {post_file}")

    print(f"\nMigration complete! {len(list(posts_dir.glob('*.md')))} posts in _posts/")

if __name__ == '__main__':
    main()
