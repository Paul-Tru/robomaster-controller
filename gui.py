import vars

import configparser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class MainGui:
    """Gui to see the robot camera and start dragrace"""
    def __init__(self):
        # read config.ini
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        
        # get debug from config.ini
        self.debug = self.config.getboolean("GENERAL", "debug")

        # set values for ctk window
        self.app = ctk.CTk()
        ctk.set_appearance_mode(self.config["GUI"]["appearance"])
        self.app.geometry(self.config["GUI"]["geometry"])
        if not self.debug:
            self.app.title("Titan")
        else:
            self.app.title("Titan (Debug)")
        self.frame_pad = self.config["GUI"]["frame_pad"]
        self.frame_font = eval(self.config["GUI"]["frame_font"])
        self.comp_pad = self.config["GUI"]["component_pad"]

        self.video()

        self.app.mainloop()

    def video(self):
        """shows video preview or test picture"""
        frame = ctk.CTkFrame(self.app)
        frame.grid(row=4, padx=self.comp_pad, pady=self.comp_pad)

        self.video_label = ctk.CTkLabel(frame, text="")
        self.video_label.pack()

        def update_frame():
            """update the video frame"""
            if not self.debug:
                try:
                    imgtk = ctk.CTkImage(vars.ep_camera, size=(160, 90))  # Adjust the size as necessary

                    # Update the video label with the new frame
                    self.video_label.configure(image=imgtk)
                    self.video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection

                except:
                    # Display an error message or a placeholder image
                    self.video_label.configure(text="Error: unable to read video stream", fg_color="darkred")
            else:
                # show debug picture
                placeholder_imgtk = ctk.CTkImage(vars.test_png, size=(160, 90))
                self.video_label.configure(image=placeholder_imgtk)
                self.video_label.image = placeholder_imgtk

            # Call this function again after a delay (e.g., 100ms)
            self.video_label.after(100, update_frame)

        update_frame()
