from tkinter import *
from tkinter import messagebox
from elements import MASS, POS, Element
import sys
from scaledata import weight
import time
import random
import threading
import platform
#from main import alive

#Functions for each button on the GUI:

#function to retrieve information from the button being pressed and inserting it into the entry boxes
def compound(element):
    """_summary_
    This function retrieves the information from the button on the GUI being pressed, then inserts the Molar Mass and Element into the Molar Mass and Compound Entry boxes resspectively. 
    Args:
        element (_String_): element is the argument representing which element is pressed on the periodic table GUI. It knows which element it is because of the get_button function, which gets its information from dictionaries in elements.py.
    """
    current = float(mMass.get())
    mMass.delete(0, END)
    mMass.insert(0, str(round(current + MASS[element], 2)))
    Element = Formula.get()
    Formula.delete(0, END)
    Formula.insert(0, Element + element)

#function for clear button
def clear():
    """
    This function deletes all of the entry boxes on the GUI (Molar Mass, Mass, Compound), and adds placeholders in the Molar Mass and Mass boxes to allow other functions to work. 
    """
    mMass.delete(0, END)
    mMass.insert(0, "0")
    Formula.delete(0, END)
    Mass.delete(0, END)
    Mass.insert(0, "0")
    Mol.delete(0, END)

def get_button(el):
    """
    This function sets the values for each button in the interactive periodic table. The text on the button is an element called from the elements.py dictionaries, the font is set to the global variable created at the top of the file, the button width is set to 4, and the Button's command is set to the compound function. 
    Args:
        el (String): el is the same value as element in the compound() function. It gets element information from a dictionary in elements.py and is called by the for loop that lays out all the Buttons on the GUI. 

    Returns:
        _tkinter Button_: 
    """
    # the following color codes are inspired by ptable.com
    if el.type == "Reactive":
        color = "green"
    elif el.type == "Unknown":
        color = "grey"
    elif el.type == "Metalloid":
        color = "cyan"
    elif el.type == "Noble":
        color = "purple"
    elif el.type == "Transition":
        color = "red"
    elif el.type == "Lanthanoid":
        color = "brown"
    elif el.type == "Actinoid":
        color = "pink"
    elif el.type == "Alkali":
        color = "orange"
    elif el.type == "Alkaline Earth":
        color = "yellow"
    elif el.type == "Post Transition":
        color = "blue"
    else:
        color = "grey"

    return Button(
        text = el.name,
        font = font,
        width = int(font[1]/element_font_scale),
        command = lambda: compound(el.name),
        bg = color
    )

def directions():
    """
    This function is the command for the "Directions" Button. It displays a pop-up message box with directions on how to use the Mol Scale. 
    """
    messagebox.showinfo("Directions", "To find the mols of your compound, first click on each individual element (H2O = HHO).\nOnce the entire compound is entered put your compound on the scale, press the Initiate button to get the weight of the compound, then click the Calculate button.")

#function to end the program
def terminate():
    """
    This function closes the GUI. 
    """
    messagebox.showinfo("Shutting Down...", "Shutting Down...")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    sys.exit() #comment this line if you are using a raspberry pi
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)
    exit()

#function that calculates the mols of the selected compound
def mol():
    """This function calculates the mols of the selected compound using the Molar Mass and Mass Entry boxes."""
    mol_mass = float(mMass.get())
    mass = float(Mass.get())
    mol_compound = round(mass / mol_mass, 2)
    Mol.delete(0, END)
    Mol.insert(0, str(mol_compound))

start_scale = False
def initiate(): 
    """I'm sitll figuring this out myself, but it is supposed to initiate the hx711 module connected to the Raspberry Pi"""
    start_scale = True

#function to read the weight from the scale
def check_mass():
    """This function reads the weight from the scaledata.py list and appends it to the Mass Entry box."""
    #import Scale
    print(weight)
    Mass.delete(0, END)
    Mass.insert(0, str(weight[-1]))

def scale():
    i = 1
    while i < 10:
        value = random.randint(0, 1000)
        weight.append(value)
        print(value)
        i += 1 
        time.sleep(1)
    # Uncomment this when you have an actual scale connected to GPIO
    """import RPi.GPIO as GPIO  # import GPIO
    from hx711 import HX711  # import the class HX711

    try:
        GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
        # Create an object hx which represents your real hx711 chip
        # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
        hx = HX711(dout_pin=29, pd_sck_pin=31)
        # measure tare and save the value as offset for current channel
        # and gain selected. That means channel A and gain 128
        err = hx.zero()
        # check if successful
        if err:
            raise ValueError('Tare is unsuccessful.')

        reading = hx.get_raw_data_mean()
        if reading:  # always check if you get correct value or only False
            # now the value is close to 0
            print('Data subtracted by offset but still not converted to units:',
                    reading)
        else:
            print('invalid data', reading)

        # In order to calculate the conversion ratio to some units, in my case I want grams,
        # you must have known weight.
        input('Put known weight on the scale and then press Enter')
        reading = hx.get_data_mean()
        if reading:
            print('Mean value from HX711 subtracted by offset:', reading)
            known_weight_grams = input(
                'Write how many grams it was and press Enter: ')
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                        known_weight_grams)

            # set scale ratio for particular channel and gain which is
            # used to calculate the conversion to units. Required argument is only
            # scale ratio. Without arguments 'channel' and 'gain_A' it sets
            # the ratio for current channel and gain.
            ratio = reading / value  # calculate the ratio for channel A and gain 128
            hx.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

        # Read data several times and return mean value
        # subtracted by offset and converted by scale ratio to
        # desired units. In my case in grams.
        print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
        input('Press Enter to begin reading')
        print('Current weight on the scale in grams is: ')
        while True:
            print(hx.get_weight_mean(20), 'g')
            weight.append(hx.get_weight_mean(20))

    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')

    finally:
        GPIO.cleanup()"""

