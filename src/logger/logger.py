import logging  # Python’s built-in logging module (used instead of print() for professional apps)
import os    # Handling file paths and creating folders
from datetime import datetime  # Generate the current date and time.

# Creating a Log File Name
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"   # gets the current date and time.

# Creating a Logs Folder
log_path=os.path.join(os.getcwd(),"logs")  # Gets the current working directory (where you run the script), and makes a path

os.makedirs(log_path,exist_ok=True)  # Creates the folder logs if it doesn’t exist, and avoids error if the folder already exists

# Full File Path for Logging
LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

# Configuring the Logger
logging.basicConfig(level=logging.INFO,  # logs messages with level INFO and above (INFO, WARNING, ERROR, CRITICAL)
                    filename=LOG_FILEPATH,  # sends all logs to the file created earlier
                    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
                    
)

# if __name__=='__main':
#     logging.info("Here again i am testing ")