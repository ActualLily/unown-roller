def rankemoji(rank: int):

    EMOJIS = {
        1: "<:starter:1053401721851887646> ",
        2: "<:beginner:1053401770094772274> ",
        3: "<:amateur:1053401803548532818> ",
        4: "<:ace:1053401851824975872> ",
        5: "<:pro:1053401872746156162> ",
        6: "<:master:1053401951590678559> ",
        7: "<:champion:1053401983748423822> "
    }

    if 0 < rank < 8:
        return EMOJIS[rank]
    else:
        return "[?]"