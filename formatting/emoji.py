def rank(rank: int):
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


def type(type: str):
    TYPES = {
       "bug": "<:typebug:1054303705056419900> ",
       "dark": "<:typedark:1054303706281164842> ",
       "dragon": "<:typedragon:1054303707736588348> ",
       "electric": "<:typeelectric:1054303709502382110> ",
       "fairy": "<:typefairy:1054303711029117028> ",
       "fighting": "<:typefighting:1054303711876350033> ",
       "fire": "<:typefire:1054303713382121503> ",
       "rock": "<:typerock:1054303778356084766> ",
       "psychic": "<:typepsychic:1054303776653180978> ",
       "poison": "<:typepoison:1054303774883188816> ",
       "normal": "<:typenormal:1054303773339693056> ",
       "ice": "<:typeice:1054303772177858590> ",
       "ground": "<:typeground:1054303770844082196> ",
       "grass": "<:typegrass:1054303769359294505> ",
       "ghost": "<:typeghost:1054303703865237524> ",
       "flying": "<:typeflying:1054303714724294686> ",
       "steel": "<:typesteel:1054303779866017792> ",
       "water": "<:typewater:1054303781350817812> "
    }

    if str in TYPES.keys():
        return TYPES[type]
    else:
        return "[?]"
