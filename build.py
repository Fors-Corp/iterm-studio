#!/usr/bin/env python3
"""Single source of truth for iTerm Studio presets.

Emits:
  presets.json   consumed by the `iterm-studio` CLI + local server
  presets.js     same data for a static / hosted build of the picker

Run:  python3 build.py
"""
import colorsys, json, pathlib, re

HERE = pathlib.Path(__file__).parent

# window defaults per category: (transparency, blur, cursor)
WIN = {
    "dark":  (0.05, 20, "block"),
    "light": (0.00, 0,  "bar"),
    "neon":  (0.12, 28, "bar"),
    "warm":  (0.03, 14, "block"),
    "mono":  (0.06, 18, "block"),
    "stack": (0.04, 18, "block"),
}
FLAVOR_CYCLE = ["lean2", "powerline", "pill", "minimal", "rainbow"]

TOOLS = {
    "modern-cli": ["eza", "bat", "fd", "fzf", "zoxide", "git-delta", "zsh-fast-syntax-highlighting"],
    "dev-stack":  ["eza", "bat", "fzf", "zoxide", "atuin", "git-delta", "btop"],
}

_presets = []

def P(pid, name, cat, flavor, base6, ansi16, *, font="MesloLGS NF", win=None, tools=None):
    fg, bg, cur, curT, sel, selT = base6.split()
    ansi = ansi16.split()
    assert len(ansi) == 16, f"{pid}: need 16 ansi, got {len(ansi)}"
    for h in [fg, bg, cur, curT, sel, selT, *ansi]:
        assert re.fullmatch(r"[0-9a-fA-F]{6}", h), f"{pid}: bad hex {h!r}"
    t, b, c = win or WIN[cat]
    _presets.append({
        "id": pid, "name": name, "category": cat, "flavor": flavor,
        "blurb": BLURB.get(pid, ""),
        "window": {"transparency": t, "blur": b, "cursor": c, "font": font},
        "tools": tools or TOOLS.get(pid, []),
        "colors": {
            "fg": "#" + fg, "bg": "#" + bg, "cursor": "#" + cur, "cursorText": "#" + curT,
            "selection": "#" + sel, "selectedText": "#" + selT, "ansi": ["#" + x for x in ansi],
        },
    })

