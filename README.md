# AI Shorts Studio

An MIT-licensed, offline Python toolkit for short-form video creators. Early prototype; no AI model or paid API is required for current features.

## Quick start
Requires Python 3.9+.

Save narration in `script.txt`, then run:

```sh
python studio.py script.txt --wpm 150 --output draft.srt
```

The tool estimates narration duration, splits narration into shot-sized text segments, and creates draft SRT captions. Timings are estimates, not audio transcription; align them with your recording before publishing.

## Roadmap
- Browser dashboard
- Optional AI-assisted script drafting
- Audio-aligned subtitles
- Storyboard export

## Contributing
Report reproducible issues or submit focused pull requests with tests. Do not commit API keys, private recordings, or copyrighted material without permission.

## License
MIT. See LICENSE.
