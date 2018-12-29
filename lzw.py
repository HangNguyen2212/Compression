import base64

def encodeLzw(input_string):
    print (input_string[0])
    print (type(input_string))
    for char in input_string:
        if char in dictionary:	
            continue
        else:
            dictionary.append(char)
    dictionary.sort()
    print (dictionary)
    next = ''
    for char in input_string:
        a = next + char
        if a in dictionary:
            next = a
        else:
            next = a[len(a)-1]
            dictionary_word = a[0:len(a)-1]	
            dictionary.append(a)
            encoded_version.append(dictionary.index(dictionary_word))
    encoded_version.append(dictionary.index(next))

def decodeLzw( encoded_version ):
	x = ""	
	for i in encoded_version:
		x = x + dictionary[i]
	return x

dictionary = []
encoded_version = []

def main(image_file, encode_file, decode_file):

    with open(image_file, 'rb') as imageFile:
        stringInput = base64.b64encode(imageFile.read())
        print (stringInput)

    encodeLzw(stringInput.decode('utf-8'))
    decoded_version = decodeLzw(encoded_version)
    with open(encode_file, 'w') as encodeFile:
        encodeFile.write(str(encoded_version))

    imgdata = base64.b64decode(decoded_version)
    with open(decode_file, 'wb') as f:
        f.write(imgdata)

if __name__ == "mainLZW":
    image_file = ''
    encode_file = ''
    decode_file = ''

    main(image_file, encode_file, decode_file)
