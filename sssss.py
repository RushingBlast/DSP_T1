import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
import tempfile
import shutil

# Create a sample data
data = [10, 21, 32, 43, 54, 65, 76, 87, 98]

# Calculate statistics
mean_value = np.mean(data)
median_value = np.median(data)
max_value = np.max(data)
min_value = np.min(data)

# Create a Matplotlib plot
plt.plot(data)
plt.title("Matplotlib Plot Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Create a temporary file to save the Matplotlib plot as an image
temp_dir = tempfile.mkdtemp()
image_path = tempfile.mktemp(suffix=".png", dir=temp_dir)
plt.savefig(image_path, format="png", bbox_inches="tight")

# Create a PDF file
pdf_file = "matplotlib_plot_with_stats.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# Add the Matplotlib plot image to the PDF
c.drawImage(image_path, 100, 300, width=400, height=300)

# Add statistics to the PDF
c.setFont("Helvetica", 12)
c.drawString(100, 200, f"Mean: {mean_value:.2f}")
c.drawString(100, 180, f"Median: {median_value}")
c.drawString(100, 160, f"Maximum: {max_value}")
c.drawString(100, 140, f"Minimum: {min_value}")

# Save the PDF file
c.showPage()
c.save()

# Close the Matplotlib plot
plt.close()

# Clean up the temporary directory and file
shutil.rmtree(temp_dir)

print(f"Screenshot with statistics saved as {pdf_file}")