# --------------------------------------------------------------------------- #
BLURB = {
 "tokyo-night": "Cool indigo, periwinkle path, amber branch. The balanced default.",
 "tokyo-night-moon": "Tokyo Night with a softer, bluer ground and mint accents.",
 "tokyo-night-day": "The same palette flipped to daylight — ink-blue on soft paper.",
 "catppuccin-mocha": "Warm charcoal with pastel mauve, peach and sage.",
 "catppuccin-macchiato": "Mocha's slightly lighter, bluer sibling.",
 "catppuccin-frappe": "The mid-tone Catppuccin — muted, cosy, low glare.",
 "catppuccin-latte": "The light Catppuccin — gentle, colourful, easy on the eyes.",
 "rose-pine": "Dusk violet, foam cyan and gold. Hushed rather than technical.",
 "rose-pine-moon": "Rosé Pine one notch brighter — a touch more contrast.",
 "rose-pine-dawn": "Rosé Pine at sunrise — rosy taupe on warm cream.",
 "gruvbox-dark-hard": "Retro warm browns, mustard and rust. Hard contrast.",
 "gruvbox-dark-medium": "The canonical Gruvbox dark.",
 "gruvbox-dark-soft": "Gruvbox with the background lifted a shade.",
 "gruvbox-light": "Gruvbox by daylight — cream paper, earthy ink.",
 "gruvbox-material-dark": "Gruvbox with the saturation pulled back. Matte and calm.",
 "nord": "Arctic slate, frost blues, snow. Evenly muted.",
 "nightfox": "EdenNight's flagship — deep blue-grey, well-tempered accents.",
 "duskfox": "Nightfox at dusk — violet ground, rosy highlights.",
 "carbonfox": "IBM Carbon in the dark — crisp, high-legibility, techy.",
 "terafox": "Earthy teal-and-terracotta take on Nightfox.",
 "kanagawa-wave": "Hokusai sumi-ink black, one wave-blue, dry gold, a sakura spark.",
 "kanagawa-dragon": "Kanagawa's darker, greyer, dragon-scale variant.",
 "kanagawa-lotus": "Kanagawa by day — warm parchment and muted ink.",
 "everforest-dark": "Earthy green-grey, matte and low-contrast.",
 "everforest-light": "Everforest daylight — pale sage paper.",
 "dracula": "The classic — bright green, pink, purple on bruise-grey.",
 "one-dark": "Atom's One Dark. Familiar, neutral, mid-contrast.",
 "one-light": "One Dark's daylight counterpart.",
 "solarized-dark": "Ethan Schoonover's precisely-balanced teal-and-tan.",
 "solarized-light": "Solarized on its cream ground.",
 "ayu-dark": "Near-black with a warm amber cursor. Minimal and modern.",
 "ayu-mirage": "The mid Ayu — muted navy, soft orange accents.",
 "ayu-light": "Ayu by day — bright, clean, warm-accented.",
 "material-ocean": "Material Theme at its deepest blue.",
 "material-palenight": "Material's soft violet-grey. A crowd favourite.",
 "material-darker": "Near-black Material — high contrast, low colour.",
 "monokai": "The Sublime Text original — lime, magenta, cyan on olive-black.",
 "monokai-pro": "Monokai refined: warmer ground, gentler accents.",
 "github-dark": "GitHub's own dark theme. Neutral and readable.",
 "github-light": "GitHub light — the web's default code look.",
 "github-dark-dimmed": "GitHub dark with the contrast eased for night work.",
 "night-owl": "Sarah Drasner's deep-ocean blue, tuned for low light.",
 "light-owl": "Night Owl's daylight sibling.",
 "synthwave-84": "Neon magenta and cyan on a purple night. Loud on purpose.",
 "horizon": "Warm coral and teal on plum-grey. Soft but vivid.",
 "panda": "Friendly, clean, high-contrast — mint, pink, blue on graphite.",
 "snazzy": "Hyper's signature look — punchy pastels on slate.",
 "cobalt2": "Wes Bos's blue — saturated, confident, yellow-accented.",
 "oceanic-next": "Deep sea-green with restrained accents.",
 "palenight": "Palenight on its own — the softer Material violet.",
 "zenburn": "The original low-contrast theme. Grey-green, restful.",
 "tomorrow-night": "Chris Kempson's balanced dark. The base16 wellspring.",
 "iceberg": "Bluish-grey with a cold, even palette. Vim classic.",
 "poimandres": "Teal, rose and pale blue on near-black. Very 2021.",
 "vitesse-dark": "Anthony Fu's editor theme — muted, warm-neutral, precise.",
 "vitesse-light": "Vitesse by day.",
 "flexoki-dark": "Steph Ango's ink-on-paper system, dark mode.",
 "flexoki-light": "Flexoki light — warm paper, saturated but calm ink.",
 "aura": "Purple-forward with electric mint. Bold and modern.",
 "molokai": "Monokai's punchier Vim cousin.",
 "railscasts": "The mid-2000s screencast staple — warm, brown, amber.",
 "spacegray": "Understated blue-grey with muted accents.",
 "twilight": "Old TextMate warmth — tan, olive, dusty blue.",
 "modern-cli": "Catppuccin Frappé + a modern toolbelt: eza, bat, fzf, fd, zoxide, delta.",
 "dev-stack": "Gruvbox + eza, bat, fzf, zoxide, atuin, delta, btop. The works.",
}

# ---- curated schemes ----------------------------------------------------- #
P("tokyo-night","Tokyo Night","dark","lean2",
  "c0caf5 24283b c0caf5 24283b 364a82 c0caf5",
  "1d202f f7768e 9ece6a e0af68 7aa2f7 bb9af7 7dcfff a9b1d6 414868 f7768e 9ece6a e0af68 7aa2f7 bb9af7 7dcfff c0caf5")
P("tokyo-night-moon","Tokyo Night Moon","dark","lean2",
  "c8d3f5 222436 c8d3f5 222436 2d3f76 c8d3f5",
  "1b1d2b ff757f c3e88d ffc777 82aaff c099ff 86e1fc 828bb8 444a73 ff757f c3e88d ffc777 82aaff c099ff 86e1fc c8d3f5")
P("tokyo-night-day","Tokyo Night Day","light","lean2",
  "3760bf e1e2e7 3760bf e1e2e7 b6bfe2 3760bf",
  "b4b5b9 f52a65 587539 8c6c3e 2e7de9 9854f1 007197 6172b0 a1a6c5 f52a65 587539 8c6c3e 2e7de9 9854f1 007197 3760bf")
P("catppuccin-mocha","Catppuccin Mocha","dark","pill",
  "cdd6f4 1e1e2e f5e0dc 1e1e2e 414356 cdd6f4",
  "45475a f38ba8 a6e3a1 f9e2af 89b4fa f5c2e7 94e2d5 bac2de 585b70 f38ba8 a6e3a1 f9e2af 89b4fa f5c2e7 94e2d5 a6adc8")
P("catppuccin-macchiato","Catppuccin Macchiato","dark","pill",
  "cad3f5 24273a f4dbd6 24273a 494d64 cad3f5",
  "494d64 ed8796 a6da95 eed49f 8aadf4 f5bde6 8bd5ca b8c0e0 5b6078 ed8796 a6da95 eed49f 8aadf4 f5bde6 8bd5ca a5adcb")
