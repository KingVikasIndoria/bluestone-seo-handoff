# -*- coding: utf-8 -*-
"""Generate clean Telugu Ugadi wish sections (ASCII source only)."""
from pathlib import Path
import json


def hx(s: str) -> str:
    return "".join(chr(int(x, 16)) for x in s.split())


UGADI_SUBHAKANKSHALU = hx(
    "0c09 0c17 0c3e 0c26 0c3f 0020 0c36 0c41 0c2d 0c3e 0c15 0c3e 0c02 0c15 0c4d 0c37 0c32 0c41"
)
HAPPY_UGADI = hx("0c39 0c4d 0c2f 0c3e 0c2a 0c40 0020 0c09 0c17 0c3e 0c26 0c3f")
UGADI_SUBHAM = hx("0c09 0c17 0c3e 0c26 0c3f 0020 0c36 0c41 0c2d 0c02")

sections = {
    "whatsapp_telugu": [
        f"{UGADI_SUBHAKANKSHALU}! "
        + hx(
            "0c2e 0c40 0020 0c15 0c41 0c1f 0c41 0c02 0c2c 0c3e 0c28 0c3f 0c15 0c3f 0020 "
            "0c38 0c02 0c24 0c4b 0c37 0c02 002c 0020 0c06 0c30 0c4b 0c17 0c4d 0c2f 0c02 002c 0020 "
            "0c35 0c3f 0c1c 0c2f 0c02 0020 0c15 0c32 0c17 0c3e 0c32 0c28 0c3f 0020 "
            "0c15 0c4b 0c30 0c41 0c15 0c41 0c02 0c1f 0c41 0c28 0c4d 0c28 0c3e 0c28 0c41"
        )
        + ".",
        f"{HAPPY_UGADI} 2027! "
        + hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2e 0c40 0020 0c07 0c02 0c1f 0c4d 0c32 0c4b 0020 0c15 0c4a 0c24 0c4d 0c24 0020 "
            "0c06 0c36 0c32 0c41 0020 0c28 0c3f 0c02 0c2a 0c3e 0c32 0c3f"
        )
        + ".",
        f"{UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c2e 0c3e 0c2e 0c3f 0c21 0c3f 0020 0c24 0c4b 0c30 0c23 0c02 0020 0c32 0c3e 0c17 0c3e 0020 "
            "0c2e 0c40 0020 0c30 0c4b 0c1c 0c41 0c32 0c41 0020 0c2a 0c1a 0c4d 0c1a 0c17 0c3e 0020 "
            "0c35 0c3f 0c15 0c38 0c3f 0c02 0c1a 0c3e 0c32 0c3f"
        )
        + ".",
        "WhatsApp Ugadi wish: "
        + hx(
            "0c09 0c17 0c3e 0c26 0c3f 0020 0c2a 0c1a 0c4d 0c1a 0c21 0c3f 0020 0c32 0c3e 0c17 0c3e 0020 "
            "0c1c 0c40 0c35 0c3f 0c24 0c02 0c32 0c4b 0020 0c24 0c40 0c2a 0c3f 002c 0020 "
            "0c1a 0c47 0c26 0c41 0020 0c30 0c46 0c02 0c21 0c42 0020 "
            "0c38 0c2e 0c24 0c41 0c32 0c4d 0c2f 0c02 0c17 0c3e 0020 0c09 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c36 0c41 0c2d 0c4b 0c26 0c2f 0c02")
        + f"! {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c2e 0c40 0020 0c15 0c32 0c32 0c41 0020 0c08 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c28 0c46 0c30 0c35 0c47 0c30 0c3e 0c32 0c3f"
        )
        + ".",
        f"{HAPPY_UGADI}! "
        + hx(
            "0c2a 0c4d 0c30 0c3f 0c2f 0c2e 0c48 0c28 0020 0c35 0c3e 0c30 0c3f 0c15 0c3f 0020 "
            "0c2a 0c4d 0c30 0c47 0c2e 0c24 0c4b 0020 0c09 0c17 0c3e 0c26 0c3f 0020 "
            "0c36 0c41 0c2d 0c3e 0c15 0c3e 0c02 0c15 0c4d 0c37 0c32 0c41 0020 "
            "0c2a 0c02 0c2a 0c41 0c24 0c41 0c28 0c4d 0c28 0c3e 0c28 0c41"
        )
        + ".",
        hx("0c09 0c17 0c3e 0c26 0c3f")
        + " 2027 "
        + hx("0c36 0c41 0c2d 0c3e 0c15 0c3e 0c02 0c15 0c4d 0c37 0c32 0c41")
        + ". "
        + hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c05 0c35 0c15 0c3e 0c36 0c3e 0c32 0c41 002c 0020 "
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c06 0c28 0c02 0c26 0c02 0020 "
            "0c2e 0c40 0020 0c26 0c17 0c4d 0c17 0c30 0c15 0c41 0020 0c30 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        "Short Telugu line: "
        + f"{UGADI_SUBHAM}! "
        + hx(
            "0c2e 0c40 0020 0c07 0c32 0c4d 0c32 0c41 0020 0c36 0c3e 0c02 0c24 0c3f 002c 0020 "
            "0c38 0c02 0c2a 0c26 0c24 0c4b 0020 0c28 0c3f 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c09 0c17 0c3e 0c26 0c3f 0020 0c35 0c3f 0c37 0c46 0c38 0c4d")
        + ": "
        + hx(
            "0c2e 0c40 0c15 0c41 0020 0c2e 0c02 0c1a 0c3f 0020 0c06 0c30 0c4b 0c17 0c4d 0c2f 0c02 002c 0020 "
            "0c2e 0c02 0c1a 0c3f 0020 0c35 0c3e 0c30 0c4d 0c24 0c32 0c41 002c 0020 "
            "0c2e 0c02 0c1a 0c3f 0020 0c1c 0c4d 0c1e 0c3e 0c2a 0c15 0c3e 0c32 0c41 0020 "
            "0c15 0c32 0c17 0c3e 0c32 0c3f"
        )
        + ".",
        f"Copy ready: {HAPPY_UGADI} 2027 | "
        + hx("0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 0c36 0c41 0c2d 0c02")
        + "!",
    ],
    "family_telugu": [
        hx("0c05 0c2e 0c4d 0c2e 0c3e 002c 0020 0c28 0c3e 0c28 0c4d 0c28 0c3e")
        + f": {UGADI_SUBHAKANKSHALU}. "
        + hx("0c2e 0c40 0020 0c06 0c36 0c40 0c30 0c4d 0c35 0c3e 0c26 0c3e 0c32 0c47 0020 0c2e 0c3e 0020 0c2c 0c32 0c02")
        + ". "
        + hx(
            "0c08 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 0c2e 0c40 0c15 0c41 0020 "
            "0c06 0c30 0c4b 0c17 0c4d 0c2f 0c02 0020 0c28 0c3f 0c32 0c15 0c21 0c17 0c3e 0020 "
            "0c09 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c2e 0c3e 0020 0c15 0c41 0c1f 0c41 0c02 0c2c 0c3e 0c28 0c3f 0c15 0c3f")
        + f" {HAPPY_UGADI} 2027. "
        + hx(
            "0c15 0c32 0c3f 0c38 0c3f 0020 0c1a 0c47 0c38 0c47 0020 0c2a 0c42 0c1c 002c 0020 "
            "0c15 0c32 0c3f 0c38 0c3f 0020 0c24 0c3f 0c28 0c47 0020 0c2a 0c1a 0c4d 0c1a 0c21 0c3f 0020 "
            "0c2e 0c3e 0020 0c06 0c28 0c02 0c26 0c02"
        )
        + ".",
        hx("0c05 0c15 0c4d 0c15 0c3e 002c 0020 0c05 0c28 0c4d 0c28 0c3e")
        + f": {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c2e 0c28 0020 0c2c 0c02 0c27 0c02 0020 0c08 0020 0c15 0c4a 0c24 0c4d 0c24 0020 "
            "0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0c32 0c4b 0020 0c2e 0c30 0c3f 0c02 0c24 0020 "
            "0c2c 0c32 0c2a 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c24 0c3e 0c24 0c2f 0c4d 0c2f 002c 0020 0c05 0c2e 0c4d 0c2e 0c2e 0c4d 0c2e 0c15 0c41")
        + f" {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c2e 0c40 0020 0c1c 0c4d 0c1e 0c3e 0c28 0c02 0020 0c2e 0c3e 0020 "
            "0c07 0c02 0c1f 0c3f 0c15 0c3f 0020 0c35 0c46 0c32 0c41 0c17 0c41"
        )
        + ".",
        hx("0c2e 0c3e 0020 0c07 0c02 0c1f 0c3f 0020 0c35 0c3e 0c30 0c02 0c26 0c30 0c3f 0c15 0c40")
        + f" {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c38 0c02 0c24 0c4b 0c37 0c02 002c 0020 0c38 0c02 0c2a 0c26 002c 0020 "
            "0c38 0c3e 0c2e 0c30 0c38 0c4d 0c2f 0c02 0020 0c28 0c3f 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c2a 0c3f 0c32 0c4d 0c32 0c32 0c15 0c41")
        + f": {UGADI_SUBHAM}! "
        + hx(
            "0c2e 0c40 0020 0c28 0c35 0c4d 0c35 0c41 0c32 0c24 0c4b 0020 0c07 0c32 0c4d 0c32 0c41 0020 "
            "0c35 0c46 0c32 0c41 0c17 0c41 0c24 0c41 0c02 0c26 0c3f"
        )
        + ". "
        + hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2e 0c40 0c15 0c41 0020 0c2e 0c02 0c1a 0c3f 0c26 0c3f 0020 0c15 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c2d 0c30 0c4d 0c24 0020 002f 0020 0c2d 0c3e 0c30 0c4d 0c2f 0c15 0c41")
        + f": {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c15 0c32 0c3f 0c38 0c3f 0020 0c28 0c21 0c3f 0c1a 0c47 0020 0c08 0020 "
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2e 0c30 0c3f 0c02 0c24 0020 0c2e 0c27 0c41 0c30 0c02 0020 0c15 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        "Family Telugu wish: "
        + hx(
            "0c2e 0c3e 0020 0c07 0c02 0c1f 0c4d 0c32 0c4b 0020 0c09 0c17 0c3e 0c26 0c3f 0020 "
            "0c05 0c02 0c1f 0c47 0020 0c2a 0c4d 0c30 0c47 0c2e 002c 0020 0c2a 0c02 0c21 0c41 0c17 002c 0020 "
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c06 0c36"
        )
        + ". "
        + hx("0c05 0c02 0c26 0c30 0c3f 0c15 0c40 0020 0c36 0c41 0c2d 0c02")
        + "!",
    ],
    "friends_telugu": [
        hx("0c38 0c4d 0c28 0c47 0c39 0c3f 0c24 0c41 0c21 0c3e")
        + f", {UGADI_SUBHAKANKSHALU}! "
        + hx(
            "0c28 0c40 0020 0c38 0c4d 0c28 0c47 0c39 0c02 0020 0c28 0c3e 0c15 0c41 0020 "
            "0c0e 0c2a 0c4d 0c2a 0c1f 0c3f 0c15 0c40 0020 0c24 0c40 0c2a 0c3f"
        )
        + ".",
        f"{HAPPY_UGADI} 2027, dear friend. "
        + hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c28 0c40 0020 0c15 0c32 0c32 0c28 0c41 0020 0c26 0c17 0c4d 0c17 0c30 0c15 0c41 0020 "
            "0c24 0c40 0c38 0c41 0c15 0c41 0c30 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        hx(
            "0c1a 0c46 0c32 0c4d 0c32 0c40 0020 002f 0020 0c05 0c28 0c4d 0c28 0c3e 0020 "
            "0c32 0c3e 0c02 0c1f 0c3f 0020 0c38 0c4d 0c28 0c47 0c39 0c3f 0c24 0c41 0c32 0c15 0c41"
        )
        + f" {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c2e 0c28 0020 0c1c 0c4d 0c1e 0c3e 0c2a 0c15 0c3e 0c32 0c41 0020 "
            "0c0e 0c2a 0c4d 0c2a 0c1f 0c3f 0c15 0c40 0020 0c09 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        "Friends group message: "
        + hx("0c05 0c02 0c26 0c30 0c3f 0c15 0c40")
        + f" {UGADI_SUBHAKANKSHALU}! "
        + hx(
            "0c08 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 0c15 0c32 0c3f 0c38 0c3f 0020 "
            "0c0e 0c15 0c4d 0c15 0c41 0c35 0020 0c28 0c35 0c4d 0c35 0c41 0c26 0c3e 0c02"
        )
        + ".",
        hx(
            "0c38 0c4d 0c28 0c47 0c39 0c02 0020 0c09 0c17 0c3e 0c26 0c3f 0020 "
            "0c2a 0c02 0c21 0c41 0c17 0c32 0c3e 0020 0c15 0c4a 0c24 0c4d 0c24 0c26 0c28 0c02 0020 "
            "0c24 0c46 0c38 0c4d 0c24 0c41 0c02 0c26 0c3f"
        )
        + ". "
        + hx(
            "0c28 0c40 0c15 0c41 0020 0c36 0c41 0c2d 0c02 002c 0020 "
            "0c35 0c3f 0c1c 0c2f 0c02 0020 0c15 0c32 0c17 0c3e 0c32 0c3f"
        )
        + ".",
        "Ugadi wish for friends: "
        + hx(
            "0c2e 0c40 0c30 0c41 0020 0c38 0c02 0c24 0c4b 0c37 0c02 0c17 0c3e 0020 "
            "0c09 0c02 0c21 0c3e 0c32 0c3f 002c 0020 0c2e 0c40 0020 0c2e 0c3e 0c30 0c4d 0c17 0c02 0020 "
            "0c38 0c41 0c17 0c2e 0c02 0020 0c15 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        hx("0c2a 0c4d 0c30 0c3f 0c2f 0c2e 0c48 0c28 0020 0c38 0c4d 0c28 0c47 0c39 0c3f 0c24 0c41 0c30 0c3e 0c32 0c3f 0c15 0c3f")
        + f": {UGADI_SUBHAKANKSHALU}. "
        + hx(
            "0c28 0c40 0020 0c28 0c35 0c4d 0c35 0c41 0020 0c08 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2e 0c30 0c3f 0c02 0c24 0020 0c2a 0c4d 0c30 0c15 0c3e 0c36 0c35 0c02 0c24 0c02 0020 "
            "0c15 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        "Copy for chat: Happy Ugadi! Thinking of you and sending warm Telugu wishes.",
    ],
    "english_2027": [
        "Happy Ugadi 2027! May this Telugu New Year fill your home with peace, health, and fresh beginnings.",
        "Ugadi 2027 wishes: May mango leaves, sweet Pachadi, and kind hearts welcome a brighter year.",
        "Wishing you happy Ugadi wishes for 2027, with courage for every sweet and sour moment ahead.",
        "May Ugadi 2027 bring prosperity, calm mornings, and goals that finally feel possible.",
        "Happy Ugadi! As the year turns, may your family stay close and your hopes stay high.",
        "Sending warm Ugadi 2027 greetings across every distance. Celebrate new beginnings with love.",
        "A short English card line: Happy Ugadi 2027. Fresh year, fresh grace, fresh gratitude.",
        "May this Ugadi remind you that every new chapter can start with hope and a smile.",
        "Happy Ugadi wishes 2027 for your WhatsApp status: New year energy, old friendships, endless thanks.",
        "Ugadi greetings for 2027: May your table stay full and your heart stay light.",
    ],
    "captions": [
        f"Ugadi caption: {UGADI_SUBHAKANKSHALU} 2027 | Fresh leaves, fresh hopes.",
        "Instagram status: Happy Ugadi! New year, same grateful heart.",
        "Story line: Mango toran, Ugadi Pachadi, and smiles all around.",
        f"Reel cover: {HAPPY_UGADI} 2027 | Celebrate the sweet and the sour.",
        "WhatsApp status: Ugadi vibes only. Peace, family, new beginnings.",
        "Caption idea: Starting the Telugu New Year with gratitude and gold light.",
        "Hashtag-ready: #HappyUgadi2027 #UgadiWishes #TeluguNewYear",
        "Photo note: Home feels brighter when Ugadi begins.",
    ],
    "traditional": [
        hx(
            "0c09 0c17 0c3e 0c26 0c3f 0020 0c2a 0c1a 0c4d 0c1a 0c21 0c3f 0020 "
            "0c17 0c41 0c30 0c4d 0c24 0c41 0020 0c1a 0c47 0c38 0c4d 0c24 0c41 0c02 0c26 0c3f"
        )
        + ": "
        + hx(
            "0c1c 0c40 0c35 0c3f 0c24 0c02 0c32 0c4b 0020 0c24 0c40 0c2a 0c3f 002c 0020 "
            "0c2a 0c41 0c32 0c41 0c2a 0c41 002c 0020 0c1a 0c47 0c26 0c41 0020 "
            "0c05 0c28 0c4d 0c28 0c40 0020 0c09 0c02 0c1f 0c3e 0c2f 0c3f"
        )
        + ". "
        + hx(
            "0c05 0c28 0c4d 0c28 0c3f 0c02 0c1f 0c3f 0c28 0c40 0020 0c06 0c28 0c02 0c26 0c02 0c17 0c3e 0020 "
            "0c38 0c4d 0c35 0c40 0c15 0c30 0c3f 0c02 0c1a 0c02 0c21 0c3f"
        )
        + ".",
        hx("0c2f 0c41 0c17 0c3e 0c26 0c3f 0020 0c05 0c02 0c1f 0c47 0020 0c15 0c4a 0c24 0c4d 0c24 0020 0c2f 0c41 0c17 0c02")
        + ". "
        + hx(
            "0c2e 0c40 0020 0c07 0c02 0c1f 0c4d 0c32 0c4b 0020 0c36 0c3e 0c02 0c24 0c3f 002c 0020 "
            "0c2d 0c15 0c4d 0c24 0c3f 002c 0020 0c10 0c15 0c4d 0c2f 0c24 0020 0c28 0c3f 0c02 0c21 0c3e 0c32 0c3f"
        )
        + ".",
        "May Lord Vishnu bless your home this Ugadi with clarity, courage, and quiet strength.",
        hx(
            "0c2e 0c3e 0c2e 0c3f 0c21 0c3f 0020 0c2a 0c42 0c32 0c41 0020 "
            "0c35 0c3f 0c15 0c38 0c3f 0c02 0c1a 0c3f 0c28 0c1f 0c4d 0c1f 0c41 0020 "
            "0c2e 0c40 0020 0c15 0c4b 0c30 0c3f 0c15 0c32 0c41 0020 0c08 0020 "
            "0c09 0c17 0c3e 0c26 0c3f 0c15 0c3f 0020 0c35 0c3f 0c15 0c38 0c3f 0c02 0c1a 0c3e 0c32 0c3f"
        )
        + ".",
        "Traditional blessing: Let prayer, gratitude, and family warmth open your Ugadi morning.",
        f"{UGADI_SUBHAM}. "
        + hx(
            "0c2a 0c42 0c1c 0c3e 0020 0c17 0c02 0c1f 0c32 0020 0c27 0c4d 0c35 0c28 0c3f 0020 "
            "0c2e 0c40 0020 0c07 0c02 0c1f 0c3f 0c15 0c3f 0020 "
            "0c36 0c41 0c2d 0c35 0c3e 0c30 0c4d 0c24 0c32 0c41 0020 "
            "0c24 0c40 0c38 0c41 0c15 0c41 0c30 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
        "Spiritual note: Welcome Ugadi with a calm mind and a generous heart.",
        hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2a 0c4d 0c30 0c3e 0c30 0c02 0c2d 0c02 0020 0c2d 0c15 0c4d 0c24 0c3f 0c24 0c4b 0020 "
            "0c15 0c3e 0c35 0c3e 0c32 0c3f 002c 0020 0c2e 0c41 0c17 0c3f 0c02 0c2a 0c41 0020 "
            "0c38 0c02 0c24 0c4b 0c37 0c02 0c24 0c4b 0020 0c15 0c3e 0c35 0c3e 0c32 0c3f"
        )
        + ".",
    ],
    "funny": [
        f"{HAPPY_UGADI}! "
        + hx("0c08 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 0c15 0c42 0c21 0c3e 0020")
        + "resolutions "
        + hx(
            "0c2e 0c30 0c4d 0c1a 0c3f 0c2a 0c4b 0c15 0c41 0c02 0c21 0c3e 0020 "
            "0c09 0c02 0c21 0c3e 0c32 0c28 0c3f 0020 0c2a 0c4d 0c30 0c3e 0c30 0c4d 0c25 0c28"
        )
        + ".",
        "May your Ugadi plate stay fuller than your to-do list. Happy Ugadi 2027!",
        f"{UGADI_SUBHAKANKSHALU}! "
        + hx("0c2a 0c1a 0c4d 0c1a 0c21 0c3f 0020 0c24 0c3f 0c28 0c4d 0c28 0c3e 0c15 0020")
        + "diet "
        + hx("0c2e 0c3e 0c1f 0c4d 0c32 0c3e 0c21 0c15 0c02 0c21 0c3f")
        + ".",
        "New year, new hope, same family WhatsApp forwards. Happy Ugadi anyway!",
        "May sweets arrive before meetings this Ugadi. Priorities matter.",
    ],
}

