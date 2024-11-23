''' GUI for Laser Calibration 
Author: Shivaraj M B , Univ. of Bern 
'''

#from devices.feedtrough import *
#from devices.laser import *
from devices.attenuator import *
#from devices.aperture import *
#from devices.mirror import *

#laser = Laser(0)
att = Attenuator()
att.color = False
att.com_init()

import tkinter as tk
from tkinter import ttk
import time

# Import your module functionalities
# from shiva_demo import LM, RM, att, laser

class LaserCalibrationApp:
    def __init__(self, master):
        self.master = master
        master.title("UV Laser Calibration Unit")
        
        # Set up theme with ttk Style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0', font=('Helvetica', 16))  # Light grey background with larger font
        style.configure('TButton', background='#dfe3e6', foreground='#2e3d49', font=('Helvetica', 16))  # Larger font for buttons
        style.configure('TLabelFrame', background='#f0f0f0', foreground='#3c474c', font=('Helvetica', 16))  # Larger font for label frames
        style.configure('TLabel', background='#f0f0f0', foreground='#3c474c', font=('Helvetica', 16))  # Larger font for labels
        style.configure('TEntry', fieldbackground='white', foreground='#2e3d49', font=('Helvetica', 16))  # Larger font for entry fields
        style.configure('TRadiobutton', background='#f0f0f0', foreground='#3c474c', font=('Helvetica', 16))  # Larger font for radio buttons
        style.configure('TCheckbutton', background='#f0f0f0', foreground='#3c474c', font=('Helvetica', 16))  # Larger font for check buttons

        # Set larger font for LabelFrame labels
        style.configure('Laser.TLabelframe.Label', font=('Helvetica', 18, 'bold'))
        style.configure('Attenuator.TLabelframe.Label', font=('Helvetica', 18, 'bold'))
        style.configure('RotaryMotor.TLabelframe.Label', font=('Helvetica', 18, 'bold'))
        style.configure('LinearMotor.TLabelframe.Label', font=('Helvetica', 18, 'bold'))
        style.configure('Messages.TLabelframe.Label', font=('Helvetica', 18, 'bold'))

        # Configure the master grid for dynamic resizing
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)  # Additional row for initialization buttons
        master.rowconfigure(4, weight=1)  # Additional row for laser stop button

        # Initialize and warm up buttons
        self.initialize_button_setup(master)
        self.warmup_button_setup(master)

        # Laser section
        self.laser_frame_setup(master)

        # Attenuator section
        self.attenuator_frame_setup(master)

        # Rotary Motor section
        self.rotary_frame_setup(master)

        # Linear Motor section
        self.linear_frame_setup(master)

        # Notes section
        self.notes_section_setup(master)
        
        # Messages section
        self.messages_section_setup(master)

    def initialize_button_setup(self, master):
        ttk.Button(master, text="Initialize", command=self.InitialiseAll).grid(row=0, column=0, padx=15, pady=15, sticky='ew')

    def warmup_button_setup(self, master):
        ttk.Button(master, text="Laser Warm Up", command=self.LaserWarming).grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(master, text="Laser Stop", command=self.LaserStop).grid(row=1, column=1, padx=15, pady=15, sticky='ew')

    def laser_frame_setup(self, master):
        laser_frame = ttk.LabelFrame(master, text="Laser", style='Laser.TLabelframe')
        laser_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        laser_frame.columnconfigure(0, weight=1)
        laser_frame.rowconfigure(1, weight=1)

        ttk.Button(laser_frame, text="Shutter Start", command=self.start_laser).grid(row=0, column=0, padx=15, pady=15, sticky='ew')
        ttk.Button(laser_frame, text="Shutter Stop", command=self.stop_laser).grid(row=0, column=1, padx=15, pady=15, sticky='ew')

        # Shutter and Frequency section
        shutter_frame = ttk.Frame(laser_frame)
        shutter_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        shutter_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)

        ttk.Label(shutter_frame, text="Frequency").grid(row=0, column=0, padx=15, pady=15, sticky='ew')
        ttk.Combobox(shutter_frame, values=["1 Hz", "2 Hz", "5 Hz", "10 Hz"], font=('Helvetica', 16)).grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(shutter_frame, text="Shoot").grid(row=0, column=2, padx=15, pady=15, sticky='ew')
        ttk.Button(shutter_frame, text="Stop").grid(row=0, column=3, padx=15, pady=15, sticky='ew')
        ttk.Button(shutter_frame, text="Single Shot").grid(row=0, column=4, padx=15, pady=15, sticky='ew')

    def attenuator_frame_setup(self, master):
        attenuator_frame = ttk.LabelFrame(master, text="Attenuator", style='Attenuator.TLabelframe')
        attenuator_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        attenuator_frame.columnconfigure([0, 1, 2], weight=1)

        self.attenuator_entry = ttk.Entry(attenuator_frame)
        self.attenuator_entry.grid(row=0, column=0, padx=15, pady=15, sticky='ew')
        ttk.Button(attenuator_frame, text="Set", command=self.set_attenuator).grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(attenuator_frame, text="Get Transmission", command=self.get_transmission).grid(row=0, column=2, padx=15, pady=15, sticky='ew')

        self.transmission_label = ttk.Label(attenuator_frame, text="Transmission: --")
        self.transmission_label.grid(row=1, column=0, columnspan=3, padx=15, pady=15, sticky='ew')

    def rotary_frame_setup(self, master):
        rotary_frame = ttk.LabelFrame(master, text="Rotary Motor", style='RotaryMotor.TLabelframe')
        rotary_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        rotary_frame.columnconfigure(0, weight=1)
        rotary_frame.rowconfigure([0, 1, 2, 3], weight=1)

        ttk.Button(rotary_frame, text="Home Button", command=self.home_rotary).grid(row=0, column=0, padx=15, pady=15, sticky='ew')
        self.position_mode_rotary = tk.StringVar(value="Relative")
        ttk.Radiobutton(rotary_frame, text="Relative Pos", variable=self.position_mode_rotary, value="Relative").grid(row=1, column=0, padx=15, pady=15, sticky='ew')
        ttk.Radiobutton(rotary_frame, text="Absolute Pos", variable=self.position_mode_rotary, value="Absolute").grid(row=1, column=1, padx=15, pady=15, sticky='ew')
        self.rotary_entry = ttk.Entry(rotary_frame)
        self.rotary_entry.grid(row=2, column=0, padx=15, pady=15, sticky='ew')
        ttk.Button(rotary_frame, text="Move", command=self.move_rotary).grid(row=2, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(rotary_frame, text="Get Position", command=self.get_position_rotary).grid(row=3, column=0, padx=15, pady=15, sticky='ew')
        self.rotary_position_label = ttk.Label(rotary_frame, text="0.000")
        self.rotary_position_label.grid(row=3, column=1, padx=15, pady=15, sticky='ew')

    def linear_frame_setup(self, master):
        linear_frame = ttk.LabelFrame(master, text="Linear Motor", style='LinearMotor.TLabelframe')
        linear_frame.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
        linear_frame.columnconfigure(0, weight=1)
        linear_frame.rowconfigure([0, 1, 2, 3], weight=1)

        ttk.Button(linear_frame, text="Home Button", command=self.home_linear).grid(row=0, column=0, padx=15, pady=15, sticky='ew')
        self.position_mode_linear = tk.StringVar(value="Relative")
        ttk.Radiobutton(linear_frame, text="Relative Pos", variable=self.position_mode_linear, value="Relative").grid(row=1, column=0, padx=15, pady=15, sticky='ew')
        ttk.Radiobutton(linear_frame, text="Absolute Pos", variable=self.position_mode_linear, value="Absolute").grid(row=1, column=1, padx=15, pady=15, sticky='ew')
        self.linear_entry = ttk.Entry(linear_frame)
        self.linear_entry.grid(row=2, column=0, padx=15, pady=15, sticky='ew')
        ttk.Button(linear_frame, text="Move", command=self.move_linear).grid(row=2, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(linear_frame, text="Get Position", command=self.get_position_linear).grid(row=3, column=0, padx=15, pady=15, sticky='ew')
        self.linear_position_label = ttk.Label(linear_frame, text="0.000")
        self.linear_position_label.grid(row=3, column=1, padx=15, pady=15, sticky='ew')

    def notes_section_setup(self, master):
        notes_frame = ttk.Frame(master)
        notes_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        notes_frame.columnconfigure(0, weight=1)

        ttk.Label(notes_frame, text="Notes:", font=('Helvetica', 16)).grid(row=0, column=0, padx=15, pady=15, sticky='w')
        self.notes_entry = ttk.Entry(notes_frame, width=40, font=('Helvetica', 16))
        self.notes_entry.grid(row=0, column=1, padx=15, pady=15, sticky='ew')
        ttk.Button(notes_frame, text="Save Note", command=self.save_note).grid(row=0, column=2, padx=15, pady=15, sticky='ew')
        
    def messages_section_setup(self, master):
        message_frame = ttk.LabelFrame(master, text="Messages", style='Messages.TLabelframe')
        message_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        message_frame.columnconfigure(0, weight=1)
        message_frame.rowconfigure(0, weight=1)
        
        self.message_text = tk.Text(message_frame, height=5, font=('Helvetica', 16))
        self.message_text.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')
        self.message_text.config(state='disabled')

    def add_message(self, message):
        self.message_text.config(state='normal')
        self.message_text.insert(tk.END, message + '\n')
        self.message_text.config(state='disabled')
        self.message_text.see(tk.END)

    # Method implementations for Initialize, Warm-up, and other device controls
    def InitialiseAll(self):
        # Placeholder for initialization logic
        print("All devices initialized.")
        laser.com_init()

    def LaserWarming(self):
        print("Starting the Laser within 5 seconds.")
        time.sleep(5)
        # Placeholder for laser start logic
        print("Laser is now ready.")
        print("Laser actually from here on")
        #laser.getStatus()
        laser.start()
        
    def LaserStop(self):
        print("Stopping the Laser.")
        # Placeholder for laser stop logic
        laser.stop()

    #________________Save notes___________________
    def save_note(self):
        note = self.notes_entry.get()
        if note.strip() != "":  # Only save if there's something written
            # Generate the directory and file names
            folder_path = "Note_Folder"
            date_str = datetime.now().strftime("%d_%m_%Y")
            filename = f"{date_str}_notes.txt"
            full_path = os.path.join(folder_path, filename)

            # Ensure the directory exists
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Save the note
            with open(full_path, "a") as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{timestamp}: {note}\n")
        
            # Clear the entry after saving
            self.notes_entry.delete(0, tk.END)
            
    #____________________________________________
    # Define methods for GUI operations here, connecting to the device control methods you have
    def start_laser(self):
        print("Laser started.")  # Placeholder for starting the laser
        #laser.start(self)  # Assuming there's a start method in your laser class

    def stop_laser(self):
        print("Laser stopped.")  # Placeholder for stopping the laser
        #laser.stop()  # Assuming there's a stop method in your laser class

    def set_attenuator(self):
        value = float(self.attenuator_entry.get())
        print(f"Attenuator set to {value}.")  # Placeholder for setting attenuator value
        att.setTransmission(value)  # Assuming a method that sets attenuation level
        
    def get_transmission(self):
        transmission_value = 0.5  # Placeholder for getting transmission value
        print(f"Transmission: {transmission_value}.")  # Placeholder for getting transmission value
        transmission_value = att.getTransmission()  # Assuming there's a getTransmission method in your att object
        self.transmission_label.config(text=f"Transmission: {transmission_value}")


    def home_rotary(self):
        print("Rotary motor homed.")  # Placeholder for homing rotary motor
        #RM.moveAbsolute(100000.0)

    def move_rotary(self):
        mode = self.position_mode_rotary.get()
        value = float(self.rotary_entry.get())
        if mode == 'Relative':
            print(f"Rotary motor moved relatively by {value}.")  # Placeholder for moving rotary motor relatively
            #RM.moveRelative(value)
        else:
            print(f"Rotary motor moved absolutely to {value}.")  # Placeholder for moving rotary motor absolutely
            #RM.moveAbsolute(value)

    def get_position_rotary(self):
        pos = 0.0  # Placeholder for getting rotary motor position
        print(f"Rotary motor position: {pos}.")  # Placeholder for getting rotary motor position
        #pos = RM.getPosition()
        self.rotary_position_label.config(text=f"{pos:.3f}")

    def home_linear(self):
        print("Linear motor homed.")  # Placeholder for homing linear motor
        #LM.moveAbsolute(100000.0)

    def move_linear(self):
        mode = self.position_mode_linear.get()
        value = float(self.linear_entry.get())
        if mode == 'Relative':
            print(f"Linear motor moved relatively by {value}.")  # Placeholder for moving linear motor relatively
            #LM.moveRelative(value)
        else:
            print(f"Linear motor moved absolutely to {value}.")  # Placeholder for moving linear motor absolutely
            #LM.moveAbsolute(value)

    def get_position_linear(self):
        pos = 0.0  # Placeholder for getting linear motor position
        print(f"Linear motor position: {pos}.")  # Placeholder for getting linear motor position
        #pos = LM.getPosition()
        self.linear_position_label.config(text=f"{pos:.3f}")


root = tk.Tk()
app = LaserCalibrationApp(root)
root.mainloop()

