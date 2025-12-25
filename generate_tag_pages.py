#!/usr/bin/env python3
"""
Script to generate individual tag pages for Jekyll
"""
import re
from pathlib import Path
from collections import defaultdict

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def extract_tags_from_posts():
    """Extract all unique tags from posts"""
    tags = set()
    posts_dir = Path('_posts')

    for post_file in posts_dir.glob('*.md'):
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            # Find tags line
            tags_match = re.search(r'^tags:\s*(.+)$', frontmatter, re.MULTILINE)
            if tags_match:
                tags_value = tags_match.group(1).strip()
                # Parse tags (handle both list format ['tag1', 'tag2'] and simple format)
                if tags_value.startswith('['):
                    # List format
                    tag_list = re.findall(r"'([^']+)'", tags_value)
                else:
                    # Simple format (comma-separated or single)
                    tag_list = [t.strip() for t in tags_value.split(',')]

                tags.update(tag_list)

    return sorted(tags)

def create_tag_page(tag, tags_dir):
    """Create a page for a specific tag"""
    slug = slugify(tag)
    content = f"""---
layout: tag
title: "Posts tagged '{tag}'"
tag: {tag}
permalink: /tags/{slug}/
---
"""

    output_path = tags_dir / f"{slug}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created tag page: {output_path}")

def main():
    # Create tags directory
    tags_dir = Path('tags')
    tags_dir.mkdir(exist_ok=True)

    # Extract all tags
    all_tags = extract_tags_from_posts()

    print(f"Found {len(all_tags)} unique tags: {all_tags}")

    # Generate a page for each tag
    for tag in all_tags:
        create_tag_page(tag, tags_dir)

    print(f"\nGenerated {len(all_tags)} tag pages in tags/ directory")

if __name__ == '__main__':
    main()