P("catppuccin-frappe","Catppuccin Frappé","dark","pill",
  "c6d0f5 303446 f2d5cf 303446 414559 c6d0f5",
  "51576d e78284 a6d189 e5c890 8caaee f4b8e4 81c8be b5bfe2 626880 e78284 a6d189 e5c890 8caaee f4b8e4 81c8be a5adce")
P("catppuccin-latte","Catppuccin Latte","light","pill",
  "4c4f69 eff1f5 dc8a78 eff1f5 bcc0cc 4c4f69",
  "5c5f77 d20f39 40a02b df8e1d 1e66f5 ea76cb 179299 acb0be 6c6f85 d20f39 40a02b df8e1d 1e66f5 ea76cb 179299 bcc0cc")
P("rose-pine","Rosé Pine","dark","lean2",
  "e0def4 191724 e0def4 191724 403d52 e0def4",
  "26233a eb6f92 31748f f6c177 9ccfd8 c4a7e7 ebbcba e0def4 6e6a86 eb6f92 31748f f6c177 9ccfd8 c4a7e7 ebbcba e0def4")
P("rose-pine-moon","Rosé Pine Moon","dark","lean2",
  "e0def4 232136 e0def4 232136 44415a e0def4",
  "393552 eb6f92 3e8fb0 f6c177 9ccfd8 c4a7e7 ea9a97 e0def4 6e6a86 eb6f92 3e8fb0 f6c177 9ccfd8 c4a7e7 ea9a97 e0def4")
P("rose-pine-dawn","Rosé Pine Dawn","light","lean2",
  "575279 faf4ed 575279 faf4ed dfdad9 575279",
  "f2e9e1 b4637a 286983 ea9d34 56949f 907aa9 d7827e 575279 9893a5 b4637a 286983 ea9d34 56949f 907aa9 d7827e 575279")
P("gruvbox-dark-hard","Gruvbox Dark Hard","warm","powerline",
  "ebdbb2 1d2021 ebdbb2 1d2021 3c3836 ebdbb2",
  "282828 cc241d 98971a d79921 458588 b16286 689d6a a89984 928374 fb4934 b8bb26 fabd2f 83a598 d3869b 8ec07c ebdbb2")
P("gruvbox-dark-medium","Gruvbox Dark","warm","powerline",
  "ebdbb2 282828 ebdbb2 282828 3c3836 ebdbb2",
  "282828 cc241d 98971a d79921 458588 b16286 689d6a a89984 928374 fb4934 b8bb26 fabd2f 83a598 d3869b 8ec07c ebdbb2")
P("gruvbox-dark-soft","Gruvbox Dark Soft","warm","powerline",
  "ebdbb2 32302f ebdbb2 32302f 3c3836 ebdbb2",
  "282828 cc241d 98971a d79921 458588 b16286 689d6a a89984 928374 fb4934 b8bb26 fabd2f 83a598 d3869b 8ec07c ebdbb2")
P("gruvbox-light","Gruvbox Light","light","powerline",
  "3c3836 fbf1c7 3c3836 fbf1c7 ebdbb2 3c3836",
  "fbf1c7 cc241d 98971a d79921 458588 b16286 689d6a 7c6f64 928374 9d0006 79740e b57614 076678 8f3f71 427b58 3c3836")
P("gruvbox-material-dark","Gruvbox Material","warm","lean2",
  "d4be98 282828 d4be98 282828 45403d d4be98",
  "3c3836 ea6962 a9b665 d8a657 7daea3 d3869b 89b482 d4be98 45403d ea6962 a9b665 d8a657 7daea3 d3869b 89b482 d4be98")
P("nord","Nord","dark","minimal",
  "d8dee9 2e3440 d8dee9 2e3440 434c5e d8dee9",
  "3b4252 bf616a a3be8c ebcb8b 81a1c1 b48ead 88c0d0 e5e9f0 4c566a bf616a a3be8c ebcb8b 81a1c1 b48ead 8fbcbb eceff4")
P("nightfox","Nightfox","dark","powerline",
  "cdcecf 192330 cdcecf 192330 2b3b51 cdcecf",
  "393b44 c94f6d 81b29a dbc074 719cd6 9d79d6 63cdcf dbdcdd 575860 d16983 8ebaa4 e0c989 86abdc baa1e2 7ad5d6 e4e4e5")
P("duskfox","Duskfox","dark","powerline",
  "e0def4 232136 e0def4 232136 433c59 e0def4",
  "393552 eb6f92 a3be8c f6c177 569fba c4a7e7 9ccfd8 e0def4 47407d eb98c3 a3be8c f6c177 65b1d3 ecb4d3 9ccfd8 e0def4")
P("carbonfox","Carbonfox","dark","powerline",
  "f2f4f8 161616 f2f4f8 161616 2a2a2a f2f4f8",
  "282828 ee5396 25be6a 08bdba 78a9ff be95ff 33b1ff dfdfe0 484848 ee5396 46c880 2dc7c4 8cb6ff c8a5ff 52bdff ffffff")
