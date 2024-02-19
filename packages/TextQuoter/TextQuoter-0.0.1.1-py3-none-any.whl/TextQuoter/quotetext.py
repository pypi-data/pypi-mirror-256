from typing import List, Tuple


def get_quotes(text: str) -> Tuple[int, List[int]]:
    """
    Count and return the total quotes and their indexes in the given text.

    Args:
        text (str): The input text.

    Returns:
        Tuple[int, List[int]]: A tuple containing the total quotes and their indexes.
    """
    text = text.replace("“", '"').replace("”", '"')

    return text.count('"'), [i for i, char in enumerate(text) if char == '"']


def clear_subquotes(text: str) -> str:
    """
    Remove sub-quotes and return the modified text.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text without sub-quotes.
    """
    simple_set = str.maketrans({"‘": "'", "’": "'"})

    return text.translate(simple_set)


def set_simple_quotes(text: str) -> str:
    """
    Replace special quotation marks with simple double quotes in the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with special quotation marks replaced by simple double quotes.
    """
    simple_set = str.maketrans({"”": '"', "“": '"'})
    res = text.translate(simple_set)
    return res.replace('""', '"')


def update_text(positions: List[int], text: str, q1: str = "“", q2: str = "”") -> str:
    """
    Update the text by enclosing specified positions with given quotation marks.

    Args:
        positions (List[int]): A list of positions where quotation marks should be applied.
        text (str): The input text.
        q1 (str, optional): The opening quotation mark. Defaults to "“".
        q2 (str, optional): The closing quotation mark. Defaults to "”".

    Returns:
        str: The updated text with specified positions enclosed by the given quotation marks.
    """
    split_version = [positions[i : i + 2] for i in range(0, len(positions), 2)]
    for pair in split_version:
        if len(pair) == 2:
            text = (
                text[: pair[0]]
                + q1
                + text[pair[0] + 1 : pair[1]]
                + q2
                + text[pair[1] + 1 :]
            )
        elif len(pair) == 1:
            text = text[: pair[0]] + "" + text[pair[0] + 1 :]
    return text


def requoter(input_text: str, use_simple: bool = False) -> str:
    """
    Process the input text, fixing and changing the quotation style.

    Args:
        input_text (str): The text input that will be converted.
        use_simple (bool, optional): If `True`, It will return the text with the simply quotes instead of the special markings. Defaults to False.

    Returns:
        str: The processed text with fixed and changed quotation style.
    """
    input_text = set_simple_quotes(input_text)

    quantity, positions = get_quotes(input_text)

    if quantity:
        if use_simple:
            input_text = update_text(positions, input_text, '"', '"')
            return clear_subquotes(input_text)
        return update_text(positions, input_text)
    return input_text
