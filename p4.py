# Write a program for error detecting code using CRC-CCITT (16- bits).

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]
    
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        
        pick += 1
    
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    
    return tmp

def encodeData(data, key):
    appended_data = data + '0'*(len(key)-1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword, remainder

def decodeData(data, key):
    remainder = mod2div(data, key)
    for bit in remainder:
        if bit == '1':
            return False
    return True

def main():
    data = input("Enter data to be transmitted: ")
    key = input("Enter the Generating polynomial: ")
    
    print("\n----------------------------------------")
    encoded_data, remainder = encodeData(data, key)
    print("Data padded with n-1 zeros: ", data + '0'*(len(key)-1))
    print("CRC or Check value is: ", remainder)
    print("Data to be transmitted: ", encoded_data)
    print("\n----------------------------------------")

    received_data = input("Enter the received data: ")
    print("\n----------------------------------------")
    if decodeData(received_data, key):
        print("No error detected in received data")
    else:
        print("Error detected in received data")
    print("\n----------------------------------------")

if __name__ == "__main__":
    main()