P("terafox","Terafox","dark","lean2",
  "e6eaea 152528 e6eaea 152528 293e40 e6eaea",
  "2f3239 e85c51 7aa4a1 fda47f 5a93aa ad5c7c a1cdd8 eaeeee 4e5157 eb746b 8eb2af fdb292 73a3b7 c58c98 b3cbd2 eeeeee")
P("kanagawa-wave","Kanagawa Wave","dark","lean2",
  "dcd7ba 1f1f28 c8c093 1f1f28 2d4f67 dcd7ba",
  "090618 c34043 76946a c0a36e 7e9cd8 957fb8 6a9589 c8c093 727169 e82424 98bb6c e6c384 7fb4ca 938aa9 7aa89f dcd7ba")
P("kanagawa-dragon","Kanagawa Dragon","dark","lean2",
  "c5c9c5 181616 c8c093 181616 2d4f67 c5c9c5",
  "0d0c0c c4746e 8a9a7b c4b28a 8ba4b0 a292a3 8ea4a2 c8c093 a6a69c e46876 87a987 e6c384 7fb4ca 938aa9 7aa89f c5c9c5")
P("kanagawa-lotus","Kanagawa Lotus","light","lean2",
  "545464 f2ecbc 43436c f2ecbc c9cbd1 545464",
  "d5cea3 c84053 6f894e 77713f 4d699b b35b79 597b75 545464 8a8980 d7474b 6e915f 836f4a 6693bf 624c83 5e857a 43436c")
P("everforest-dark","Everforest Dark","dark","minimal",
  "d3c6aa 2d353b d3c6aa 2d353b 475258 d3c6aa",
  "4b565c e67e80 a7c080 dbbc7f 7fbbb3 d699b6 83c092 d3c6aa 5c6a72 e67e80 a7c080 dbbc7f 7fbbb3 d699b6 83c092 d3c6aa")
P("everforest-light","Everforest Light","light","minimal",
  "5c6a72 fdf6e3 5c6a72 fdf6e3 edeada 5c6a72",
  "e6e2cc f85552 8da101 dfa000 3a94c5 df69ba 35a77c 5c6a72 939f91 f85552 8da101 dfa000 3a94c5 df69ba 35a77c 5c6a72")
P("dracula","Dracula","dark","rainbow",
  "f8f8f2 282a36 f8f8f2 282a36 44475a f8f8f2",
  "21222c ff5555 50fa7b f1fa8c bd93f9 ff79c6 8be9fd f8f8f2 6272a4 ff6e6e 69ff94 ffffa5 d6acff ff92df a4ffff ffffff")
P("one-dark","One Dark","dark","powerline",
  "abb2bf 282c34 abb2bf 282c34 3e4451 abb2bf",
  "3f4451 e05561 8cc265 d18f52 4aa5f0 c162de 42b3c2 e6e6e6 4f5666 ff616e a5e075 f0a45d 4dc4ff de73ff 4cd1e0 d7dae0")
P("one-light","One Light","light","powerline",
  "383a42 fafafa 383a42 fafafa e5e5e6 383a42",
  "383a42 e45649 50a14f c18401 4078f2 a626a4 0184bc a0a1a7 4f525d e06c75 98c379 e5c07b 61afef c678dd 56b6c2 090a0b")
P("solarized-dark","Solarized Dark","dark","lean2",
  "839496 002b36 93a1a1 002b36 073642 93a1a1",
  "073642 dc322f 859900 b58900 268bd2 d33682 2aa198 eee8d5 002b36 cb4b16 586e75 657b83 839496 6c71c4 93a1a1 fdf6e3")
P("solarized-light","Solarized Light","light","lean2",
  "657b83 fdf6e3 586e75 fdf6e3 eee8d5 586e75",
  "073642 dc322f 859900 b58900 268bd2 d33682 2aa198 eee8d5 002b36 cb4b16 586e75 657b83 839496 6c71c4 93a1a1 fdf6e3")
P("ayu-dark","Ayu Dark","dark","minimal",
  "bfbdb6 0b0e14 e6b450 0b0e14 1b3a5b bfbdb6",
  "01060e ea6c73 91b362 f9af4f 53bdfa fae994 90e1c6 c7c7c7 686868 f07178 c2d94c ffb454 59c2ff ffee99 95e6cb ffffff")
P("ayu-mirage","Ayu Mirage","dark","minimal",
  "cbccc6 1f2430 ffcc66 1f2430 33415e cbccc6",
  "191e2a ed8274 a6cc70 fad07b 6dcbfa cfbafa 90e1c6 c7c7c7 686868 f28779 bae67e ffd580 73d0ff d4bfff 95e6cb ffffff")
P("ayu-light","Ayu Light","light","minimal",
  "5c6166 fcfcfc ff9940 fcfcfc 8fb3ff 5c6166",
  "010101 e7666a 6cbf43 f2ae49 3199e1 9e75c7 46ba94 c7c7c7 686868 f0717a 86b300 f2ae49 399ee6 a37acc 4cbf99 fcfcfc")
