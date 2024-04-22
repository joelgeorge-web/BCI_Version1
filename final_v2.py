import pickle
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import csv
import time 
import bluetooth

#Load the model
model = pickle.load(open('EEGNet.pkl', 'rb'))

#cidrie car
esp32 = "ESP32test"
address = "A0:A3:B3:AB:89:BA"
devices = bluetooth.discover_devices()

def run_prediction_loop():
    """
    Function to run prediction loop 
    """
    global index
    index = 0  # Reset index to 0
    run_prediction() 

def run_prediction():
    """     
    Function to run prediction and update GUI  
    with EEG data and prediction
    """
    global index
    if index < len(predicted_data):
        pred = predicted_data[index]
        sample = X_test_loaded[index].squeeze()

        try:
            if pred == 0:
                print("Forward")
                prediction_label.config(text=f'Prediction: Forward')
            elif pred == 1:
                print("Left")
                prediction_label.config(text=f'Prediction: Left')
            elif pred == 2:
                print("Right")
                prediction_label.config(text=f'Prediction: Right')
            elif pred == 3:
                print("Reverse")
                prediction_label.config(text=f'Prediction: Reverse')
            sock.send(str(pred+1))
        except Exception as e:
            print(f"Exception Occured: {e}")

        time.sleep(3)


        # Plot EEG data
        plt.figure(figsize=(6, 4))
        plt.plot(sample)
        plt.xlabel('Time Step')
        plt.ylabel('EEG Value')
        plt.title(f'Sample {index} EEG Data')
        plt.savefig("temp_plot.png")
        plt.close()

        # Update graphical plot
        img = Image.open("temp_plot.png")
        img = img.resize((400, 300), Image.BILINEAR)  # Use BILINEAR as an alternative
        img = ImageTk.PhotoImage(img)
        graphical_plot_label.config(image=img)
        graphical_plot_label.image = img

        # Plot EEG data with color bar
        plt.figure(figsize=(10, 6))
        plt.imshow(sample, aspect='auto', cmap='viridis')
        plt.colorbar(label='EEG Value')
        plt.xlabel('Time Step')
        plt.ylabel('Sample')
        plt.title(f'EEG Data - Prediction: {pred}')
        plt.savefig("temp_plot_eeg.png")
        plt.close()

        img_eeg = Image.open("temp_plot_eeg.png")
        img_eeg = img_eeg.resize((400, 300), Image.BILINEAR)  # Use BILINEAR as an alternative
        img_eeg = ImageTk.PhotoImage(img_eeg)
        eeg_plot_label.config(image=img_eeg)
        eeg_plot_label.image = img_eeg

        # Update index for next prediction
        index += 1

        # Call run_prediction after a delay of 3 seconds
        root.after(300, run_prediction)


for addr in devices:
    if esp32 == bluetooth.lookup_name(addr):
        address = addr
        break

port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    """
    Connect to ESP32 via Bluetooth
    """
    sock.connect((address, port))
except OSError as e:
    print(f"Bluetooth Error: {e}")
except Exception as e:
    print(f"Bluetooth Error: {e}")


with open('X.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    original_shape = None

    for row in reader:
        if 'Original Shape:' in row:
            original_shape = tuple(map(int, row[1].strip('()').split(',')))
        else:
            data.append([float(val) for val in row]) 

if original_shape:
    X_test_loaded = np.array(data).reshape(original_shape)
    X_test_loaded = X_test_loaded[:4]
    predicted_data = model.predict(X_test_loaded).argmax(axis=-1) 

time.sleep(2)


# Create main window

root = tk.Tk()
root.title("EEG Prediction GUI")
root.geometry("1500x700")
# root.attributes('-fullscreen', True)



prediction_label = ttk.Label(root, text="")
prediction_label.place(x=200, y=350) 

graphical_plot_label = ttk.Label(root)
graphical_plot_label.place(x=1000, y=20)  

eeg_plot_label = ttk.Label(root)
eeg_plot_label.place(x=1000, y=400) 




l = ttk.Label(root, text = "EEG Prediction GUI")
l.config(font =("Courier", 14))
 
Fact = """This is a GUI application to predict EEG data."""
T = ttk.Label(root,  width = 52)
T.config(text = Fact)

b2 = ttk.Button(root, text = "Exit", command = root.destroy) 
predict_button = ttk.Button(root, text="Run Prediction", command=run_prediction_loop)
predict_button.place(x=200, y=10) 

l.pack()
T.pack()
b2.pack()
predict_button.pack()




# Run the GUI
index = 0  
root.mainloop()