# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 Michał Góral.

import re
from functools import cache


@cache
def _parse_codes(path: str):
    codes = {}

    # define may be either base 10 int, base 16 int (hex) or a reference to the
    # other field
    key_re = re.compile(r"^#define KEY_(\w+)\s+(0x[a-fA-F0-9]+|\d+|KEY_\w+)")

    with open(path, encoding="utf-8") as file_:
        for line in file_:
            m = key_re.match(line.strip())
            if m:
                key = m.group(1)
                val = m.group(2)

                if val.startswith("KEY_"):
                    ref = val[4:]
                    try:
                        val = codes[ref]
                    except KeyError:
                        continue
                else:
                    try:
                        val = int(val, 0)  # base 0 auto-converts strings
                    except ValueError:
                        continue

                codes[key] = val

    return codes


@cache
def get_ydotool_keys():
    codes = _parse_codes("/usr/include/linux/input-event-codes.h")

    # when there's no code available, None will be retrned, which is
    # interpreted appropriately by kpsh. It skips that key.
    return {
        "{TAB}": codes.get("TAB"),
        "{ENTER}": codes.get("ENTER"),
        "{UP}": codes.get("UP"),
        "{DOWN}": codes.get("DOWN"),
        "{LEFT}": codes.get("LEFT"),
        "{RIGHT}": codes.get("RIGHT"),
        "{INSERT}": codes.get("INSERT"),
        "{INS}": codes.get("INSERT"),
        "{DELETE}": codes.get("DELETE"),
        "{DEL}": codes.get("DELETE"),
        "{HOME}": codes.get("HOME"),
        "{END}": codes.get("END"),
        "{PGUP}": codes.get("PAGEUP"),
        "{PGDN}": codes.get("PAGEDOWN"),
        "{SPACE}": codes.get("SPACE"),
        "{BACKSPACE}": codes.get("BACKSPACE"),
        "{BS}": codes.get("BACKSPACE"),
        "{BKSP}": codes.get("BACKSPACE"),
        "{BREAK}": codes.get("BREAK"),
        "{CAPSLOCK}": codes.get("CAPSLOCK"),
        "{ESC}": codes.get("ESC"),
        "{WIN}": codes.get("LEFTMETA"),
        "{LWIN}": codes.get("LEFTMETA"),
        "{RWIN}": codes.get("RIGHTMETA"),
        "{NUMLOCK}": codes.get("NUMLOCK"),
        "{SCROLLLOCK}": codes.get("SCROLLLOCK"),
        "{F1}": codes.get("F1"),
        "{F2}": codes.get("F2"),
        "{F3}": codes.get("F3"),
        "{F4}": codes.get("F4"),
        "{F5}": codes.get("F5"),
        "{F6}": codes.get("F6"),
        "{F7}": codes.get("F7"),
        "{F8}": codes.get("F8"),
        "{F9}": codes.get("F9"),
        "{F10}": codes.get("F10"),
        "{F11}": codes.get("F11"),
        "{F12}": codes.get("F12"),
        "{F13}": codes.get("F13"),
        "{F14}": codes.get("F14"),
        "{F15}": codes.get("F15"),
        "{F16}": codes.get("F16"),
        "{ADD}": codes.get("KPPLUS"),
        "{SUBTRACT}": codes.get("KPMINUS"),
        "{MULTIPLY}": codes.get("KPASTERISK"),
        "{DIVIDE}": codes.get("KPSLASH"),
        "{NUMPAD0}": codes.get("KP0"),
        "{NUMPAD1}": codes.get("KP1"),
        "{NUMPAD2}": codes.get("KP2"),
        "{NUMPAD3}": codes.get("KP3"),
        "{NUMPAD4}": codes.get("KP4"),
        "{NUMPAD5}": codes.get("KP5"),
        "{NUMPAD6}": codes.get("KP6"),
        "{NUMPAD7}": codes.get("KP7"),
        "{NUMPAD8}": codes.get("KP8"),
        "{NUMPAD9}": codes.get("KP9"),
    }
