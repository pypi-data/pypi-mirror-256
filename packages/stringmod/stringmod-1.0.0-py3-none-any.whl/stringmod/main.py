def reverse_string(s):
    print(s[::-1])

def is_palindrome(string):
    string = string.replace(" ", "").lower()
    
    if string == string[::-1]:
        print("The string is a palindrome.")
    else:
        print("The string is not a palindrome.")

def is_anagram(s1, s2):
    s1 = s1.replace(" ", "").lower()
    s2 = s2.replace(" ", "").lower()
    
    if sorted(s1) == sorted(s2):
        print("The strings are anagrams.")
    else:
        print("The strings are not anagrams.")

def is_fibonacci(n):
    a = 0
    b = 1
    while a < n:
        a, b = b, a + b
    if a == n:
        print("The number is a Fibonacci number.")
    else:
        print("The number is not a Fibonacci number.")

def is_prime(n):
    if n <= 1:
        print("The number is not prime.")
    elif n <= 3:
        print("The number is prime.")
    elif n % 2 == 0 or n % 3 == 0:
        print("The number is not prime.")
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            print("The number is not prime.")
        i += 6
    print("The number is prime.")

def is_odd(n):
    if n % 2 != 0:
        print("The number is odd.")
    else:
        print("The number is not odd.")

def is_even(n):
    if n % 2 == 0:
        print("The number is even.")
    else:
        print("The number is not even.")

def is_positive(n):
    if n > 0:
        print("The number is positive.")
    else:
        print("The number is not positive.")


def is_negative(n):

    if n < 0:
        print("The number is negative.")
    else:
        print("The number is not negative.")


def is_integer(n):

    if isinstance(n, int):
        print("The number is an integer.")
    else:
        print("The number is not an integer.")

def is_float(n):
    
        if isinstance(n, float):
            print("The number is a float.")
        else:
            print("The number is not a float.")

def is_numeric(n):

    if isinstance(n, int) or isinstance(n, float):
        print("The number is numeric.")
    else:
        print("The number is not numeric.")


def is_string(s):
    if isinstance(s, str):
        print("The input is a string.")
    else:
        print("The input is not a string.")

def is_list(l):
    if isinstance(l, list):
        print("The input is a list.")
    else:
        print("The input is not a list.")

def is_tuple(t):
    if isinstance(t, tuple):
        print("The input is a tuple.")
    else:
        print("The input is not a tuple.")

def is_set(s):
    if isinstance(s, set):
        print("The input is a set.")
    else:
        print("The input is not a set.")

def is_dict(d):
    if isinstance(d, dict):
        print("The input is a dictionary.")
    else:
        print("The input is not a dictionary.")

def is_boolean(b):

    if isinstance(b, bool):
        print("The input is a boolean.")
    else:
        print("The input is not a boolean.")

def is_factorial(n):
    i = 1
    factorial = 1
    while factorial < n:
        i += 1
        factorial *= i
    if factorial == n:
        print("The number is a factorial.")
    else:
        print("The number is not a factorial.")


def is_armstrong(n):
    num = n
    order = len(str(n))
    sum = 0
    while n > 0:
        digit = n % 10
        sum += digit ** order
        n //= 10
    if num == sum:
        print("The number is an Armstrong number.")
    else:
        print("The number is not an Armstrong number.")

def is_perfect(n):
    sum = 0
    for i in range(1, n):
        if n % i == 0:
            sum += i
    if sum == n:
        print("The number is a perfect number.")
    else:
        print("The number is not a perfect number.")

def vowel_count(word):
    vowels = 'aeiou'
    count = 0
    for char in word:
        if char in vowels:
            count += 1
          
    print(f"The word has {count} vowels.")
                  