#begin the GUI loop20
def main():
    root = Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(screen_width, screen_height)
    
    root.title("Mol Calculator")
    root_background_color = "dark grey"
    root.configure(background=root_background_color)

    global button_scale
    global entry_scale
    global font_scale
    global element_font_scale

    if screen_width == 2560 and screen_height == 1440:
        button_scale = 150
        entry_scale = 24.7
        font_scale = 44.44
        element_font_scale = 5.4
    elif screen_width == 1440 and screen_height == 900:
        button_scale = 150
        entry_scale = 15
        font_scale = 40
        element_font_scale = 5.4
    elif screen_width == 1920 and screen_height == 1080:
        button_scale = 150
        entry_scale = 20.2
        font_scale = 40.5
        element_font_scale = 4.7
    elif screen_width == 1920 and screen_height == 1200:
        button_scale = 150
        entry_scale = 20
        font_scale = 40.5
        element_font_scale = 4.7
    elif screen_width == 800 and screen_height == 600:
        button_scale = 80
        entry_scale = 9
        font_scale = 47
        element_font_scale = 3.2
        
    global BUTTON_WIDTH
    BUTTON_WIDTH = int(screen_width / button_scale)
    global ENTRY_WIDTH
    ENTRY_WIDTH = int(screen_width / entry_scale)
    global font
    font = ("Times", int(screen_height/font_scale))

    Elements = set()
    for i in MASS:
        Elements.add(Element(i))

    #for loop to create and display the periodic table buttons
    BUTTONS = {}
    for i in Elements:
        BUTTONS[i] = get_button(i)
        BUTTONS[i].grid(
            row = i.position[0],
            column = i.position[1],
        )

    #space holder label to make the periodic table look like the periodic table
    Space_holder = Label(text=" ", font=font, bg=root_background_color)
    Space_holder.grid(row=8, column=0, columnspan=18)

    #label to display the selected compound
    formula = Label(text="Compound: ", font=font, bg=root_background_color)
    formula.grid(row=11, column=0, columnspan=2)

    #Entry box that holds the chemical formula of the compound
    global Formula
    Formula = Entry(root, width=ENTRY_WIDTH, font=font)
    Formula.grid(row=11, column=2, columnspan=16)

    #Label to display the molar mass of the compound
    Molmass = Label(text="Molar Mass: ", font=font, bg=root_background_color)
    Molmass.grid(row=12, column=0, columnspan=2)

    #Entry box that holds the molar mass of the compound (based on what buttons are pressed)
    global mMass
    mMass = Entry(root, width=ENTRY_WIDTH, font=font)
    mMass.grid(row=12, column=2, columnspan=16)
    mMass.insert(0, "0")

    #Label to display the mass read by the scale
    massC = Label(text="Mass(g): ", font=font, bg=root_background_color)
    massC.grid(row=13, column=0, columnspan=2)

    #Entry box that holds the mass inputted by the scale
    global Mass
    Mass = Entry(root, width=ENTRY_WIDTH, font=font)
    Mass.grid(row=13, column=2, columnspan=16)
    Mass.insert(0, "0")

    #Label to display mols of the compoound
    molC = Label(text="Mol: ", font=font, bg=root_background_color)
    molC.grid(row=14, column=0, columnspan=2)

    #Entry box that holds the calculated mols of the compount (after pressing the calculate button)
    global Mol
    Mol = Entry(root, width=ENTRY_WIDTH, font=font)
    Mol.grid(row=14, column=2, columnspan=16)

    #Button that uses the clear function to clear the text from every entry box
    Clear_Button = Button(text="Clear", font=('Times', int(screen_height/40)), width=BUTTON_WIDTH, command=clear)
    Clear_Button.grid(row=15, column=12, columnspan=6)

    #Button that uses the mol function to take all the data from the entry boxes and calculate the mols of the selected compound
    Calculate_Button = Button(text="Calculate", font=('Times', int(screen_height/40)), width=BUTTON_WIDTH, command=mol)
    Calculate_Button.grid(row=15, column=0, columnspan=6)

    #Button that uses the initiate function to take the scale readings from the "weight" list in "scaledata.py" and insert it into the mass box
    Initiate_Button = Button(text="Initiate Scale", font=font, width=BUTTON_WIDTH, command= lambda: initiate)
    Initiate_Button.grid(row=0, column=12, columnspan=6)

    Check_Mass_Button = Button(text="Check Mass", font=font, width=BUTTON_WIDTH, command=check_mass)
    Check_Mass_Button.grid(row=0, column=6, columnspan=6)

    #Button that uses the directions function to display a messagebox with instructions of how to use the scale
    Directions = Button(text="Directions", font=font, width=BUTTON_WIDTH, command=directions)
    Directions.grid(row=0, column=0, columnspan=6)

    #Button that uses the terminate function to shut down the mol scale. 
    Terminate_Button = Button(text="Terminate", font=('Times', int(screen_height/40)), width=BUTTON_WIDTH, command=terminate)
    Terminate_Button.grid(row=15, column=6, columnspan=6)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #maintain the GUI loop

    root.attributes('-fullscreen', True)

    root.mainloop()

if __name__ == "__main__":
    if platform.uname()[0] == "Darwin" or "Mac" in platform.uname()[1]:
        main()
    else:
        t1 = threading.Thread(target=main)
        t2 = threading.Thread(target=scale)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
