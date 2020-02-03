"""Gets the encoding of read in file."""


from chardet.universaldetector import UniversalDetector
import pathlib

def detect_encoding(file):
    """Reads in binary file rows, and returns a dictionary of
    encoding, confidence, and language, which can be fed into a open.
    detector.done will be True as soon as confidence is 1.0, so the whole file
    won't be read. """
    detector = UniversalDetector()
    detector.reset()
    with open(file, 'rb') as file_in:
        for row in file_in:
            detector.feed(row)
            if detector.done:
                break
    detector.close()
    return detector.result

