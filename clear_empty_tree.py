import os

def is_empty(directory, force = False, showFiles = True):
    empty = True
    try:
        for entry in os.listdir(directory):
            if os.path.isdir(directory + '/' + entry):
                empty = is_empty(directory + '/' + entry, force = force,
                            showFiles = showFiles) and empty

            else:
                if showFiles:
                    print(f"File {entry:50s} at: " + directory)
                empty = False

    except PermissionError:
        empty = False

    if empty:
        delete = True
        if not force:
            rmdir = input("Delete directory: " + directory + '? ')
            delete = rmdir.startswith('y')
            
        if delete:
            print("Deleting directory: " + directory)
            try:
                os.rmdir(directory)
            except PermissionError:
                print(">>> Permission denied")

            except OSError:
                print(">>> Couldn't list directory content")
                
            else:
                print(">>> Deleted")
        else:
            print(">>> Skipped")
        
    return empty

if __name__ == "__main__":
    for directory in [directory for directory in os.listdir()
                      if os.path.isdir(directory)]:
        
        print("===" + directory + "===")
        is_empty(directory, force = True, showFiles=False)