P("material-ocean","Material Ocean","dark","powerline",
  "8f93a2 0f111a ffcc00 0f111a 1f2233 8f93a2",
  "546e7a ff5370 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff 546e7a ff5370 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff")
P("material-palenight","Material Palenight","dark","powerline",
  "a6accd 292d3e ffcc00 292d3e 444267 a6accd",
  "292d3e f07178 c3e88d ffcb6b 82aaff c792ea 89ddff d0d0d0 434758 ff8b92 ddffa7 ffe585 9cc4ff ddb0f6 a3f7ff ffffff")
P("material-darker","Material Darker","dark","powerline",
  "eeffff 212121 ffcc00 212121 404040 eeffff",
  "000000 ff5370 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff 545454 ff5370 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff")
P("monokai","Monokai","dark","rainbow",
  "f8f8f2 272822 f8f8f0 272822 49483e f8f8f2",
  "272822 f92672 a6e22e f4bf75 66d9ef ae81ff a1efe4 f8f8f2 75715e f92672 a6e22e f4bf75 66d9ef ae81ff a1efe4 f9f8f5")
P("monokai-pro","Monokai Pro","dark","rainbow",
  "fcfcfa 2d2a2e fcfcfa 2d2a2e 5b595c fcfcfa",
  "403e41 ff6188 a9dc76 ffd866 fc9867 ab9df2 78dce8 fcfcfa 727072 ff6188 a9dc76 ffd866 fc9867 ab9df2 78dce8 fcfcfa")
P("github-dark","GitHub Dark","dark","lean2",
  "c9d1d9 0d1117 58a6ff 0d1117 264f78 c9d1d9",
  "484f58 ff7b72 3fb950 d29922 58a6ff bc8cff 39c5cf b1bac4 6e7681 ffa198 56d364 e3b341 79c0ff d2a8ff 56d4dd f0f6fc")
P("github-light","GitHub Light","light","lean2",
  "24292f ffffff 0969da ffffff add6ff 24292f",
  "24292f cf222e 116329 4d2d00 0969da 8250df 1b7c83 6e7781 57606a a40e26 1a7f37 633c01 218bff a475f9 3192aa 8c959f")
P("github-dark-dimmed","GitHub Dimmed","dark","lean2",
  "adbac7 22272e 539bf5 22272e 2d333b adbac7",
  "545d68 f47067 57ab5a c69026 539bf5 b083f0 39c5cf 909dab 636e7b ff938a 6bc46d daaa3f 6cb6ff dcbdfb 56d4dd cdd9e5")
P("night-owl","Night Owl","dark","lean2",
  "d6deeb 011627 80a4c2 011627 1d3b53 d6deeb",
  "011627 ef5350 22da6e c5e478 82aaff c792ea 21c7a8 ffffff 575656 ef5350 22da6e ffeb95 82aaff c792ea 7fdbca ffffff")
P("light-owl","Light Owl","light","lean2",
  "403f53 fbfbfb 90a7b2 fbfbfb dbf0ff 403f53",
  "403f53 de3d3b 08916a e0af02 288ed7 d6438a 2aa298 f0f0f0 626262 de3d3b 08916a daaa01 288ed7 d6438a 2aa298 090a0b")
P("synthwave-84","Synthwave '84","neon","rainbow",
  "ffffff 262335 ff7edb 262335 463465 ffffff",
  "262335 fe4450 72f1b8 fede5d 03edf9 ff7edb 03edf9 ffffff 495495 fe4450 72f1b8 fede5d 03edf9 ff7edb 03edf9 ffffff")
P("horizon","Horizon","dark","pill",
  "d5d8da 1c1e26 fab795 1c1e26 2e303e d5d8da",
  "16161c e95678 29d398 fab795 26bbd9 ee64ac 59e1e3 d5d8da 2e303e ec6a88 3fdaa4 fbc3a7 3fc4de f075b5 6be4e6 d5d8da")
P("panda","Panda","dark","lean2",
  "e6e6e6 292a2b ff2c6d 292a2b 3b3c3d e6e6e6",
  "292a2b ff2c6d 19f9d8 ffb86c 45a9f9 ff75b5 6fc1ff e6e6e6 676b79 ff2c6d 19f9d8 ffcc95 6fc1ff ff9ac1 6fc1ff fefeff")
P("snazzy","Hyper Snazzy","dark","pill",
  "eff0eb 282a36 97979b 282a36 3f4451 eff0eb",
  "282a36 ff5c57 5af78e f3f99d 57c7ff ff6ac1 9aedfe f1f1f0 686868 ff5c57 5af78e f3f99d 57c7ff ff6ac1 9aedfe eff0eb")
