# Create a dictionary to store the network and host bits associated with each class. Can use this dictionary in the functions later to access them
classes = {
    "A" : {
        "network_bits": 7, #class A has 7 network bits
        "host_bits": 24     #and 24 host bits
     },
    "B": {
        "network_bits": 14, #class B has 14 network bits
        "host_bits": 16     #and 16 host bits
    },
    "C": {
        "network_bits": 21, #class C has 21 network bits
        "host_bits": 8      #and 8 host bits
    },
    "D": {
        "network_bits": "N/A", # For class D and E, network bits are reserved for multicasting (sending packets to multiple IP addresses)
         "host_bits": "N/A"  # For class D and E, host bits are reserved for multicasting (sending packets to multiple IP addresses)
    },
    "E": {
        "network_bits": "N/A",
        "host_bits": "N/A"
    }
}
#part 1
def get_class_stats(ip_addr):
    ip_addr_split = ip_addr.split(".") #Get everything up to decimal point as this is the first octet(e.g 1.1.1.1 or 136.206.18.7)
    first_octet = int(ip_addr_split[0]) #Convert to integer in order to make it eaiser to compare later on
    if first_octet <= 127:
        print("Class: A") #0-127 is class A
        print("Network: " + str(2 ** (classes["A"]["network_bits"]))) #The number of networks for class A is 2 ** network bits (ie 2 ** 7). Uses the global dictionary "classes" to access the network bit information
        print("Host: " + str(2 ** (classes["A"]["host_bits"]))) # The number of hosts for class A is 2 ** host bits (ie 2 ** 24). Uses the global dictionary "classes" to access the network bit information
        print("First address: 0.0.0.0")
        print("Last address: 127.255.255.255")

    elif first_octet <= 191 and first_octet >= 128:
        print("Class: B") #128-191 is class B
        print("Network: " + str(2 ** (classes["B"]["network_bits"])))
        print("Host: " + str(2 ** (classes["B"]["host_bits"])))
        print("First address: 128.0.0.0")##################################doesn't want it hard coding##############prefix nibble
        print("Last address: 191.255.255.255")

    elif first_octet <= 223 and first_octet >= 192:
        print("Class: C") #192-223 is class C
        print("Network: " + str(2 ** (classes["C"]["network_bits"])))
        print("Host: " + str(2 ** (classes["C"]["host_bits"])))
        print("First address: 192.0.0.0")
        print("Last address: 223.255.255.255")

    elif first_octet <= 239 and first_octet >= 224:
        print("Class: D") # 224-239 is class D
        print("Network: N/A") # For class D and E, network bits are reserved for multicasting (sending packets to multiple IP addresses)
        print("Host: N/A") # For class D and E, host bits are reserved for multicasting (sending packets to multiple IP addresses)
        print("First address: 224.0.0.0")
        print("Last address: 239.255.255.255")

    else:
        print("Class: E") # 240-255 is class E
        print("Network: N/A") 
        print("Host: N/A")
        print("First address: 240.0.0.0")
        print("Last address: 255.255.255.255")
        

get_class_stats("126.168.10.0") #Run part 1 code here


def to_binary_string(ip_addr):
 #split into array of four ["136","206","19","9"]
    byte_split = ip_addr.split(".")
 # convert each number into a int, format it as binary, turn it back into a stirng
    return ['{0:08b}'.format(int(x)) for x in byte_split]


def to_decimal_dot(ip_addr_list):
 # for each string in the list
 # use str(int(x,2)) to convert it into a decimal number
 # and then turn that number into a string e.g. '10000100' -> '132'
 # put all converted numbers into a list ["132","206","19","7"]
 # call ".".join on the list to merge them into a string separated by "."
 return ".".join([str(int(x,2)) for x in ip_addr_list])


