#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Philip Zerull

# This file is part of "The Cursed Editor"

# "The Cursed Editor" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import os
import curses

from typing import Optional, List, Union, Tuple, Callable, Dict


class BaseBackend:
    def main(self, mainloop_callback: Callable[[], None]) -> None:
        mainloop_callback()

    def get_size(self) -> Tuple[int, int]:
        raise NotImplementedError

    def get_key(self) -> Optional[str]:
        raise NotImplementedError

    def draw_character(self, character: str, x: int, y: int) -> None:
        raise NotImplementedError

    def clear_screen(self) -> None:
        raise NotImplementedError

    def move_cursor(self, *, x: int, y: int) -> None:
        raise NotImplementedError

    def get_screen_contents(self) -> List[str]:
        result = []
        height, width = self.get_size()
        for y in range(height):
            line = ""
            for x in range(width):
                line = line + self.get_character(y=y, x=x)
            result.append(line)
        return result

    def get_character(self, *, x: int, y: int) -> str:
        raise NotImplementedError


class TestBackend(BaseBackend):
    def __init__(self, *, width: int = 50, height: int = 50) -> None:
        self.width = width
        self.height = height
        self.keys: List[str] = []
        self.screen: Dict[Tuple[int, int], str] = {}

    def get_size(self) -> Tuple[int, int]:
        return self.height, self.width

    def get_key(self) -> Optional[str]:
        result = None
        if self.keys:
            key = self.keys.pop(0)
            if key not in "\r":
                result = key
        else:
            raise KeyboardInterrupt
        return result

    def draw_character(self, character: str, x: int, y: int) -> None:
        self.screen[(y, x)] = character

    def clear_screen(self) -> None:
        self.screen = {}

    def move_cursor(self, *, x: int, y: int) -> None:
        pass

    def get_character(self, *, y: int, x: int) -> str:
        return self.screen.get((y, x), " ")


class CursesBackend(BaseBackend):
    def __init__(self) -> None:
        self.mainloop_callback: Callable[[], None] = lambda: None
        self.stdscr: Optional[curses.window] = None
        self._key_queue: List[Union[int, str, None]] = []

    def main(self, mainloop_callback: Callable[[], None]) -> None:
        self.mainloop_callback = mainloop_callback
        os.environ.setdefault("ESCDELAY", "25")
        curses.wrapper(self._wrapped_curses_app)

    def _wrapped_curses_app(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.initialize_screen()
        self.mainloop_callback()

    def initialize_screen(self) -> None:
        if self.stdscr is not None:
            curses.nl()
            curses.use_default_colors()
            self.stdscr.keypad(True)
            self.stdscr.clear()
            self.stdscr.nodelay(True)

    def get_size(self) -> Tuple[int, int]:
        if self.stdscr is None:
            return (0, 0)
        return self.stdscr.getmaxyx()

    def pop_key(self) -> Union[int, str, None]:
        if self.stdscr is None:
            return None
        key = None
        if self._key_queue:
            key = self._key_queue.pop(0)
        else:
            try:
                key = self.stdscr.get_wch()
            except curses.error:
                pass
        return key

    def push_key(self, key: Union[int, str, None]) -> None:
        self._key_queue.append(key)

    def get_key(self) -> Optional[str]:
        if self.stdscr is None:
            return None
        key = self.pop_key()
        if isinstance(key, int):
            key = curses.keyname(key).decode()
        return key

    def draw_character(self, character: str, x: int, y: int) -> None:
        if self.stdscr is None:
            return
        try:
            self.stdscr.addch(y, x, character[:1])
        except curses.error:
            pass

    def clear_screen(self) -> None:
        if self.stdscr is not None:
            self.stdscr.clear()

    def move_cursor(self, *, x: int, y: int) -> None:
        if self.stdscr is not None:
            height, width = self.get_size()
            x = min(width - 1, max(0, x))
            y = min(height - 1, max(0, y))
            self.stdscr.move(y, x)

    def get_character(self, *, y: int, x: int) -> str:
        if not self.stdscr:
            return ""
        return chr(self.stdscr.inch(y, x))

    def get_cursor(self) -> Tuple[int, int]:
        if self.stdscr is None:
            return (0, 0)
        return self.stdscr.getyx()


default = CursesBackend()
