f = open("cache.txt", "r")

print( f.read() )

f.close()

f = open("cache.txt", "w")
f.write('This is a test\n')
f.write('This is a test\n')
f.write('This is a test\n')
f.close()

f = open("cache.txt", "r")
print(f.read())
f.close()