#part 2 -Subnet(class C) calculator
#Part 3 - Subnet (Class B) calculator
#Nice little extras -Subnet (Class A) calculator
#to get in CIDR  notation-convert subnet mask into binary and add up all the 1s (e.g. 255.255.255.192 is 1111 1111.1111 1111.1111 1111.1100 0000) number of 1s = 26
#This tells us how many bits are used for the network (ie network bits)
def get_subnet_stats(ip_addr, subnet_mask): # Takes in a class C or class B or class A ip address in decimal dot notation as a string and a subnet mask
    
    binary = to_binary_string(subnet_mask) # Use the helper function from above to convert the subnet mask to binary. Returns a list
    binary_string = "".join(binary) #Join this list to a string
    network_bits =  0 #Stores the total amount of network bits
    for num in binary_string: #Iterate through the binary string to find how many network bits
        if int(num) == 1:
            network_bits += 1
    print("\n" + "Address: " + ip_addr + "/" + str(network_bits)) #Print out in CIDR notation


    subnet_bits = 0 # Stores the total amount of subnet bits
    if subnet_mask.split(".")[2] == "255": #check if this is a class C
        i = 3 #If it is, let i = 3
    elif subnet_mask.split(".")[1] != "255": #Check if this is a class A
        i = 1
    elif subnet_mask.split(".")[2] != "255": #Check if this is a class B
        i = 2 #If it is, let i = 2
        # As class C has default subnet mask - 255.255.255.0, we can just look at the last byte to find how many subnet bits there are.
        #As class B has default subnet mask - 255.255.0.0, we can look at the second last byte to find out how many subnet bits there are.
    for num in binary[i]:
        if int(num) == 1:
            subnet_bits += 1
    subnets = 2 ** subnet_bits
    print("Subnets: " + str(subnets))

    #Addressable hosts per subnet
    unmasked_bits = 0
    if subnet_mask.split(".")[1] != "255": #Check it's a class A
        i = 1
        while i < 4:
            for num in binary[i]:
                if int(num) == 0:
                    unmasked_bits += 1
            i += 1
    elif subnet_mask.split(".")[2] != "255": #Check it's a class B
            i = 2
            while i < 4:
                for num in binary[i]:
                    if int(num) == 0:
                        unmasked_bits += 1
                i += 1
    elif subnet_mask.split(".")[2] == "255": #Check it's a class C
        for num in binary[3]:
            if int(num) == 0:
                unmasked_bits += 1
    hosts = (2 ** unmasked_bits) - 2 # Have to subtract 2 for the network address and the broadcast address, otherwise the network would be unusable
    print("Addressable hosts per subnet:", str(hosts))
    
    #Valid subnets
    valid_subnets = [] #Start counting at 0 and increment by the increment number until you reach the mask, e.g. 0, 64, 128, 192
    index_of_last_octet = ip_addr.rindex(".") #As the last octet will the be the changing values in a class C, we need to know this index
    subnet_mask_split = subnet_mask.split(".")

    if subnet_mask.split(".")[1] != "255":
        ip_addr_split = ip_addr.split(".")
        index_of_second_octet = ip_addr.index(".")
        third_octet = str(ip_addr_split[2])
        i = 1
        increment_number = 256 - int(subnet_mask_split[i]) #e.g. 256 - 192 = 64
        for i in range(0, int(subnet_mask_split[1]) + 1, increment_number): #int(subnet_mask_split[1]) is the subnet mask byte
            valid_subnets.append(ip_addr[:index_of_second_octet] + "."+ str(i) + "." + third_octet + ip_addr[index_of_last_octet:]) #Append each valid subnet to a list

    elif subnet_mask.split(".")[2] != "255": # Need the find the second last byte for a class B address
        i = 2
        j = 0
        total = 0 #This will be the counter to check how many "." we pass through. Once we hit 2 "." then we know we are on the second last byte
        while total < 2:
            if ip_addr[j] == ".":
                total += 1
            j += 1
        index_of_second_last_octet = j
        increment_number = 256 - int(subnet_mask_split[i])
        for k in range(0, int(subnet_mask_split[2]) + 1, increment_number): #int(subnet_mask_split[2]) is the subnet mask byte
            valid_subnets.append(ip_addr[:index_of_second_last_octet] + str(k) + str(ip_addr[index_of_last_octet:])) #Append each valid subnet to a list
    
    elif subnet_mask.split(".")[2] == "255": #If it's a class C address
        i = 3
        increment_number = 256 - int(subnet_mask_split[i]) #e.g. 256 - 192 = 64
        for i in range(0, int(subnet_mask_split[3]) + 1, increment_number): #int(subnet_mask_split[3]) is the subnet mask byte
            valid_subnets.append(ip_addr[: index_of_last_octet] + "."+ str(i)) #Append each valid subnet to a list
    
    print("Valid subnets:", valid_subnets)

    #broadcast address
    #Broadcast is always the number just before the next subnet(so if subnets were 0, 64, 128, 192...then broadcasts are 63, 127, 191, and the last one is always 255)
    broadcast_addresses = []
    if subnet_mask.split(".")[1] != "255":
        for i in range(increment_number, int(subnet_mask_split[1]) + 1, increment_number):
            broadcast_addresses.append((ip_addr[:index_of_second_octet] + "."+ str(i-1) + ".255.255"))
        broadcast_addresses.append((ip_addr[:index_of_second_octet] + "."+ "255.255.255"))

    elif subnet_mask.split(".")[2] != "255": #If it's a class B address
        for i in range(increment_number, int(subnet_mask_split[2]) + 1, increment_number):
            broadcast_addresses.append(ip_addr[: index_of_second_last_octet] + str(i-1) + ".255")
        broadcast_addresses.append(ip_addr[: index_of_second_last_octet] + "255" + ".255") #broadcast address of last subnet is always 255
    
    elif subnet_mask.split(".")[2] == "255": #If it's a class C address
        for i in range(increment_number, int(subnet_mask_split[3]) + 1, increment_number):
            broadcast_addresses.append(ip_addr[: index_of_last_octet] + "."+ str(i-1))
        broadcast_addresses.append(ip_addr[: index_of_last_octet] + "."+ str(255)) #broadcast address of last subnet is always 255
    print("Broadcast addresses: \n", broadcast_addresses)

    #Valid hosts
    #The numbers between the subnet address and broadcast
    i = 0
    first_addresses = [] #A list to store the subnets
    last_addresses = [] #A list to store the broadcasts
    while i < len(valid_subnets): #loop through the valid subnets we found earlier
        subnet_index = valid_subnets[i].rindex(".") + 1 #get the index of the subnet
        subnet = valid_subnets[i][subnet_index:] #Store the value of the start of the valid hosts for each subnet
        subnet = int(subnet) + 1 #increment by 1 to get the first value in the valid hosts
        first_addresses.append(valid_subnets[i][:subnet_index] + str(subnet)) #join the valid hosts to the original ip address and append these to the first_addresses list
        i += 1
    
    i = 0
    while i < len(broadcast_addresses):#Loop through the broadcast addresses
        broadcast_index = broadcast_addresses[i].rindex(".") + 1 #get the index of the broadcast
        broadcast = broadcast_addresses[i][broadcast_index:] #Store the value of the end of the valid hosts for each subnet
        broadcast = int(broadcast) -1 #decrement by 1 to get the last value in range of the valid hosts
        last_addresses.append(broadcast_addresses[i][:broadcast_index] + str(broadcast)) #join the valid hosts to the original ip address and append these to the first_addresses list
        i += 1

    print("First addresses: \n", first_addresses)
    print("Last addresses: \n", last_addresses)


