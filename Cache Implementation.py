import math

global cache_size,block_size,L1_cache_lines,block_offset_bit
global L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines
global address_len
L1_Data=[]
L1_words_data=[]
L2_Data=[]
L2_words_Data=[]


def print_cache():
    global L1_cache_lines,block_size,L1_words_data,L1_Data,L2_Data,L2_words_Data,L2_cache_lines
    print('-------------------------L1 Cache-------------------------------')
    for i in range(L1_cache_lines):
        print(i,L1_Data[i],end="\t")
        for j in range(block_size):
            print(L1_words_data[i*block_size+j],end=" ")
        print()
    print()
    print('-------------------------L2 Cache-------------------------------')
    for i in range(L2_cache_lines):
        print(i,L2_Data[i],end="\t")
        for j in range(block_size):
            print(L2_words_Data[i*block_size+j],end=" ")
        print()


def cache_initialisation():
    global L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines,L1_cache_lines
    # print()
    for i in range(L1_cache_lines):
        L1_Data.append("none")
    for j in range(block_size*L1_cache_lines):
        L1_words_data.append("null")

    for i in range(L2_cache_lines):
        L2_Data.append("none")
    for j in range(block_size*L2_cache_lines):
        L2_words_Data.append("null")


def Direct_Mapping(address,operation):
    global block_offset_bit,L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines
    block_no=int(address[:-block_offset_bit],2)
    word_no=int(address[-block_offset_bit:],2)
    L1_locator=int(block_no%L1_cache_lines)
    if (operation=='1'):  # read
        if (block_no in L1_Data):
            print("cache hit")
        elif (block_no in L2_Data):
            L2_locator=int(block_no%L2_cache_lines)
            print("cache hit")
            temp_data=[block_no]  # pick data from L2
            for i in range(len(L2_Data)):
                if (L2_Data[i]==block_no):
                    L2_Data[i]="none"
                    for j in range(block_size):
                        temp_data.append(L2_words_Data[i*block_size+j])
                        L2_words_Data[i*block_size+j]="null"
                    break
            # loading data from L2 to L1
            L1_full=True
            if (L1_Data[L1_locator]=="none"):
                L1_Data[L1_locator]=temp_data[0]
                L1_full=False
                for i in range(block_size):
                    L1_words_data[i+block_size*L1_locator]=temp_data[i+1]

            # if L1 is full then dumping data of L1 to L2
            if (L1_full):
                L1_temp_data=[L1_Data[L1_locator]]
                for i in range(block_size):
                    L1_temp_data.append(L1_words_data[L1_locator*block_size+i])

                L2_full=True

                if (L2_Data[L2_locator]=="none"):
                    L2_Data[L2_locator]=L1_temp_data[0]
                    L2_full=False
                    for j in range(block_size):
                        L2_words_Data[L2_locator*block_size+j]=L1_temp_data[j+1]
                if (L2_full):
                    replaced_data=[L2_Data[L2_locator]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[L2_locator*block_size+i])
                        L2_words_Data[L2_locator*block_size+i]="null"
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[L2_locator]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]
                L1_Data[L1_locator]=temp_data[0]
                for i in range(block_size):
                    L1_words_data[L1_locator*block_size+i]=temp_data[i+1]
        elif (block_no not in L1_Data and block_no not in L2_Data):
            print("Cache Miss")
            temp_data=[L1_Data[L1_locator]]+[L1_words_data[L1_locator*block_size+i] for i in range(block_size)]
            # print(temp_data,type(temp_data[0]))
            L1_full=True
            if (L1_Data[L1_locator]=="none"):
                L1_Data[L1_locator]=block_no
                L1_full=False
            if (L1_full):
                L2_locator=temp_data[0]%L2_cache_lines
                for i in range(block_size):
                    L1_words_data[i+L1_locator*block_size]="null"
                L2_full=True
                if (L2_Data[L2_locator]=='none'):
                    L2_Data[L2_locator]=temp_data[0]
                    L2_full=False
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]
                L1_Data[L1_locator]=block_no
                if (L2_full):
                    replaced_data=[L2_Data[L2_locator]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[L2_locator*block_size+i])
                        L2_words_Data[L2_locator*block_size+i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[L2_locator]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]

    if operation=='2':  # write
        d=input("Enter Data\t")
        if (block_no in L1_Data):
            print("cache hit")
            L1_words_data[L1_locator*block_size+word_no]=d
        elif (block_no in L2_Data):
            print("cache hit")
            temp_data=[block_no]  # pick data from L2
            for i in range(len(L2_Data)):
                if (L2_Data[i]==block_no):
                    L2_Data[i]="none"
                    L2_words_Data[i*block_size+word_no]=d
                    for j in range(block_size):
                        temp_data.append(L2_words_Data[i*block_size+j])
                        L2_words_Data[i*block_size+j]="null"
                    break
            # loading data from L2 to L1
            L1_full=True
            if (L1_Data[L1_locator]=="none"):
                L1_Data[L1_locator]=temp_data[0]
                L1_full=False
                for i in range(block_size):
                    L1_words_data[i+block_size*L1_locator]=temp_data[i+1]

            # if L1 is full then dumping data of L1 to L2
            if (L1_full):
                L1_temp_data=[L1_Data[L1_locator]]
                for i in range(block_size):
                    L1_temp_data.append(L1_words_data[L1_locator*block_size+i])
                    L1_words_data[L1_locator*block_size+i]="null"
                L2_full=True

                if (L2_Data[L2_locator]=="none"):
                    L2_Data[L2_locator]=L1_temp_data[0]
                    L2_full=False
                    for j in range(block_size):
                        L2_words_Data[i*block_size+L2_locator]=L1_temp_data[j+1]
                if (L2_full):
                    replaced_data=[L2_Data[L2_locator]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[L2_locator*block_size+i])
                        L2_words_Data[L2_locator*block_size+i]="null"

                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[L2_locator]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]
                L1_Data[L1_locator]=temp_data[0]
                for i in range(block_size):
                    L1_words_data[L1_locator*block_size+i]=temp_data[i+1]
        elif (block_no not in L1_data and block_no not in L2_Data):
            print("Cache Miss")
            temp_data=[L1_Data[L1_locator]]+[L1_words_data[L1_locator*block_size+i] for i in range(block_size)]
            L1_full=True
            if (L1_Data[L1_locator]=="none"):
                L1_Data[L1_locator]=block_no
                L1_words_data[L1_locator*block_size+word_no]=d
                L1_full=False

            if (L1_full):
                L2_locator=temp_data[0]%L2_cache_lines
                for i in range(block_size):
                    L1_words_data[i+L1_locator*block_size]="null"
                L2_full=True
                if (L2_Data[L2_locator]=='none'):
                    L2_Data[L2_locator]=temp_data[0]
                    L2_full=False
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]
                L1_Data[L1_locator]=block_no
                L1_words_data[L1_locator*block_size+word_no]=d
                if (L2_full):
                    replaced_data=[L2_Data[L2_locator]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[L2_locator*block_size+i])
                        L2_words_Data[L2_locator*block_size+i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[L2_locator]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[L2_locator*block_size+i]=temp_data[i+1]

    print_cache()


def isBinary(num):
    if (len(num)<1):
        return False
    Binary_Digits=['0','1']
    for i in str(num):
        if i not in Binary_Digits:
            return False
    return True


def Associative_Mapping(address,operation):
    global block_offset_bit,L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines
    block_no=int(address[:-block_offset_bit],2)
    word_no=int(address[-block_offset_bit:],2)
    if (operation=='1'):  # read
        if (block_no in L1_Data):
            print("cache hit")
        elif (block_no in L2_Data):
            print("cache hit")
            temp_data=[block_no]  # pick data from L2
            for i in range(len(L2_Data)):
                if (L2_Data[i]==block_no):
                    L2_Data[i]="none"
                    for j in range(block_size):
                        temp_data.append(L2_words_Data[i*block_size+j])
                        L2_words_Data[i*block_size+j]="null"
                    break
            # loading data from L2 to L1
            L1_full=True
            for i in range(len(L1_Data)):
                if (L1_Data[i]=="none"):
                    L1_Data[i]=temp_data[0]
                    L1_full=False
                    for j in range(block_size):
                        L1_words_data[i*block_size+j]=temp_data[j+1]
                    break
            # if L1 is full then dumping data of L1 to L2
            if (L1_full):
                L1_temp_data=[L1_Data[0]]
                for i in range(block_size):
                    L1_temp_data.append(L1_words_data[i])
                L2_full=True
                for i in range(len(L2_Data)):
                    if (L2_Data[i]=="none"):
                        L2_Data[i]=L1_temp_data[0]
                        L2_full=False
                        for j in range(block_size):
                            L2_words_Data[i*block_size+j]=L1_temp_data[j+1]
                        break
                if (L2_full):
                    replaced_data=[L2_Data[0]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[i])
                        L2_words_Data[i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[0]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[i]=temp_data[i+1]
                L1_Data[0]=temp_data[0]
                for i in range(block_size):
                    L1_words_data[i]=temp_data[i+1]
        elif (block_no not in L1_Data and block_no not in L2_Data):
            print("Cache Miss")
            temp_data=[L1_Data[0]]+[L1_words_data[i] for i in range(block_size)]
            L1_full=True
            for i in range(len(L1_Data)):
                if (L1_Data[i]=="none"):
                    L1_Data[i]=block_no
                    L1_full=False
                    break
            if (L1_full):
                L2_full=True
                for i in range(len(L2_Data)):
                    if (L2_Data[i]=='none'):
                        L2_Data[i]=temp_data[0]
                        L2_full=False
                        for j in range(block_size):
                            L2_words_Data[i*block_size+j]=temp_data[j+1]
                        break
                L1_Data[0]=block_no
                if (L2_full):
                    replaced_data=[L2_Data[0]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[i])
                        L2_words_Data[i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[0]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[i]=temp_data[i+1]

    if operation=='2':  # write
        d=input("Enter Data\t")
        if (block_no in L1_Data):
            print("cache hit")
            for i in range(len(L1_Data)):
                if (L1_Data[i]==block_no):
                    L1_words_data[i*block_size+word_no]=d
                    break

        elif (block_no in L2_Data):
            print("cache hit")
            temp_data=[block_no]  # pick data from L2
            for i in range(len(L2_Data)):
                if (L2_Data[i]==block_no):
                    L2_words_Data[i*block_size+word_no]=d
                    L2_Data[i]="none"
                    for j in range(block_size):
                        temp_data.append(L2_words_Data[i*block_size+j])
                        L2_words_Data[i*block_size+j]="null"
                    break
            # loading data from L2 to L1
            L1_full=True
            for i in range(len(L1_Data)):
                if (L1_Data[i]=="none"):
                    L1_Data[i]=temp_data[0]
                    L1_full=False
                    for j in range(block_size):
                        L1_words_data[i*block_size+j]=temp_data[j+1]
                    break
            # if L1 is full then dumping data of L1 to L2
            if (L1_full):
                L1_temp_data=[L1_Data[0]]
                for i in range(block_size):
                    L1_temp_data.append(L1_words_data[i])
                L2_full=True
                for i in range(len(L2_Data)):
                    if (L2_Data[i]=="none"):
                        L2_Data[i]=L1_temp_data[0]
                        L2_full=False
                        for j in range(block_size):
                            L2_words_Data[i*block_size+j]=L1_temp_data[j+1]
                        break
                if (L2_full):
                    replaced_data=[L2_Data[0]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[i])
                        L2_words_Data[i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[0]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[i]=temp_data[i+1]
                L1_Data[0]=temp_data[0]
                for i in range(block_size):
                    L1_words_data[i]=temp_data[i+1]
        elif (block_no not in L1_Data and block_no not in L2_Data):
            print("Cache Miss")
            temp_data=[L1_Data[0]]+[L1_words_data[i] for i in range(block_size)]
            L1_full=True
            for i in range(len(L1_Data)):
                if (L1_Data[i]=="none"):
                    L1_Data[i]=block_no
                    L1_words_data[i*block_size+word_no]=d
                    L1_full=False
                    break
            if (L1_full):
                L1_Data[0]="none"
                for i in range(block_size):
                    L1_words_data[i]="null"
                L2_full=True
                for i in range(len(L2_Data)):
                    if (L2_Data[i]=='none'):
                        L2_Data[i]=temp_data[0]
                        L2_full=False
                        for j in range(block_size):
                            L2_words_Data[i*block_size+j]=temp_data[j+1]
                        break
                L1_Data[0]=block_no
                L1_words_data[word_no]=d
                if (L2_full):
                    replaced_data=[L2_Data[0]]
                    for i in range(block_size):
                        replaced_data.append(L2_words_Data[i])
                        L2_words_Data[i]='null'
                    print("Data is replaced with",end="  ")
                    print(replaced_data)
                    L2_Data[0]=temp_data[0]
                    for i in range(block_size):
                        L2_words_Data[i]=temp_data[i+1]

    print_cache()


def k_way_Asso_Mapping(address,operation,k):
    global block_offset_bit,L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines
    L1_set=L1_cache_lines//k
    L2_set=L2_cache_lines//k
    if L2_set==0:
        Associative_Mapping(address,operation)
    elif L2_set!=0:
        block_no=int(address[:-block_offset_bit],2)
        word_no=int(address[-block_offset_bit:],2)
        L1_locator=0
        L1_size=len(L1_Data)
        if (L1_set!=0):
            L1_locator=int(block_no%L1_set)
            L1_size=k
        x=L1_locator*L1_size
        L1=L1_Data[x:x+L1_size]
        if (operation=='1'):  # read
            if (block_no in L1):
                print("cache hit")
            elif (block_no in L2_Data):
                print("cache hit")
                temp_data=[block_no]  # pick data from L2
                for i in range(len(L2_Data)):
                    if (L2_Data[i]==block_no):
                        L2_Data[i]="none"
                        for j in range(block_size):
                            temp_data.append(L2_words_Data[i*block_size+j])
                            L2_words_Data[i*block_size+j]="null"
                        break
                # loading data from L2 to L1
                L1_full=True
                for i in range(len(L1)):
                    if (L1[i]=="none"):
                        L1_Data[L1_locator*L1_size+i]=temp_data[0]
                        L1_full=False
                        for j in range(block_size):
                            L1_words_data[(L1_locator*L1_size+i)*block_size+j]=temp_data[j+1]
                        break
                # if L1 is full then dumping data of L1 to L2
                if (L1_full):
                    L1_temp_data=[L1_Data[L1_locator*L1_size]]
                    for i in range(block_size):
                        L1_temp_data.append(L1_words_data[(L1_locator*L1_size)*block_size+i])
                    L2_full=True

                    L2_locator=L1_temp_data[0]%L2_set
                    y=L2_locator*L2_set
                    L2=L2_Data[y:y+k]
                    for i in range(len(L2)):
                        if (L2[i]=="none"):
                            L2_Data[L2_locator*k+i]=L1_temp_data[0]
                            L2_full=False
                            for j in range(block_size):
                                L2_words_Data[(L2_locator*k+i)*block_size+j]=L1_temp_data[j+1]
                            break
                    if (L2_full):
                        replaced_data=[L2_Data[L2_locator*k]]
                        for i in range(block_size):
                            replaced_data.append(L2_words_Data[L2_locator*block_size*k+i])
                            L2_words_Data[L2_locator*block_size*k+i]='null'
                        print("Data is replaced with",end="  ")
                        print(replaced_data)
                        L2_Data[L2_locator*k]=L1_temp_data[0]
                        for i in range(block_size):
                            L2_words_Data[L2_locator*block_size*k+i]=L1_temp_data[i+1]
                    L1_Data[L1_locator*L1_size]=temp_data[0]
                    for i in range(block_size):
                        L1_words_data[(L1_locator*L1_size)*block_size+i]=temp_data[i+1]
            elif (block_no not in L1_Data and block_no not in L2_Data):
                print("Cache Miss")
                L1_temp_data=[L1_Data[L1_locator*L1_size]]+[L1_words_data[L1_locator*block_size*L1_size+i] for i in
                                                            range(block_size)]
                L1_full=True
                for i in range(len(L1)):
                    if (L1[i]=="none"):
                        L1_Data[i+L1_locator*k]=block_no
                        L1_full=False
                        break
                # print(L1_full)
                if (L1_full):
                    L2_locator=L1_temp_data[0]%L2_set
                    y=L2_locator*L2_set
                    L2=L2_Data[y:y+k]
                    L2_full=True
                    for i in range(len(L2)):
                        if (L2[i]=='none'):
                            L2_Data[i+L2_locator*k]=L1_temp_data[0]
                            L2_full=False
                            for j in range(block_size):
                                L2_words_Data[(i+L2_locator*k)*block_size+j]=L1_temp_data[j+1]
                            break
                    L1_Data[L1_locator*k]=block_no
                    if (L2_full):
                        replaced_data=[L2_Data[L2_locator*k]]
                        for i in range(block_size):
                            replaced_data.append(L2_words_Data[L2_locator*k*block_size+i])
                            L2_words_Data[L2_locator*k*block_size+i]='null'
                        print("Data is replaced with",end="  ")
                        print(replaced_data)
                        L2_Data[L2_locator*k]=L1_temp_data[0]
                        for i in range(block_size):
                            L2_words_Data[L2_locator*k*block_size+i]=L1_temp_data[i+1]

        if operation=='2':  # write
            d=input("Enter Data\t")
            if (block_no in L1):
                print("cache hit")
                for i in range(len((L1))):
                    if (L1[i]==block_no):
                        L1_Data[i+k*L1_locator]=block_no
                        L1_words_data[(i+k*L1_locator)*block_size+word_no]=d
            elif (block_no in L2_Data):
                print("cache hit")
                temp_data=[block_no]  # pick data from L2
                for i in range(len(L2_Data)):
                    if (L2_Data[i]==block_no):
                        L2_Data[i]="none"
                        L2_words_Data[i*block_size+word_no]=d
                        for j in range(block_size):
                            temp_data.append(L2_words_Data[i*block_size+j])
                            L2_words_Data[i*block_size+j]="null"
                        break
                # loading data from L2 to L1
                L1_full=True
                for i in range(len(L1)):
                    if (L1[i]=="none"):
                        L1_Data[L1_locator*L1_size+i]=temp_data[0]
                        L1_full=False
                        for j in range(block_size):
                            L1_words_data[(L1_locator*L1_size+i)*block_size+j]=temp_data[j+1]
                        break
                # if L1 is full then dumping data of L1 to L2
                if (L1_full):
                    L1_temp_data=[L1_Data[L1_locator*L1_size]]
                    for i in range(block_size):
                        L1_temp_data.append(L1_words_data[(L1_locator*L1_size)*block_size+i])
                    L2_full=True
                    L2_locator=L1_temp_data[0]%L2_set
                    y=L2_locator*L2_set
                    L2=L2_Data[y:y+k]
                    # print(L1_temp_data)
                    for i in range(len(L2)):
                        if (L2[i]=="none"):
                            L2_Data[L2_locator*k+i]=L1_temp_data[0]
                            L2_full=False
                            for j in range(block_size):
                                L2_words_Data[(L2_locator*k+i)*block_size+j]=L1_temp_data[j+1]
                            break
                    if (L2_full):
                        replaced_data=[L2_Data[L2_locator*k]]
                        for i in range(block_size):
                            replaced_data.append(L2_words_Data[L2_locator*block_size*k+i])
                            L2_words_Data[L2_locator*block_size*k+i]='null'
                        print("Data is replaced with",end="  ")
                        print(replaced_data)
                        L2_Data[L2_locator*k]=L1_temp_data[0]
                        for i in range(block_size):
                            L2_words_Data[L2_locator*block_size*k+i]=L1_temp_data[i+1]
                    L1_Data[L1_locator*L1_size]=temp_data[0]
                    for i in range(block_size):
                        L1_words_data[(L1_locator*L1_size)*block_size+i]=temp_data[i+1]
            elif (block_no not in L1_Data and block_no not in L2_Data):
                print("Cache Miss")
                L1_temp_data=[L1_Data[L1_locator*k]]+[L1_words_data[L1_locator*block_size*k+i] for i in
                                                      range(block_size)]

                L1_full=True
                for i in range(len(L1)):
                    if (L1[i]=="none"):
                        L1_Data[i+L1_locator*L1_size]=block_no
                        L1_words_data[(i+L1_locator*L1_size)*block_size+word_no]=d
                        L1_full=False
                        break
                if (L1_full):
                    for i in range(block_size):
                        L1_words_data[L1_locator*block_size*k+i]="null"
                    L2_locator=L1_temp_data[0]%L2_set
                    y=L2_locator*L2_set
                    L2=L2_Data[y:y+k]
                    L2_full=True
                    for i in range(len(L2)):
                        if (L2[i]=='none'):
                            L2_Data[i+L2_locator*k]=L1_temp_data[0]
                            L2_full=False
                            for j in range(block_size):
                                L2_words_Data[(i+L2_locator*k)*block_size+j]=L1_temp_data[j+1]
                            break
                    L1_Data[L1_locator*k]=block_no
                    L1_words_data[L1_locator*block_size*k+word_no]=d
                    if (L2_full):
                        replaced_data=[L2_Data[L2_locator*k]]
                        for i in range(block_size):
                            replaced_data.append(L2_words_Data[L2_locator*k*block_size+i])
                            L2_words_Data[L2_locator*k*block_size+i]='null'
                        print("Data is replaced with",end="  ")
                        print(replaced_data)
                        L2_Data[L2_locator*k]=L1_temp_data[0]
                        for i in range(block_size):
                            L2_words_Data[L2_locator*k*block_size+i]=L1_temp_data[i+1]

    print_cache()


def performer(cache_mapping,operation,address,k):
    if (cache_mapping=='1'):
        Direct_Mapping(address,operation)
    if (cache_mapping=='2'):
        Associative_Mapping(address,operation)
    if (cache_mapping=='3'):
        k_way_Asso_Mapping(address,operation,k)


def isPowerofTwo(x):
    return x>1 and (x&(x-1))==0


def main():
    global block_offset_bit,block_size,L1_words_data,L1_Data
    global L1_Data,L1_words_data,L2_Data,L2_words_Data,L2_cache_lines,L1_cache_lines
    print("----------------------Cache Implementation----------------------------------")
    L2_cache_size=int(input("Enter the cache size\t"))
    size_checker=True
    while (not isPowerofTwo(L2_cache_size)):
        print("Cache Size should be in power of 2")
        L2_cache_size=int(input("Re-enter the Cache size\t"))
    L1_cache_size=L2_cache_size//2
    block_size=int(input("Enter block size\t"))
    while (not isPowerofTwo(block_size)):
        print("block Size should be in power of 2")
        block_size=int(input("Re-enter the Block size\t"))
    while (L1_cache_size<block_size):
        print("Cache size should be greater than or equal to Block size")
        print("Program terminating!!!\nRun again")
        size_checker=False
        break
    if (size_checker):
        L2_cache_lines=L2_cache_size//block_size
        L1_cache_lines=L2_cache_lines//2
        cache_initialisation()
        block_offset_bit=int(math.log2(block_size))
        cache_mapping=(
            input("Enter the Cache Mode\n1.Direct Mapping\n2.Associative Mapping\n3.K-way Associative Mapping\n"))
        k='0'
        if cache_mapping=='3':
            k=int(input("Enter value of K\t"))
            while (not isPowerofTwo(k)):
                k=int(input("Enter value of k\t"))

        while (cache_mapping not in ['1','2','3']):
            print("Enter Correct input")
            cache_mapping=(
                input(
                    "Enter the cache Mode\n1.Direct Mapping\n2.Associative Mapping\n3.K-way Associative Mapping\n"))
            if cache_mapping=='3':
                k=int(input("Enter value of K\t"))
                while (not isPowerofTwo(k)):
                    k=int(input("Enter value of k\t"))

        counter=0
        flag=True
        while (flag):
            address=input("Enter address\t")
            while (len(address)<=block_size or not isBinary(address)):
                address=input("Enter correct address (should be greater than block offset bit and in Binary no)\t")
            if (counter==0):
                global address_len
                address_len=len(address)
                counter=1
            if counter>0:
                while (address_len!=len(address) or not isBinary(address)):
                    address=input("Enter address of length "+str(address_len)+" and should be in Binary no\t")
            print("Enter operation")
            operation=input("1.Read\n2.Write\n")
            while (operation not in ['1','2']):
                print("Enter correct option no")
                operation=input("1.Read\n2.Write\n")

            performer(cache_mapping,operation,address,k)
            option=input("Want to perform more operation?\nEnter 0\t")
            if (option=='0'):
                flag=True
            else:
                flag=False


main()
