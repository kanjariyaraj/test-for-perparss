import unittest

from hello_world import (
    RESET,
    build_gradient_line,
    colored_char,
    gradient_color,
)


class TestGradientColor(unittest.TestCase):
    def test_returns_rgb_tuple_in_range(self):
        for i in range(0, 30):
            r, g, b = gradient_color(i, 30)
            for channel in (r, g, b):
                self.assertTrue(0 <= channel <= 255, channel)

    def test_first_and_last_colors_match_for_smooth_loop(self):
        self.assertEqual(gradient_color(0, 12), gradient_color(12, 12))


class TestColoredChar(unittest.TestCase):
    def test_wraps_char_in_truecolor_ansi_sequence(self):
        self.assertEqual(
            colored_char("A", (255, 0, 0)),
            "\x1b[38;2;255;0;0mA" + RESET,
        )

    def test_preserves_non_ascii_char(self):
        self.assertEqual(
            colored_char("!", (0, 128, 255)),
            "\x1b[38;2;0;128;255m!" + RESET,
        )


class TestBuildGradientLine(unittest.TestCase):
    def test_empty_string_returns_empty_string(self):
        self.assertEqual(build_gradient_line(""), "")

    def test_builds_expected_output(self):
        text = "Hi!"
        expected = (
            colored_char("H", gradient_color(0, len(text)))
            + colored_char("i", gradient_color(1, len(text)))
            + colored_char("!", gradient_color(2, len(text)))
        )
        self.assertEqual(build_gradient_line(text), expected)

    def test_every_char_has_color_code(self):
        line = build_gradient_line("HELLO WORLD")
        parts = line.split(RESET)
        self.assertEqual(len(parts), len("HELLO WORLD") + 1)


if __name__ == "__main__":
    unittest.main()