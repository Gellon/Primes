# Prime Number Searcher v1.4
import math
import multiprocessing
import platform
import sys
import threading
import time

def search_prime(thread_num, threads_num, input_num, divider_found):
    print(f"[DEBUG] Start thread {thread_num}.")
    start_time = time.time()
    basic_primes = (2, 3, 5, 7, 11, 13, 17) # More primes - less process conflicts. But generated Number_Dictionary should fits in CPU core cache
    num_dict = []
    for n in range(3, math.prod(basic_primes), 2):
        if all(n % prime for prime in basic_primes):
            num_dict.append(n)
    num_dict.append(math.prod(basic_primes) + 1)
    num_dict = num_dict[thread_num::threads_num] 

    if thread_num == 0:
        for ii in basic_primes:
            if input_num % ii == 0:
                if input_num != ii:
                    print(f"Thread {thread_num} find the divider.", ii, "*", input_num // (ii), f"= {input_num}")
                else:
                    print(f"Number {input_num} is a prime!")
                divider_found.value = True
                break
        print(f"[DEBUG] Items in Number Dictionary for every thread = {len(num_dict)}")
    
    for n in range(0, math.trunc(math.sqrt(input_num)), math.prod(basic_primes)):
        if divider_found.value:
            break
        for i in num_dict:
            ii = i + n
            if input_num % (ii) == 0 and input_num != (ii):
                print(f"Thread {thread_num} find the divider.", ii, "*", input_num // (ii), f"= {input_num}")
                divider_found.value = True
                break

    print(f"[DEBUG] Finish thread {thread_num}.\t{(time.time() - start_time):.03f}sec")


if __name__ == "__main__":

  len_argv = len(sys.argv)
  if len_argv < 2 or len_argv > 3:
    print("Launch Primes Number Searcher with arguments like: pns.py <Number to test> [Number of threads]")
    sys.exit(-0)

  input_num = int(sys.argv[1])
  if int(input_num) <= 1:
    print("[ERROR] Prime number shold be grater than one")
    sys.exit(-1)

  threads_num = int(sys.argv[2]) if len_argv == 3 else multiprocessing.cpu_count()
  if threads_num <= 0:
    print("[ERROR] Threads number shold be grater than zero")
    sys.exit(-2)

  print(f"[DEBUG] Starting {threads_num} threads on {platform.processor()} CPU")
  threads = []
  divider_found = multiprocessing.Value('b', False)

  start_time = time.time()

  for thread_num in range(threads_num):
    thread = multiprocessing.Process(target=search_prime, args=(thread_num, threads_num, input_num, divider_found))
#   thread = threading.Thread       (target=search_prime, args=(thread_num, threads_num, input_num, divider_found))
    thread.start()
    threads.append(thread)

  for thread in threads:
    thread.join()

  if not divider_found.value:
    print(f"Number {input_num} is a prime!")

  print(f"Common execution time: {(time.time() - start_time):.03f}sec")
