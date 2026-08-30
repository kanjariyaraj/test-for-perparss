import sys
import time

RESET = "\x1b[0m"
DEFAULT_TEXT = "Hello, World!"


def _hsv_to_rgb(hue, saturation=1.0, value=1.0):
    hi = int(hue * 6) % 6
    f = hue * 6 - int(hue * 6)
    p = value * (1.0 - saturation)
    q = value * (1.0 - saturation * f)
    t = value * (1.0 - saturation * (1.0 - f))

    value *= 255
    p *= 255
    q *= 255
    t *= 255

    rgb = [
        (value, t, p),
        (q, value, p),
        (p, value, t),
        (p, q, value),
        (t, p, value),
        (value, p, q),
    ][hi]
    return tuple(round(channel) for channel in rgb)


def gradient_color(index, total):
    if total <= 0:
        return (255, 0, 0)
    hue = (index % total) / total
    return _hsv_to_rgb(hue)


def colored_char(char, rgb):
    r, g, b = rgb
    return f"\x1b[38;2;{r};{g};{b}m{char}" + RESET


def build_gradient_line(text):
    return "".join(
        colored_char(char, gradient_color(i, len(text)))
        for i, char in enumerate(text)
    )


def type_line(text, delay=0.05):
    for i, char in enumerate(text):
        sys.stdout.write(colored_char(char, gradient_color(i, len(text))))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def blink_cursor(cycles=3, on_time=0.4, off_time=0.4):
    for _ in range(cycles):
        sys.stdout.write("\x1b[5m_")
        sys.stdout.flush()
        time.sleep(on_time)
        sys.stdout.write("\r\x1b[K")
        sys.stdout.flush()
        time.sleep(off_time)


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEXT
    type_line(text)
    blink_cursor()


if __name__ == "__main__":
    main()