P("cobalt2","Cobalt2","dark","powerline",
  "ffffff 132738 f8dd00 132738 18384c ffffff",
  "000000 ff0000 38de21 ffe50a 1460d2 ff005d 00bbbb bbbbbb 555555 f40e17 3bd01d edc809 5555ff ff55ff 6ae3fa ffffff")
P("oceanic-next","Oceanic Next","dark","lean2",
  "d8dee9 1b2b34 cdd3de 1b2b34 4f5b66 d8dee9",
  "343d46 ec5f67 99c794 fac863 6699cc c594c5 5fb3b3 d8dee9 65737e ec5f67 99c794 fac863 6699cc c594c5 5fb3b3 d8dee9")
P("palenight","Palenight","dark","pill",
  "bfc7d5 292d3e ffcc00 292d3e 3c435e bfc7d5",
  "292d3e f07178 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff 676e95 f07178 c3e88d ffcb6b 82aaff c792ea 89ddff ffffff")
P("zenburn","Zenburn","warm","minimal",
  "dcdccc 3f3f3f 8faf9f 3f3f3f 585858 dcdccc",
  "4d4d4d 705050 60b48a dfaf8f 506070 dc8cc3 8cd0d3 dcdccc 709080 dca3a3 c3bf9f f0dfaf 94bff3 ec93d3 93e0e3 ffffff")
P("tomorrow-night","Tomorrow Night","dark","lean2",
  "c5c8c6 1d1f21 c5c8c6 1d1f21 373b41 c5c8c6",
  "1d1f21 cc6666 b5bd68 f0c674 81a2be b294bb 8abeb7 c5c8c6 969896 cc6666 b5bd68 f0c674 81a2be b294bb 8abeb7 ffffff")
P("iceberg","Iceberg","dark","minimal",
  "c6c8d1 161821 c6c8d1 161821 272c42 c6c8d1",
  "1e2132 e27878 b4be82 e2a478 84a0c6 a093c7 89b8c2 c6c8d1 6b7089 e98989 c0ca8e e9b189 91acd1 ada0d3 95c4ce d2d4de")
P("poimandres","Poimandres","dark","lean2",
  "a6accd 1b1e28 a6accd 1b1e28 303340 a6accd",
  "1b1e28 d0679d 5de4c7 fffac2 89ddff fcc5e9 add7ff ffffff a6accd d0679d 5de4c7 fffac2 add7ff fae4fc add7ff ffffff")
P("vitesse-dark","Vitesse Dark","dark","minimal",
  "dbd7ca 121212 dbd7ca 121212 191919 dbd7ca",
  "393a34 cb7676 4d9375 e6cc77 6394bf 9e7cb0 5eaab5 dbd7ca 5a5b53 d17070 87ae94 f0d999 74add4 c586c0 8bcdcf f5f4ec")
P("vitesse-light","Vitesse Light","light","minimal",
  "393a34 ffffff 393a34 ffffff e5e5e5 393a34",
  "121212 ab5959 4d9375 bda437 296aa3 a35ca3 2993a3 dbd7ca 777777 ab5959 4d9375 bda437 296aa3 a35ca3 2993a3 393a34")
P("flexoki-dark","Flexoki Dark","warm","lean2",
  "cecdc3 100f0f cecdc3 100f0f 282726 cecdc3",
  "1c1b1a d14d41 879a39 d0a215 4385be ce5d97 3aa99f cecdc3 575653 d14d41 879a39 d0a215 4385be ce5d97 3aa99f fffcf0")
P("flexoki-light","Flexoki Light","light","lean2",
  "100f0f fffcf0 100f0f fffcf0 e6e4d9 100f0f",
  "100f0f af3029 66800b ad8301 205ea6 a02f6f 24837b 6f6e69 b7b5ac d14d41 879a39 d0a215 4385be ce5d97 3aa99f cecdc3")
P("aura","Aura","dark","rainbow",
  "edecee 15141b edecee 15141b 3d375e 61ffca",
  "110f18 ff6767 61ffca a1efd3 a277ff a277ff 61ffca edecee 6d6d6d ff6767 61ffca c9a0ff a277ff a277ff 61ffca edecee")
P("molokai","Molokai","dark","rainbow",
  "f8f8f2 1b1d1e f8f8f2 1b1d1e 403d3d f8f8f2",
  "1b1d1e f92672 82b414 fd971f 56c2d6 8c54fe 465457 ccccc6 505354 ff669d 9fd016 fd971f 56c2d6 8c54fe 465457 f8f8f2")
P("railscasts","Railscasts","warm","powerline",
  "e6e1dc 2b2b2b e6e1dc 2b2b2b 4b4b4b e6e1dc",
  "2b2b2b da4939 a5c261 ffc66d 6d9cbe b6b3eb 519f50 e6e1dc 5a647e da4939 a5c261 ffc66d 6d9cbe b6b3eb 519f50 f9f7f3")
