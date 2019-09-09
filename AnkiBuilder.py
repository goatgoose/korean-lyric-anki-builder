from lyricsgenius import Genius
from gtts import gTTS
from googletrans import Translator
import genanki


class AnkiBuilder:
    def __init__(self, deck_name, deck_id):
        self.deck_name = deck_name
        self.deck_id = deck_id

        self.genius = Genius("DhLgBRFiLg4HOiABUzSJvGjpTDgX6vwVSFvyV3P6igiKdAhNdvq0VbwnF8QEXxa0")
        self.translator = Translator()

        self.model = genanki.Model(
            1313562696, "lyrics-model",
            fields=[
                {"name": "Term"},
                {"name": "Translation"}
            ],
            templates=[
                {
                    "name": "term card",
                    "qfmt": "{{Term}}",
                    "afmt": "{{FrontSide}}<hr id='answer'>{{Translation}}"
                }
            ]
        )

    @staticmethod
    def char_is_hangul(char):
        value = ord(char)

        # https://jrgraphix.net/research/unicode_blocks.php
        return 0x1100 <= value <= 0x11FF or 0x3130 <= value <= 0x318F or 0xAC00 <= value <= 0xD7AF

    @staticmethod
    def block_is_hangul(block):
        for char in block:
            if not AnkiBuilder.char_is_hangul(char):
                return False
        return True

    @staticmethod
    def get_hangul_blocks(song):
        lines = []
        for line in song.lyrics.split("\n"):
            blocks_in_line = []

            line = line.strip()
            if line.startswith("["):
                continue

            for word in line.split(" "):
                if AnkiBuilder.block_is_hangul(word) and word:
                    blocks_in_line.append(word)
            if len(blocks_in_line) > 0:
                lines.append(blocks_in_line)

        return lines

    def build(self):
        hangul = self.get_hangul_blocks(self.genius.search_song("likey", artist="TWICE"))

        translated = {}
        for line in hangul:
            phrase = " ".join(line)
            translated[phrase] = self.translator.translate(phrase).text

            for block in line:
                translated[block] = self.translator.translate(block).text

        deck = genanki.Deck(self.deck_id, self.deck_name)
        for term in translated:
            deck.add_note(genanki.Note(
                model=self.model,
                fields=[term, translated[term]]
            ))

        genanki.Package(deck).write_to_file("decks/" + self.deck_name + ".apkg")


if __name__ == '__main__':
    builder = AnkiBuilder("Likey", 1768730765)
    builder.build()
