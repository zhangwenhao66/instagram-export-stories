# instagram-export-stories

Sort the Stories in your Instagram data export into dated folders (`2024/2024-03/2024-03-10_000000.mp4`), with each file's modified time set to when the Story was posted.

Instagram keeps your own past Stories in the **Archive**, but the app only lets you save them one at a time. The official bulk route is **Accounts Center → Your information and permissions → Download your information**. Pick **JSON** as the format. The zip you get contains every archived Story under `media/stories/`, but the files have opaque names and are grouped by month only. This script fixes that.

## Use

```
python3 organize_stories.py ~/Downloads/instagram-yourname-2026-11-26 ./my-stories
```

- Python 3.8+, no packages to install.
- Reads every `stories.json` in the export and copies (never moves) the media it points to.
- Times are converted to your computer's local time; add `--utc` to name files in UTC.
- Two Stories posted in the same second get `_2`, `_3` suffixes instead of overwriting each other.

## What the export does and does not include

- Included: your own Stories that are in your Archive (the archive is on by default), photo and video, at the resolution Instagram stored.
- Not included: other people's Stories, including ones you were tagged in and did not reshare.

To save a public Story from someone else's account, a browser tool such as [Stories Download](https://storiesdownload.com/) works from the Story link without logging in. Please keep it to personal use and ask before reposting someone else's content.

## License

MIT
