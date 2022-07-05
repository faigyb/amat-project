import pandas as pd

import extractImages
import visualize_DB
selected_classes = [1, 2, 4, 14, 17]

# extractImages.load_all_data(r'C:\amatProject',selected_classes)
# extractImages.add_our_pictures(r'C:\Users\biali\Pictures\Camera Roll',r'C:\amatProject\our_resized_images')
extractImages.add_one_image(r'C:\faigy bootcamp\basic-original.png',r'C:\amatProject\our_resized_images')

#extractImages.create_labels_json()
# visualize_DB.class_samples_number()