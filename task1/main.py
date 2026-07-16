from threading import Thread
import tracker
import count

if __name__ == "__main__":
    t1 = Thread(target=tracker.run_tracker)
    t2 = Thread(target=count.run_counter)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
