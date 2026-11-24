"""Offline short-form video planning toolkit."""
import argparse
import re
from pathlib import Path

def plan(text, wpm=150, chunk=8):
    if wpm <= 0 or chunk <= 0:
        raise ValueError("wpm and chunk must be positive")
    words = text.split()
    return [(i*60/wpm, min(i+chunk,len(words))*60/wpm, " ".join(words[i:i+chunk])) for i in range(0,len(words),chunk)]

def timestamp(seconds):
    ms = round(seconds*1000)
    h, ms = divmod(ms,3600000)
    m, ms = divmod(ms,60000)
    s, ms = divmod(ms,1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def subtitles(rows):
    return "\n\n".join(f"{i}\n{timestamp(a)} --> {timestamp(b)}\n{line}" for i,(a,b,line) in enumerate(rows,1)) + "\n"

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("script", type=Path)
    p.add_argument("--wpm", type=int, default=150)
    p.add_argument("--output", type=Path, default=Path("draft.srt"))
    args = p.parse_args()
    if args.wpm <= 0:
        p.error("--wpm must be positive")
    text = args.script.read_text(encoding="utf-8")
    rows = plan(text,args.wpm)
    if not rows:
        p.error("Script is empty")
    args.output.write_text(subtitles(rows),encoding="utf-8")
    print(f"Estimated duration: {rows[-1][1]:.1f}s")
    for i,(a,b,line) in enumerate(plan(text,args.wpm,20),1):
        print(f"Shot {i}: {a:.1f}-{b:.1f}s | {line}")
    print(f"Draft captions: {args.output} (estimated timing; align to recorded audio)")

if __name__ == "__main__":
    main()
