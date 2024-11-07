# Import Libraries
import tkinter as tk
import pandas as pd
from tkinter import messagebox


# Load Data
data = pd.read_excel("./data/bearing_data.xlsx")


# Initialize the main window
root = tk.Tk()
root.title("Bearing Inventory Search")

# Initialize a variable to hold current results for sorting
current_result = data.copy()


# Search function
def search():
    search_term = entry.get()

    # Handle empty search input
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a bearing number or car type to search.")
        return
    
    # Filter results based on the search term
    try:
        if search_term.isdigit():  # Assuming bearing numbers are numeric
            result = data[data['BearingNumber'] == int(search_term)]
        else:
            result = data[data['CarType'].str.contains(search_term, case=False)]
    except Exception as e:
        messagebox.showerror("Search Error", f"An error occurred: {e}")
        return
    

    # Display no results message if applicable
    if result.empty:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No results found.\n")
        current_result = data.copy()  # Reset to full data in case of empty result
        return
    
    # Update current_result and display it
    current_result = result
    display_data(current_result)



# Sorting function for quantity and price that works on current results
def sort_by(column_name):
    global current_result
    current_result = current_result.sort_values(by=column_name, ascending=True)
    display_data(current_result)


# Clear search results and show full data
def clear_search():
    global current_result
    entry.delete(0, tk.END)  # Clear the search entry
    current_result = data.copy()  # Reset to full data
    display_data(current_result)



# Display data function for sorting and initial load
def display_data(dataset):
    # clear the text widget and add headers
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"{'Bearing':<8} {'Warehouse':<9} {'Grid':<5} {'Car':<6} {'Price':<5} {'Quantity':<5}\n")
    result_text.insert(tk.END, "-"*60 + "\n")

    # Display each row in the dataset
    for _, row in dataset.iterrows():
        result_text.insert(tk.END, f"{row['BearingNumber']:<8} {row['Warehouse']:<9} {row['Grid']:<5} {row['CarType']:<6} {row['Price']:<5} {row['Quantity']:<5}\n")



# GUI layout
entry_label = tk.Label(root, text="Enter Bearing Number or Car Type")
entry_label.pack()

entry = tk.Entry(root)
entry.pack()

search_button = tk.Button(root, text="Search", command=search)
search_button.pack()

# Sorting buttons
sort_quantity_button = tk.Button(root, text="Sort by Quantity", command=lambda: sort_by('Quantity'))
sort_quantity_button.pack()

sort_price_button = tk.Button(root, text="Sort by Price", command=lambda: sort_by('Price'))
sort_price_button.pack()

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_search)
clear_button.pack()

# Result display area with scrollbar
result_text = tk.Text(root, height=20, width=60)
scrollbar = tk.Scrollbar(root, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


# Display initial data sorted by BearingNumber
display_data(data)

root.mainloop()