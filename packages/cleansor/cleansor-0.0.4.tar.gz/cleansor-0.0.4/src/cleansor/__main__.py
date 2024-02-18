
import os

def find_duplicates(directory,filetype):
    # Dictionary to store file hashes
    hash_dict = {}
    # List to store duplicate file paths
    duplicates = []

    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(f"."+filetype):
                filepath = os.path.join(root, filename)
                # Calculate the hash of the file
                with open(filepath, 'rb') as f:
                    file_hash = hash(f.read())
                
                # Check if the hash already exists
                if file_hash in hash_dict:
                    duplicates.append(filepath)
                else:
                    hash_dict[file_hash] = filepath

    return duplicates

def delete_duplicates(duplicates):
    # Delete duplicate files
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Deleted duplicate file: {duplicate}")

if __name__ == "__main__":
    filetype = input("Enter file extension without dot [.] (i.e., png, jpg, etc.): ")

    current_directory = os.getcwd()
    duplicates = find_duplicates(current_directory,filetype)

    if duplicates:
        print("Duplicate files found:")
        for duplicate in duplicates:
            print(duplicate)
        
        # Prompt a final confirmation to user since deleted file(s) cannot be recovered
        user_confirmation = input("Confirm to clean it all? (Y/n) ")

        if user_confirmation.lower() == 'y':
            delete_duplicates(duplicates)
            print("Duplicate files deleted.")
        else:
            print("Cancelled.")
    else:
        print("No duplicate files found.")