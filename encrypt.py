def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(encrypted_text, shift):
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text


# def test_encrypt_decrypt():
#     input_text = ""
#     shift = 5
#
#     encrypted_text = encrypt(input_text, shift)
#     decrypted_text = decrypt(encrypted_text, shift)
#
#     assert decrypted_text == input_text, "Encryption and decryption failed"
#     print(encrypted_text)
#     print(decrypted_text)
#     return "Test passed"
# print(test_encrypt_decrypt())
