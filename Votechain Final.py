from hashlib import sha256
from datetime import datetime, timedelta
import csv

def updatehash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Block:
    def __init__(self, data, number, timestamp, previous_hash="0"*64, nonce=0):
        self.data = data 
        self.number = number
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self._hash = self.calculate_hash()

    def calculate_hash(self):
        return updatehash(self.previous_hash, self.data, self.number, self.nonce, self.timestamp)
    
    def __str__(self):
        return ("Block#: %s\nHash: %s\nPrevious Hash: %s\nData: %s\nNonce: %s\nTimestamp: %s" 
                % (self.number, self._hash, self.previous_hash, self.data, self.nonce, self.timestamp))
    
class Blockchain:
    difficulty = 4
    
    def __init__(self, chain=[]):
        self.chain = chain
        self.genesis_block()  
    
    def addblock(self, block):
        self.chain.append(block)
    
    def genesis_block(self):
        genesis_block = Block("Genesis Block", 0, datetime.now().timestamp())
        self.mine(genesis_block)
        
    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1]._hash
        except IndexError:
            pass
        
        while True:
            block._hash = block.calculate_hash()
            if block._hash[:self.difficulty] == "0" * self.difficulty:
                self.addblock(block)
                break
            else:
                block.nonce += 1

    def create_vote(self, voter_id, voted_for, index):
        voter_block = Block(f"{voter_id}-{voted_for}", index, datetime.now().timestamp())
        self.mine(voter_block)
        
    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i - 1]
            _current = self.chain[i]
            
            if _previous._hash != _current.previous_hash:
                return False
            if _current._hash != _current.calculate_hash():
                return False
            if _current._hash[:self.difficulty] != "0" * self.difficulty:
                return False
        return True

class Voting:
    def __init__(self, timestamp, voter_id, candidate_id, candidate_name=None):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.timestamp = timestamp

class Candidate:
    def __init__(self, candidate_id, candidate_name, vote_count):
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.vote_count = vote_count
    
    def add_vote(self):
        self.vote_count += 1

    def __repr__(self):
        return f"Candidate({self.candidate_id}, {self.candidate_name}, {self.vote_count})"

def cast_vote(candidate_id, registered_candidates, candidates_dict):        #this is the primary method used to cast votes
    candidate_id = int(candidate_id)
    if candidate_id in registered_candidates:
        candidates_dict[candidate_id].add_vote()
        print(f"Vote casted for {candidates_dict[candidate_id].candidate_name}")
    else:
        print("Invalid candidate ID.")

def declare_winner(candidates_dict):                                        # accesses candidate objects from dictionary to check who has max votes
    winner = None
    max_votes = -1
    for candidate in candidates_dict.values():
        if candidate.vote_count > max_votes:
            max_votes = candidate.vote_count
            winner = candidate
    return winner

def main():
    voters_set = []                                             # to maintain a list of voters who have already voted
  
    candidate1 = Candidate(439, "Rishit Kesharwani", 0)         #we now define 4 candidate objects, which are also present in the CSV file
    candidate2 = Candidate(348, "Ojas Goel", 0)                 #the purpose of explicitly defining these objects is to keep track of vote counts
    candidate3 = Candidate(688, "Dhruvi Desai", 0)              #and access other important information easily
    candidate4 = Candidate(739, "Siddharth Mungee", 0)


    candidates_dict = {                                          #the candidate objects are stored in this dictionary
        candidate1.candidate_id: candidate1,
        candidate2.candidate_id: candidate2,
        candidate3.candidate_id: candidate3,
        candidate4.candidate_id: candidate4,
    }

    voting_deadline = datetime.now() + timedelta(days=1)        # this is defined in addition to admin access to end voting
                                                                # if admin does not end voting explicitly, the while loop 
                                                                # for voting runs till the deadline mentioned here, i.e. 1 day
                                                          
    blockchain = Blockchain()                                   #blockchain declaration that will store voting data in the blocks

    #fetching the voter data from CSV file and adding them to a list
    registered_voters = []
    registered_voterpasswords = []
    with open('Registered Voters.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            registered_voters.append(row[0])
            registered_voterpasswords.append(row[2])

    #fetching the candidate data from CSV file and adding them to a list
    registered_candidates = []
    with open('Registered Candidates.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            registered_candidates.append(int(row[0]))

    end_voting = False

    # Our main while loop that simulates the voting process

    while (datetime.now() <= voting_deadline) and not end_voting:
        inputvoter_id = input("Enter your voter id: ")
        
        if inputvoter_id in registered_voters and inputvoter_id not in voters_set:                    #verifying if voter is authentic and has not already voted
            voter_index = registered_voters.index(inputvoter_id)
            password = input("Enter password: ")
            if password == registered_voterpasswords[voter_index]:                                    #verifying password
                print("\nAuthentication successful. You may proceed to vote.\n")
                inputcandidate_id = input("Enter the ID of the candidate you want to cast your vote for: ")
                cast_vote(inputcandidate_id, registered_candidates, candidates_dict)
                voters_set.append(inputvoter_id)
                new_vote = Voting(datetime.now().timestamp(), inputvoter_id, inputcandidate_id)       #creates vote info as objects in the Voting class
                blockchain.create_vote(inputvoter_id, inputcandidate_id, len(blockchain.chain) + 1)
                displayvote = input("Check vote status? Enter YES or NO \n")
                if displayvote == "YES":
                    print(new_vote.voter_id, "casted vote for", new_vote.candidate_id, "at", new_vote.timestamp)
                    print("Vote status validity:", blockchain.isValid())                               #uses isValid() method to verify blockchain validity
                elif displayvote == "NO":
                    print("Thank you for voting!")
                else:
                    print("Error, please enter YES or NO")
                continue
            else:
                print("Incorrect password")
            
        
        elif inputvoter_id in voters_set:
            print("Vote already casted\n")
           
        
        # Administrator access code
        # Can perform actions to check voting statistics, candidate-wise count, blockchain details, and winner declaration
        elif inputvoter_id == "admin1234":
            password = input("Enter administrator password: ")
            if password == "30062005":
             
             print("\n\nWelcome administrator!")
             while (True):
            
                operation = input("\n\nEnter the number to select action: \n1. Check voting statistics \n2. Check candidate-wise vote count \n3. Show blockchain vote transactions \n4. End voting and declare winner \n5. Log out \n")
                if operation == "1":
                    print("Total votes casted: " + str(sum(candidate.vote_count for candidate in candidates_dict.values()))) # Minor Change
                elif operation == "2":
                    for candidate in candidates_dict.values():
                        print(f"{candidate.candidate_id} {candidate.candidate_name} Total votes: {candidate.vote_count}\n")
                elif operation == "3":
                    for block in blockchain.chain:
                        print(block)
                elif operation == "5":
                    break
                elif operation == "4":
                    end_voting = True
                    print("The winner of the election is " + str(declare_winner(candidates_dict).candidate_name))
                    break
                
                else:
                    print("Invalid action number")
            else:
                print("Incorrect password")
        else:
            print("Invalid voter_id, make sure ID is in the form 23bxxxx")

if __name__ == '__main__':
    main()