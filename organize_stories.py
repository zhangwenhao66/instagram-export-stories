#!/usr/bin/env python3
"""Copy the Stories from an Instagram "Download your information" export into
dated folders, named by the time each Story was posted.

Usage:
    python3 organize_stories.py /path/to/instagram-export ./my-stories

No dependencies. Works with JSON exports (choose JSON, not HTML, when you
request the download). Your files are only read and copied; nothing is uploaded.
"""
import json, os, shutil, sys
from datetime import datetime, timezone

def find_story_json(root):
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f == "stories.json":
                yield os.path.join(dirpath, f)

def entries(obj):
    """Yield every dict that has a media 'uri' and a 'creation_timestamp'."""
    if isinstance(obj, dict):
        if "uri" in obj and "creation_timestamp" in obj:
            yield obj
        for v in obj.values():
            yield from entries(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from entries(v)

def main(src, dst, use_utc=False):
    count = 0
    for js in find_story_json(src):
        with open(js, encoding="utf-8") as fh:
            data = json.load(fh)
        for e in entries(data):
            media = os.path.join(src, e["uri"])
            if not os.path.isfile(media):
                print("missing:", e["uri"])
                continue
            ts = e["creation_timestamp"]
            t = datetime.fromtimestamp(ts, timezone.utc) if use_utc else datetime.fromtimestamp(ts)
            folder = os.path.join(dst, t.strftime("%Y"), t.strftime("%Y-%m"))
            os.makedirs(folder, exist_ok=True)
            ext = os.path.splitext(media)[1].lower()
            name = t.strftime("%Y-%m-%d_%H%M%S") + ext
            n = 1
            while os.path.exists(os.path.join(folder, name)):
                n += 1
                name = t.strftime("%Y-%m-%d_%H%M%S") + f"_{n}{ext}"
            shutil.copy2(media, os.path.join(folder, name))
            os.utime(os.path.join(folder, name), (ts, ts))
            count += 1
    print(f"copied {count} stories into {dst}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], "--utc" in sys.argv)
