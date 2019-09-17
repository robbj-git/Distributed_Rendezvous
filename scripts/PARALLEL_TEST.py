from multiprocessing import  Process, Pipe
import time
import numpy as np

class MyTestClass():

    def __init__(self, a):
        self.a = a
        self.b = 2*a
        print "Set b to", self.b

    def f(self, conn):
        temp_arr = [0]*20
        for i in range(20):
            temp_arr[i] = self.a+i
            time.sleep(0.1)
        conn.send(np.array(temp_arr))
        self.print_a_thing()
        conn.close()

    def run(self):
        parent_conn, child_conn = Pipe()
        p = Process(target=self.f, args=(child_conn,))
        self.b = 54
        p.start()

        my_arr = [0]*20

        for i in range(20):
            my_arr[i] = i
            time.sleep(0.1)

        # my_arr = [my_arr, parent_conn.recv()]
        rec_arr = parent_conn.recv()
        print rec_arr, rec_arr.shape, self.b
        p.join()


    def print_a_thing(self):
        print "Totally printing a thing! Plz don't complain!"
        # THIS DOESN'T WORK, NOT UNEXPECTED!
        self.b = 78
        print "HEre I set it to", self.b

if __name__ == '__main__':
    obj = MyTestClass(5.2)
    obj.run()

# if __name__ == '__main__':
#     parent_conn, child_conn = Pipe()
#     p = Process(target=f, args=(child_conn,))
#     p.start()
#
#     my_arr = [0]*20
#
#     for i in range(20):
#         my_arr[i] = i
#         time.sleep(0.1)
#
#     # my_arr = [my_arr, parent_conn.recv()]
#     rec_arr = parent_conn.recv()
#     print rec_arr, rec_arr.shape
#     p.join()
