from hashlib import sha256
from datetime import datetime

def updatehash(*args) :
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Block():
    data = None
    previous_hash = "0"*64
    nonce = 0
    _hash = None
    timestamp = 0

    def __init__ (self, data, number, timestamp) :
        self.data = data 
        self.number = number
        self.timestamp = timestamp
        self._hash = self.calculate_hash()
        
    

    def calculate_hash (self) :
        return updatehash(self.previous_hash, 
                          self.data, self.number, 
                          self.nonce, 
                          self.timestamp)
    
    def __str__ (self) :
        return ("Block#: %s\nHash: %s\nPrevious Hash: %s\nData: %s\nNonce: %s\nTimestamp: %s" 
                %(self.number, self._hash, self.previous_hash, self.data, self.nonce, self.timestamp))
    

class Blockchain:
    difficulty = 4
    def __init__(self,  chain=[]):
        self.chain = chain
    def addblock (self, block) :
        self.chain.append(block)
    pass 
    
    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1]._hash
        except IndexError:
            pass
        
        while True:
            block._hash = block.calculate_hash()
            if block.calculate_hash() [:self.difficulty] == "0"*self.difficulty :
                self.addblock(block) ; break
       
            else:
             block.nonce += 1
    def isValid(self):
        for i in range (1, len(self.chain)):
            _previous = self.chain[i-1]
            _current = self.chain[i]
            if _previous._hash != _current.previous_hash: 
                return False
            if _current._hash != _current.calculate_hash():
                return False
            if _current.calculate_hash()[:self.difficulty] != "0"*self.difficulty:
                return False
            
        return True


def main():
 blockchain = Blockchain()
 database = ["My", "Name", "is", "Rishit"]

 num = 0
 for data in database:
       num +=1
       blockchain.mine(Block(data, num, datetime.now().timestamp()))
       print(blockchain.chain)
       for block in blockchain.chain:
           print (block)
          
       print(blockchain.isValid())
       
 blockchain.chain[2].data = "HACKED"
 for block in blockchain.chain:
     print(block)
 print(blockchain.isValid())

if __name__ == '__main__':
    main()
