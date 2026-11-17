"""clean_text.py: clean and mask a customer message before it goes to a model (Session 3 lab)

Fill in each function body. Do not change the function names: the tests call them.
Check your work from the adv-genai folder:  uv run pytest tests/test_s03.py
"""

import re


def normalise_spaces(text):
    """Remove spaces at both ends and squeeze repeated spaces into one."""
    return " ".join(text.split())


def mask_pan(word):
    """A PAN looks like ABCDE1234F: 5 letters, 4 digits, 1 letter. Keep only the last 4 characters."""
    return "*" * (len(word) - 4) + word[-4:]


def mask_phone(word):
    """A phone number is exactly 10 digits. Keep only the last 4 digits."""
    return "*" * 6 + word[-4:]


def unique_lines(lines):
    """Drop repeated lines, keeping the first of each, in the original order."""
    return list(dict.fromkeys(lines))


def word_counts(text):
    """Count how many times each word appears, ignoring upper and lower case."""
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def mask_message(text):
    """Clean the spaces, then mask every PAN and phone number in the message."""
    text = normalise_spaces(text)
    text = re.sub(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
    lambda m: mask_pan(m.group()), text)
    text = re.sub(r'\b[0-9]{10}\b',
    lambda m: mask_phone(m.group()), text)
    return text


MESSAGES = [
    "  Hello,   I applied for a home loan   last week.  ",
    "My PAN is ABCDE1234F and my phone is 9876543210",
    "My PAN is ABCDE1234F and my phone is 9876543210",
    "Please   call me back about the loan  status",
]

if __name__ == "__main__":
    for line in unique_lines(MESSAGES):
        print(mask_message(line))
    print(word_counts("Loan status please. Home loan status"))
