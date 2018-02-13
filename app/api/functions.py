from bs4 import BeautifulSoup


def is_html(string):
    """If string contains html returns true."""
    result = bool(BeautifulSoup(string, 'html.parser').find())
    return result


def cap_sentence(string):
  return ' '.join(word[:1].upper() + word[1:] for word in string.split(' '))
