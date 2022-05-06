# %%
import re
from typing import Iterable

from nytext.loader import load_or_download_archive_data
from nbex.interactive import session, print_interactive, pprint_interactive, pprint
from collections import Counter

# %%
data = load_or_download_archive_data()


# %%
def extract_subject_keywords_from_item(item):
    keyword_dicts = item.get("keywords", [])
    return {keyword_dict["value"] for keyword_dict in keyword_dicts
            if keyword_dict["name"] == "subject"}


# %%
pprint_interactive(extract_subject_keywords_from_item(data[0]))


# %%
def extract_subject_keywords(items):
    subject_keywords_per_item = (extract_subject_keywords_from_item(item)
                                 for item in items)
    return set().union(*subject_keywords_per_item)


# %%
pprint_interactive(list(extract_subject_keywords(data))[:10])

# %%
name_without_birth_date_rx = re.compile("[^(]+")


# %%
def remove_birth_date_from_name(name):
    match = name_without_birth_date_rx.match(name)
    assert match, f"Name {name} has unrecognized format."
    return match.group(0).strip()


# %%
def extract_person_names_from_item(item, remove_birth_dates=True):
    def get_name(keyword_dict):
        raw_name = keyword_dict["value"]
        if remove_birth_dates:
            return remove_birth_date_from_name(raw_name)
        else:
            return raw_name.strip()

    keyword_dicts = item.get("keywords", [])
    return {get_name(keyword_dict) for keyword_dict in keyword_dicts
            if keyword_dict["name"] == "persons"}


# %%
pprint_interactive(extract_person_names_from_item(data[0]))


# %%
def extract_person_names(items, remove_birth_dates=True):
    person_names_per_item = (extract_person_names_from_item(item, remove_birth_dates)
                             for item in items)
    return set().union(*person_names_per_item)


# %%
pprint_interactive(extract_person_names(data))


# %%
def words_for_item_key(item, key, words_to_skip: Iterable = frozenset()):
    if key == "headline":
        text = item.get(key, {}).get("main", "")
    else:
        text = item.get(key, "")
    words = (word.strip(' \t\n\r.,!?-=—').lower() for word in text.split())
    words = (word for word in words if word not in words_to_skip)
    return words


# %%
def naive_word_frequencies_for_item_key(
        item, key="headline", words_to_skip: Iterable = frozenset("")) -> Counter:
    words = words_for_item_key(item, key, words_to_skip)
    return Counter(words)


# %%
print_interactive(naive_word_frequencies_for_item_key(data[0]))
print_interactive(naive_word_frequencies_for_item_key(data[0], "headline", {"will"}))
print_interactive(naive_word_frequencies_for_item_key(data[0], "abstract"))
print_interactive(naive_word_frequencies_for_item_key(data[0], "snippet"))
print_interactive(naive_word_frequencies_for_item_key(data[0], "lead_paragraph"))


# %%
def naive_word_frequencies_for_key(items, key="headline",
                                   words_to_skip: Iterable = frozenset("")) -> Counter:
    result = Counter()
    for item in items:
        words = words_for_item_key(item, key, words_to_skip=words_to_skip)
        result.update(words)
    return result


# %%
if session.is_interactive:
    word_frequencies = naive_word_frequencies_for_key(data, "headline")
    pprint(word_frequencies.most_common(10))

# %% Maybe don't remove he/his/her/hers, etc. if you want to analyze gender inequality
stop_words = frozenset(
    {"", "the", "a", "to", "in", "of", "and", "for", "is", "on", "at", "with", "how",
     "are", "what", "as", "from", "case", "your", "an", "it", "will", "after", "this",
     "you", "about", "who", "that", "be", "was", "by", "his", "he", "has", "have",
     "her", "but", "their", "its", "i", "had", "when", "or", "they", "she", "not",
     "were"})

# %%
if session.is_interactive:
    word_frequencies_without_stop_words = naive_word_frequencies_for_key(data,
                                                                         "headline",
                                                                         words_to_skip=stop_words)
    pprint(word_frequencies_without_stop_words.most_common(10))

# %%
if session.is_interactive:
    pprint(naive_word_frequencies_for_key(data, "lead_paragraph", stop_words)
           .most_common(20))
