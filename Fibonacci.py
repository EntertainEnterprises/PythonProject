def fibonacci(n):
    a = 0
    b = 1
    for i in range(n):
        temp = a
        a = b
        b = temp + b
    return a

################################## Main Programm ########################################
#just change filename
filename = "Eingabe2.txt"
file = open(filename, "r")
content = file.readlines()
for entry in content:
    print("Die Fibonacci Zahl für " + entry[:-1] + " ist: " + str(fibonacci(int(entry[:-1]))))


file.close()


	

