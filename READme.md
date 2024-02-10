# Submission to the Coding Challenge by Tejas Kalsait

This repository contains code for efficient representation of microscope and dye sensor images, creation of simulated images, parasite cancer detection, optimization for speed, and exploration of compression techniques.

I have used a 2-dimensional NumPy array (ignoring the third dimension to save space) and used uint8 datatype.

# Creation of Simulated Images

### Simulating a parasite that is randomized but always consumes more than 25% space
![alt text](https://github.com/TejasKalsait/CodingChallenge/blob/main/parasite.png?raw=true)

### Simulating veins in the parasite
![alt text](https://github.com/TejasKalsait/CodingChallenge/blob/main/veins.png?raw=true)

# Improvements

> [!TIP]
> To truly reduce the time and space complexity of the algorithm, we can use the PIL library and store the pixel values as a single bit.
> For example, Each pixel value will correspond to either True or False that consumes a single bit instead of storing information in 8 bits for each pixel.
> `Doing this would reduce the worst case space complexity from 10GB to 1.25 GB for 100,000x100,100 image`.
> Moreover, we could apply a mask over the image that pools the image (Similar to Convolutional Neural Networks). If we choose the appropriate pool techniques like 1:10 compression we could resuce the size of the image without losing the dye information.
> Since the challenge expects participants to `not spend more than 2 hours`, I have not implemented these techniques yet achieving decent results. (Image below)
> Going forward, I'd love to implement these methods.

### My Results
![alt text](https://github.com/TejasKalsait/CodingChallenge/blob/main/Results.png?raw=true)

# Contact Information
- LinkedIn - https://www.linkedin.com/in/tkalsait/
- Portfolio - https://tejaskalsait.github.io/

# Thank You
