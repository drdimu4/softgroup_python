def is_palindrom(text):
    text = text.lower().replace(' ', '')
    return text == text[::-1]
print(is_palindrom('Eve'))