P("spacegray","Spacegray","dark","minimal",
  "b3b8c3 20242d b3b8c3 20242d 16181e b3b8c3",
  "000000 b04b57 87b379 e5c179 7d8fa4 a47996 85a7a5 b3b8c3 000000 b04b57 87b379 e5c179 7d8fa4 a47996 85a7a5 ffffff")
P("twilight","Twilight","warm","lean2",
  "ffffff 141414 ffffff 141414 313131 ffffff",
  "141414 c06d4d cf9a4e 87af5f 5f87af 5f5f87 5f8787 ffffd7 262626 c06d4d cf9a4e 87af5f 5f87af 5f5f87 5f8787 ffffff")
P("modern-cli","Modern CLI","stack","powerline",
  "c6d0f5 303446 f2d5cf 303446 414559 c6d0f5",
  "51576d e78284 a6d189 e5c890 8caaee f4b8e4 81c8be b5bfe2 626880 e78284 a6d189 e5c890 8caaee f4b8e4 81c8be a5adce",
  font="JetBrainsMono Nerd Font")
P("dev-stack","Dev Stack","stack","powerline",
  "ebdbb2 1d2021 ebdbb2 1d2021 3c3836 ebdbb2",
  "282828 cc241d 98971a d79921 458588 b16286 689d6a a89984 928374 fb4934 b8bb26 fabd2f 83a598 d3869b 8ec07c ebdbb2")

# --------------------------------------------------------------------------- #
#  procedurally generated "creative" families — coherent HSL ramps
# --------------------------------------------------------------------------- #
def hx(r, g, b):
    return f"{max(0,min(255,round(r))):02x}{max(0,min(255,round(g))):02x}{max(0,min(255,round(b))):02x}"

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l, s)
    return hx(r * 255, g * 255, b * 255)

def make(pid, name, cat, flavor, base_h, *, mode="dark", accent_s=0.62, tint=0.0, font="MesloLGS NF"):
    """Build a 16-colour ramp around base_h.  tint biases the neutral toward base_h."""
    dark = mode != "light"
    bg_l   = 0.07 if dark else 0.955
    fg_l   = 0.86 if dark else 0.22
    dim_l  = 0.42 if dark else 0.55
    sel_l  = 0.20 if dark else 0.86
    bg  = hsl(base_h, 0.16 + tint, bg_l)
    fg  = hsl(base_h, 0.10, fg_l)
    dim = hsl(base_h, 0.14, dim_l)
    sel = hsl(base_h, 0.25, sel_l)
    # 6 accent hues fanned around base_h: red · green · yellow · orange · blue · magenta
    hues = [base_h - 25, base_h + 95, base_h + 55, base_h + 20, base_h + 200, base_h + 260]
    norm_l = 0.58 if dark else 0.42
    brt_l  = 0.70 if dark else 0.36
    normal = [hsl(h, accent_s, norm_l) for h in hues]
    bright = [hsl(h, min(1, accent_s + 0.12), brt_l) for h in hues]
    ansi = [
        hsl(base_h, 0.18, 0.16 if dark else 0.90),          # 0  black
        normal[0], normal[1], normal[2], normal[4], normal[5], hsl(hues[4] + 20, accent_s, norm_l), fg,   # 1-7
        dim,                                                # 8  bright black
        bright[0], bright[1], bright[2], bright[4], bright[5], hsl(hues[4] + 20, accent_s + .1, brt_l),
        hsl(base_h, 0.05, 0.97 if dark else 0.12),          # 15 bright white
    ]
    cur = normal[3]
    BLURB.setdefault(pid, name + " — a generated palette built around one hue.")
    P(pid, name, cat, flavor, f"{fg} {bg} {cur} {bg} {sel} {fg}", " ".join(ansi), font=font)

