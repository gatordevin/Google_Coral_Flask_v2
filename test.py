from edgetpuvision.apps2 import run_server
from edgetpuvision.classify import add_render_gen_args, render_gen

l = run_server(add_render_gen_args, render_gen)

def main():
    while True:
        test = l.image()
        
        print(test.overlay, "test")

if __name__ == '__main__':
    main()
