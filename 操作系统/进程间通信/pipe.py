import os
import time
 
(r, w)  = os.pipe()
pid = os.fork()
 
if pid == 0:
    os.close(w)
    while True:
        msg = os.read(r, 1024)
        print msg
        if msg == 'q':
            os.close(r)
            break
else:
    os.close(r)
    while True:
        str1 = raw_input(">")
        os.write(w, str1)
        if str1 == "q":
            os.close(w)
            os.wait()
            break
        time.sleep(0.2)
