import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
import tempfile
import shutil
import os

# Create four different signals with different colors
signal1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
signal2 = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1])
signal3 = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5])
signal4 = np.array([2, 7, 1, 8, 2, 8, 4, 6, 9])

# Calculate statistics for each signal
def calculate_statistics(signal):
    mean_value = np.mean(signal)
    median_value = np.median(signal)
    max_value = np.max(signal)
    min_value = np.min(signal)
    return mean_value, median_value, max_value, min_value

mean1, median1, max1, min1 = calculate_statistics(signal1)
mean2, median2, max2, min2 = calculate_statistics(signal2)
mean3, median3, max3, min3 = calculate_statistics(signal3)
mean4, median4, max4, min4 = calculate_statistics(signal4)

# Create a PDF file
pdf_file = "individual_signals_with_stats.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# Create a temporary directory for saving plot images
temp_dir = tempfile.mkdtemp()

# Define a list of signals with their names, colors, and statistics
signals = [
    (signal1, "Signal 1", "blue", mean1, median1, max1, min1),
    (signal2, "Signal 2", "red", mean2, median2, max2, min2),
    (signal3, "Signal 3", "green", mean3, median3, max3, min3),
    (signal4, "Signal 4", "purple", mean4, median4, max4, min4)
]

# Loop through each signal and create a plot, take a screenshot, and add details to the PDF
for idx, (signal, signal_name, color, mean, median, max_val, min_val) in enumerate(signals):
    # Create a Matplotlib plot
    plt.figure(figsize=(8, 4))
    plt.plot(signal, label=signal_name, color=color)
    plt.title(f"{signal_name} Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()

    # Save the Matplotlib plot as an image
    image_path = tempfile.mktemp(suffix=".png", dir=temp_dir)
    plt.savefig(image_path, format="png", bbox_inches="tight")

    # Add the Matplotlib plot image to the PDF
    c.drawImage(image_path, 100, 350, width=400, height=200)

    # Add statistics for the current signal to the PDF
    c.setFont("Helvetica", 12)
    c.drawString(100, 250, f"{signal_name} Statistics:")
    c.drawString(120, 230, f"Mean: {mean:.2f}")
    c.drawString(120, 210, f"Median: {median}")
    c.drawString(120, 190, f"Maximum: {max_val}")
    c.drawString(120, 170, f"Minimum: {min_val}")

    # Close the Matplotlib plot and clean up the temporary directory and file
    plt.close()
    os.remove(image_path)

    # Add a new page for the next signal (except on the last iteration)
    if idx < len(signals) - 1:
        c.showPage()

# Save the PDF file
c.save()

# Remove the temporary directory
shutil.rmtree(temp_dir)

print(f"Individual signals with statistics saved as {pdf_file}")
