def min_val(x, y):
    return x if x < y else y

def leaky_bucket():
    drop = 0
    mini = 0
    count = 0

    inp = [0] * 25
    cap = int(input("Enter the bucket size: "))
    process = int(input("Enter the operation rate: "))
    nsec = int(input("Enter the number of seconds you want to stimulate: "))

    for i in range(nsec):
        inp[i] = int(input(f"Enter the size of the packet entering at {i + 1} sec: "))

    print("\nSecond | Packet Received | Packet Sent | Packet Left | Packet Dropped\n")
    
    for i in range(nsec):
        count += inp[i]
        if count > cap:
            drop = count - cap
            count = cap
        
        print(f"{i + 1}\t\t{inp[i]}\t\t{min_val(count, process)}\t\t{count - min_val(count, process)}\t\t{drop}")
        
        count -= min_val(count, process)
        drop = 0
    
    i = nsec
    while count != 0:
        if count > cap:
            drop = count - cap
            count = cap
        
        print(f"{i + 1}\t\t0\t\t{min_val(count, process)}\t\t{count - min_val(count, process)}\t\t{drop}")
        
        count -= min_val(count, process)
        drop = 0
        i += 1

if __name__ == "__main__":
    leaky_bucket()
