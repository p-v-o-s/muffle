from glob import glob
import readline
import datetime, os
import serial
import numpy as np

SERIAL_PORT_PATTERN = "/dev/ttyACM*"
BAUDRATE = 9600
DELIMITER = ','
DATA_DIR = "data"
EOL = "\n"

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

serial_port = glob(SERIAL_PORT_PATTERN)[0]
ser = serial.Serial(serial_port, baudrate=BAUDRATE)

if __name__ == "__main__":
    #flush the input
    ser.flushInput()
    ser.setTimeout(0.1)
    while ser.read():
        pass
    ser.setTimeout(None)


    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
        
    now = datetime.datetime.now()
    out_filename = now.strftime("%Y-%m-%d_%H_%M_%S.csv")
    out_filepath = os.path.sep.join((DATA_DIR,out_filename))
    out_file = open(out_filepath,'w')

    try:
        while True:
            line = ser.readline()
            line = line.strip()
            print line
            out_file.write(line + EOL)
            out_file.flush()
    except KeyboardInterrupt:
        print ""
    finally:
        ser.close()
        out_file.close()

    new_filename = rlinput("Change filename (blank deletes): ", prefill=out_filename)
    new_filename = new_filename.strip()
    new_filepath = os.path.sep.join((DATA_DIR,new_filename))
    if new_filename == "":
        print "Deleting data file."
        os.remove(out_filepath)
    elif new_filepath != out_filepath:
        os.rename(out_filepath, new_filepath)
