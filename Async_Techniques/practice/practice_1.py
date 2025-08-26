import threading

def generate_data(num:int, inputs:list):
    pass

# daemon = True  
# if the main method exits, it is gonna shut down the thread

work = threading.Thread(target= generate_data, args=(20, []), daemon=True)

work.start()


data= []


threads = [
    threading.Thread(target=generate_data, args=(20, data), daemon=True),
]


[t.start() for t in threads]