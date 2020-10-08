#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      derekolson
#
# Created:     18/07/2018
# Copyright:   (c) derekolson 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import gdal, gdalconst
from scipy.cluster.vq import *
import matplotlib.pyplot as plt

# Read SAR image into Numpy Array
filename = "//166.2.126.25/teui1/4_Derek/SalmonChallis/LayersForSegmentation/Final_Data/projected/sc_composite.img"
composite = gdal.Open(filename, gdalconst.GA_ReadOnly)
array = composite.ReadAsArray()
print(array.shape)

# Flatten image to get line of values
flatraster = array.flatten()

# Create figure to receive results
fig = plt.figure()
fig.suptitle('K-Means Classification')

# In first subplot add original SAR image
ax = plt.subplot(241)
plt.axis('off')
ax.set_title('Original Image')
plt.imshow(array, cmap = 'gray')

# In remaining subplots add k-means classified images
for i in range(10):
    print "Calculate k-means with ", i+2, " cluster."

    #This scipy code classifies k-mean, code has same length as flattened
    #raster and defines which class the value corresponds to
    centroids, variance = kmeans(flatraster, i+2)
    code, distance = vq(flatraster, centroids)

    #Since code contains the classified values, reshape into SAR dimensions
    codeim = code.reshape(array.shape[0], array.shape[1])

    #Plot the subplot with (i+2)th k-means
    ax = plt.subplot(2,4,i+2)
    plt.axis('off')
    xlabel = str(i+2) , ' clusters'
    ax.set_title(xlabel)
    plt.imshow(codeim)

plt.show()