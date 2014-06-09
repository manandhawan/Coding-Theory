'''
201101052 - Manan Dhawan
Input - Text File containing a Generator Matrix with each row in new line with no space in between.

The program will generate all the possible codewords from the Generator Matrix.
The Weight Enumerator of the code will be calculated.
The Weight Enumerator of the Dual code will be calculated using MacWilliams Identity.
The program will generate the dual of the code.
The Weight Enumerator of the dual will be calculated.
Output - Code generated from the input Generator Matric,
		 Dual of the code,
		 Weight Enumerator of the Code, Dual 
		 and Weight Enumerator of the Dual of the given code using MacWilliams Identity,
		 hence verifying MacWilliams Identity, in an output file and console.

P.S.: Please read README.txt for installation of requirements and dependencies.
'''
import itertools
try:
	from sympy import Poly
	from sympy.abc import z	
except Exception, e:
	print "Sympy not found. Please install sympy as directed in README.txt"


def generator_to_code(filename):
	'''
	Returns a list consisting of the codes generated from the Generator in the file.

	Keyword arguments:
	filename -- filename of the Generator matrix. 
	'''
	global output_file
	f = open(filename)
	matrix = [line.strip() for line in f]
	f.close()
	output = open(output_file,'a')
	print "The input Generator Matrix is : ", matrix
	print
	
	output.write("The input Generator Matrix is : ")
	output.write(str(matrix))
	output.close()

	k = len(matrix)
	n = len(matrix[0])
	lambda_value = pow(2,k)

	lambda_list = list()
	matrix_list = list()

	for i in matrix:
		matrix_list.append(i)

	for x in map(''.join, itertools.product('01', repeat=k)):
		lambda_list.append(x)

	code_list = list()

	for i in xrange(lambda_value):
		temp_list = list()
		temp = 0

		for j in xrange(k):
			temp_list.append(int(lambda_list[i][j],2)*int(matrix_list[j],2))

		for j in xrange(len(temp_list)):
			temp = temp^temp_list[j]

		code_list.append(str(bin(temp)[2:]).zfill(n))

	code_to_dual(code_list)

	return code_list


def code_to_dual(code_list):
	'''
	Returns the dual code from the code_list.

	Keyword arguments:
	code_list -- list of codewords
	'''
	n = len(code_list[0])
	check_list = list()
	for x in map(''.join, itertools.product('01', repeat=n)):
		check_list.append(x)

	dual_list = list()
	for i in xrange(len(check_list)):
		count_zero = 0
		for j in xrange(len(code_list)):
			temp_single_code = list()
			flag = 0

			for x in xrange(n):
				temp_single_code.append(int(list(check_list[i][x])[0])&int(list(code_list[j][x])[0]))

			for x in xrange(len(temp_single_code)):
				flag = flag^temp_single_code[x]

			if flag == 0:
				count_zero += 1

			if count_zero == len(code_list):
				dual_list.append(check_list[i])

	return dual_list

def weight_enum(code):
	'''
	Returns a list of Weight Enumerator of the input code.

	Keyword arguments:
	code -- list of codewords
	'''
	global n,m,output_file
	single_code=""
	single_code = code[0]

	m = len(code)						
	n = len(single_code)				
	output = open(output_file,'a')
	print "Values of n, M are : ", n, m
	print

	output.write("\n")
	output.write("Values of n, M are : ")
	output.write(str(n)+", ")
	output.write(str(m))
	

	print "The Weight Enumerator function is given by W(C) = Sum[A(i)*z^i]" 
	print

	output.write("\n")
	output.write("\n")
	output.write("The Weight Enumerator function is given by W(C) = Sum[A(i)*z^i]")
	output.close()

	weight_enum = []					
	no_of_ones = []

	for x in xrange(0,m):
		no_of_ones.append(code[x].count('1'))

	for i in xrange(0,n+1):
		no_of_ones.count(i)
		weight_enum.insert(i,no_of_ones.count(i))

	return weight_enum

def dual_weight_enum(reversed_weight_enum):
	'''
	Returns a list of Weight Enumerator of the dual code.

	Keyword arguments:
	reversed_weight_enum -- reversed list of weight enumerator
	'''
	try:
		from sympy import Poly,poly,simplify,expand
		from sympy.abc import x,z
	except Exception, e:
		print "Sympy not found. Please install sympy as directed in README.txt"
	

	w1 = Poly(reversed_weight_enum,x)

	print "The MacWilliams Identity is given by W(Cdual)  = [{(1+z)^n)*W((1-z)/(1+z)}]/[2^k]"
	print
	output = open(output_file,'a')
	output.write("\n")
	output.write("\n")
	output.write("The MacWilliams Identity is given by W(Cdual)  = [{(1+z)^n)*W((1-z)/(1+z)}]/[2^k]")
	output.close()

	w2 = w1((1-z)/(1+z))

	w3 = poly((1+z)**n)

	temp_expr = w3*w2/m

	wcd = simplify(expand(temp_expr))

	return wcd

def main():
	global n,m,output_file
	input_filename = str(raw_input("Enter the Generator Matrix file: "))
	filename = input_filename + ".txt"

	output_file = "output_" + filename
	output = open(output_file,'w+')
	output.write("Output generated using Generator Matrix from file: ")
	output.write(filename)
	output.write("\n \n")
	output.close()
	code = generator_to_code(filename)
	
	print "Thus, the code is : ", code
	print
	output = open(output_file,'a')
	output.write("\n")
	output.write("Thus, the code is : ")
	output.write(str(code))
	output.close()


	weight_enum_c = weight_enum(code)

	reversed_weight_enum = []
	for i in reversed(weight_enum_c):
		reversed_weight_enum.append(i)

	print "Weight Enumerator of Code (C) is ", str(Poly(reversed_weight_enum,z))[5:-17]
	print
	output = open(output_file,'a')
	output.write("\n")
	output.write("Weight Enumerator of Code (C) is ")
	output.write(str(Poly(reversed_weight_enum,z))[5:-17])
	output.close()

	weight_enum_c_dual = dual_weight_enum(reversed_weight_enum)
	print "Weight Enumerator of Dual Code (using MacWilliams) is ", weight_enum_c_dual
	print
	output = open(output_file,'a')
	output.write("\n")
	output.write("Weight Enumerator of Dual Code (using MacWilliams) is ")
	output.write(str(weight_enum_c_dual))
	output.write("\n")
	output.close()

	dual = code_to_dual(code)

	print "The dual of the code is: ", dual
	print

	output = open(output_file,'a')
	output.write("\n")
	output.write("\n")
	output.write("The dual of the code is: ")
	output.write(str(dual))
	output.close()

	weight_enum_c = weight_enum(dual)

	reversed_weight_enum = []
	for i in reversed(weight_enum_c):
		reversed_weight_enum.append(i)

	print "Weight Enumerator of Dual Code (Cdual) is ", str(Poly(reversed_weight_enum,z))[5:-17]
	print
	output = open(output_file,'a')
	output.write("\n")
	output.write("Weight Enumerator of Dual Code (Cdual) is ")
	output.write(str(Poly(reversed_weight_enum,z))[5:-17])
	output.close()

if __name__ == '__main__':
	main()
