#!/usr/bin/env python3

import argparse

from expressionive.expressionive import htmltags as T
from orgbookchapterverse.orgbookchapterverse import TextCollection, interlinear_chapter

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", "-b")
    parser.add_argument("--chapter", "-c")
    parser.add_argument("--verse", "-v")
    parser.add_argument("--language", "-l", action='append')
    parser.add_argument("reference")
    return vars(parser.parse_args())

def emphasize_word(text):
    """Convert markdown-style bolding to expressionive."""
    result = []
    while "**" in text:
        try:
            before, between, after = text.split("**", 2)
            result.append(before)
            result.append(T.span(class_='word')[between])
            text = after
        except:
            # there was an unmatched "**" in the text
            result.append(text)
            return result
    result.append(text)
    return result

def spanify_verse(verse):
    """Put span markers into a numbered verse."""
    number, text = verse.strip(' ').split(' ', 1)
    return [T.span(class_='verse_number')[number], T.span(class_='verse_text')[emphasize_word(text)]]

def chapter_html(bible, chapter):
    """Return the expressionive structure for a Bible chapter."""
    return T.div(class_="bible_chapter")[[T.p(class_="bible_verse")[spanify_verse(line)]
                                          for line in bible.chapter(chapter_name_hack(chapter)).lines()
                                          if line]]

def chapters_html(bible, chapters):
    """Return the expressionive structure for a list of Bible chapters."""
    return [[T.h3[chapter], chapter_html(bible, chapter)]
            for chapter in chapters]

def interlinear_verse(number, verse):
    return [T.tr[[T.th[str(number)],
                  [[T.td[text]
                    for text in verse]]
                  ]]]

def chapter_interlinear_html(versions, chapter):
    """Return the expressionive structure for an interlinear text."""
    try:
        book_name, chapter_number = chapter.rsplit(" ", 1)
    except ValueError:
        print("problem splitting", chapter, "into book name and chapter number")
        return []
    return T.table(class_="interlinear_chapter")[
        [[T.tr[[T.th(class_="verse_number")[str(vnumber)],
                [[T.td(class_=(("verse_text_%d_%d" % (len(versions), colno))
                               if len(versions) <= 4
                               else "verse_text"))[emphasize_word(text)]
                  for colno, text in enumerate(verse)]]
                ]]]
         for vnumber, verse in enumerate(
                 interlinear_chapter(versions, book_name, chapter_number),
                 start=1)]]

def chapters_interlinear_html(versions, chapters, heading=T.h2):
    """Return the expressionive structure for a list of Bible chapters."""
    return [[heading[chapter], chapter_interlinear_html(versions, chapter)]
            for chapter in chapters]

VERSION_FILES = {
    "albanian": "al",
    "deutsch": "de",
    "dutch": "nl",
    "finnish": "fi",
    "français": "fr",
    "french": "fr",
    "german": "de",
    "greek": "gr",
    "hebrew": "he",
    "icelandic": "is",
    "italian": "it",
    "kiswahili": "sw",
    "kjv": "kj",
    "latin": "vg",
    "mongolian": "mn",
    "nederlands": "nl",
    "norsk": "no",
    "norwegian": "no",
    "polska": "pl",
    "portuguese": "po",
    "português": "po",
    "romanian": "ro",
    "românește": "ro",
    "russian": "ru",
    "shqip": "al",
    "suomi": "fi",
    "svenska": "se",
    "swahili": "sw",
    "swedish": "se",
    "ukrainian": "uk",
    "vulgate": "vg",
    "íslenska": "is",
    "ελληνικά": "gr",
    "русский": "ru",
    "українська": "uk",
    "עִבְרִית": "he",
    "ἑλληνική": "gr",
}

NORMALISED_NAMES = {
    "Psalm": "Psalms",
}

def bible_main(book, chapter, verse, language, reference):
    book = NORMALISED_NAMES.get(book, book)
    chapters = (["%s %d" % (book, i) for i in range(*chapter.split("-"))]
                if "-" in chapter
                else ["%s %d" % (book, chapter)])
    print("chapters are", chapters)
    versions = [
        TextCollection(os.path.expandvars("$BIBLE/%s.org" % VERSION_FILES[version.lower()]), version)
        for version in language
    ]
    # chapters_interlinear_html(versions,
    #                           chapters
    #                           )