get_subnet_stats("192.168.10.0","255.255.255.192") #Run part 2 and 3 code here. Part 3 can be run with: get_subnet_stats("172.16.0.0","255.255.192.0")

#part 4
#supernetting-combing multiple networks together
def get_supernet_stats(list_of_class_c):
    list_of_binary2 = [] #A list to store the network addresses in list_of_class_c when converted to binary strings
    for network in list_of_class_c: #loop through these networks
        list_of_binary = to_binary_string(network) #Use the helper function from above to convert to binary
        binary = "".join(list_of_binary) #Join the lists to strings
        list_of_binary2.append(binary) #Append to the new list_of_binary2 list

#Want to find the common prefix of all these network addresses. Loop through the strings to find out what is common
    i = 0
    j = 1
    counter = 0 # Once the loop hits a different value, that is the point where the common prefix ends and so "counter" will be that value
    while i < len(list_of_binary2[i]):
        if list_of_binary2[i][counter] == list_of_binary2[j][counter]:
            counter += 1
        else:
            break
    
    commmon_prefix = list_of_binary2[0][0:counter-1] #The common prefix

    common_prefix_list = [] # A list used to store the common prefix so that it can be overwritten with 1s and 0s(network and host bits)
    for bit in commmon_prefix:
        common_prefix_list.append("1") #Get the common prefix to represent the network bits (1s)
    print("\n" + "Address: " + list_of_class_c[0] + "/" + str(len(common_prefix_list))) #The length of the common prefix is the network bits
    
    
    #common_prefix_list.append(list_of_binary2[0][counter-1:]) #append the rest of the binary network address to the list
    length_of_rest_of_network_address = len(list_of_binary2[0][counter-1:])
    for i in range(0, length_of_rest_of_network_address, 1):
        common_prefix_list.append("0") #Append "0" for the amount left in the network address
    network_mask = "".join(common_prefix_list)
    
    
    #Convert network mask to decimal
    network_mask_list = [] # A list used to store the network mask in four strings in order to use the helper function "to_decimal_dot"
    network_mask_list.append(network_mask[0:8]) #Get the first 8 bits
    network_mask_list.append(network_mask[8:16]) #2nd 8 bits
    network_mask_list.append(network_mask[16:24]) # 3rd 8 bits
    network_mask_list.append(network_mask[24:]) #4th 8 bits
    #Append the divided up bits into the list
    
    print("Network Mask:", to_decimal_dot(network_mask_list)) #Use the helper function from above to convert the network mask back out to decimal


get_supernet_stats(["205.100.0.0","205.100.1.0","205.100.2.0","205.100.3.0"]) #Run part 4 code here