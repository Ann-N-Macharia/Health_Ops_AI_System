import re

phone_pattern = re.compile(r'(?:\+254|0)[17]\d{8}')
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def mask_pii(message: str) -> str:
    message = phone_pattern.sub("[MASKED]", message)
    message = email_pattern.sub("[MASKED]", message)
    return message

if __name__ == "__main__":
    message = "Call me on 0712345678 or email ann@example.com about my appointment."

    masked_message = mask_pii(message)

    print("Original:", message)
    print("Masked:", masked_message)