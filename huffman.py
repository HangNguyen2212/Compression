import heapq
import os,sys
import numpy as np
from functools import total_ordering
from scipy.misc import imread
from scipy.misc import toimage
from PIL import Image

size_x = 0
size_y = 0
a_image = []

#Function to make image flatten
def preprocess(string):
	global x,y,a_image
	im = imread(string)
	x =  im.shape[0]
	y =  im.shape[1]
	 
	return im.flatten()

class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


class HuffmanCoding:
	def __init__(self, path, encode_file,decode_file):
		self.path = path
		self.encode_path = encode_file
		self.decode_path = decode_file
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		output_path = self.encode_path
		flatten_img = preprocess(self.path)
		img2str = (', '.join(str(x) for x in flatten_img))

		with open(output_path, 'wb') as output:
			text = img2str
			text = text.rstrip()

			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))

		return output_path

	#Decompress Function start here

	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self):
		global a_image
		output_path = self.decode_path

		with open(self.encode_path, 'rb') as file:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			unprocess_decode = self.decode_text(encoded_text).split(",")
			decompressed_text = np.zeros(x*y*3)
			for i in range(len(unprocess_decode)):
				j = unprocess_decode[i].replace(' ','')
				decompressed_text[i] = int(j)
				
			text = np.reshape(decompressed_text,(x,y,3))
			toimage(text).save(output_path)

		return output_path

def main(image_file,encode_file,decode_file):
	h = HuffmanCoding(image_file,encode_file,decode_file)
	h.compress()
	h.decompress()

if __name__ == "__main__":
	image_file = ''
	encode_file = ''
	decode_file = ''
	main(image_file,encode_file,decode_file)