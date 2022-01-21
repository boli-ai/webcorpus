"""
Copyright © Divyanshu Kakwani 2019, all rights reserved
"""

import string
import unicodedata as ud

LC_NAME = {
    "as": "assamese",
    "bd": "bodo",
    "bn": "bengali",
    "bh": "bihari",
    "en": "english",
    "gu": "gujarati",
    "hi": "hindi",
    "kn": "kannada",
    "ks": "kashmiri",
    "ml": "malayalam",
    "mr": "marathi",
    "ne": "nepali",
    "or": "oriya",
    "pa": "punjabi",
    "sa": "sanskrit",
    "sd": "sindhi",
    "ta": "tamil",
    "te": "telugu",
    "ur": "urdu",
}


LC_SCRIPT = {
    "hi": "devanagari",
    "kn": "kannada",
    "mr": "devanagari",
    "te": "telugu",
    "ta": "tamil",
    "gu": "gujarati",
    "or": "oriya",
    "bn": "bengali",
    "ml": "malayalam",
    "ne": "devanagari",
    "pa": "gurmukhi",
    "as": "bengali",
    "en": "latin",
    "ur": "arabic",
    "bd": "devanagari",
    "sa": "devanagari",
    "san": "ol chiki",
    "dg": "devanagari",
    "mni": "manipuri",
    "gom": "devanagari",
    "mai": "devanagari"
}


SCRIPT_DIGITS = {
    "devanagari": "०१२३४५६७८९",
    "gujarati": "૦૧૨૩૪૫૬૭૮૯",
    "telugu": "౦౧౨౩౪౫౬౭౮౯",
    "bengali": "০১২৩৪৫৬৭৮৯",
    "malayalam": "൦൧൨൩൪൫൬൭൮൯",
    "tamil": "௦௧௨௩௪௫௬௭௮௯௰",
    "kannada": "೦೧೨೩೪೫೬೭೮",
    "oriya": "୦୧୨୩୪୫୬୭୮୯",
    "gurmukhi": "੦੧੨੩੪੫੬੭੮੯",
    "latin": "0123456789",
    "urdu": "٠١٢٣٤٥٦٧٨٩٪",
}

dogri = ['𑠀','𑠁','𑠂','𑠃','𑠄','𑠅','𑠆','𑠇','𑠈','𑠉','𑠊','𑠋','𑠌','𑠍','𑠎','𑠏','𑠐','𑠑','𑠒','𑠓','𑠔','𑠕','𑠖','𑠗','𑠘','𑠙','𑠚','𑠛','𑠜','𑠝','𑠞','𑠟','𑠠','𑠡','𑠢','𑠣','𑠤','𑠥','𑠦','𑠧','𑠨','𑠩','𑠪','𑠫','𑠬','𑠭','𑠮','𑠯','𑠰','𑠱','𑠲','𑠳','𑠴','𑠵','𑠶','𑠷','𑠸','𑠹','𑠺']
manipuri = ['ꯀ','ꯁ','ꯂ','ꯃ','ꯄ','ꯅ','ꯆ','ꯇ','ꯈ','ꯉ','ꯊ','ꯋ','ꯌ','ꯍ','ꯎ','ꯏ','ꯐ','ꯑ','ꯒ','ꯓ','ꯔ','ꯕ','ꯖ','ꯗ','ꯘ','ꯙ','ꯚ','ꯛ','ꯜ','ꯝ','ꯞ','ꯟ','ꯠ','ꯡ','ꯢ','ꯣ','ꯤ','ꯥ','ꯦ','ꯧ','ꯨ','ꯩ','ꯪ','꯫','꯬','','꯭','꯰','꯱','꯲','꯳','꯴','꯵','꯶','꯷','꯸','꯹']
santhali = ['᱐','᱑','᱒','᱓','᱔','᱕','᱖','᱗','᱘','᱙','ᱚ','ᱛ','ᱜ','ᱝ','ᱞ','ᱟ','ᱠ','ᱡ','ᱢ','ᱣ','ᱤ','ᱥ','ᱦ','ᱧ','ᱨ','ᱩ','ᱪ','ᱫ','ᱬ','ᱭ','ᱮ','ᱯ','ᱰ','ᱱ','ᱲ','ᱳ','ᱴ','ᱵ','ᱶ','ᱷ','ᱸ','ᱹ','ᱺ','ᱻ','ᱼ','ᱽ','᱾','᱿']


def name2code(lang):
    for k, v in LC_NAME.items():
        if v.lower() == lang.lower():
            return k
    return None


def code2script(iso_code):
    iso_code = iso_code.lower()
    for c, s in LC_SCRIPT.items():
        if c == iso_code:
            return s.lower()
    return None


def in_script(char, script_name):
    if char == "।" or char.isspace() or char in string.punctuation:
        return True
    try:
        if script_name not in ud.name(char).lower():
            return False
    except:
        if char in santhali:
            return True
        elif char in dogri:
            return True
        elif char in manipuri:
            return True
        return False
    return True
