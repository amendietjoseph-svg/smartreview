#!/usr/bin/env python3
"""Batch-update SmartReview HTML pages to the new app-wrapper layout."""

import re
from pathlib import Path

FRONTEND = Path(__file__).parent / "frontend"

PAGES = [
    "journal.html", "calendar.html", "stats.html", "coach.html", "accounts.html",
    "notes.html", "backtesting.html", "marketplace.html", "community.html",
    "podcasts.html", "live.html", "copy-trading.html", "strategy-builder.html",
    "settings.html", "help.html",
]

LAYOUT_SCRIPT = '<script src="/js/layout.js"></script>'

# Match from app-container through end of sidebar
OLD_LAYOUT_RE = re.compile(
    r'<div class="app-container">\s*'
    r'(?:<!--.*?-->\s*)?'
    r'<aside class="sidebar">.*?</aside>\s*',
    re.DOTALL,
)

def ensure_layout_script(html: str) -> str:
    if '/js/layout.js' in html:
        return html
    if '<script>lucide.createIcons();</script>' in html:
        return html.replace(
            '<script>lucide.createIcons();</script>',
            LAYOUT_SCRIPT + '\n    <script>lucide.createIcons();</script>',
        )
    return html.replace('</body>', f'    {LAYOUT_SCRIPT}\n</body>')


def wrap_main_content(html: str) -> str:
    """Wrap main-content in app-wrapper if not already."""
    if 'id="appWrapper"' in html:
        return html

    html = html.replace(
        '<main class="main-content">',
        '<div id="app-layout-root"></div>\n    <div class="app-wrapper" id="appWrapper">\n        <main class="main-content">',
        1,
    )

    # Close app-wrapper after first </main>
    html = re.sub(
        r'(</main>)(\s*(?:<!--.*?-->\s*)*)',
        r'\1\n    </div>\2',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Remove stray app-container closing div if present right after app-wrapper close
    html = re.sub(r'</div>\s*</div>\s*(<!-- New Trade|<div class="modal")', r'</div>\n    \1', html, count=1)

    return html


def process_file(path: Path) -> bool:
    html = path.read_text(encoding='utf-8')
    if 'class="app-container"' not in html:
        print(f"  skip (no app-container): {path.name}")
        return False

    new_html = OLD_LAYOUT_RE.sub('', html, count=1)
    if new_html == html:
        print(f"  skip (pattern not matched): {path.name}")
        return False

    new_html = wrap_main_content(new_html)
    new_html = ensure_layout_script(new_html)

    path.write_text(new_html, encoding='utf-8')
    print(f"  updated: {path.name}")
    return True


def main():
    for name in PAGES:
        process_file(FRONTEND / name)
    print("Done.")


if __name__ == '__main__':
    main()