GEN = [
 # id, name, category, flavor, base hue, mode, saturation, tint
 ("ember","Ember","warm","lean2", 18, "dark", 0.70, 0.05),
 ("rust","Rust","warm","powerline", 12, "dark", 0.58, 0.06),
 ("amberglow","Amber Glow","warm","minimal", 38, "dark", 0.72, 0.08),
 ("espresso","Espresso","warm","lean2", 26, "dark", 0.40, 0.10),
 ("sandstone","Sandstone","warm","minimal", 34, "light", 0.42, 0.06),
 ("clay","Clay","warm","lean2", 20, "light", 0.40, 0.05),
 ("moss","Moss","dark","minimal", 110, "dark", 0.45, 0.04),
 ("fern","Fern","dark","lean2", 130, "dark", 0.52, 0.03),
 ("pine","Pine","dark","powerline", 155, "dark", 0.48, 0.04),
 ("matcha","Matcha","light","minimal", 105, "light", 0.44, 0.05),
 ("seaglass","Sea Glass","dark","lean2", 175, "dark", 0.50, 0.03),
 ("lagoon","Lagoon","dark","pill", 190, "dark", 0.58, 0.03),
 ("tide","Tide","dark","lean2", 205, "dark", 0.52, 0.04),
 ("abyss","Abyss","dark","minimal", 220, "dark", 0.55, 0.06),
 ("cobalt","Cobalt","dark","powerline", 215, "dark", 0.70, 0.05),
 ("sapphire","Sapphire","dark","pill", 230, "dark", 0.64, 0.04),
 ("indigo-wash","Indigo Wash","dark","lean2", 245, "dark", 0.46, 0.05),
 ("iris","Iris","dark","pill", 265, "dark", 0.55, 0.04),
 ("plum","Plum","dark","lean2", 290, "dark", 0.50, 0.05),
 ("orchid","Orchid","dark","rainbow", 310, "dark", 0.58, 0.03),
 ("mulberry","Mulberry","dark","powerline", 330, "dark", 0.54, 0.05),
 ("crimson","Crimson","dark","rainbow", 350, "dark", 0.62, 0.05),
 ("rosewater","Rosewater","light","minimal", 345, "light", 0.40, 0.05),
 ("slate","Slate","dark","minimal", 210, "dark", 0.10, 0.02),
 ("graphite","Graphite","dark","lean2", 220, "dark", 0.06, 0.01),
 ("gunmetal","Gunmetal","dark","powerline", 200, "dark", 0.12, 0.02),
 ("ivory","Ivory","light","lean2", 45, "light", 0.10, 0.03),
 ("porcelain","Porcelain","light","minimal", 210, "light", 0.06, 0.01),
 ("linen","Linen","light","lean2", 35, "light", 0.14, 0.04),
 ("blueprint","Blueprint","dark","minimal", 212, "dark", 0.55, 0.10),
 ("nebula","Nebula","neon","rainbow", 275, "dark", 0.85, 0.06),
 ("aurora","Aurora","neon","rainbow", 160, "dark", 0.80, 0.05),
 ("vaporwave","Vaporwave","neon","rainbow", 300, "dark", 0.85, 0.06),
 ("miami","Miami","neon","pill", 190, "dark", 0.85, 0.05),
 ("laser","Laser","neon","rainbow", 330, "dark", 0.90, 0.05),
 ("toxic","Toxic","neon","minimal", 95, "dark", 0.90, 0.04),
 ("ultraviolet","Ultraviolet","neon","rainbow", 258, "dark", 0.88, 0.06),
 ("sunset","Sunset","warm","pill", 15, "dark", 0.72, 0.06),
 ("dune","Dune","warm","lean2", 40, "dark", 0.44, 0.08),
 ("volcano","Volcano","warm","rainbow", 8, "dark", 0.72, 0.06),
 ("mono-amber","Mono Amber","mono","minimal", 40, "dark", 0.85, 0.10),
 ("mono-green","Mono Green","mono","minimal", 130, "dark", 0.80, 0.08),
 ("mono-cyan","Mono Cyan","mono","minimal", 190, "dark", 0.70, 0.08),
 ("mono-magenta","Mono Magenta","mono","minimal", 320, "dark", 0.72, 0.08),
 ("mono-paper","Mono Paper","mono","minimal", 40, "light", 0.10, 0.05),
 ("frost","Frost","light","minimal", 205, "light", 0.30, 0.04),
 ("glacier","Glacier","dark","lean2", 195, "dark", 0.34, 0.05),
 ("obsidian","Obsidian","dark","powerline", 225, "dark", 0.20, 0.03),
 ("midnight","Midnight","dark","lean2", 235, "dark", 0.40, 0.07),
 ("cacao","Cacao","warm","minimal", 24, "dark", 0.36, 0.12),
 ("honey","Honey","warm","pill", 44, "dark", 0.64, 0.07),
 ("sakura","Sakura","light","pill", 340, "light", 0.42, 0.05),
 ("jade","Jade","dark","pill", 150, "dark", 0.55, 0.04),
 ("teal-noir","Teal Noir","dark","minimal", 180, "dark", 0.30, 0.05),
 ("wine","Wine","dark","lean2", 345, "dark", 0.45, 0.08),
 ("marina","Marina","dark","powerline", 200, "dark", 0.50, 0.04),
]
for g in GEN:
    make(g[0], g[1], g[2], g[3], g[4], mode=g[5], accent_s=g[6], tint=g[7])

# --------------------------------------------------------------------------- #
for i, p in enumerate(_presets):
    if not p["flavor"]:
        p["flavor"] = FLAVOR_CYCLE[i % len(FLAVOR_CYCLE)]

(HERE / "presets.json").write_text(json.dumps({"version": 2, "presets": _presets}, indent=1))
(HERE / "presets.js").write_text("window.ITERM_STUDIO_PRESETS = " +
                                 json.dumps(_presets, separators=(",", ":")) + ";\n")
cats = {}
for p in _presets:
    cats[p["category"]] = cats.get(p["category"], 0) + 1
print(f"wrote {len(_presets)} presets  ·  {dict(sorted(cats.items()))}")
