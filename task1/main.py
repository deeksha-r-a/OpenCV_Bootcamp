import threading

from tracker import run_tracker
from count import run_counter


def main():

    t1 = threading.Thread(target=run_tracker)
    t2 = threading.Thread(target=run_counter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
