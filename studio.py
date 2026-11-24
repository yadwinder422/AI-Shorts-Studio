"""Offline short-form video planning toolkit."""
import argparse
import os
import stat
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
    if not 30 <= args.wpm <= 600:
        p.error("--wpm must be between 30 and 600")
    if args.script.suffix.lower() != ".txt" or args.output.suffix.lower() != ".srt":
        p.error("Use a .txt input and .srt output")
    try:
        if args.script.is_symlink() or not args.script.is_file():
            p.error("Input must be a regular text file, not a symlink")
        with args.script.open("rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                p.error("Input must be a regular file")
            data = source.read(1_048_577)
        if len(data) > 1_048_576:
            p.error("Input exceeds 1 MiB")
        text = data.decode("utf-8")
        if any(ord(c) < 32 and c not in "\n\r\t" or 127 <= ord(c) <= 159 for c in text):
            p.error("Unsupported control characters in input")
    except (OSError, UnicodeError):
        p.error("Cannot read a valid UTF-8 input file")
    rows = plan(text,args.wpm)
    if not rows:
        p.error("Script is empty")
    try:
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            output.write(subtitles(rows))
    except OSError:
        p.error("Cannot create output; choose a new writable path. Existing files are never overwritten.")
    print(f"Estimated duration: {rows[-1][1]:.1f}s")
    for i,(a,b,line) in enumerate(plan(text,args.wpm,20),1):
        print(f"Shot {i}: {a:.1f}-{b:.1f}s")
    print(f"Draft captions: {args.output} (estimated timing; align to recorded audio)")

if __name__ == "__main__":
    main()
