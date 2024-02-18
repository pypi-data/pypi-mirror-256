class solo():
    def __init__(self,name):
        self.name = name
    def printer(self):
        print(f'получилось {self.name}')
#ege demo 24 god/12.01.24
# zadanie_5
# a = int(input())
# b = list(bin(a))
# b = b[2:]
# b = ''.join(b)
# if a%3 == 0:
#     b += b[-3:]
#     print(int(b,2))
# else:
#     f = list(bin((a%3)*3))
#     f = f[2:]
#     f = ''.join(f)
#     b +=f
#     print(int(b,2))
#
#
# zadanie_5
# k = []
# for a in range(1,500):
#     b = list(bin(a))
#     b = b[2:]
#     b = ''.join(b)
#     if a%3 == 0:
#         b += b[-3:]
#     else:
#         f = list(bin((a%3)*3))
#         f = f[2:]
#         f = ''.join(f)
#         b +=f
#     if int(b,2)>151:
#         k.append(int(b,2))
# print(min(k))
#
#
# for n in range(4,10000):
#     a = '5'+ '2' *n
#     while '52' in a or '2222' in a or '1122' in a:
#         a = a.replace('52','11',1)
#         a = a.replace('2222','5',1)
#         a = a.replace('1122','25',1)
#     print(sum(map(int,a)),n)
#
# a = 3*(3125**8)+2*(625**7)-4*(625**6)+3*(125**5) - 2*(25**4) - 2024
# c = []
# while a>25:
#     c.append(a%25)
#     a = a//25
# c.append(a)
# c.reverse()
# d = ''
# for i in c:
#     d +=str(i)
# print(d.count('0'))
# print(d)
#
# def F(n):
#     if n >2024: return n
#     elif n<=2024: return n*F(n+1)
# print(F(2022)//F(2024))
#
#
# def f(x,y):
#     if x == 11: return 0
#     elif x>y: return 0
#     elif x == y: return 1
#     elif x<y: return f(x+1,y)+f(x*2,y)+f(x**2,y)
# print(f(2,20))
#
# with open(file = '24_10105.txt') as f:
#     a = f.readline()
# count = 0
# c = ''
# len_max = 0
# for i in range(len(a)):
#     if count != 100:
#         if a[i] == 'T':
#             count +=1
#             c +=a[i]
#         else:
#             c +=a[i]
#     else:
#         if len(c)>len_max:
#             len_max = len(c)
#         c = ''
#         count = 0
# print(len_max)



# EGE (fipi 4.02.23)/16.01.24
# print('x y z w F')
# for x in 0,1:
#     for y in 0,1:
#         for z in 0,1:
#             for w in 0,1:
#                 F = not((w or not(y)) and x) or y == z
#                 if F == False:
#                     print(x,y,z,w,F)
# wxzy

# Задание 8 не правильно
# count = 0
# g = 0
# for i in range(100000,666666):
#     for n in range(len(str(i))):
#         if str(i)[n] == '6':
#             g +=1
#     if g == 1:
#         g = 0
#         i = str(i)
#         if int(i[0]) % 2 == 0 and int(i[2]) % 2 == 0 and int(i[4]) % 2 == 0 and int(i[1]) % 2 == 1 and int(i[3]) % 2 == 1 and int(i[5]) % 2 == 1:
#             count += 1
#     else:
#         g = 0
# print(count)


# Задание 12
# a = '8'*120
# while '888' in a or '2222' in a:
#     a = a.replace('2222','88',1)
#     a = a.replace('888','22',1)
# print(a)

# Задание 14
# a = 3 * 1024**75 + 2*256**76- 16*77-2023
# c = ''
# count = 0
# while a>32:
#     c += str(a%32)
#     a //= 32
# print(a)
# c +=str(a)
# print(c)
# for i in c:
#     if i == '0':
#         count +=1
# print(count)

# Задание 15 ++
# def f(x,y):
#     return (x>a) or (y>a) or (y-2*x+12 !=0)
# for a in range(200):
#     if all(f(x,y) == 1 for x in range(200) for y in range(200)):
#         print(a)


# Задание 16
# def f(n):
#     if n<3: return 1
#     elif n>2 and n%2 == 0: return f(n-1) + 2*n-1
#     elif n>2 and n%2 == 1: return f(n-2) + 2*n
# print(f(21)-f(19))


# Задание 23
# def f(x,y):
#     if x == 9: return 0
#     if x>y: return 0
#     elif x ==y: return 1
#     elif x<y: return f(x+1,y)+f(x*2,y)
# print(f(2,12)*f(12,42))

