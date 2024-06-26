# Votechain-SoCProject
**Introduction**

I really loved the fundamental breakdown of Blockchain by Daniel Drescher in his book, which I'll be expanding upon here. Daniel presents the formal definition in this sentence:

_"The blockchain is a purely distributed peer-to-peer system of ledgers that utilizes a software unit that consists of an algorithm, which negotiates the informational content of ordered and connected blocks of data together with cryptographic and security technologies in order to achieve and maintain its integrity."_ 


**Anatomy of a Block**

The simplest description of blockchain involves nodes, or blocks, interconnected with each other. In this sense, let us now see the anatomy of a block in a blockchain. The figure above provides a good description of how the information mechanism works in blockchain. Every block has certain elements that contribute to the principles of blockchain as we know them. Let us see the applications of each of them below:

**1. Header**: It is used to identify the particular block in the entire blockchain. It handles all blocks in the blockchain. A block header is hashed periodically by miners by changing the nonce value as part of normal mining activity, also Three sets of block metadata are contained in the block header.

**2. Previous Block Address/ Hash**: It is used to connect the i+1th block to the ith block using the hash. In short, it is a reference to the hash of the previous (parent) block in the chain.

**3. Timestamp**: It is a system that verifies the data into the block and assigns a time or date of creation for digital documents. The timestamp is a string of characters that uniquely identifies the document or event and indicates when it was created.

**4. Nonce**: A nonce is a number which is used only once. It is a central part of the proof of work in the block. It is compared to the live target if it is smaller or equal to the current target. People who mine, test, and eliminate many Nonce per second until they find that valuable Nonce is valid.

**5. Merkle Root**: It is a type of data structure frame of different blocks of data. A Merkle Tree stores all the transactions in a block by producing a digital fingerprint of the entire transaction. It allows the users to verify whether a transaction can be included in a block or not.

**Mining**

As the entire network is widely distributed, every miner in the network is expected to receive multiple messages from multiple vendors at any given period of time. What the miner does is combine these messages in a single block. This is illustrated in image −

<img width="320" alt="image" src="https://github.com/nexus3006/Votechain-SoCProject/assets/148470464/a62f2cfd-b22d-4f58-91db-1d1a2741fbb9">

After a block of messages is formed, the miner creates a hash on the block using the hashing function described earlier. Now, as you know if any third party modifies the contents of this block, its hash will become invalid. Incidentally, each message is time-stamped so that nobody can modify its chronological order without affecting the block’s hash value. Thus, the messages in the block are perfectly secured from tampering.


 **Connecting the blocks**
 
 The following diagram shows how the elements of a block interact with each other in a network of blocks:

 <img width="614" alt="image" src="https://github.com/nexus3006/Votechain-SoCProject/assets/148470464/4c0cc5f0-71dc-468b-9558-7030b3b81507">

 For this project, we will focus on three different classes in Python that will essentially form the skeleton of the system:

- Blockchain Class: We'll consider the blockchain as a linked list where each block points to the previous one.
- Block Class: Each block contains critical information like data, timestamps, nonce, and hashes.
- Vote Class: It handles the creation, encryption, verification, and storage of individual votes in the VoteChain system.
