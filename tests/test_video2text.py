import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video2text import pixel_to_char, frame_to_ascii, calculate_dimensions, ASCII_CHARS, BW_CHARS


class TestPixelToChar:
    def test_black_pixel_returns_densest_char(self):
        assert pixel_to_char(0) == "@"

    def test_white_pixel_returns_sparsest_char(self):
        assert pixel_to_char(255) == " "

    def test_midtone_returns_middle_char(self):
        char = pixel_to_char(128)
        assert char in ASCII_CHARS

    def test_all_values_return_valid_char(self):
        for v in range(256):
            assert pixel_to_char(v) in ASCII_CHARS

    def test_binary_black_pixel_returns_at(self):
        assert pixel_to_char(0, BW_CHARS) == "@"

    def test_binary_white_pixel_returns_dot(self):
        assert pixel_to_char(255, BW_CHARS) == "."

    def test_binary_all_values_return_valid_char(self):
        for v in range(256):
            assert pixel_to_char(v, BW_CHARS) in BW_CHARS


class TestCalculateDimensions:
    def test_both_none_uses_default_width_120(self):
        w, h = calculate_dimensions(1920, 1080, None, None)
        assert w == 120
        assert h > 0

    def test_only_width_scales_height_proportionally(self):
        # 1920x1080 video, char aspect ratio 2:1
        w, h = calculate_dimensions(1920, 1080, 80, None)
        assert w == 80
        # height = 80 * (1080/1920) / 2 = ~22
        assert h == round(80 * 1080 / 1920 / 2)

    def test_only_height_scales_width_proportionally(self):
        w, h = calculate_dimensions(1920, 1080, None, 30)
        assert h == 30
        # width = 30 * 2 * (1920/1080) = ~106
        assert w == round(30 * 2 * 1920 / 1080)

    def test_both_specified_uses_exact_values(self):
        w, h = calculate_dimensions(1920, 1080, 100, 50)
        assert w == 100
        assert h == 50

    def test_minimum_dimension_is_1(self):
        w, h = calculate_dimensions(1920, 1080, 1, None)
        assert w == 1
        assert h >= 1


class TestFrameToAscii:
    def test_output_has_correct_number_of_lines(self):
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 40, 20)
        lines = result.split("\n")
        assert len(lines) == 20

    def test_output_lines_have_correct_width(self):
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 40, 20)
        for line in result.split("\n"):
            assert len(line) == 40

    def test_black_frame_uses_dense_chars(self):
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 10, 5)
        assert "@" in result

    def test_white_frame_uses_sparse_chars(self):
        frame = np.full((100, 200, 3), 255, dtype=np.uint8)
        result = frame_to_ascii(frame, 10, 5)
        assert " " in result

    def test_returns_string(self):
        frame = np.zeros((50, 100, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 20, 10)
        assert isinstance(result, str)

    def test_binary_mode_only_uses_bw_chars(self):
        frame = np.random.randint(0, 256, (50, 100, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 20, 10, BW_CHARS)
        for ch in result:
            assert ch in BW_CHARS or ch == "\n"

    def test_binary_black_frame_uses_at(self):
        frame = np.zeros((50, 100, 3), dtype=np.uint8)
        result = frame_to_ascii(frame, 10, 5, BW_CHARS)
        assert "@" in result
        assert "." not in result

    def test_binary_white_frame_uses_dot(self):
        frame = np.full((50, 100, 3), 255, dtype=np.uint8)
        result = frame_to_ascii(frame, 10, 5, BW_CHARS)
        assert "." in result
        assert "@" not in result
