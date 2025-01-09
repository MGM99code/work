#write the python code to identify number of 'N's and '-' in a fasta file. 

#Secondly if you see a fasta sequence with continuous N regions, 
#Identify the starting and end position of those N regions in the sequence.

'''
IF file is FASTA:
    FOR each sequence:
        CALCULATE length    
        IDENTIFY 'N' start/end positions and count
        COUNT '-' characters
        EXTRACT label and sequence
        WRITE results to output file
ELSE:
    PRINT error

    
'''
# Function to check if the file is in FASTA format
def is_fasta(lines):
    # If the first line does not start with '>', it’s not FASTA format
    if not lines or not lines[0].startswith('>'):
        return False
    return True

# Function to calculate the length of the sequence
def seq_length(seq):
    seq_length = len(seq)
    return seq_length

# Function to identify regions of consecutive 'N's in the sequence
def process_n_regions(seq):
    n_regions = [] # List to store start/end positions of 'N' regions
    start = None   # Keep track of the start of 'N' regions
    n_count = 0    # Counter for total 'N' characters

    # Iterate through each character in the sequence
    for i in range(len(seq)):
        char = seq[i]
        if char == 'N':
            n_count += 1   # Increase 'N' count
            if start is None:
                start = i  # Mark the start of a new 'N' region
        else:
            if start is not None:
                n_regions.append((start + 1, i))  # Add region to the list
                start = None   # Reset the start for the next 'N' region
    
    # If the sequence ends with an 'N', add the last region
    if start is not None:
        n_regions.append((start + 1, len(seq)))

    return n_regions, n_count  # Return both regions and total 'N' count

# Function to count the number of '-' characters in the sequence
def process_dash_regions(sequence):
    dash_count = sequence.count('-')  # Count the dashes
    return dash_count

# Main function to process the FASTA file and generate the output
def process_fasta(input_filename, output_filename):
        
    try:
        # Open the input file and read its content
        with open(input_filename, 'r') as file:
            file_content = file.readlines()

        #print('filecontent', file_content)

        #check if file is in fasta format
        if is_fasta(file_content):
            print('The file is in FASTA format.')
            
            #initialize variables to hold seq
            sequences = []
            current_sequence = ""
            labels = []

            #loop through each line in the file
            for line in file_content:
                #print('file_content:',  line)
                line = line.strip()
                
                # If the line is a label (starts with '>'), it's a new sequence
                if line.startswith('>'):
                    seq_label = line[1:]
                    if current_sequence:
                        sequences.append(current_sequence)  # Add the previous sequence to the list
                    current_sequence = ""                   # Reset for the next sequence
                    labels.append(seq_label)                # Store the label

                else:
                    current_sequence += line   # Add the sequence to the current sequence
            
            # Add the last sequence to the list
            if current_sequence:
                sequences.append(current_sequence)
            #print('sequences', sequences)
            
            # Open the output file to write the results
            with open(output_filename, 'w') as out_file:
                for label, seq in zip(labels, sequences):  # Iterate through sequences and labels
                    seq_len = seq_length(seq)              # Get the sequence length
                    n_pos, n_count = process_n_regions(seq)# Get 'N' regions and count
                    dash_count = process_dash_regions(seq) # Get dash count
                    
                    # Write the results for each sequence to the output file
                    out_file.write(f"Sequence {label}:\n")
                    out_file.write(f"{seq}\n\n")
                    out_file.write(f"Length: {seq_len}\n")
                    out_file.write(f"Total N count: {n_count}\n")
                    out_file.write(f"Total - count: {dash_count}\n")
                    
                    if n_pos:
                        out_file.write(f"Continuous N regions:\n")
                        for start, end in n_pos:
                            out_file.write(f"Start:{start}, End: {end}\n")
                    else:
                        out_file.write("No continuous N regions found. \n")

                    out_file.write("-" * 40 + "\n\n")    # Separator between sequences
            print(f"Results have been saved to {output_filename}")
        else:
            print('Error: the file is NOT in FASTA format.')

    except FileNotFoundError:
        print('Error: The file was not found.')

# Main function to prompt user for input file and start the processing
def main():
    try: 
        #prompt user to input file name
        input_file = input("Enter name of sequence file: ")
        output_file = "processed_"+input_file.split('.')[0] +".txt"

        # Call the process_fasta function to process the file
        process_fasta(input_file, output_file) 

    except FileNotFoundError:
        print('Error: The file was not found')

# Run the program
if __name__ == "__main__":
    main()
