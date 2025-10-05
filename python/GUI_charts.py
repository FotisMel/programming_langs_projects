 # Import the necessary libraries.
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import pandas as pd 
import threading 
from chatbot import CryptoChatbot



class CryptoGUI:
    # Creation of an attribute.
    def __init__(self, root, csv_file = None):
        self.root = root                # Main self for app.
        self.csv_file = csv_file
        self.df = None                  # An empty DataFrame which stores the data. 

        try:
            # Create a loading screen.
            self.setup_loading_screen()

            # Load data on a separate thread to avoid freezing the GUI
            self.load_data_thread()

        except:
            # Close loading screen.
            self.loading_screen.destroy()

            # Show error message.
            messagebox.showerror("Error!", "Failed to load data ")
            self.root.destroy()


    # Creation of loading popup.
    def setup_loading_screen(self):
        self.loading_screen = tk.Toplevel(self.root)
        self.loading_screen.title("Loading...")
        self.loading_screen.geometry("600x600")


        # Message for user waiting.
        tk.Label(
            self.loading_screen,
            text = "Loading cryptocurrency data..Please wait...",
            font = ("Arial", 12)
        ).pack(pady = 20)


        # Moving bar
        self.progress = ttk.Progressbar(
            self.loading_screen,
            orient = "horizontal",
            length = 200,
            mode = "indeterminate"      # We don't know when it lasts..
        )
        self.progress.pack(pady = 10)
        self.progress.start()


    # Run data loading in a separate thread.
    def load_data_thread(self):
        thread = threading.Thread(target = self.load_data)
        thread.daemon = True
        thread.start()


    # Load the data from CSV file and uses sort based on the market cap.
    def load_data(self):
            # Simulate some loading time 
            import time
            time.sleep(5)


            # Loading the data from CSV.
            self.df = pd.read_csv(self.csv_file, sep = ';')


            # Convert column 'Market Cap' to number (without $ and ,) for a better sorting.
            self.df['Market Cap'] = (
                self.df['Market Cap']
                .str.replace(r"[\\$,]", '', regex = True)
                .astype(float)
            )


            # Sorting based on the Market Cap.
            self.df = self.df.sort_values(by = 'Market Cap', ascending = False)


            self.on_data_loaded()



    def on_data_loaded(self):
        # Close loading screen.
        self.loading_screen.destroy()
        # Setup main GUI.
        self.setup_main_gui()



    # Create the main self with the list of the cryptocurrencies.
    def setup_main_gui(self):
        self.root.title("Cryptocurrencies")
        self.root.geometry("600x600")
        self.root.deiconify()


        # Create a frame which will include the coins. 
        main_frame = tk.Frame(self.root)
        main_frame.pack(side = tk.TOP, expand = True, padx = 10, pady = 10)


        title_frame = tk.Label(
            main_frame,
            text = "Top 20 Cryptocurrencies by Market Cap",
            font = ("Arial", 16, "bold")
        )
        title_frame.pack(pady = (0, 20))


        # Create frame for listbox and scrollbar.
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(fill = tk.BOTH, expand = True)


        # Create a vertical scrollbar to the right side of the frame.
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)


        # Create a widget with a list of elements.
        self.listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand = scrollbar.set,
            font = ("Arial", 12),
            background = "lightblue" 
        )
        self.listbox.pack(fill = tk.BOTH, expand = True)


        # Configure scrollbar to follow the scrolling.
        scrollbar.config(command = self.listbox.yview)


        # Fill the list with the data from coins.
        self.populate_listbox()

        # Initialize that the user when does a double click to a coin, then will show it's details. 
        self.listbox.bind("<Double-Button-1>", self.show_crypto_details)

        # 'Ask Bitbot' button to ask the chatbot.
        tk.Button(
            listbox_frame,
            text = "Ask Bitbot",
            command = self.open_chatbot,
            background = "black",
            foreground = "white"
        ).pack(side = tk.RIGHT, padx = 5)



    def populate_listbox(self):
        # Showing the tags of the list.
        tags = "#   Name    Market Cap"
        self.listbox.insert(tk.END, tags)

        # Filling the list with the cryptocurrencies.
        for index, crypto_data in self.df.head(20).iterrows():

            rank = index + 1
            name = crypto_data['Name']
            market_cap = crypto_data['Market Cap']


            display_text = f"{rank}. {name} - ${market_cap}"
            self.listbox.insert(tk.END, display_text)
            self.listbox.pack()



    # Showing the details of the selected coin.
    def show_crypto_details(self, crypto_data):
        selected_coin = self.listbox.curselection()

        if selected_coin: 
            # Stores the index of the first selected element.
            index = selected_coin[0]
            crypto_data = self.df.iloc[index - 1]   # There is -1 because there are tags.


            # Creation of a new popup.
            details_window = tk.Toplevel(self.root)
            details_window.title(f"{crypto_data['Name']} Details")
            details_window.geometry("400x300")

            # Compose the data of the coin.
            details = f"""
            Name: {crypto_data['Name']}
            Price: {crypto_data['Price']}
            Change24h: {crypto_data['24h']}
            Change7d: {crypto_data['7d']}
            Volume24h: {crypto_data['24h Volume']}
            MarketCap: {crypto_data['Market Cap']} """

            # Show the details.
            tk.Label(
                details_window,
                text = details,
                font = ("Arial", 11, "bold"),
                background = "purple",
                foreground = "white",
                justify = tk.LEFT,
            ).pack(fill = tk.BOTH, padx = 20, pady = 50)


            # Call the function for the options with the charts.
            self.show_chart_confirmation(crypto_data, details_window)


    # Show a message to confirm if the user want to see the chart.
    def show_chart_confirmation(self, crypto_data, details_window):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirmation")
        confirm_window.geometry("400x200")
        

        # Choice for showing the chart of coin.
        tk.Label(
            confirm_window,
            text = f"΅What would you like to do with the data of {crypto_data['Name']} and the other top 5 crypto coins?",
            font = ("Arial", 11),
            wraplength = 350
        ).pack(pady = 20)


        button_frame = tk.Frame(confirm_window)
        button_frame.pack()

        # 'Create Chart' button to show comparison with the other coins chart.
        tk.Button(
            button_frame,
            text = "Create Chart",
            command = lambda: [ 
                details_window.destroy(),
                confirm_window.destroy(),
                self.show_chart_options(crypto_data)
            ],
            background = "gray",
            foreground = "black",
        ).pack(side = tk.LEFT, padx = 10)



        # No button to show the chart of the selected coin only.
        tk.Button(
            button_frame,
            text = "Nothing",
            command = confirm_window.destroy,
            background = "gray",
            foreground = "black",
        ).pack(side = tk.RIGHT, padx = 10)



        # Extract data button to show the chart of the selected coin only.
        tk.Button(
            button_frame,
            text = "Extract data",
            command = lambda: [
                confirm_window.destroy(),
                details_window.destroy(),
                self.extract_coin_data(crypto_data)
            ],
            background = "gray",
            foreground = "black",
        ).pack(side = tk.RIGHT, padx = 10)


    # Extract selected coin data to CSV file.
    def extract_coin_data(self, crypto_data):
        # Ask user where to save the file.
        filename = filedialog.asksaveasfilename(
            defaultextension = ".csv",
            title = "Save cryptocurrency data as..."
        )


        # If user didn't cansel the save dialog.
        if filename:
            # Create a Data Frame with just the selected coin's data.
            selected_data = pd.DataFrame([crypto_data])
            
            # Save to CSV
            selected_data.to_csv(filename, index = False)



    # Show to user a popup of the options to select which option wants his chart.
    def show_chart_options(self, crypto_data):
        options_window = tk.Toplevel(self.root)
        options_window.title("Chart Options")
        options_window.geometry("700x400")


        tk.Label(
            options_window,
            text = f"Chart options for {crypto_data['Name']} with Top Coins.",
            font = ("Arial", 14, "bold"),
            wraplength = 400
        ).pack(pady = (20, 10))


        tk.Label(
            options_window,
            text = "Select what data to display on the chart:",
            font = ("Arial", 11),
        ).pack(pady = (0, 20))



        options_frame = tk.Frame(options_window)
        options_frame.pack(pady = 10)

        # Data frame with the options (left: tags and right: descriptions).
        options = [
            ("Price", "Price($)"),
            ("Market Cap", "Market Cap ($)"),
            ("24h Change (%)", "Price change in the last 24 hours"),
            ("7d Change (%)", "Price change in the last 7 days")
        ]

        # Create a variable to load the selected options of the user.
        selected_option = tk.StringVar()

        # Create a data frame with the options.
        for display_text, description in options:
            button_frame = tk.Frame(options_frame)
            button_frame.pack(fill = tk.X, pady = 5)


            radio = tk.Radiobutton(
                button_frame,
                text = display_text,
                variable = selected_option,
                value = f"{display_text}",
                font = ("Arial", 11, "bold"),
            ).pack(anchor = "w")
            selected_option.get()


            tk.Label(
                button_frame,
                text = f"{description}",
                font = ("Arial", 9),
                foreground = "gray",
            ).pack(anchor = "w", padx = 20)


            # 'Show the Chart' button to show the chart to user.  
            tk.Button(
                button_frame,
                text = "Show the Chart",
                command = lambda: [
                    options_window.destroy(),
                    self.show_chart_comparison5(crypto_data, selected_option)
                ],
                background = "green",
                foreground = "white",
                font = ("Arial", 11, "bold"),
                padx = 20,
                pady = 5
            ).pack(side = tk.LEFT)

            # 'Cancel' button for the user if he regrets to see the chart of the coin.
            tk.Button(
                button_frame,
                text = "Cancel",
                command = options_window.destroy,
                background = "red",
                foreground = "white",
                font = ("Arial", 11, "bold"),
                padx = 20,
                pady = 5
            ).pack(side = tk.RIGHT)



    # Show the chart of the selected coin with the top coins.
    def show_chart_comparison5(self, crypto_data, selected_option):
        # Get the actual value from the StringVar.
        selected_option_var = selected_option.get()

        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"Top Cryptos Comparison - {selected_option_var}")
        chart_window.geometry("1000x700")


        # Select the top 5 coins from the Data Frame.
        top5 = self.df.head(5).copy()


        # Get top 5 cryptos (excluding selected one if it's between top 5).
        selectedcoin = crypto_data['Name']
        if selectedcoin in top5['Name'].values:
            # Keep top 4 (without the selected coin) + selected coin. 
            top4 = top5[top5['Name'] != selectedcoin].head(4)
            selected_data = top5[top5['Name'] == selectedcoin]
            display_data = pd.concat([selected_data, top4])
        else:
            # Keep top 5 and add the selected coin as 6th in the position of the previous coin. 
            top4 = top5.head(5)
            selected_row = self.df[self.df['Name'] == selectedcoin].iloc[0:1]
            display_data = pd.concat([selected_row, top4])


        # TO hold only five coins and no more.
        display_data = display_data.head(6)


        # Extract names for teh X-axis.
        names = display_data['Name'].tolist()


        # Define a mapping for finding more efficiently the column from the selected option which user selects.
        required_columns = {
            "Price": "Price",
            "Market Cap": "Market Cap",
            "24h Change (%)": "24h",
            "7d Change (%)": "7d"
        }
        column_name = required_columns[selected_option_var]



        # Process data based on the selected option of the user for the window of the chart.
        if selected_option_var == "Price":
            values = display_data[column_name].str.replace("[\\$,]", "", regex = True).astype(float).tolist()
            ylabel = "Price ($)"
            title = f"Bar Chart Comparison: {selectedcoin} vs Top Cryptos"
        elif selected_option_var == "Market Cap":
            values = display_data[column_name].replace("[\\$,]", "", regex = True).astype(float).tolist()
            ylabel = "Market Cap ($)"
            title = f"Bar Chart Comparison: {selectedcoin} vs Top Cryptos"
        elif selected_option_var == "24h Change (%)":
            values = display_data[column_name].str.replace("%", "", regex = True).tolist()
            ylabel = "Price change in the last 24 hours"
            title = f"Line Plot Comparison: {selectedcoin} vs Top Cryptos"
        elif selected_option_var == "7d Change (%)":
            values = display_data[column_name].str.replace("%", "", regex = True).tolist()
            ylabel = "Price change in the last 7 days"
            title = f"Line Plot Comparison: {selectedcoin} vs Top Cryptos"
        


        # Create the size of the chart.
        fig, ax = plt.subplots(figsize = (14, 8))



        # Create colors for the rest of the other coins and highlight the selected one.
        colors = []
        for name in names:
            if name == selectedcoin:
                colors.append("orange")
            else:
                colors.append("steelblue")


        # Create a bar to represent the situation between these 5 coins.
        line = ax.plot(names,
            values,
            color = "yellow" 
        )



        # Add the title and the tags for the axes.
        ax.set_title(title, fontsize = 16, fontweight = "bold", pad = 20)
        ax.set_ylabel(ylabel, fontsize = 12, fontweight = "bold")
        ax.set_xlabel("Name", fontsize = 12, fontweight = "bold")


        # Add grid for better readability.
        ax.grid(True, alpha = 0.3)
        ax.set_axisbelow(True)
        plt.xticks(rotation = 45, ha = "right")


        # Adjust layout.
        plt.tight_layout()


        # Set colors for background of the chart.
        ax.set_facecolor("white")
        ax.patch.set_facecolor("black")




        chart_frame = tk.Frame(chart_window)
        chart_frame.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)


        canvas = FigureCanvasTkAgg(ax.get_figure(), master = chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)


    # Asking chatbot for help.
    def open_chatbot(self):
        chatbot = CryptoChatbot()
        chatbot.start_chat()





if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = CryptoGUI(root, "crypto_data.csv")
    root.mainloop()