faqs = [
    (
        "What are some happy Ugadi wishes in Telugu for 2027?",
        "Start with a clear greeting such as \u201c"
        + UGADI_SUBHAKANKSHALU
        + "! "
        + hx(
            "0c2e 0c40 0020 0c15 0c41 0c1f 0c41 0c02 0c2c 0c3e 0c28 0c3f 0c15 0c3f 0020 "
            "0c38 0c02 0c24 0c4b 0c37 0c02 002c 0020 0c06 0c30 0c4b 0c17 0c4d 0c2f 0c02 002c 0020 "
            "0c35 0c3f 0c1c 0c2f 0c02 0020 0c15 0c32 0c17 0c3e 0c32 0c28 0c3f 0020 "
            "0c15 0c4b 0c30 0c41 0c15 0c41 0c02 0c1f 0c41 0c28 0c4d 0c28 0c3e 0c28 0c41"
        )
        + ".\u201d Happy Ugadi wishes in Telugu work best when they mention family, health, and a fresh year. "
        "Update older 2021, 2022, or 2023 lines to Ugadi 2027 before you send them.",
    ),
    (
        "What is a good WhatsApp Ugadi wish in Telugu?",
        "Keep WhatsApp Ugadi wishes under three lines: greeting, one blessing, and a warm close. "
        "Example: \u201c"
        + HAPPY_UGADI
        + " 2027! "
        + hx(
            "0c15 0c4a 0c24 0c4d 0c24 0020 0c38 0c02 0c35 0c24 0c4d 0c38 0c30 0c02 0020 "
            "0c2e 0c40 0020 0c07 0c02 0c1f 0c4d 0c32 0c4b 0020 0c15 0c4a 0c24 0c4d 0c24 0020 "
            "0c06 0c36 0c32 0c41 0020 0c28 0c3f 0c02 0c2a 0c3e 0c32 0c3f"
        )
        + ".\u201d Short Telugu lines share cleanly in family groups.",
    ),
    (
        "How do I write ugadi wishes in Telugu for family?",
        "Name the relation, thank them, and add one hope for the new year. "
        "Example for parents: \u201c"
        + hx("0c05 0c2e 0c4d 0c2e 0c3e 002c 0020 0c28 0c3e 0c28 0c4d 0c28 0c3e")
        + f": {UGADI_SUBHAKANKSHALU}. "
        + hx("0c2e 0c40 0020 0c06 0c36 0c40 0c30 0c4d 0c35 0c3e 0c26 0c3e 0c32 0c47 0020 0c2e 0c3e 0020 0c2c 0c32 0c02")
        + ".\u201d Ugadi wishes in Telugu 2027 feel warmer when they sound personal.",
    ),
    (
        "What are happy Ugadi wishes 2027 in English?",
        "Try: \u201cHappy Ugadi 2027! May this Telugu New Year fill your home with peace, health, and fresh beginnings.\u201d "
        "English Ugadi 2027 wishes help when your chat has mixed-language friends or colleagues.",
    ),
    (
        "Can I reuse Ugadi 2021, 2022, or 2023 wishes this year?",
        "Yes, but refresh the year to 2027 and check the tone still fits. "
        "Searchers looking for Ugadi 2021 wishes or happy Ugadi 2023 wishes usually want current, "
        "copy-ready greetings for the next Ugadi celebration.",
    ),
    (
        "What is a thoughtful Ugadi gift idea from BlueStone?",
        "Earrings, pendants, bangles, and mangalsutra styles such as The Rohal Huggie Earrings, "
        "The Valeria Rose Pendant, or The Aarabhi Mangalsutra make lasting Ugadi keepsakes that go beyond sweets and cards.",
    ),
    (
        "What does Ugadi Pachadi teach us for wishes?",
        "Ugadi Pachadi mixes sweet, sour, and bitter tastes to mirror real life. "
        "A thoughtful Ugadi message can wish someone balance through every flavour of the year ahead.",
    ),
]


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "output/Week1_Rank21_Ugadi_sections.json"
    payload = {"sections": sections, "faqs": faqs}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if "\ufffd" in text:
        raise SystemExit("Replacement character found in generated Telugu content")
    out.write_text(text, encoding="utf-8")
    print("Wrote", out)
    print("Sample:", sections["whatsapp_telugu"][0])
    print("Counts:", {k: len(v) for k, v in sections.items()})


if __name__ == "__main__":
    main()
