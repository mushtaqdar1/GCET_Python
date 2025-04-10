# Python3 implementation to print the
# N terms of the series whose three
# terms are given

# Function to print the series
def printSeries(n, a, b, c):

	# Generate the ith term and
	# print it
	if (n == 1):
		print(a, end = " ");
		return;
	
	if (n == 2):
		print(a, b, end = " ");
		return;
	
	print(a, b, c, end = " ");

	for i in range (4, n + 1):
		d = a + b + c;
		print(d, end = " ");
		a = b;
		b = c;
		c = d;
	
# Driver Code
N = 7; a = 1; b = 3;
c = 4;

# Function Call
printSeries(N, a, b, c);

