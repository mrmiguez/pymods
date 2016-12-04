class A(object):
 def __init__(self):
   print("world")

class B(A):
 def __init__(self):
   print("hello")
   super(B, self).__init__()

B()