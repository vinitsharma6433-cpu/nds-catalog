#!/usr/bin/env python3
"""
WhatsApp Link Preview Validator
Run this BEFORE pushing to GitHub to catch issues.
"""

import re, sys

def validate_index_html(filepath="index.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    issues = []
    checks = []

    # 1. Check og:title
    if 'property="og:title"' in html:
        checks.append("✓ og:title present")
    else:
        issues.append("✗ MISSING: og:title")

    # 2. Check og:description
    if 'property="og:description"' in html:
        checks.append("✓ og:description present")
    else:
        issues.append("✗ MISSING: og:description")

    # 3. Check og:image
    if 'property="og:image"' in html:
        checks.append("✓ og:image present")
        # Extract URL
        m = re.search(r'property="og:image"[^>]*content="([^"]+)"', html)
        if m:
            img_url = m.group(1)
            checks.append(f"  → Image URL: {img_url}")
            if img_url.startswith("http"):
                checks.append("  → URL is absolute (good)")
            else:
                issues.append("✗ BAD: og:image URL is relative, must be absolute (https://...)")
        else:
            issues.append("✗ BAD: og:image content not found")
    else:
        issues.append("✗ MISSING: og:image")

    # 4. Check og:image:width
    if 'property="og:image:width"' in html:
        checks.append("✓ og:image:width present")
    else:
        issues.append("✗ MISSING: og:image:width (WhatsApp NEEDS this)")

    # 5. Check og:image:height
    if 'property="og:image:height"' in html:
        checks.append("✓ og:image:height present")
    else:
        issues.append("✗ MISSING: og:image:height (WhatsApp NEEDS this)")

    # 6. Check og:url
    if 'property="og:url"' in html:
        checks.append("✓ og:url present")
    else:
        issues.append("✗ MISSING: og:url")

    # 7. Check Schema.org thumbnail
    if 'itemprop="thumbnailUrl"' in html:
        checks.append("✓ Schema.org thumbnailUrl present")
    else:
        issues.append("⚠ WARNING: Schema.org thumbnailUrl missing (recommended)")

    # 8. Check twitter:card
    if 'name="twitter:card"' in html:
        checks.append("✓ twitter:card present")
    else:
        issues.append("⚠ WARNING: twitter:card missing")

    # 9. Check image file exists locally
    import os
    if os.path.exists("og-image.jpg"):
        size = os.path.getsize("og-image.jpg")
        checks.append(f"✓ og-image.jpg exists ({size} bytes = {round(size/1024,1)} KB)")
        if size > 300*1024:
            issues.append(f"✗ BAD: Image is {round(size/1024,1)} KB — WhatsApp limit is ~300KB. COMPRESS IT!")
        else:
            checks.append("  → Image size is OK for WhatsApp")
    else:
        issues.append("✗ CRITICAL: og-image.jpg NOT FOUND in same folder!")

    # 10. Check JS redirect placement
    if html.find("window.location.replace") > html.find("property=\"og:image\""):
        checks.append("✓ JS redirect is AFTER meta tags (good for crawlers)")
    else:
        issues.append("⚠ WARNING: JS redirect might be before meta tags")

    print("\n" + "="*50)
    print("WHATSAPP LINK PREVIEW VALIDATION REPORT")
    print("="*50)

    for c in checks:
        print(c)

    if issues:
        print("\n" + "-"*50)
        print("ISSUES FOUND:")
        for i in issues:
            print(i)
        print("-"*50)
        print(f"\n❌ FAILED: {len(issues)} issue(s) found. Fix before pushing.")
        return False
    else:
        print("\n" + "="*50)
        print("✅ ALL CHECKS PASSED! Ready to push to GitHub.")
        print("="*50)
        return True

if __name__ == "__main__":
    success = validate_index_html()
    sys.exit(0 if success else 1)
