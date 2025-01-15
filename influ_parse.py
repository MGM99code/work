#script to separate HA or NA segment influenza fasta files 

'''
IF file is FASTA:
    for each sequence:
        check if sample ID is same
        separate HA and NA
ELSE:
    print error

'''
import os

# Function to check if the file is in FASTA format
def is_fasta(lines):
    # If the first line does not start with '>', it’s not FASTA format
    if not lines or not lines[0].startswith('>'):
        return False
    return True

def extract_info(header):
    # Parse the header string and extract ID and segment information
    header_parts = header.split('|')
    if len(header_parts) >= 3:
        id = header_parts[1].strip()       # Extract the ID from the second part
        segment = header_parts[2].strip()  # Extract the segment from the third part
        # Check if the segment is one of the expected values ('HA' or 'NA')
        if segment in ['HA', 'NA']:
            return id, segment
    return None, None
        

# Main function to process the FASTA file and generate the output
def process_fasta(input_filename):
        
    try:
        #Define folder to save the output files
        output_folder = 'gisaid_epiflu_sequence'

        #Create output folder if it does not already exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open the input file and read its content
        with open(input_filename, 'r') as file:
            file_content = file.readlines()

        #print('filecontent', file_content)

        #check if file is in fasta format
        if is_fasta(file_content):
            print('The file is in FASTA format.')
            
            #print('file_content',file_content)
            # Dictionary to store sequences with keys as "id_segment"
            sequences = {}
            current_header = None # Track the current header line
            current_sequence = [] # Accumulate sequence lines under the current header

            # Parse the file line by line
            for line in file_content:
                line = line.strip()
                if line.startswith('>'):  # Header line
                    # Save the previous header and sequence (if any) before processing the new header
                    if current_header:
                        id, segment = extract_info(current_header)
                        if id and segment:
                            key = f"{id}_{segment}"
                            sequences[key] = (current_header, ''.join(current_sequence))

                    # Update the current header and reset the sequence
                    current_header = line
                    current_sequence = []
                elif line:  # Sequence line
                    current_sequence.append(line)

            # Handle the last header and sequence in the file    
            if current_header:
                id, segment = extract_info(current_header)
                if id and segment:
                    key = key = f"{id}_{segment}"
                    sequences[key] = (current_header, ''.join(current_sequence))

            # Write each sequence to a separate output file
            for key, (header, sequence) in sequences.items():
                output_filename = os.path.join(output_folder, f"{key}.fasta")
                with open(output_filename, 'w') as outfile:
                    outfile.write(f"{header}\n{sequence}\n")
                print(f"Created file: {output_filename}")

    except FileNotFoundError:
        print('Error: The file was not found.')
    
    except Exception as e:  # Handle other unexpected errors
        print(f'Error: An unexpected error occurred: {str(e)}')

# Main function to prompt user for input file and start the processing
def main():
    try: 
        #prompt user to input file name
        input_file = input("Enter name of sequence file: ")

        # Call the process_fasta function to process the file
        process_fasta(input_file) 

    except FileNotFoundError:
        print('Error: The file was not found')

# Run the program
if __name__ == "__main__":
    main()