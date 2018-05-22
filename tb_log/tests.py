from django.test import TestCase

# Create your tests here.
a='/tb_log/tb_log-123.html'
b=a.split('.')
print(b[0].split('-')[1])
print()