# Задание 24
# with open(file = '24_6054.txt') as f:
#     a = f.readline()
# s = 'BC'
# g = 'A'
# st_max = ''
# st =''
# for i in range(2,len(a)+3,3):
#     if a[i-2] in s and a[i-1] in s and a[i] in g:
#         st +=a[i-2:i+1]
#         print(st)
#     else:
#         if len(st)>len(st_max):
#             st_max = st
#         st =''
# print(len(st_max),st_max)

# Задание 5 не правильно
# for N in range(1,1000):
#     c = list(bin(N))
#     c = c[2:]
#     if sum(map(int,c))%2 ==0:
#         c.append('0')
#         c = c[1:]
#         c[0] = '1'
#     elif sum(map(int,c))%2 ==1:
#         c.append('1')
#         c = c[1:]
#         c[0] = '11'
#     g = ''
#     for i in c:
#         g +=i
#     g= int(g,2)
#     if g>25:
#         print(N)



# Еге последнее 23 год/17.01.24
# print('x y z w')
# for x in 0,1:
#     for y in 0,1:
#         for z in 0,1:
#             for w in 0,1:
#                 if ((x<=(z==w)) or not(y<=w)) == 0:
#                     print(x,y,z,w)

# Задание 5
# for n in range(1,1000):
#     c = []
#     h = ''
#     N = n
#     while n>2:
#         c.append(str(n%3))
#         n //=3
#     c.append(str(n))
#     c.reverse()
#     if N%3 == 0:
#         c.append('02')
#         c[0] = '1' +c[0]
#         for i in c:
#             h +=i
#     else:
#         f = (N%3)*4
#         g = []
#         while f>2:
#             g.append(str(f%3))
#             f //= 3
#         g.append(str(f))
#         g.reverse()
#         for i in c:
#             h +=i
#         for i in g:
#             h +=i
#     if int(h,3)<199:
#         print(N,int(h,3))
# Задание 8
# n = 33
# a = '1'+'8'*n
# while '18' in a or '388' in a or '888' in a:
#     a = a.replace('18','8',1)
#     a = a.replace('388','81',1)
#     a = a.replace('888','3',1)
# if a.count('1') == 3:
#     print(n)

# Задание 15
# def f(x,y):
#     return (x+2*y)>a or (y<x) or (x<30)
#
# for a in range(200):
#     if all(f(x,y) for x in range(200) for y in range(200)):
#         print(a)

# Задание 16
# import sys
# sys.setrecursionlimit(3200)
# def f(n):
#     if n<3: return 3
#     elif n>=3: return 2*n+5+f(n-2)
# print(f(3027)-f(3023))

# Еге вариант чайкина 24/21.01.24
# print('x y z w F')
# for x in 0,1:
#     for y in 0,1:
#         for z in 0,1:
#             for w in 0,1:
#                 F = ((x<=y) or (z<=w)) and (not(x<=w))
#                 if x != 0:
#                     print(x,y,z,w, int(F))


# 5
# for n in range(1,100):
#     h = n
#     f = ''
#     while n>2:
#         f +=str(n%3)
#         n //=3
#     f +=str(n)
#     f = f[::-1]
#     if h%4 == 0:
#         f = f +f[-3:]
#     else:
#         g = (h%4)*4
#         u = ''
#         while g>2:
#             u +=str(g%3)
#             g //=3
#         u +=str(g)
#         u = u[::-1]
#         f += u
#         if int(f,3)<127:
#             print(int(f,3))


# 12
# for n in range(1,100):
#     it = [1,4,9,16,25,36,49,64,81,100,121,144,169,196,225]
#     a = '5' +'2'*n
#     while '52' in a or '222' in a or '122' in a:
#         a = a.replace('52','11',1)
#         a = a.replace('222','15',1)
#         a = a.replace('122','21',1)
#     if sum(map(int,a)) in it:
#         print(n)
#
#
# with open(file = '27-B_12479.txt') as f:
#     k = int(f.readline())
#     n = int(f.readline())
#     a = [int(s) for s in f]
#
# ans = -10
# max_razn = -100000000
# for i in range(k,n):
#     max_razn = max(max_razn,a[i-k] - (i-k))
#     ans = max(ans,max_razn+a[i] +i)
# print(ans)

#Еге 31.01.24 волна 2 23 года
#2 zad
# print('x y z w F')
# for x in 0,1:
#     for y in 0,1:
#         for z in 0,1:
#             for w in 0,1:
#                 F = (y<=x) and not(z) and w
#                 if F == True:
#                     print(x,y,z,w,F)
# 5zad

