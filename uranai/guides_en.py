# -*- coding: utf-8 -*-
"""英語版：占術解説記事のコンテンツデータ。

uranai/guides.py（日本語版）の内容を踏まえ、英語ネイティブの読者向けに
書き起こした記事データ。日本語版とは独立したコンテンツとして管理し、
日本語版のロジック・データには一切手を加えない。

slug は日本語版と共通のものを使う（URLの対応関係を保つため）。
module は uranai/i18n.py の MODULE_NAME_EN と表記を揃えている。
"""
from __future__ import annotations

GUIDES_EN = [
    # ------------------------------------------------------------ Four Pillars
    {
        "slug": "shichu-suimei",
        "module": "Four Pillars of Destiny (BaZi)",
        "title": "What Is BaZi (Four Pillars of Destiny)? Reading Your Chart from Birth Data",
        "description": "How the Year, Month, Day and Hour Pillars are built, what your Day Master and Five Element balance mean, and how this site calculates your daily reading.",
        "lead": (
            "Four Pillars of Destiny — BaZi in Chinese — converts your year, month, day "
            "and hour of birth into four sexagenary (stem-and-branch) pairs, then reads "
            "your fate from how those four pillars relate to one another. It was "
            "systematised in China's Song dynasty and reached Japan during the Edo "
            "period. Because it packs in more information than most other Eastern "
            "traditions, it is sometimes called \"the king of fortune-telling.\""
        ),
        "sections": [
            {
                "heading": "What the four pillars are",
                "paragraphs": [
                    "The \"four pillars\" are the Year, Month, Day and Hour Pillars. Each is "
                    "expressed as a pairing of one of the 10 Heavenly Stems (Jia, Yi, Bing, "
                    "Ding, Wu, Ji, Geng, Xin, Ren, Gui) with one of the 12 Earthly Branches "
                    "(Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, "
                    "Dog, Pig). There are 60 possible stem-branch combinations, known as the "
                    "sexagenary cycle.",
                    "Each pillar governs a different stretch of your life. The Year Pillar "
                    "reflects your ancestry, early childhood, and your standing in society. "
                    "The Month Pillar covers your parents, career, and your years from youth "
                    "into adulthood. The Day Pillar is your own essential nature, and also "
                    "shows your relationship with a partner. The Hour Pillar speaks to "
                    "children, subordinates, and your later years.",
                ],
            },
            {
                "heading": "The Day Master sits at the centre of the chart",
                "paragraphs": [
                    "The single most important element in BaZi is the stem of your Day "
                    "Pillar, called your Day Master. It stands in for you, and the entire "
                    "chart is read from the viewpoint of how every other stem and branch "
                    "relates back to it.",
                    "A Day Master of Jia, for instance, grows straight and tall like a great "
                    "tree — direct, unbending, and unwilling to abandon a path once chosen. "
                    "Yi, though also Wood, is more like a flowering plant: supple, and "
                    "skilled at adapting its shape to whatever environment it finds itself "
                    "in. Each of the ten stems carries its own distinct nature, and that "
                    "nature is the foundation of your personality reading.",
                ],
            },
            {
                "heading": "Reading the Five Element balance",
                "paragraphs": [
                    "Every stem and branch belongs to one of the Five Elements: Wood, Fire, "
                    "Earth, Metal or Water. With four stems and four branches, a full chart "
                    "has eight elements in total — known as the \"Eight Characters.\" "
                    "Counting how many of each element appear reveals where your "
                    "temperament runs strong or thin.",
                    "The Five Elements interact through two cycles: generation (Wood feeds "
                    "Fire, Fire feeds Earth, Earth feeds Metal, Metal feeds Water, Water "
                    "feeds Wood) and control (Wood parts Earth, Earth dams Water, Water "
                    "douses Fire, Fire melts Metal, Metal cuts Wood). The idea that you can "
                    "compensate for an element you're short on through colour, objects, or "
                    "direction is exactly what underlies this tradition's lucky colours and "
                    "lucky directions.",
                ],
            },
            {
                "heading": "The Ten Gods reveal today's fortune",
                "paragraphs": [
                    "The name given to the relationship between your Day Master and any "
                    "other stem is one of the Ten Gods: Companion, Rob Wealth, Eating God, "
                    "Hurting Officer, Indirect Wealth, Direct Wealth, Seven Killings, Direct "
                    "Officer, Indirect Resource, and Direct Resource.",
                    "On a day when today's stem forms an Eating God relationship with your "
                    "Day Master, for example, eating, talking and enjoying yourself are all "
                    "favoured, and generosity toward others tends to be repaid twofold. A "
                    "Seven Killings day, by contrast, tends to bring pressure — it favours "
                    "letting time work in your favour rather than forcing a confrontation. "
                    "This site combines that day's Ten God relationship with branch "
                    "compatibility to calculate your score for the day.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "The Year Pillar is calculated on a 60-year cycle from 1924 as its Jiazi "
                    "base year, with the boundary between years set at the Start of Spring "
                    "(around February 4th) rather than January 1st — so anyone born before "
                    "roughly that date is calculated under the previous year's pillar. The "
                    "Month Pillar uses the \"Five Tigers\" method to derive the month stem "
                    "from the year stem; because the exact solar-term boundary is "
                    "approximated by a representative day for each month, results for "
                    "birthdays within a day or so of a solar term may drift slightly from a "
                    "strict astronomical calendar.",
                    "The Day Pillar is found by counting elapsed days from January 1st, "
                    "1924 (set as a Jiazi day). The Hour Pillar assigns your birth time to "
                    "one of the twelve two-hour branches and derives the hour stem from the "
                    "day stem. When birth time is unknown, the Day Pillar's own branch is "
                    "used as a stand-in for the Hour Pillar's branch.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Western Astrology
    {
        "slug": "seiyo-uranai",
        "module": "Western Astrology",
        "title": "Western Astrology 101: Sun Sign, Moon Sign and Ascendant",
        "description": "How the 12 zodiac signs came to be, the different roles played by your Sun sign, Moon sign and Ascendant, and how transits and aspects shape your day-to-day fortune.",
        "lead": (
            "Western astrology reads personality and fortune from the position of the "
            "planets at the moment you were born. It traces back to ancient Babylon and "
            "developed further through Greece and Rome into the system used across "
            "Europe today. The \"star sign horoscope\" you see in a magazine or on TV is "
            "only a small slice of this much larger tradition."
        ),
        "sections": [
            {
                "heading": "The 12 signs are 12 equal slices of the sky",
                "paragraphs": [
                    "In astrology, a \"sign\" isn't an actual constellation of stars — it's "
                    "one of twelve equal 30° divisions of the ecliptic, the Sun's apparent "
                    "path across the sky. Starting from the spring equinox point, the signs "
                    "run Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, "
                    "Sagittarius, Capricorn, Aquarius, and Pisces.",
                    "Each sign also belongs to one of four elements. Fire (Aries, Leo, "
                    "Sagittarius) governs passion and action; Earth (Taurus, Virgo, "
                    "Capricorn) governs the practical and the stable; Air (Gemini, Libra, "
                    "Aquarius) governs intellect and relationships; Water (Cancer, Scorpio, "
                    "Pisces) governs emotion and empathy. Signs of the same element sit 120° "
                    "apart — a relationship known as a favourable Trine.",
                ],
            },
            {
                "heading": "What the Sun, Moon and Ascendant each show",
                "paragraphs": [
                    "When someone says \"I'm a [sign],\" they almost always mean their Sun "
                    "sign. The Sun represents the direction you consciously aim for in "
                    "life — the self you deliberately choose to become.",
                    "Your Moon sign shows your raw, unguarded emotional nature and "
                    "unconscious reactions. It's the Moon's face, not the Sun's, that tends "
                    "to show when you're tired or with someone you fully trust. Because the "
                    "Moon moves through a full sign roughly every two and a half days, it "
                    "depends on your birth time as well as your birth date.",
                    "Your Ascendant (rising sign) is whichever sign was rising over the "
                    "eastern horizon at the exact moment you were born. It shapes the first "
                    "impression you make on others and your general physical presence. "
                    "Because it shifts to a new sign roughly every two hours, calculating it "
                    "accurately requires both your birth time and birthplace.",
                ],
            },
            {
                "heading": "Aspects drive your day-to-day fortune",
                "paragraphs": [
                    "The actual, real-time position of a planet right now is called a "
                    "transit. Your daily fortune is read from the angle — the aspect — that "
                    "today's transits form against the positions in your natal chart, the "
                    "map of the sky at the moment you were born.",
                    "A 0° Conjunction intensifies through overlap; a 60° Sextile brings a "
                    "light, easy opportunity; a 90° Square brings friction and a challenge "
                    "to work through; a 120° Trine is the smoothest, most fortunate angle of "
                    "all; and a 180° Opposition brings confrontation and insight. This site "
                    "determines your aspect from the angular distance between your natal Sun "
                    "and today's transiting Sun, then fine-tunes the score using your "
                    "relationship to today's Sun from your Moon sign as well.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your Sun sign is read directly from your birth-date range. Your Moon "
                    "sign is approximated with a simplified formula based on the Moon's "
                    "orbital period and your date of birth. Your Ascendant is estimated by "
                    "starting from your Sun sign and correcting for your birth time (one "
                    "sign roughly every two hours) and the longitude difference of your "
                    "birthplace; if your birth time is unknown, the Ascendant is treated as "
                    "identical to your Sun sign.",
                    "A fully rigorous calculation would require an ephemeris — precise "
                    "planetary tables. Because this site is built to run lightly on Render's "
                    "free tier, it instead uses approximations accurate enough to capture "
                    "meaningful day-to-day trends.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Name Analysis
    {
        "slug": "seimei",
        "module": "Name Analysis (Kumazaki Method)",
        "title": "The Five Grids of Japanese Name Analysis: Heaven, Personality, Earth, Outer and Total",
        "description": "How the five grids of the Kumazaki method of name analysis are calculated, what the 1–81 numerology table means, how stroke-counting conventions differ between schools, and how this site implements it.",
        "lead": (
            "Japanese name analysis (seimei handan) reads fortune from the stroke count "
            "of a person's kanji name. The school most widely used in Japan today is the "
            "\"Kumazaki method,\" systematised by Kumazaki Kenō in the early twentieth "
            "century, which splits the strokes of a surname and given name into five "
            "grids."
        ),
        "sections": [
            {
                "heading": "How the five grids are worked out",
                "paragraphs": [
                    "The Heaven Grid is the total stroke count of your surname. It "
                    "represents fortune inherited from your family line — something beyond "
                    "your own control — so it is not judged for luck on its own.",
                    "The Personality Grid adds the stroke count of the last character of "
                    "your surname to the first character of your given name. It is "
                    "considered the most important of the five grids, reflecting your core "
                    "personality and your fortune through the middle years of life.",
                    "The Earth Grid is the total stroke count of your given name, showing "
                    "your innate disposition and your fortune from childhood into young "
                    "adulthood. The Outer Grid is the Heaven Grid plus the Earth Grid, minus "
                    "the Personality Grid, and reflects the impression you make on others "
                    "and your relationships. The Total Grid is the sum of every stroke in "
                    "your full name, summing up your life as a whole.",
                ],
            },
            {
                "heading": "The 1–81 numerology table",
                "paragraphs": [
                    "The Kumazaki method maps each grid's number onto a table running from "
                    "1 to 81 to judge its fortune. The numbers 1, 3, 5, 15, 21, 23, 24, 31, "
                    "32, 33, 41, 45, 47, 48, 52, 57, 58, 61, 63, 65, 67, 68 and 81 are "
                    "considered Great Fortune, while 6, 7, 8, 11, 13, 16, 17, 18, 25, 29, "
                    "35, 37, 38 and 39 are considered Fortune.",
                    "That said, a single number's fortune doesn't determine your whole "
                    "life. A grid landing on a number considered unlucky simply suggests "
                    "that area may need a little more conscious attention — and is generally "
                    "seen as something you can compensate for once you're aware of it. Name "
                    "analysis is best treated as a tool for self-understanding, not a "
                    "verdict.",
                ],
            },
            {
                "heading": "Stroke-counting conventions differ between schools",
                "paragraphs": [
                    "One point of frequent disagreement in name analysis is how strokes "
                    "should be counted. The original Kumazaki method uses the older, "
                    "traditional (Kangxi Dictionary) forms of characters, and counts "
                    "simplified radicals by the stroke count of the character they stand "
                    "in for — for example the three-dot water radical (氵) is counted as 4 "
                    "strokes (as 水), the grass radical (艹) as 6 strokes (as 艸), and the "
                    "movement radical (辶) as 7 strokes (as 辵).",
                    "Other schools simply use the modern, standard stroke count instead, so "
                    "the same name can produce a different result depending on which school "
                    "calculated it. Since there's no settled consensus on which approach is "
                    "\"correct,\" it's entirely normal to see different results across "
                    "different sites.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "This site holds an internal dictionary of roughly 1,500 kanji, hiragana "
                    "and katakana characters commonly used in names, and counts strokes "
                    "using the modern, standard forms. Following Kumazaki convention, "
                    "however, the kanji numerals one through ten are counted by the stroke "
                    "count of their numeric meaning (一 = 1 stroke, 十 = 10 strokes) rather "
                    "than their literal shape.",
                    "For rare characters not in the dictionary, a deterministic fallback "
                    "estimates a stroke count from the character's Unicode code point. This "
                    "estimate is only approximate, so treat any result built on it as a "
                    "rough reference rather than an exact figure.",
                    "The lucky colour is drawn from the element associated with the Total "
                    "Grid's number, the lucky item from the Personality Grid's number, and "
                    "the lucky direction from the Outer Grid's number.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Nine Star Ki
    {
        "slug": "kyusei-kigaku",
        "module": "Nine Star Ki",
        "title": "Nine Star Ki: Finding Your Birth Star, from One White Water to Nine Purple Fire",
        "description": "How to work out your Birth Star and Month Star in Nine Star Ki, what each of the nine stars means, how the yearly, monthly and daily charts work, and how lucky and unlucky directions are judged.",
        "lead": (
            "Nine Star Ki reads the fortune of directions from a \"Birth Star\" derived "
            "from your year of birth. It draws on nine stars rooted in the Chinese Luo "
            "Shu diagram, and was systematised in Japan as kigaku by Sonoda Shinjirō in "
            "the Taishō era. It's especially well known for guiding decisions about which "
            "direction to move house or travel in."
        ),
        "sections": [
            {
                "heading": "The nine stars and their natures",
                "paragraphs": [
                    "The nine stars are One White Water, Two Black Earth, Three Jade Wood, "
                    "Four Green Wood, Five Yellow Earth, Six White Metal, Seven Red Metal, "
                    "Eight White Earth, and Nine Purple Fire. Each is assigned an element "
                    "and a colour.",
                    "One White Water flows like water, adapting to any container with "
                    "flexibility and patience. Two Black Earth receives like the earth "
                    "itself, a steady, practical star that nurtures things slowly. Three "
                    "Jade Wood shoots up like a young tree — quick, energetic, expressive. "
                    "Four Green Wood spreads like the wind, connecting people together with "
                    "quiet, mediating influence. Five Yellow Earth sits at the very centre "
                    "of the chart, an imperial star whose influence — for better or worse — "
                    "is unusually large.",
                    "Six White Metal is a heavenly star of responsibility and leadership; "
                    "Seven Red Metal brings sociability, joy and abundance; Eight White "
                    "Earth is a mountain star turning change into a firm foundation; and "
                    "Nine Purple Fire, the star of the Sun and flame, symbolises brilliance, "
                    "intellect and being noticed.",
                ],
            },
            {
                "heading": "Working out your Birth Star and Month Star",
                "paragraphs": [
                    "Your Birth Star is derived from your year of birth using the formula "
                    "(11 − ((year − 1) mod 9)) mod 9, with a result of 0 read as 9. The key "
                    "thing to remember is that the Nine Star Ki year begins at the Start of "
                    "Spring (around February 4th), not January 1st — so anyone born on or "
                    "before roughly February 3rd is calculated as though born in the "
                    "previous year.",
                    "Your Month Star is derived from the combination of your Birth Star's "
                    "group and your month of birth. Where the Birth Star reflects your "
                    "basic, lifelong nature, the Month Star is said to reflect tendencies "
                    "shaped in early childhood. It is likewise calculated as the previous "
                    "month if you were born before that month's solar-term boundary.",
                ],
            },
            {
                "heading": "Yearly, monthly and daily charts, and lucky directions",
                "paragraphs": [
                    "Nine Star Ki works with \"charts\" — grids showing how the nine stars "
                    "are arranged across the eight directions plus the centre. The baseline "
                    "arrangement places One White in the North, Two Black in the Southwest, "
                    "Three Jade in the East, Four Green in the Southeast, Five Yellow in the "
                    "centre, Six White in the Northwest, Seven Red in the West, Eight White "
                    "in the Northeast, and Nine Purple in the South.",
                    "For an actual reading, the star sitting at the centre changes by year, "
                    "by month, and by day, and every other star shifts direction along with "
                    "it — producing the yearly, monthly and daily charts. Whichever "
                    "direction holds a star compatible with your own Birth Star becomes a "
                    "lucky direction for that period.",
                    "However, wherever Five Yellow Earth currently sits is called the "
                    "Gōō-satsu direction, and its opposite the Anken-satsu direction — both "
                    "are treated as unlucky no matter how compatible the star would "
                    "otherwise be. The direction occupied by your own Birth Star (Honmei-"
                    "satsu) and its opposite (Honmei-teki-satsu) are avoided on the same "
                    "principle.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your Birth Star is found with the formula above plus the Start-of-"
                    "Spring correction, and your Month Star is read from the Nine Star Ki "
                    "month-star table. The daily chart's central star cycles deterministically "
                    "based on the remainder of elapsed days from a fixed base date, divided "
                    "by nine.",
                    "Lucky directions are calculated by building the day's monthly chart, "
                    "excluding the Gōō-satsu, Anken-satsu, Honmei-satsu and Honmei-teki-"
                    "satsu directions, then ranking the remaining directions by how well "
                    "their star aligns with your Birth Star (through generation or a shared "
                    "element) — the top three are returned, and the highest-ranked one is "
                    "shown as your lucky direction.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Zi Wei Dou Shu
    {
        "slug": "shibi-tosuu",
        "module": "Zi Wei Dou Shu",
        "title": "What Is Zi Wei Dou Shu? Reading Your Chart Through the Life Palace and 14 Main Stars",
        "description": "How the Zi Wei Dou Shu natal chart is structured, what the 12 palaces and 14 main stars mean, how the Life Palace is found, why the lunar calendar is used, and how this site calculates it.",
        "lead": (
            "Zi Wei Dou Shu is an astrological system that originated in China, said to "
            "have been founded by the Song-dynasty Taoist Chen Xiyi. It remains, alongside "
            "BaZi, one of the two major traditions still widely practised in Taiwan and "
            "Hong Kong. It builds a chart from your birth date and time, then reads your "
            "life from the stars placed within it."
        ),
        "sections": [
            {
                "heading": "The 12 palaces: twelve areas of life",
                "paragraphs": [
                    "A Zi Wei Dou Shu chart is divided into twelve palaces: the Life "
                    "Palace, Siblings Palace, Spouse Palace, Children Palace, Wealth "
                    "Palace, Health Palace, Travel Palace, Friends Palace, Career Palace, "
                    "Property Palace, Fortune Palace, and Parents Palace.",
                    "The Life Palace reflects your own essential nature; the Spouse Palace, "
                    "your relationship with a partner; the Wealth Palace, income and "
                    "spending; the Career Palace, your work and how it's recognised; the "
                    "Health Palace, your physical condition; and the Fortune Palace, your "
                    "peace of mind and enjoyment. Dividing life into twelve distinct areas "
                    "that can each be read on its own is what sets Zi Wei Dou Shu apart.",
                ],
            },
            {
                "heading": "The 14 main stars shape your personality",
                "paragraphs": [
                    "Many stars are placed across a chart, but fourteen of them — the main "
                    "stars — form its core: Zi Wei, Tian Ji, Tai Yang, Wu Qu, Tian Tong, "
                    "Lian Zhen, Tian Fu, Tai Yin, Tan Lang, Ju Men, Tian Xiang, Tian Liang, "
                    "Qi Sha, and Po Jun.",
                    "Zi Wei is an emperor star that performs best the more it's relied "
                    "upon. Tian Ji is a star of wisdom, strong in planning and analysis; Tai "
                    "Yang is a star whose fortune improves the more it gives to others. Wu "
                    "Qu governs wealth and practical matters, Tian Tong brings a "
                    "non-confrontational warmth, and Lian Zhen represents a passion that "
                    "commits fully to its own convictions. Whichever main star occupies "
                    "your Life Palace is thought to shape your basic approach to life.",
                ],
            },
            {
                "heading": "Why the lunar calendar is used",
                "paragraphs": [
                    "Finding your Life Palace requires your lunar-calendar month and the "
                    "two-hour \"branch hour\" corresponding to your time of birth. The Life "
                    "Palace is calculated as (14 − lunar month − branch-hour index) mod 12.",
                    "The lunar calendar is used because Zi Wei Dou Shu is a system built "
                    "around the phases of the Moon. Using a solar-calendar date directly "
                    "would throw the whole chart off, so conversion to the lunar calendar "
                    "is essential. This site performs that conversion accurately using the "
                    "lunardate library.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your date of birth is converted to the lunar calendar to obtain the "
                    "lunar month, your birth time is converted to its branch-hour index, "
                    "and the Life Palace is fixed from these two values. If your birth time "
                    "is unknown, the branch-hour index is treated as 0. The 14 main stars "
                    "are then placed across the twelve palaces relative to that Life "
                    "Palace.",
                    "The combination of the yin-yang polarity of your birth year and your "
                    "gender also determines which direction your fortune \"flows.\" A man "
                    "born in a yang year, or a woman born in a yin year, is read as moving "
                    "forward; a man born in a yin year, or a woman born in a yang year, is "
                    "read as moving in reverse. If \"prefer not to say\" is chosen for "
                    "gender, the calculation defaults to a neutral, forward-moving "
                    "interpretation.",
                    "Your fortune for a given day is judged by how many palaces separate "
                    "your Life Palace from the day's transiting palace, which is derived "
                    "from today's lunar month and day.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Sanmei-gaku
    {
        "slug": "sanmei",
        "module": "Sanmei-gaku",
        "title": "Tenchusatsu in Sanmei-gaku: Reading the Body Star Chart and the Void Periods",
        "description": "The origins of Sanmei-gaku, what the Ten Main Stars and Body Star Chart represent, the six kinds of Tenchusatsu (Void) periods and how to navigate them, and how this site calculates it all.",
        "lead": (
            "Sanmei-gaku is a fortune-telling system built on the Chinese philosophy of "
            "yin-yang and the Five Elements, systematised in Japan by Takao Yoshimasa. "
            "Like BaZi, it works from the sexagenary stems and branches, but its "
            "distinguishing feature is the \"Body Star Chart\" — a unique diagram that "
            "maps stars onto the human body to build a picture of the person. Many people "
            "will recognise the term \"Tenchusatsu\" even without knowing this tradition "
            "by name."
        ),
        "sections": [
            {
                "heading": "What the Body Star Chart is",
                "paragraphs": [
                    "Sanmei-gaku builds a chart centred on the stem of your Day Pillar "
                    "(your Day Master), placing a star at each of five positions: centre, "
                    "north, south, east and west. This is the Body Star Chart.",
                    "The centre (chest) position holds your Main Star and represents your "
                    "core personality. The north (head) position reflects your relationship "
                    "with elders and society; the south (abdomen), your relationship with "
                    "children and subordinates; and east (right hand) and west (left hand), "
                    "your relationships with your partner and with colleagues or business "
                    "counterparts respectively. Mapping a person's character onto parts of "
                    "the body is a distinctly Sanmei-gaku way of thinking.",
                ],
            },
            {
                "heading": "The meaning of the Ten Main Stars",
                "paragraphs": [
                    "Ten possible stars can occupy a position on the Body Star Chart: the "
                    "Star of Independence, Star of Cooperation, Star of Ease, Star of "
                    "Sensitivity, Star of Service, Star of Accumulation, Star of Speed, Star "
                    "of Honour, Star of Exploration, and Star of Scholarship.",
                    "The Star of Independence brings a stubborn self-reliance; the Star of "
                    "Cooperation, a talent for drawing people together in harmony. The Star "
                    "of Ease expresses itself naturally, achieving results while enjoying "
                    "the process; the Star of Sensitivity is a delicate creativity honed in "
                    "solitude. The Star of Service gains wealth by giving to others; the "
                    "Star of Accumulation excels at steadily saving and protecting what it "
                    "has. The Star of Speed thinks while moving; the Star of Honour builds "
                    "trust through pride and a sense of duty; the Star of Exploration grows "
                    "by venturing into the unknown; and the Star of Scholarship organises "
                    "knowledge and is suited to teaching it to others.",
                ],
            },
            {
                "heading": "Understanding Tenchusatsu (the Void)",
                "paragraphs": [
                    "Tenchusatsu refers to the branches that are inevitably \"left over\" "
                    "when pairing the 10 stems with the 12 branches. Because there are 10 "
                    "stems and 12 branches, grouping them ten at a time always leaves two "
                    "branches unpaired — and the period governed by those leftover branches "
                    "is your Void.",
                    "There are six kinds of Tenchusatsu — Rat-Ox, Tiger-Rabbit, Dragon-"
                    "Snake, Horse-Goat, Monkey-Rooster, and Dog-Pig — and each tests a "
                    "different theme. Dog-Pig Void concerns spirituality and learning; "
                    "Monkey-Rooster Void, friendships; Horse-Goat Void, relationships with "
                    "elders and parents; Dragon-Snake Void, your own sense of self; Tiger-"
                    "Rabbit Void, home and household; and Rat-Ox Void, ancestry and roots.",
                    "A Void period is best understood not as \"bad luck\" but as \"a time "
                    "when your foundations haven't settled yet.\" The conventional advice is "
                    "to avoid decisions with long-term consequences — new contracts, moving "
                    "house — and instead spend the time tidying up what you already have.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your Day Pillar's stem-branch pair is found the same way as in BaZi, "
                    "and your Tenchusatsu is judged from which group of ten that pillar's "
                    "index number falls into — for example, anyone whose Day Pillar falls "
                    "in the Jiazi group (index 0–9) carries the Dog-Pig Void.",
                    "The five stars of the Body Star Chart are placed from the "
                    "relationships between your Day Master and the stems of your Year, "
                    "Month and Hour Pillars (and stems derived from their branches); which "
                    "side is read as east and which as west is swapped depending on "
                    "gender.",
                    "Your daily score reflects whether today's branch falls within your own "
                    "Void branches — a Void day is scored down, and this is stated plainly "
                    "in the full reading. Your lucky direction is the opposite of your "
                    "Void's associated direction.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Numerology
    {
        "slug": "suuhi",
        "module": "Numerology",
        "title": "The Life Path Number in Numerology: How It's Calculated, and What 11, 22 and 33 Mean",
        "description": "The origins of numerology, how the Life Path and Destiny Numbers are calculated, how Master Numbers are handled, and how the Personal Day Number reads your day-to-day fortune.",
        "lead": (
            "Numerology converts a birth date or name into numbers, then reads "
            "personality and fortune from the meaning attached to each. It's often traced "
            "back to the ancient Greek mathematician Pythagoras, and remains, alongside "
            "astrology, one of the most popular systems in the Western world."
        ),
        "sections": [
            {
                "heading": "How the Life Path Number is calculated",
                "paragraphs": [
                    "The core figure in numerology is the Life Path Number, found by "
                    "adding together every digit of your birth date until a single digit "
                    "remains. For someone born on May 15th, 1990, for example: 1+9+9+0 = "
                    "19, then 1+9 = 10, then 1+0 = 1 for the year; the month is 5; the day "
                    "1+5 = 6; adding these together, 1+5+6 = 12, then 1+2 = 3 — a Life Path "
                    "of 3.",
                    "The Life Path Number is said to represent the road you walk through "
                    "life — something like an inborn mission. In broad strokes: 1 is the "
                    "Pioneer, 2 the Mediator, 3 the Performer, 4 the Builder, 5 the "
                    "Adventurer, 6 the Nurturer, 7 the Seeker, 8 the Achiever, and 9 the "
                    "Humanitarian.",
                ],
            },
            {
                "heading": "The Master Numbers: 11, 22 and 33",
                "paragraphs": [
                    "If 11, 22 or 33 appear at any point while reducing a number, "
                    "convention holds that they are kept as they are rather than reduced "
                    "any further. These are the Master Numbers.",
                    "11 is the Intuitive Messenger, guiding others with a finely tuned "
                    "sensitivity. 22 is the Master Builder, with a rare ability to turn "
                    "grand visions into reality. 33 is the embodiment of selfless love, "
                    "carrying a role centred on healing others. Master Numbers are said to "
                    "carry unusual power, but also to be difficult to work with, often "
                    "taking longer than other numbers to come fully into their own.",
                ],
            },
            {
                "heading": "The Destiny Number and converting a name",
                "paragraphs": [
                    "The Destiny Number is found by converting the letters of your name to "
                    "numbers (A=1, B=2, ... Z=26) and reducing the total. It's said to show "
                    "how your innate talents are best put to use in society.",
                    "For a Japanese name, the first step is converting it to Roman letters. "
                    "Because this site doesn't ask users to type in a romanised version of "
                    "their own name, it holds an internal \"kanji-to-kana\" table and a "
                    "\"kana-to-Hepburn-romaji\" table, and generates the romanisation "
                    "automatically from the kanji name entered.",
                    "Because a Japanese name's reading isn't always uniquely determined — "
                    "the character 和, for instance, might be read \"kazu,\" \"wa,\" or "
                    "\"nagomi\" depending on the person — any kanji not in the dictionary is "
                    "assigned a kana reading deterministically from its Unicode code point. "
                    "This is an inherent limitation of the method, so treat any result built "
                    "on it as a reference value rather than a precise figure.",
                ],
            },
            {
                "heading": "The Personal Day Number reads today specifically",
                "paragraphs": [
                    "Your day-to-day fortune is read through the Personal Day Number, "
                    "found by adding today's month and day to your Life Path Number and "
                    "reducing the result.",
                    "A 1 day has value simply in starting something; a 2 day rewards "
                    "listening to others; a 3 day carries luck through self-expression and "
                    "play; a 4 day turns unglamorous, careful work into later results. A 5 "
                    "day is worth getting outside for; a 6 day fulfils you through caring "
                    "for someone else; a 7 day calls for solitary time; an 8 day rewards "
                    "facing numbers and negotiation; and a 9 day makes room for what's next "
                    "by finishing things and letting go.",
                    "This site uses the Personal Day Number directly as the \"today's lucky "
                    "number\" in the combined verdict.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Sukuyo Astrology
    {
        "slug": "shukuyo",
        "module": "Sukuyo Astrology",
        "title": "The 27 Lunar Mansions of Sukuyo Astrology: Your Birth Mansion and Its Relationships",
        "description": "The origins of the Sukuyokyo text, how the 27 lunar mansions are determined, what the ten relationships — Destiny, Prosperity, Affinity, Friendship, Collapse, Success, Danger, Peace, Karma and Gestation — mean, and how daily fortune is judged.",
        "lead": (
            "Sukuyo astrology traces a path from Indian astronomy, through Buddhism and "
            "China, into Japan. Its source text, the Sukuyokyo, is said to have been "
            "brought back from Tang-dynasty China by the monk Kukai, and it was widely "
            "used among Heian-era court nobility. It reads fortune through 27 lunar "
            "mansions based on the Moon's movement through the sky."
        ),
        "sections": [
            {
                "heading": "What the 27 mansions are",
                "paragraphs": [
                    "Because the Moon takes roughly 27.3 days to orbit the Earth, Sukuyo "
                    "astrology divides the celestial sphere into 27 \"mansions\": the "
                    "Pleiades, Net, Turtle Beak, Three Stars, Well, Ghost, Willow, Star, "
                    "Extended Net, Wings, Chariot, Horn, Neck, Root, Room, Heart, Tail, "
                    "Winnowing Basket, Dipper, Girl, Emptiness, Rooftop, Encampment, Wall, "
                    "Legs, Bond, and Stomach Mansions.",
                    "Whichever mansion the Moon occupied on the day you were born is your "
                    "\"birth mansion,\" reflecting your basic temperament. The Ghost "
                    "Mansion, for example, is considered the very best of the 27 — carrying "
                    "high virtue and a protected fortune. The Pleiades Mansion brings an "
                    "almost fastidious sense of justice, while the Heart Mansion brings "
                    "passion and quick decisiveness.",
                ],
            },
            {
                "heading": "The relationship between your mansion and today's decides your fortune",
                "paragraphs": [
                    "What makes Sukuyo astrology distinctive is that a day's fortune is "
                    "decided purely by the distance between your birth mansion and today's "
                    "mansion — meaning the same calendar day can be lucky for one person and "
                    "unlucky for another.",
                    "A distance of zero — the day your own birth mansion comes back around "
                    "— is called Destiny, a day to face yourself and find your answer by "
                    "returning to first principles. From there, nine relationships repeat in "
                    "cycle: Prosperity, Affinity, Friendship, Collapse, Success, Danger, "
                    "Peace, Karma, and Gestation.",
                    "Prosperity is your most fortunate day, when recognition, income and "
                    "results tend to gather. Affinity deepens relationships and brings "
                    "support; Friendship rewards working with others. Collapse, by "
                    "contrast, is a day to avoid new commitments or big purchases, and "
                    "Danger calls for care with travel, wording, and your health.",
                ],
            },
            {
                "heading": "Using it to size up how much to take on each day",
                "paragraphs": [
                    "The practical use of Sukuyo astrology is deciding how much weight to "
                    "put on a given day. Important negotiations or a confession of feelings "
                    "are best scheduled on a Prosperity, Affinity, Friendship, Success, or "
                    "Peace day, while plans should be shifted off a Collapse, Danger, or "
                    "Karma day wherever possible.",
                    "It's thought that Heian-era nobles kept track of their mansion in "
                    "their diaries for exactly this kind of scheduling. Even today, it "
                    "pairs well with a calendar app for genuinely practical use.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your date of birth is converted to the lunar calendar, and your birth "
                    "mansion is found from the remainder of (lunar month × 30 + lunar day) "
                    "divided by 27, with the first day of the first lunar month set as the "
                    "baseline for the Pleiades Mansion.",
                    "Today's mansion is found the same way, and the relationship name is "
                    "judged from its distance from your birth mansion — a distance of 0 is "
                    "Destiny, with the remaining nine relationships cycling from there. Your "
                    "lucky colour, item and direction are all drawn from the table "
                    "associated with your birth mansion.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Mayan Calendar
    {
        "slug": "maya",
        "module": "Mayan Calendar (Tzolk'in)",
        "title": "What Is Your KIN Number? The 20 Glyphs and 13 Galactic Tones of the Mayan Calendar",
        "description": "How the Mayan sacred calendar Tzolk'in works, how your KIN number is calculated, what the 20 glyphs and 13 tones mean, and how this site calculates your daily reading.",
        "lead": (
            "The Mayan calendar reading used here is based on the Tzolk'in, the sacred "
            "260-day calendar of the ancient Maya. It reads a person's essential nature "
            "and role in life from exactly where in that 260-day cycle they were born. "
            "The version most widely known today comes filtered through José Argüelles's "
            "modern interpretation, the Dreamspell."
        ),
        "sections": [
            {
                "heading": "The Tzolk'in: a 260-day calendar",
                "paragraphs": [
                    "The Tzolk'in pairs 20 glyphs with 13 tones to form a 260-day cycle "
                    "(20 × 13 = 260); once every combination has appeared, the cycle "
                    "returns to its start. This 260-day cycle was, for the Maya, a "
                    "fundamental unit of time.",
                    "There are several theories about why 260 was chosen — that it's close "
                    "to the length of human pregnancy, and that it matched agricultural "
                    "cycles in the Mayan region, among others. It was used as a separate "
                    "calendar from the solar year, dedicated to ritual and divination.",
                ],
            },
            {
                "heading": "The 20 glyphs point to the direction of your gifts",
                "paragraphs": [
                    "The 20 glyphs are Red Dragon, White Wind, Blue Night, Yellow Seed, "
                    "Red Serpent, White Worldbridger, Blue Hand, Yellow Star, Red Moon, "
                    "White Dog, Blue Monkey, Yellow Human, Red Skywalker, White Wizard, "
                    "Blue Eagle, Yellow Warrior, Red Earth, White Mirror, Blue Storm, and "
                    "Yellow Sun.",
                    "Red Dragon represents birth and nurturing; White Wind, communication "
                    "through words; Blue Night, abundance and intuition; Yellow Seed, the "
                    "power to plant possibility. Each glyph's name cycles through one of "
                    "four colours — red, white, blue and yellow — which in turn correspond "
                    "to the four cardinal directions of east, north, west and south.",
                ],
            },
            {
                "heading": "The 13 galactic tones show how you approach things",
                "paragraphs": [
                    "The 13 tones are named Magnetic, Lunar, Electric, Self-Existing, "
                    "Overtone, Rhythmic, Resonant, Galactic, Solar, Planetary, Spectral, "
                    "Crystal, and Cosmic.",
                    "Tone 1, Magnetic, begins with deciding what you want; Tone 2, Lunar, "
                    "finds its direction by first identifying the obstacle; Tone 3, "
                    "Electric, generates energy the moment you start moving. As the tones "
                    "progress they define form, radiate power, organise, integrate, "
                    "declare intent, manifest results, release, cooperate, and finally, at "
                    "Tone 13, Cosmic, transcend everything to simply be.",
                    "It helps to think of the glyph as showing \"what kind of person you "
                    "are\" and the tone as showing \"how you go about it.\"",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "January 1st, 1900 is set as KIN 1, and your KIN number is found from "
                    "the number of days elapsed since then, taken modulo 260, plus one. "
                    "Your glyph is the remainder of your KIN number divided by 20; your "
                    "tone is the remainder of (KIN − 1) divided by 13, plus one.",
                    "Your fortune for a given day is judged from the remainder, modulo 13, "
                    "of the difference between your KIN and today's KIN, with a bonus "
                    "applied when your glyph's colour family (red, white, blue or yellow) "
                    "matches today's. Your lucky colour comes from your glyph's colour "
                    "family, your lucky item from your tone, and your lucky direction from "
                    "your glyph's associated cardinal point.",
                    "Note that there is more than one convention for the Tzolk'in's start "
                    "date, so KIN numbers can differ from site to site. This site prioritises "
                    "internal consistency and uses the base date above throughout.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Vedic Astrology
    {
        "slug": "india-uranai",
        "module": "Vedic Astrology",
        "title": "What Is Vedic Astrology (Jyotish)? The Ayanamsa and the 27 Nakshatras",
        "description": "The key difference between Vedic and Western astrology, what the ayanamsa (precession correction) means, the 12 Rashis and 27 Nakshatras, and how daily fortune is judged through Tarabala.",
        "lead": (
            "Vedic astrology, known as Jyotish (\"the science of light\"), is a "
            "tradition said to be more than 3,000 years old. Like Western astrology, it "
            "reads the positions of the planets — but because it anchors the zodiac "
            "differently, the same person's sign can come out one sign earlier than in "
            "the Western system."
        ),
        "sections": [
            {
                "heading": "Sidereal versus tropical",
                "paragraphs": [
                    "Western astrology uses the \"tropical\" system, which fixes the spring "
                    "equinox point as 0° Aries. Vedic astrology instead uses the "
                    "\"sidereal\" system, anchored to the actual position of the fixed "
                    "stars.",
                    "The Earth's axis slowly wobbles over a roughly 26,000-year cycle "
                    "(precession), so the equinox point gradually drifts against the "
                    "background stars. Today, that drift between the equinox point and the "
                    "actual stellar positions has reached roughly 24°. The correction "
                    "figure used to account for this gap is called the ayanamsa.",
                    "Because the ayanamsa is roughly 24° — almost exactly one sign's width "
                    "— someone who is a Western Aries will typically come out as Pisces in "
                    "Vedic astrology: one sign earlier, as a rule of thumb.",
                ],
            },
            {
                "heading": "The 12 Rashis and their ruling planets",
                "paragraphs": [
                    "The 12 signs of Vedic astrology are called Rashis: Mesha (Aries), "
                    "Vrishabha (Taurus), Mithuna (Gemini), Karka (Cancer), Simha (Leo), "
                    "Kanya (Virgo), Tula (Libra), Vrishchika (Scorpio), Dhanu "
                    "(Sagittarius), Makara (Capricorn), Kumbha (Aquarius), and Meena "
                    "(Pisces).",
                    "Each Rashi has a ruling planet. Mesha and Vrishchika are ruled by "
                    "Mars; Vrishabha and Tula by Venus; Mithuna and Kanya by Mercury; Karka "
                    "by the Moon; Simha by the Sun; Dhanu and Meena by Jupiter; and Makara "
                    "and Kumbha by Saturn. Vedic astrology doesn't use Uranus, Neptune or "
                    "Pluto, working instead with the naked-eye planets plus two calculated "
                    "points, Rahu and Ketu.",
                ],
            },
            {
                "heading": "The 27 Nakshatras and Tarabala",
                "paragraphs": [
                    "A particularly important concept in Vedic astrology is the Nakshatra "
                    "(lunar mansion) — 27 divisions of the celestial sphere running from "
                    "Ashwini through to Revati. Whichever Nakshatra the Moon occupied at "
                    "your birth becomes your birth Nakshatra.",
                    "Day-to-day fortune is judged through Tarabala. Taking the distance "
                    "from your birth Nakshatra to today's Nakshatra, modulo 9, sorts each "
                    "day into one of nine categories: Janma (Birth), Sampat (Wealth), Vipat "
                    "(Danger), Kshema (Well-being), Pratyak (Obstacle), Sadhaka "
                    "(Accomplishment), Vadha (Destruction), Mitra (Friendship), and "
                    "Ati-Mitra (Best Friend).",
                    "Sampat, Sadhaka and Ati-Mitra days favour decisive action, while Vipat "
                    "and Vadha days call for playing defence. The strong resemblance to "
                    "Sukuyo astrology is no coincidence — both trace back to the same "
                    "Indian astronomical roots.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "Your Rashi is approximated by taking your Western tropical Sun sign "
                    "and shifting it back one sign to account for the ayanamsa (roughly "
                    "23.85°). Your Nakshatra is calculated deterministically on a 27-part "
                    "cycle from your date of birth.",
                    "Your Lagna (rising sign) is approximated from your birth time and the "
                    "longitude difference between your birthplace and the Indian Standard "
                    "Time meridian (82.5°E). If your birth time is unknown, your Lagna is "
                    "treated as identical to your Rashi.",
                    "Full Jyotish practice goes on to layer in Dasha (planetary periods), "
                    "Varga (divisional charts), and much more besides. What this site "
                    "offers is best understood as an entry point into that much larger "
                    "system.",
                ],
            },
        ],
    },
    # ------------------------------------------------------------ Tibetan Astrology
    {
        "slug": "tibet",
        "module": "Tibetan Astrology",
        "title": "What Is Tibetan Astrology? Reading Fate Through Element, Mewa and Parkha",
        "description": "The origins of Tibetan astrology, how the animal-year and element pairing works, what the Mewa (magic-square number) and Parkha (trigram) mean, and why the calculation differs by gender.",
        "lead": (
            "Tibetan astrology grew from a fusion of Indian astrology and Chinese "
            "yin-yang / Five Element philosophy within the culture of Tibetan Buddhism. "
            "It reads a person's fate from four elements combined together: the animal "
            "year, the Five Great Elements, the Mewa (magic-square number), and the "
            "Parkha (trigram)."
        ),
        "sections": [
            {
                "heading": "The animal year paired with an element",
                "paragraphs": [
                    "The Tibetan calendar has its own set of twelve animal years — Rat, "
                    "Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Bird, Dog, and "
                    "Pig — closely mirroring the animals used in Japan and China.",
                    "These are combined with the Five Great Elements: Wood, Fire, Earth, "
                    "Metal and Water. Because the element changes every two years, the "
                    "combination of animal and element repeats on a 60-year cycle — hence "
                    "phrases like \"Wood Tiger year\" or \"Fire Rabbit year.\"",
                    "Wood is a growing force governing expansion and development; Fire, a "
                    "burning force governing passion and change; Earth, a supporting force "
                    "governing stability and accumulation; Metal, a cutting force governing "
                    "decisiveness and refinement; and Water, a circulating force governing "
                    "intellect and adaptability.",
                ],
            },
            {
                "heading": "What the Mewa is",
                "paragraphs": [
                    "The Mewa is a number from 1 to 9, each tied to a colour: 1, 6 and 8 "
                    "are white; 2 is black; 3 is blue; 4 is green; 5 is yellow; and 7 and 9 "
                    "are red. It draws on the same idea as the nine stars of the Chinese Luo "
                    "Shu diagram, and is calculated with the same formula used for a Nine "
                    "Star Ki Birth Star.",
                    "A white Mewa represents purity and a fresh start; a black Mewa, "
                    "strength gained by overcoming obstacles; a blue Mewa, vitality and "
                    "drive; a green Mewa, harmony and good relationships; a yellow Mewa, "
                    "influence from standing at the centre; and a red Mewa, passion and "
                    "honour.",
                ],
            },
            {
                "heading": "The Parkha (trigram) is calculated differently by gender",
                "paragraphs": [
                    "The Parkha is Tibetan astrology's counterpart to the eight trigrams "
                    "of the I Ching: Li (Fire), Kun (Earth), Da (Lake), Ken (Heaven), Kan "
                    "(Water), Gon (Mountain), Shin (Thunder), and Son (Wind).",
                    "A distinctive feature of Tibetan astrology is that the Parkha formula "
                    "itself differs by gender. For men, it's the remainder, divided by 8, of "
                    "(100 minus the last two digits of the birth year) divided by 3; for "
                    "women, the remainder, divided by 8, of (the last two digits of the "
                    "birth year plus 4) divided by 3. This reflects an Eastern philosophical "
                    "idea that the flow of yin and yang runs in opposite directions for men "
                    "and women.",
                    "This site uses the male formula whenever \"prefer not to say\" is "
                    "chosen for gender, and states this plainly in the full reading in the "
                    "interest of transparency about how the number was derived.",
                ],
            },
            {
                "heading": "How this site calculates it",
                "paragraphs": [
                    "The animal year is found on a 12-year cycle from 1924 as the base "
                    "Rat year, and the element cycles through the Five Great Elements based "
                    "on the animal-year index divided by two. The Mewa uses the same "
                    "Start-of-Spring-corrected formula as a Nine Star Ki Birth Star, and "
                    "the Parkha uses the gender-specific formulas above.",
                    "A given day's fortune is calculated by combining your animal-year "
                    "compatibility with today's day-branch (weighing relationships such as "
                    "the Three Harmonies, Six Combinations, and Clashes) with the "
                    "relationship between your element and today's day-stem element. Your "
                    "lucky colour comes from your Five Great Element, and your lucky item "
                    "and direction from your Parkha.",
                ],
            },
        ],
    },
]

# slug -> 記事 の索引
GUIDE_EN_BY_SLUG = {g["slug"]: g for g in GUIDES_EN}


def get_guide_en(slug: str):
    """slug から英語版記事を取得する。存在しない場合は None。"""
    return GUIDE_EN_BY_SLUG.get(slug)
