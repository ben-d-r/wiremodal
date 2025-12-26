# Jekyll GitHub Pages Setup

This branch (`github-pages-setup`) contains the migration from omg.lol to GitHub Pages using Jekyll.

## What's Changed

### New Structure
- `_config.yml` - Jekyll configuration
- `_layouts/` - HTML templates (default, post, page)
- `_posts/` - All blog posts in Jekyll format (YYYY-MM-DD-title.md)
- `assets/css/` - Custom CSS styling
- `index.html` - Homepage with recent posts
- `archive.html` - All posts archive page
- `about.md` - About page
- `.github/workflows/jekyll.yml` - GitHub Actions workflow for deployment
- `Gemfile` - Ruby dependencies

### Migrated Posts
All 20 posts from `weblog/YYYY/*.md` have been migrated to `_posts/` with:
- Jekyll-compatible frontmatter (layout, title, date, tags)
- Proper filename format (YYYY-MM-DD-slug.md)
- Original content preserved

### Old Files (Still Present)
- `weblog/` - Original blog structure (can be deleted after confirming migration)
- `.github/workflows/main.yml` - Old omg.lol workflow (can be deleted)

## Next Steps to Enable GitHub Pages

1. **Commit and push this branch:**
   ```bash
   git add .
   git commit -m "Migrate to Jekyll and GitHub Pages"
   git push -u origin github-pages-setup
   ```

2. **Enable GitHub Pages in repository settings:**
   - Go to repository Settings → Pages
   - Under "Build and deployment":
     - Source: GitHub Actions
   - The Jekyll workflow will automatically build and deploy

3. **Merge to main (after testing):**
   ```bash
   git checkout main
   git merge github-pages-setup
   git push
   ```

4. **Clean up (optional):**
   - Delete `weblog/` directory
   - Delete `.github/workflows/main.yml`
   - Delete `migrate_posts.py` (migration script no longer needed)

## Testing Locally

If you want to test locally, you'll need Ruby installed:

```bash
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000`

## Customization

- **Styling:** Edit `assets/css/style.css`
- **Layout:** Edit files in `_layouts/`
- **Site info:** Edit `_config.yml`
- **Navigation:** Edit `_layouts/default.html`

## Reverting to omg.lol

If you want to go back to the original setup:

```bash
git checkout main
```

The old structure is preserved on the `main` branch.
