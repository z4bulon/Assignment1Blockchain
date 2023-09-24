import hashlib
import time
import copy

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree()

    def build_tree(self):
        if not self.transactions:
            return None

        if len(self.transactions) == 1:
            return hashlib.sha256(self.transactions[0].encode()).hexdigest()

        mid = len(self.transactions) // 2
        left_tree = MerkleTree(self.transactions[:mid])
        right_tree = MerkleTree(self.transactions[mid:])

        return hashlib.sha256((left_tree.root + right_tree.root).encode()).hexdigest()

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        merkle_tree = MerkleTree(self.transactions)
        return merkle_tree.root

    def calculate_hash(self):
        data = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.merkle_root)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.branches = {"master": [self.create_genesis_block()]}
        self.current_branch = "master"
        self.index = 0

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [])

    def get_latest_block(self):
        return self.branches[self.current_branch][-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = int(time.time())
        new_block = Block(new_index, previous_block.hash, new_timestamp, transactions)
        self.branches[self.current_branch].append(new_block)
        self.index = new_index

    def switch_branch(self, branch_name):
        if branch_name not in self.branches:
            self.branches[branch_name] = copy.deepcopy(self.branches[self.current_branch])
        self.current_branch = branch_name

    def validate_block(self, block):
        previous_block = self.get_latest_block()

        if block.index != previous_block.index + 1:
            return False

        if block.previous_hash != previous_block.hash:
            return False

        if block.calculate_hash() != block.hash:
            return False

        merkle_tree = MerkleTree(block.transactions)
        if block.merkle_root != merkle_tree.root:
            return False

        return True

    def is_valid_chain(self):
        for i in range(1, len(self.branches[self.current_branch])):
            if not self.validate_block(self.branches[self.current_branch][i]):
                return False

        return True

def main():
    my_blockchain = Blockchain()

    while True:
        print("\nBlockchain Menu:")
        print("1. Add a Block")
        print("2. Print Blockchain")
        print("3. Validate Blockchain")
        print("4. Switch Branch")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            transactions = input("Enter transactions (comma-separated): ").split(",")
            my_blockchain.add_block(transactions)
            print("Block added to the blockchain.")

        elif choice == "2":
            for block in my_blockchain.branches[my_blockchain.current_branch]:
                print(f"Block #{block.index}")
                print(f"Timestamp: {block.timestamp}")
                print("Transactions:")
                for transaction in block.transactions:
                    print(f"  {transaction}")
                print(f"Merkle Root: {block.merkle_root}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Hash: {block.hash}")
                print()

        elif choice == "3":
            if my_blockchain.is_valid_chain():
                print("Blockchain is valid.")
            else:
                print("Blockchain is NOT valid.")

        elif choice == "4":
            branch_name = input("Enter branch name: ")
            my_blockchain.switch_branch(branch_name)
            print(f"Switched to branch: {branch_name}")

        elif choice == "5":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