# for n in range(1,500):
#     n1 = n
#     s = ''
#     n2 = n
#     while n>2:
#         s = str(n%3) +s
#         n //=3
#     s = str(n) +s
#     if n1%3==0:
#         s +=s[-2:]
#     else:
#         s1 = ''
#         n1 = (n1%3)*5
#         while n1>2:
#             s1 = str(n1%3) +s1
#             n1 //=3
#         s1 = str(n1) +s1
#         s +=s1
#     if int(s,3)>133:
#         print(n2,int(s,3))


# 12 zad
# c = []
# for n in range(3,10000):
#     a = '1' + '2'*n
#     while '12' in a or '322' in a or '222' in a:
#         a = a.replace('12','2',1)
#         a = a.replace('322','21',1)
#         a = a.replace('222','3',1)
#     c.append(sum(map(int,a)))
# print(max(c))


# 15 zad
# def f (x,y):
#     return (x*y<A) or (x<y) or (9<x)
# for A in range(1,200):
#     if all(f(x,y) for x in range(1,200) for y in range(1,200)) == 1:
#         print(A)

# 16
# from sys import *
# setrecursionlimit(3200)
# def F(n):
#     if n<7: return 7
#     elif n>=7: return n+1+F(n-2)
# print(F(2024)-F(2020))

# 23 zad
# def f(x,y):
#     if x<y: return 0
#     elif x == 9: return 0
#     elif x == 16: return 0
#     elif x == y: return 1
#     elif x>y: return f(x-1,y) +f(x-2,y) + f(x//3,y)
# print(f(19,3))



# варик от яндекса/06.02.24/20:17/21/11
# 5
# def f(n):
#     s = ''
#     while n>4:
#         s = str(n%5) + s
#         n = n//5
#     s = str(n) + s
#     return s
# for n in range(1,1000):
#     n5=f(n)
#     if n%25==0:
#       n5= n5[-3:] + n5
#     else:
#       n5 = n5+ f(n%25)
#     r = int(n5 , 5)
#     if r > 10000:
#       print(n, r)

# print('a b c d F')
# for a in 0,1:
#     for b in 0,1:
#         for c in 0,1:
#             for d in 0,1:
#                 F = (a<=b) and (b<=c) and (c<=d)
#                 if F == True:
#                     print(a,b,c,d,F)


# 12
# for n in range(3,10000):
#     a = '5' + '2'*n
#     while '52' in a or '2222' in a or '1112' in a:
#         a = a.replace('52','11',1)
#         a = a.replace('2222','5',1)
#         a = a.replace('1112','2',1)
#     if sum(map(int,a)) == 1685:
#         print(n)

# 13
# from ipaddress import *
# ip = ip_address('20.24.110.42')
# net = ip_address('20.24.96.0')
# for mask in range(33):
#    network = ip_network(f'{ip}/{mask}', 0)
#    if network.network_address == net:
#        print(mask)
#        break


# 14
# a = ((18*(7**108))-(5*(49**76))+(343**35)-50)
# b = []
# print(a)
# a = abs(a)
# while a>48:
#     b.append(a%49)
#     a //=49
# b.append(a)
# print(sum(b))


# 15
# 1/120
# def f(x,y):
#     return (3*x+y>A) and (y<x) and (x<30)
# for A in range(1,200):
#     if all(f(x,y) for x in range(1,200) for y in range(1,200)):
#         print(A)

# 16
# def f(n):
#     if n >10000: return 42
#     elif n<=10000 and n%2 == 0: return 2*n +f(n+3) +f(n+4) +f(n+6)
#     elif n<=10000 and n%2 == 1: return (-1)*(n + f(n+1) + f(n+3))
# print(f(9996)-f(9994))
# 16
# from functools import*
# @lru_cache(None)
# def f(n):
#   if n>10000: return 42
#   if n<=10000 and n%2==0: return 2*n + f(n+3)+ f(n+4) +f(n+6)
#   if n<=10000 and n%2 !=0: return -(n+f(n+1) + f(n+3))
#
# print(f(9996) - f(9994))

# 23
# def f(x,y):
#     if x>y: return 0
#     elif x == 81: return 0
#     elif x==y: return 1
#     elif x<y: return f(x+x//10,y) +f(x +3,y) +f(2*x-1,y)
# print(f(42,73)*f(73,89))

# 24
# with open(file = '24.txt') as f:
#     a = f.readline()
# max_len = 0
# less = ''
# glas = 'AEIOUY'
# glass_1 = 0
# for i in range(len(a)):
#     if ord(a[i-1])<ord(a[i]) and glass_1 <=1:
#         if a[i-1] in glas:
#             glass_1 +=1
#         less += a[i-1]
#     else:
#         if len(less)>max_len:
#             max_len = len(less)
#         less = ''
#         glass_1 = 0
# print(max_len)