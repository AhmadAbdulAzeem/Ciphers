import numpy as np
import string

alphabetValues = dict(zip(string.ascii_uppercase, range(0, 26)))


def caeserCipher(plainText, key):
    cipherText = str()
    plainText = plainText.upper()

    for p in plainText:
        cipherText += chr((alphabetValues[p]+key) % 26 + ord('A'))

    return cipherText

# print(caeser("abcdefghijklmnopqrstuvwxyz", 3))


def VigenereCipher(plainText, key, mode):
    cipherText = str()
    plainText = plainText.upper()
    key = key.upper()

    if mode is True:
        key += plainText
    else:
        numberOfRepetion = (len(plainText) // len(key) + 1)
        key = key * numberOfRepetion

    for i in range(0, len(plainText)):
        cipherText += caeserCipher(plainText[i], alphabetValues[key[i]])
    return cipherText


# print(VigenereCipher("wearediscoveredsaveyourself", "deceptive", False))

def vernamCipher(plainText, key):
    cipherText = str()
    plainText = plainText.upper()
    key = key.upper()

    itr = 0
    for p in plainText:
        cipherText += chr((alphabetValues[p] ^
                           alphabetValues[key[itr]]) + ord('A'))
        itr += 1
        if itr == len(key):
            itr = 0

    return cipherText

# print(vernamCipher("RAMSWARUPK", "RANCHOBABA"))


# playfair cipher helper functions
def formatPlainText(plainText):
    plainText = plainText.replace(" ", "")  # remove soaces
    plainText = plainText.upper()
    plainText = plainText.replace("J", "I")
    result = str()
    itr = 0
    while itr < len(plainText):
        # If a pair is a repeated letter, insert ‘X’ as filler between the two characters.
        if(((itr+1) < len(plainText)) and (plainText[itr] == plainText[itr+1])):
            result += plainText[itr] + 'X'
        else:
            result += plainText[itr]
        itr += 1
    if(len(result) % 2 == 1):
        result += 'X'
    return result


def createTable(key):
    key = key.upper()
    key = key.replace(" ", "")
    table = list()
    temp = list()
    i = 0
    uniqueChars = list()
    for c in key:
        if c not in uniqueChars:
            i += 1
            if c == 'J':
                uniqueChars.append('I')
                temp.append('I')
            else:
                uniqueChars.append(c)
                temp.append(c)
        if i == 5:
            i = 0
            table.append(temp)
            temp = list()
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":

        if c not in uniqueChars:
            i += 1
            uniqueChars.append(c)
            temp.append(c)
        if i == 5:
            i = 0
            table.append(temp)
            temp = list()
    return np.array(table)

# search in table and find indeces of chars a, b


def search(keyTable, a, b):
    if a == 'J':
        a = 'I'
    elif b == 'J':
        b = 'I'
    i, j = 0, 0
    x, y, z, m = 0, 0, 0, 0
    indeces = list()

    for i in range(5):
        for j in range(5):
            if keyTable[i][j] == a:
                x = i  # row index
                y = j  # column index
            elif keyTable[i][j] == b:
                z = i
                m = j
    indeces.append(x)
    indeces.append(y)
    indeces.append(z)
    indeces.append(m)
    return np.array(indeces)


def encrypt(plainText, keyTable):
    i = 0
    cipehrText = str()
    while i < len(plainText)-1:
        indeces = search(keyTable, plainText[i], plainText[i + 1])
        if indeces[0] == indeces[2]:  # same row
            a = keyTable[indeces[0]][(indeces[1]+1) % 5]
            b = keyTable[indeces[0]][(indeces[3]+1) % 5]
        elif indeces[1] == indeces[3]:  # same column
            a = keyTable[(indeces[0]+1) % 5][indeces[1]]
            b = keyTable[(indeces[2]+1) % 5][indeces[1]]
        else:
            a = keyTable[indeces[0]][indeces[3]]
            b = keyTable[indeces[2]][indeces[1]]
        i += 2
        cipehrText += a + b
    return cipehrText


def playFairCipher(plainText, key):
    plainText = formatPlainText(plainText)
    keyTable = createTable(key)
    cipherText = encrypt(plainText, keyTable)
    return cipherText


#print(playFairCipher("hello world", "CHARLES"))

# keySize = 3 or 2


def hillCipher(plainText, key, keySize):
    plainText = plainText.upper()
    plainText += "X" * ((keySize-len(plainText) % keySize) % keySize)
    # parse the plainText into pairs of 2 or 3 chars according to keySize
    pairs = list()
    for i in range(0, len(plainText), keySize):
        templist = list()
        for j in range(0, keySize):
            templist.append(ord(plainText[i + j]) - ord("A"))
        pairs.append(np.array(templist))
    cipherText = str()
    for i in range(0, pairs.__len__()):
        pairs[i] = np.dot(pairs[i], key)
        for i in pairs[i]:
            cipherText += chr((((i % 26) + 26) % 26) + ord("A"))
    return cipherText


def readfile(filename):
    file = open(filename, "r")
    ans = []
    for p in file.readlines():
        ans.append(p.replace("\n", ""))
    return ans


def writefile(filename, strlist):
    file = open(filename, "w")
    for st in strlist:
        file.write(st + "\n")


if __name__ == "__main__":
    # Caeser
    keys = [3, 6, 12]
    ciphers = list()
    plains = readfile("caesar_plain.txt")
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(caeserCipher(p, k))
        ciphers.append("\n")
    writefile("caesar_cipher.txt", ciphers)

    # playfair
    plains = readfile("playfair_plain.txt")
    keys = ["rats", "archangel"]
    ciphers = list()
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(playFairCipher(p, k))
        ciphers.append("\n")
    writefile("playfair_cipher.txt", ciphers)

    # hill_2x2
    plains = readfile("hill_plain_2x2.txt")
    key = np.array([[5, 17], [8, 3]])
    ciphers = []
    for p in plains:
        ciphers.append(hillCipher(p, key, 2))
    writefile("hill_cipher_2x2.txt", ciphers)

    # hill_3x3
    plains = readfile("hill_plain_3x3.txt")
    key = np.array([[2, 4, 12], [9, 1, 6], [7, 5, 3]])
    ciphers = []
    for p in plains:
        ciphers.append(hillCipher(p, key, 3))
    writefile("hill_cipher_3x3.txt", ciphers)

    # Vigenere
    plains = readfile("vigenere_plain.txt")
    keys = [("PIE", False), ("AETHER", True)]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k[0]))
        for p in plains:
            ciphers.append(VigenereCipher(p, k[0], k[1]))
        ciphers.append("\n")
    writefile("vigenere_cipher.txt", ciphers)

    # vernam
    plains = readfile("vernam_plain.txt")  
    keys = ["SPARTANS"]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(vernamCipher(p, k))
        ciphers.append("\n")
    writefile("vernam_cipher.txt", ciphers)