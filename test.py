from edgetpuvision.apps2 import run_server
from edgetpuvision.classify import add_render_gen_args, render_gen
from threading import Thread, Event

l = run_server(add_render_gen_args, render_gen)

def background():
    test = l.image()
    print("hello")
    # while True:
    #     test = l.image()
        
    #     print(test.overlay, "test")
def main():
    # thread1 = Thread(target=background)
    # thread1.deamon = True
    # thread1.start()
    # while True:
    #     print("ok")
    while True:
        
        test = l.image()
        
if __name__ == '__main__':
    main()
