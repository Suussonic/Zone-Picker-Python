import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pyperclip
import matplotlib.pyplot as plt

# Fonction pour sélectionner un fichier image
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    return file_path

# Fonction pour afficher l'image et sélectionner une zone par deux clics
def interactive_selection(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(img)
    
    points = []  # Stocke les deux points cliqués
    rect_patch = None  # Stocke le rectangle dessiné
    point_markers = []  # Stocke les marqueurs des points
    
    def on_click(event):
        nonlocal rect_patch
        if event.xdata is None or event.ydata is None:
            return  # Ignore les clics hors de l'image
        
        points.append((int(event.xdata), int(event.ydata)))
        
        # Afficher le premier point cliqué
        marker, = ax.plot(points[-1][0], points[-1][1], 'bo', markersize=5)
        point_markers.append(marker)
        fig.canvas.draw()
        
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            
            selected_coords = f"{{{x_min}, {y_min}, {x_max - x_min}, {y_max - y_min}}}"
            print(selected_coords)
            pyperclip.copy(selected_coords)
            
            # Dessiner un rectangle sur les bords extérieurs de la sélection
            rect_patch = plt.Rectangle((x_min - 0.5, y_min - 0.5), (x_max - x_min) + 1, (y_max - y_min) + 1,
                                       edgecolor='red', linewidth=2, fill=False)
            ax.add_patch(rect_patch)
            fig.canvas.draw()
            
            points.clear()  # Réinitialiser après la sélection
    
    def on_key(event):
        nonlocal rect_patch
        if event.key == 'ctrl+z' and point_markers:
            # Supprimer les points marqués
            for marker in point_markers:
                marker.remove()
            point_markers.clear()
            
            # Supprimer le rectangle s'il existe
            if rect_patch:
                rect_patch.remove()
                rect_patch = None
            
            fig.canvas.draw()
            points.clear()
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

# Programme principal
if __name__ == "__main__":
    image_path = select_file()
    if image_path:
        interactive_selection(image_path)
