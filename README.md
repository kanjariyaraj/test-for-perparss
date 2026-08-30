# 🌈 Animated Colored "Hello, World!" in Python

A single-file Python program that types **"Hello, World!"** into your terminal one
letter at a time, with a smooth rainbow color gradient — plus a blinking cursor to
finish it off. No external libraries, no `pip install` — it uses only the Python
standard library, so it runs on **any** machine that has Python.

```
H     (red)        e     (orange)      l     (yellow)
l     (green)      o     (light-green) ,   →   smooth rainbow sweep …
```

This repository is also a **beginner-friendly tutorial**. The README explains how
Python works, walks through every line of the code, and shows you how to adapt it
into your own programs.

---

## 📚 Table of Contents

- [What is Python?](#what-is-python)
- [Installing Python](#installing-python)
- [Running the Animation](#running-the-animation)
- [What the Program Does](#what-the-program-does)
- [How It Works — Line by Line](#how-it-works--line-by-line)
  - [ANSI Escape Codes (terminal colors)](#ansi-escape-codes-terminal-colors)
  - [The HSV → RGB color trick](#the-hsv--rgb-color-trick)
  - [Coloring a single character](#coloring-a-single-character)
  - [Building the whole line](#building-the-whole-line)
  - [The typing animation](#the-typing-animation)
  - [The blinking cursor](#the-blinking-cursor)
- [Python Basics Mini-Course](#python-basics-mini-course)
  - [Variables](#variables)
  - [Strings](#strings)
  - [Printing](#printing)
  - [Lists](#lists)
  - [Conditionals (`if`)](#conditionals-if)
  - [Loops (`for` / `while`)](#loops-for--while)
  - [Functions (`def`)](#functions-def)
  - [Modules and `import`](#modules-and-import)
- [Customizing the Program](#customizing-the-program)
- [Running the Tests](#running-the-tests)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## What is Python?

Python is a **general-purpose programming language** created by Guido van Rossum
and first released in 1991. It is designed to be **easy to read and write**, which
makes it one of the best first languages to learn.

People use Python for almost everything:

- **Websites and web apps** (Django, Flask, FastAPI)
- **Data science and machine learning** (Pandas, NumPy, TensorFlow)
- **Automation and scripting** (renaming files, scraping the web, sending emails)
- **Games and graphics** (Pygame, Arcade)
- **Network and system tools**

Python is **interpreted**, meaning you run your code directly instead of compiling
it into a separate executable first. The program that reads and runs your code is
called an **interpreter**.

> **Python vs. Python 3** — "Python 3" is the current, supported version of the
> language (Python 2 is retired). Throughout this README, "Python" means Python 3.

---

## Installing Python

### On Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Click the big **Download Python** button.
3. Run the installer.
4. **Important:** tick the box that says **"Add Python to PATH"** before clicking
   Install.

### On macOS

- The easiest way is via **Homebrew**:

  ```bash
  brew install python
  ```

- Or download the installer from [python.org/downloads](https://www.python.org/downloads/).

### On Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Check your install

Open a terminal (Command Prompt / PowerShell on Windows) and run:

```bash
python --version
```

or (on Linux/macOS it is often `python3`):

```bash
python3 --version
```

If you see something like `Python 3.12.1`, you are ready. This project was tested
on Python 3.14.

### Running Python files

A Python program is just a text file ending in `.py`. You run it like this:

```bash
python3 hello_world.py
```

The interpreter reads the file top-to-bottom and executes each statement.

You can also type code **interactively** inside the interpreter itself:

```bash
python3
>>> print("hi")
hi
>>>
```

Type `exit()` or press `Ctrl+D` to leave the interactive prompt.

---

## Running the Animation

From the folder that contains `hello_world.py`:

```bash
python3 hello_world.py
```

You should see "Hello, World!" appear **letter by letter**, each letter a different
color of the rainbow, followed by a flashing underline cursor.

You can also pass your own text as a command-line argument:

```bash
python3 hello_world.py "Python is fun!"
python3 hello_world.py 你好世界
python3 hello_world.py "I love colors"
```

The script grabs whatever you type on the command line and animates *that* instead.

> **By the way — command-line arguments** `sys.argv` is a list that Python fills
> with everything you typed after the program name. `sys.argv[0]` is the program
> name itself, `sys.argv[1]` is the first real argument, and so on.

---

## What the Program Does

The whole program is one file: **`hello_world.py`**. Its six building blocks are:

| Piece | Job |
|-------|-----|
| `_hsv_to_rgb()` | Converts a color from HSV (hue/saturation/value) space to RGB. This is what makes the gradient mathematically smooth. |
| `gradient_color()` | Picks a rainbow color for character `i` out of `total` characters. |
| `colored_char()` | Wraps a single character in the ANSI codes that make the terminal paint it a given color. |
| `build_gradient_line()` | Turns a whole string into a color-coded string (used for testing). |
| `type_line()` | Performs the typing animation — prints one colored character at a time and pauses. |
| `blink_cursor()` | Prints a blinking underline to finish the show. |
| `main()` | Picks the text to use and runs the show. |

---

## How It Works — Line by Line

### ANSI Escape Codes (terminal colors)

Terminals are text-based, but they support *colors* through special control
sequences called **ANSI escape codes**. They all start with the ESC character,
which in Python is written as `"\x1b"` (hexadecimal for the escape key code).

The one we use is the **truecolor** (24-bit RGB) foreground code:

```
\x1b[38;2;R;G;Bm
```

Where `R`, `G`, `B` are numbers from `0` to `255`. Everything printed *after* this
code is painted with that color, until the terminal sees a **reset** code:

```
\x1b[0m
```

So to print a red `H`:

```
\x1b[38;2;255;0;0mH\x1b[0m
   └───── red ─────┘ └reset┘
```

Our constant:

```python
RESET = "\x1b[0m"
```

### The HSV → RGB color trick

Rainbows are naturally described in **HSV** space: **H**ue is the position on the
color wheel (red → orange → yellow → green → blue → purple → back to red),
**S**aturation is how vivid the color is, and **V**alue is how bright it is.

If we move `hue` smoothly from `0` to `1`, we get every color of the rainbow in
order — and the last hue wraps back to the first, so the gradient loops perfectly.

```python
def _hsv_to_rgb(hue, saturation=1.0, value=1.0):
    hi = int(hue * 6) % 6          # which of the 6 color segments are we in?
    f = hue * 6 - int(hue * 6)     # how far inside that segment?
    p = value * (1.0 - saturation)
    q = value * (1.0 - saturation * f)
    t = value * (1.0 - saturation * (1.0 - f))

    value *= 255
    p *= 255
    q *= 255
    t *= 255

    rgb = [
        (value, t, p),   # red   → yellow
        (q, value, p),   # yellow → green
        (p, value, t),   # green → cyan
        (p, q, value),   # cyan  → blue
        (t, p, value),   # blue  → magenta
        (value, p, q),   # magenta → red
    ][hi]
    return tuple(round(channel) for channel in rgb)
```

The integer indices `0..5` pick one of the six standard hue-to-rgb formulas, and
the fraction `f` smoothly interpolates inside that segment. The `[hi]` at the end
indexes into the list of six candidate tuples — a neat trick: build all six, pick
one with the index.

### Picking a gradient color

```python
def gradient_color(index, total):
    if total <= 0:
        return (255, 0, 0)
    hue = (index % total) / total
    return _hsv_to_rgb(hue)
```

- `index` is the character's position (`0`, `1`, `2`, …).
- `total` is the number of characters in the text.
- `index / total` maps the position onto the range `0.0 → 1.0`, which is exactly
  what `_hsv_to_rgb` expects as a hue.
- The `% total` guard means position `total` maps back to `0`, so the first and
  last colors match — a smooth loop.
- The `total <= 0` check stops a division-by-zero crash on empty input.

Character `0/13` is red, character `6/13` is cyan, then it cycles back.

### Coloring a single character

```python
def colored_char(char, rgb):
    r, g, b = rgb
    return f"\x1b[38;2;{r};{g};{b}m{char}" + RESET
```

- `rgb` is a tuple like `(255, 0, 0)`.
- `r, g, b = rgb` **unpacks** the tuple into three names.
- The f-string builds `\x1b[38;2;255;0;0mH`, then we append `RESET`.
- The result is one complete, self-contained color-coded character that the
  terminal can render no matter what came before it.

### Building the whole line

```python
def build_gradient_line(text):
    return "".join(
        colored_char(char, gradient_color(i, len(text)))
        for i, char in enumerate(text)
    )
```

This uses a **generator expression**: for each character and its position
(`enumerate` gives you both), it computes the right gradient color and wraps the
character. `"".join(...)` glues all the colored pieces into one string.

Putting all the coloring logic in one pure function means we can **test it
without running any animation** — that's why it exists separate from the typing.

### The typing animation

```python
def type_line(text, delay=0.05):
    for i, char in enumerate(text):
        sys.stdout.write(colored_char(char, gradient_color(i, len(text))))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()
```

- `sys.stdout.write(...)` writes directly to the terminal.
- `sys.stdout.flush()` forces the text to appear **immediately**. Without a flush,
  Python's output buffering may hold the characters back, and you'd see no
  animation at all.
- `time.sleep(delay)` pauses `0.05` seconds (50 ms) between letters — fast enough
  to feel smooth, slow enough to watch.
- Each letter is colored by its *overall* position in the text, so the rainbow
  pans across the line smoothly as the typing progresses.

### The blinking cursor

```python
def blink_cursor(cycles=3, on_time=0.4, off_time=0.4):
    for _ in range(cycles):
        sys.stdout.write("\x1b[5m_")
        sys.stdout.flush()
        time.sleep(on_time)
        sys.stdout.write("\r\x1b[K")
        sys.stdout.flush()
        time.sleep(off_time)
```

- `"\x1b[5m"` is the ANSI **blink** code — the terminal flashes the text for us.
- `"\r"` (carriage return) moves the cursor back to the start of the line.
- `"\x1b[K"` erases everything from the cursor to the end of the line, "unprinting"
  the cursor so the next loop can show it fresh.

### Tying it together

```python
def main():
    text = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEXT
    type_line(text)
    blink_cursor()


if __name__ == "__main__":
    main()
```

- `sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEXT` is a concise **ternary
  expression**: "use the first argument if it exists, otherwise use the default."
- `if __name__ == "__main__":` — every module has a `__name__`. When run directly,
  it's `"__main__"`; when imported by another file (like the tests), it's the
  module name. This line means: only auto-run `main()` when the file is run
  directly, never when imported.

---

## Python Basics Mini-Course

Everything the animation uses, explained for true beginners. Type each example in
the Python interpreter or save it in a `.py` file and run it.

### Variables

A variable is a name that points to a value. No declaration needed — assignment
both creates the variable and stores the value.

```python
name = "Ada"       # a string (text)
age = 36           # an integer
height = 1.68      # a float (decimal)
is_coder = True    # a boolean (True / False)

print(name, age, height, is_coder)
```

Variable names should be lowercase, with underscores between words:
`my_favorite_color` not `MyFavoriteColor`.

### Strings

Text in Python is a **string**, created with single or double quotes.

```python
greeting = "Hello"
whole = greeting + ", World!"   # + concatenates strings
repeat = "ha" * 3               # * repeats a string  -> "hahaha"
length = len(whole)             # len() gives the character count
first = whole[0]                # indexing starts at 0 -> "H"
last = whole[-1]                # -1 counts from the end -> "!"

print(f"length is {length}, first char is {first}")
```

`f"..."` is an **f-string**: anything in `{braces}` is evaluated and inserted.

### Printing

`print()` is the workhorse. It joins its arguments with spaces and adds a newline.

```python
print("Hello")                 # Hello
print("A", "B", "C")           # A B C
print("no newline", end="")    # print without a trailing newline
```

Inside the animation we don't use `print()` for the letters — we use
`sys.stdout.write()` because it gives us precise control over when each character
appears.

### Lists

A list is an ordered collection:

```python
colors = ["red", "green", "blue"]
colors.append("purple")    # add to the end
colors[0] = "crimson"      # change an item
print(len(colors))         # 4
print(colors[-1])          # purple

for c in colors:           # loop over every item
    print(c)
```

A **tuple** is like a list but cannot be changed:

```python
rgb = (255, 0, 0)          # tuples use parentheses
r, g, b = rgb              # unpacking: r=255, g=0, b=0
```

### Conditionals (`if`)

```python
score = 85

if score >= 90:
    print("Excellent!")
elif score >= 60:
    print("Passed")
else:
    print("Try again")
```

Indentation (4 spaces) is **part of Python's syntax** — it defines the block, no
braces needed.

### Loops (`for` / `while`)

`for` iterates over a sequence; `range()` produces a sequence of numbers.

```python
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i, char in enumerate("abc"):   # enumerate gives (index, value) pairs
    print(i, char)                 # 0 a  /  1 b  /  2 c

count = 0
while count < 3:
    print("looping", count)
    count += 1             # count = count + 1
```

The animation's typing loop uses exactly this pattern:

```python
for i, char in enumerate(text):
    ...
```

### Functions (`def`)

A function bundles reusable logic. Define it once, call it anywhere.

```python
def greet(name, punctuation="!"):
    return f"Hello, {name}{punctuation}"

print(greet("Ada"))            # Hello, Ada!
print(greet("Grace", "?"))     # Hello, Grace?
```

- `name` and `punctuation` are **parameters**; `punctuation="!"` gives it a
  **default value**.
- `return` hands a value back to the caller.
- The animation's `type_line(text, delay=0.05)` follows the same shape.

### Modules and `import`

Related code lives in **modules** (files). `import` pulls another module in.

```python
import time
import sys
import random

time.sleep(1)                 # pause 1 second
print(sys.argv)               # command-line arguments as a list
print(random.randint(1, 6))   # a random dice roll
```

The standard library is huge — `os` (files), `json`, `math`, `datetime`,
`pathlib`, and hundreds more. You use them exactly like the three above.

---

## Customizing the Program

The program is deliberately small so you can experiment. A few ideas:

**Change the speed of the typing** — edit `type_line`'s default:

```python
def type_line(text, delay=0.05):   # try 0.15 for slow, 0.01 for fast
```

**Change the default message**:

```python
DEFAULT_TEXT = "Hello, World!"     # -> "Welcome to Python!"
```

**Change the color scheme** — replace gradient with a fixed color:

```python
def purple_line(text):
    return "".join(colored_char(c, (150, 0, 255)) for c in text)
```

**Add a bounce-back effect** — type the text twice, once each direction:

```python
def bouncing_text():
    text = "HELLO!"
    type_line(text)
    for offset in range(len(text) - 1, 0, -1):
        time.sleep(0.3)
```

**Clear the screen first** so the show starts clean:

```python
import os
print("\033[2J")   # ANSI "clear screen" code
```

---

## Running the Tests

The project includes tests in **`test_hello_world.py`**, written with Python's
built-in `unittest` framework — no installation required.

Run them all:

```bash
python3 -m unittest test_hello_world -v
```

You should see 7 passing tests:

```text
test_builds_expected_output                 ... ok
test_empty_string_returns_empty_string      ... ok
test_every_char_has_color_code              ... ok
test_preserves_non_ascii_char               ... ok
test_wraps_char_in_truecolor_ansi_sequence  ... ok
test_first_and_last_colors_match_for_smooth_loop ... ok
test_returns_rgb_tuple_in_range             ... ok

Ran 7 tests in 0.001s

OK
```

What the tests guard against:

- The RGB channels of the gradient are always valid `0–255` integers.
- The gradient loops smoothly (first color == last color).
- `colored_char` emits exactly the ANSI sequence we expect.
- Non-ASCII characters pass through intact.
- Empty input doesn't crash.

**This is the payoff of separating pure logic from the animation**: the animated
parts can't be asserted easily, but the color math and string building can — so
we unit-test those.

---

## Troubleshooting

**I see raw escape codes like `[38;2;255;0;0m` instead of colors.**

Your terminal doesn't support 24-bit truecolor, or it's an older one. Try the
256-color fallback by editing `colored_char` to use a 256-color code:

```python
def colored_char(char, rgb):
    index = 16 + 36 * (rgb[0] // 51) + 6 * (rgb[1] // 51) + (rgb[2] // 51)
    return f"\x1b[38;5;{index}m{char}" + RESET
```

**The letters all appear at once, no animation.**

You probably redirected output to a file (`> out.txt`). `time.sleep` still runs,
but a file has no concept of "typing." Run it directly in a real terminal.

**On Windows Command Prompt / PowerShell, no colors.**

Windows 10+ terminals support ANSI colors. If yours doesn't, run the program via
**Windows Terminal** (free from the Microsoft Store).

**`python` is not recognized (Windows).**

Python wasn't added to PATH during install. Reinstall, or use the full path:
`py hello_world.py` (the Windows launcher).

**`python3` is not found (Linux/macOS).**

Try `python`. If neither exists, install via the steps in [Installing Python](#installing-python).

---

## Next Steps

Now that you understand a complete, working program, here's where to grow:

- **Read the official tutorial** — [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/)
- **Practice** — [exercism.org/tracks/python](https://exercism.org/tracks/python) and
  [projecteuler.net](https://projecteuler.net/)
- **Learn project structure** — try splitting your code into multiple files and
  importing functions between them.
- **Add arguments properly** — the `argparse` standard module turns
  `sys.argv` fiddling into clean, documented options (`--text`, `--delay`).
- **Think about input** — let the user type a message, animate it, repeat.
- **Level up** — learn `itertools.cycle` and use it to rotate colors infinitely:

  ```python
  import itertools
  palette = itertools.cycle([(255,0,0), (0,255,0), (0,0,255)])
  for c in "LOOP!":
      print(colored_char(c, next(palette)), end="", flush=True)
      time.sleep(0.3)
  ```

The best way to learn Python is to **write Python**. Take `hello_world.py`, break
it, fix it, add to it, and make it yours.

Happy coding! 🐍