import numpy as np
import math
from PIL import Image

import random
from tqdm import tqdm

import cv2
import matplotlib.pyplot as plt

import os
import sys
import psutil
import time

class Simulate():

    def __init__(self, dim = 1000, visualize = False):
        
        self.dim = dim
        self.max_dim = 100000

        self.parasite_img = None
        self.veins_img = None

        self.parasite_center_height = None
        self.parasite_center_width = None
        self.parasite_radius = None

        self.parasite_area = None
        self.veins_area = None

        self.visualize = visualize


    def fake_parasite(self):
        
        # Storing dimensions
        height = min(self.dim, self.max_dim)
        width = min(self.dim, self.max_dim)
        area = height * width
 
        # Generating center coordinates and radius for the fake parasite
        # the number 6 just works really well to make sure to stay away from the borders while generating fake parasites
        self.parasite_center_height = random.randint(int(height//6), height - int(height//6))
        self.parasite_center_width = random.randint(int(width//6), width - int(width//6))
        self.parasite_radius = int(random.uniform(0.45, 0.55) * height)

        # Creating an image with a parasite in it
        self.parasite_img = np.full((height, width), 0, dtype=np.uint8)
        #print("Numpy array size is", sys.getsizeof(self.parasite_img), "and max value is", np.max(self.parasite_img))

        cv2.circle(self.parasite_img, (self.parasite_center_width, self.parasite_center_height), self.parasite_radius, 1, thickness = -1)

        # Calculating the area of the parasite
        self.parasite_area = np.sum(self.parasite_img)

        # Converting to 1 Bit size
        # self.parasite_img = Image.fromarray(self.parasite_img).convert("1")
        # print("PIL array size is", sys.getsizeof(self.parasite_img), "and max value is", np.max(np.asarray(self.parasite_img)))

        # Visualize the parasite
        if self.visualize and self.dim < 50001:             # Don't Visualise if the dimensions are more than 50,000
            plt.imshow(np.asarray(self.parasite_img), cmap = 'gray')
            print("Displaying the parasite with area", self.parasite_area)
            plt.show()

        print("Fake parasite generated.")

        return self.parasite_img

    def fake_veins(self, num_of_vein_nodes = 4, num_of_veins_per_node = 10, has_cancer = True):

        # Storing dimensions
        height = min(self.dim, self.max_dim)
        width = min(self.dim, self.max_dim)
        area = height * width

        # If information not avalable... Generate it to avoid errora
        if not self.parasite_radius:
            print("Center infomation not available. Generating...")
            self.parasite_center_height = random.randint(int(height//6), height)
            self.parasite_center_width = random.randint(int(width//6), width)
            self.parasite_radius = int(random.uniform(0.45, 0.55) * height)

        self.veins_img = np.full((height, width), 0, dtype = np.uint8)


        # Generate starting points for the veins to expand from. Always including the center point
        veins_starting_points = [(self.parasite_center_width, self.parasite_center_height)]
        for i in range(num_of_vein_nodes):
            random_x = random.randint(self.parasite_center_width - self.parasite_radius, self.parasite_center_height + self.parasite_radius)
            random_y = random.randint(self.parasite_center_width - self.parasite_radius, self.parasite_center_height + self.parasite_radius)
            veins_starting_points.append((random_x, random_y))

        # Drawing lines as veins
        for vein_node in veins_starting_points:

            start_x = vein_node[0]
            start_y = vein_node[1]

            for i in range(num_of_veins_per_node):

                
                # end_x = random.randint(self.parasite_center_width - self.parasite_radius, self.parasite_center_height + self.parasite_radius)
                # end_y = random.randint(self.parasite_center_width - self.parasite_radius, self.parasite_center_height + self.parasite_radius)

                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                if self.dim >= 100000:
                    cancer_thick = 50
                    non_cancer_thick = 5
                else:
                    cancer_thick = 10
                    non_cancer_thick = 3
                
                if has_cancer:
                    # Generate a case of having cancer
                    cv2.line(self.veins_img, (start_x, start_y), (end_x, end_y), 1, thickness = cancer_thick)
                else:
                    # Generate a case of not having cancer
                    cv2.line(self.veins_img, (start_x, start_y), (end_x, end_y), 1, thickness = non_cancer_thick)

        self.veins_area = np.sum(self.veins_img)

        if self.visualize and self.dim < 50001:             # Don't Visualise if the dimensions are more than 50,000
            plt.imshow(self.veins_img, cmap = 'gray')
            print("Displaying the Veins with dye with area", self.veins_area)
            plt.show()

        print("Fake veins generated.")

        return self.veins_img
    

    def calculate_cancer(self):
        
        total_area =  np.sum(self.parasite_img * self.veins_img)
        return (total_area / self.parasite_area) * 100


if __name__ == '__main__':

    # To see time and space taken
    process = psutil.Process()
    tock = time.time()

    # Constructing the object
    #simulate = Simulate(dim = 100000, visualize = True)
    simulate = Simulate(dim = 20000, visualize = True)

    # Running the simulation
    parasite_img = simulate.fake_parasite()
    veins_img = simulate.fake_veins(num_of_vein_nodes = 8, num_of_veins_per_node = 50, has_cancer = False)
    overlap = simulate.calculate_cancer()

    tick = time.time()
    print(process.memory_info().rss, "bytes used.")  # in bytes
    print("Overall time taken", tick - tock, "seconds.")

    # Deleting the object to store space before starting the next example
    print("Clearing up RAM...")
    del simulate
    
    # Results
    print("Overlaping found to be", overlap, "percent.")
    if overlap >= 10.0:
        print("******CANCER DETECTED******")
        
        # Saving images if needed
        print("Saving both the images...")
        cv2.imwrite("parasite.jpg", parasite_img * 255)
        cv2.imwrite("veins.jpg", veins_img * 255)
    else:
        print("******cancer NOT detected******")
        print("Saving parasite image")
        cv2.imwrite("parasite.jpg", parasite_img * 255)

    print("Done")