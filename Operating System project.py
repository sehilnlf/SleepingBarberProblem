# Just for cutting hair, not doing other something -> time to cut hair approximately between 10 to 60 minutes
import threading
import time
import random
# from datetime import datetime, timedelta, time as dt_time

class BarberShop:
  # OPENING_HOUR = 8
  # CLOSING_HOUR = 19
  # LUNCH_START_HOUR = 12
  # LUNCH_END_HOUR = 13

  def __init__(self, num_chairs, max_customers, served_customers):
    self.max_customers = max_customers
    self.barber_semaphore = threading.Semaphore(0)
    self.customer_semaphore = threading.Semaphore(0)
    self.mutex = threading.Semaphore(1)
    self.waiting_customers = []
    self.num_chairs = num_chairs
    self.leaving_customers = []
    self.served_customers = served_customers
    self.remain_customers = []

  def print_entering_message(self, index):
    print(f">>>>>>Customer {index} is ENTERING...")

  def barber(self):
    # current_hour = self.get_current_hour()
    # print("current_hour: ", current_hour)
    while True:
      self.barber_semaphore.acquire()
      self.mutex.acquire()
      # if self.is_shop_open(current_hour):
      if len(self.waiting_customers)>0:
        customer = self.waiting_customers.pop(0)
        print(f"The barber is cutting hair for customers {customer} \n")
        self.mutex.release()
        # Define the time to cut hair
        cutting_time = random.randint(10, 60)
        time.sleep(cutting_time)
        print(f"The barber has finished cutting hair for customer {customer} \n"
              f"Cutting time: {cutting_time} minutes\n")
        self.customer_semaphore.release()
      else:
        print("The barber is sleeping... \n")
        self.mutex.release()
        # if not self.customer_semaphore.acquire(blocking = False):
        #   break
      # else:
      #   #Barber shop is closed
      #   print("Barber shop is closed")
      #   break
    
  def customer(self):
    # The time to come to the shop and choose chair
    arrival_time = random.randint(30, 50)
    time.sleep(arrival_time)
    print("Time to wait the next customers: ", arrival_time)

    list_of_customers = self.get_random_customer(self.served_customers)
    print(f"The number of customer in this visit: {len(list_of_customers)} \n"
          f" The list of customer: {list_of_customers}")
    
    self.mutex.acquire()

    if len(list_of_customers) + len(self.waiting_customers) <= self.num_chairs: #and self.is_shop_open(current_hour):
      for i in (list_of_customers):
        self.print_entering_message(i)
        self.waiting_customers.append(i)
        print(f"Customer {i} is waiting in the waiting room. Remaining seats: {self.num_chairs - len(self.waiting_customers)} \n")
        print("List of served customer: ", self.waiting_customers)
      self.mutex.release()
      self.barber_semaphore.release()

      for i in (list_of_customers):
        self.customer_semaphore.acquire()
        print(f"Customer {i} has finish cutting hair cut \n")
      
      self.mutex.acquire()
      self.leaving_customers.append(list_of_customers[0])
      print("List of leaving customers: ", self.leaving_customers)

      for i in self.waiting_customers:
        if self.customer_decides_to_leave():
          print(f"Customer {i} left because of a long wait\n")
          self.waiting_customers.remove(i)

      print("List of served customers: ", self.waiting_customers)
      self.mutex.release()
    
    else:
      print("The number of the next customer is over for the wating chairs")
      #Not enough chairs for all arriving customers
      remain_customers = self.num_chairs - len(self.waiting_customers) 
      #Randomly select customers to wait in the waiting room
      available_team = random.sample(list_of_customers, remain_customers)
      print("Available team: ", available_team)

      for i in (list_of_customers):
        if i in available_team:
          self.print_entering_message(i)
          self.waiting_customers.append(i)
          print(f"Customer {i} is waiting in the waiting room. Remaining seats: {self.num_chairs - len(self.waiting_customers)} \n")
          self.mutex.release()
          self.barber_semaphore.release()

          for i in (available_team):
            self.customer_semaphore.acquire()
            print(f"Customer {i} has finish cutting hair cut \n")
            
          self.mutex.acquire()
          self.leaving_customers.append(available_team[0])
          print("List of leaving customers: ", self.leaving_customers)
        else:
          print(f"Customer {i} is leaving as the queue is full\n")

      for i in self.waiting_customers:
        if self.customer_decides_to_leave():
          print(f"Customer {i} left because of a long wait\n")
          self.waiting_customers.remove(i)

      print("List of served customer: ", self.waiting_customers)
      self.mutex.release()

  # # Check the time to activate the shop
  # def is_shop_open(self, current_hour):
  #   return self.OPENING_HOUR <= int(current_hour.split(":")[0]) < self.CLOSING_HOUR and not (
  #             self.LUNCH_START_HOUR <= int(current_hour.split(":")[0]) < self.LUNCH_END_HOUR
  #     )

  def get_random_customer(self, customer_list, num_customers=1):
    selected_customers = random.sample(customer_list, min(num_customers, len(customer_list)))
    for customer in selected_customers:
      customer_list.remove(customer)
    return selected_customers

  def customer_decides_to_leave(self):
    return random.random() < 0.3
  
  def run_barber_shop(self):
    barber_thread = threading.Thread(target=self.barber)
    customer_threads = []  # FIFO

    barber_thread.start()

    for i in range(self.max_customers):
      customer_thread = threading.Thread(target=self.customer)
      customer_threads.append(customer_thread)
      customer_thread.start()  # Start to service customer

    barber_thread.join()  # Wait for the barber thread to complete

    for customer_thread in customer_threads:
      customer_thread.join()

def main():
  num_chairs = 5
  max_customers = 10
  served_customers = list(range(max_customers))
  print("List of customers: ", served_customers)
  barber_shop = BarberShop(num_chairs, max_customers, served_customers)
  barber_shop.run_barber_shop()
  print("End time")


if __name__ == "__main__":
  main()
