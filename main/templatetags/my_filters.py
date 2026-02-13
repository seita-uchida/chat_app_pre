from django import template

register = template.Library()

@register.filter(name="censor")
def censor(value, word):
    """
    value: 元のメッセージ
    word: 消したい言葉
    """
    # その言葉を「〇」に置き換える（文字数分）
    return value.replace(word, "〇" * len(word))