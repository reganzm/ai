import nltk
input_expr = nltk.sem.Expression.fromstring
a = input_expr('X | (Y -> Z)')
print(type(a),a)
b = input_expr('-(X & Y)')
print(type(b),b)
print(input_expr('X & Y'))
print(input_expr('X <-> -- X'))
