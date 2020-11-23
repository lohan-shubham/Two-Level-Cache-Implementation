# 2–Level Cache Implementation
## Working of Code:
In my code I’m using Cache of 2 Level. Cache implementation is completely based on
the principle of exclusion policy.
#### How Cache Data is stored:
All the Data of cache is stored in List.
#### Detail working of code:
When an address is entered to Read/Write a block
Then there are two cases arises
1. Data is present in the cache
2. Data is not present in the cache
* If Data is present in the cache:
    1. If Data is present in the L1: then it prints cache hit and also print the entire data
    of cache memory
    2. If data is present in L2: Because I’m using exclusion policy, the data present in L2
shift to L1. then it prints cache hit and also print the entire data of cache
memory
* If Data is not present in the cache:
    then the data is load to L1 cache memory and print cache miss and the entire data of
    cache memory.
