import base64
from operator import itemgetter

dic = {}
counts = {}

def ShannonFanoCoding(stringImage, code):
    a = {}
    b = {}
    if len(stringImage) == 1:
        dic[stringImage.popitem()[0]] = code
        return 0
    for i in sorted(stringImage.items(), key=itemgetter(1), reverse=True):
        if sum(a.values()) < sum(b.values()):
            a[i[0]] = stringImage[i[0]]
        else:
            b[i[0]] = stringImage[i[0]]
    ShannonFanoCoding(a, code + "0")
    ShannonFanoCoding(b, code + "1")

def main (image_file, encode_file, decode_file):
    with open(image_file, 'rb') as imageFile:
        stringInput = base64.b64encode(imageFile.read())
        print (stringInput)
    input_string = stringInput.decode('utf-8')
    for char in input_string:
        if char in counts:	
            counts[char] += 1
        else:
            counts[char] = 1
    for char in sorted(counts):
        print (char, '=>', counts[char]/len(input_string))

    compressed = []
    ShannonFanoCoding(counts, "")

    with open('dictionary.txt', 'w') as dicFile:
        for i in sorted(dic):
            dicFile.write(str(i) + "=" + str(dic[i]) + '\n')
    with open(encode_file, 'w') as encodedFile:
        for i in input_string:
            encodedFile.write(dic[i] + '\n')
            compressed.append(dic[i])	
    
    print("Decompressed Image: ")
    decompressed = ''
    for i in compressed:
        for j in dic:
            if dic[j] == i:
                decompressed += j

    imgdata = base64.b64decode(decompressed)
    with open(decode_file, 'wb') as f:
        f.write(imgdata)

if __name__ == "mainShannon":
	image_file = ''
	encode_file = ''
	decode_file = ''

	main(image_file, encode_file, decode_file)

	