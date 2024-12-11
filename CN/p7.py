# Write a program for simple RSA algorithm to encrypt and decrypt the data.

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def encrypt(message, e, n):
    encrypted_message = []
    for char in message:
        encrypted_char = (ord(char) - 96) ** e % n
        encrypted_message.append(encrypted_char)
    return encrypted_message


def decrypt(encrypted_message, d, n):
    decrypted_message = []
    for num in encrypted_message:
        decrypted_char = chr((num ** d % n) + 96)
        decrypted_message.append(decrypted_char)
    return ''.join(decrypted_message)


def main():
    p = int(input("Enter value of p: "))
    q = int(input("Enter value of q: "))

    n = p * q
    phi = (p - 1) * (q - 1)

    e = next(i for i in range(2, phi) if gcd(i, phi) == 1)
    d = modinv(e, phi)

    message = input("Enter the Message to be encrypted: ")

    nummes = [ord(c) - 96 for c in message]

    encrypted_message = encrypt(message, e, n)
    print("\nEncrypted message:")
    for num in encrypted_message:
        print(num, end=' ')

    decrypted_message = decrypt(encrypted_message, d, n)
    print("\n\nDecrypted message:\n", decrypted_message)


if __name__ == "__main__":
    main()
