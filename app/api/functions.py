from bs4 import BeautifulSoup


def is_html(string):
    """
    Check if string contains html.
    If html, return true, otherwise, return false.
    """
    result = bool(BeautifulSoup(string, 'html.parser').find())
    return result


def cap_sentence(string):
    """
    Capitalize first letter of each word in string.
    """
    return ' '.join(word[:1].upper() + word[1:] for word in string.split(' '))
