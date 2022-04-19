s = "hello world"
l = [ord(c) for c in s]
print(l)

for char in "€uro":
    print(char, char.encode("utf-8"))
