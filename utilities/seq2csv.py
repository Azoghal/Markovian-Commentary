import argparse
import os

FILE_CHUNK_SIZE = 800
MAX_EXPECTED_STARTS = 10
start_words = set([f"START{i}" for i in range(MAX_EXPECTED_STARTS)])

def find_number_of_starts(fname:str)->int:
    with open(fname) as f:
        seqs = f.read(FILE_CHUNK_SIZE)
        seq = seqs.split(" ")
        count = 0
        for word in seq:
            if word in start_words: 
                count +=1
            else:
                break
        return count
    
def print_seqs(seqs):
    for seq in seqs:
        print(seq)
    print()

def sequential_file_clean(fname:str)->None:
    n_starts:int = find_number_of_starts(fname)
    print(f"{fname} has {n_starts} start words")
    with open(fname) as f:
        chunk = "x"
        last_seq = ""
        while(chunk!=""):
            chunk = f.read(FILE_CHUNK_SIZE)
            seqs = chunk.split('END')
            # put the first with the last of the last before resolving
            seqs[0] = last_seq + seqs[0]
            print_seqs(seqs)
        last_seq = seqs[-1]

def clean_seq_file(fname:str) -> None:
    fsize:int = os.path.getsize(fname)
    print(f"Size of {fname}: {fsize}.",end="")
    if fsize > FILE_CHUNK_SIZE:
        print(f"Reading file, >1 chunk")
    else:
        print(f"Reading file, 1 chunk")
    sequential_file_clean(fname)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #TODO make mutually exclusive file path and file list path to control if cleaning more than one file at once
    parser.add_argument('-f', '--file-path',type=str)
    parser.add_argument('-l', '--is-list',action="store_true")
    args = parser.parse_args()

    file_list = [args.file_path]
    if args.is_list:
        with open(args.file_path) as f:
            file_list = f.read().splitlines()
    
    for seq_file in file_list:
        clean_seq_file(seq_file)

    print(f"Turning sequence file {args.file_path} to a nice csv")