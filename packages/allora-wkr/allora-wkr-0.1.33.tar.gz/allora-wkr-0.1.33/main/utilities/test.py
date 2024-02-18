import os


# Get the directory of the current file (utils.py)
current_file_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(current_file_dir)
allora_chain_dir = os.path.join(main_dir, 'allora-chain')

# Now allora_chain_dir points to '/main/allora-chain'
print(allora_chain_dir)  # Just for verification, you can remove this line

# Your function logic here
