# Porosity characterization of Coke images

Automatically determine porosity of a Coke Microstructure from its image.

### Challenges in Computer Vision for Processing Coke Microstructure Images:

<table>
  <tr>
    <th>Challenge</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Identification of pores</td>
    <td>Minerals and pores are both in black color.
        <br>Minerals are embedded inside binders and fillers, reflections from the bottom of the pores, seen using microscope, appear in lighter shre in the Coke images. 
        <br>Pores are big and round (long when multiple pores are joined together), and have reflections from bottom inside them.
        <br>Minerals are smaller and thinner and irregular.
    </td>
  </tr>
    <tr>
    <td>Porosity characterization</td>
    <td>To calculate average porosity of the Coke microstructure, pairwise distances between each pores among all points in the pores' borders are to be measured.</td>
  </tr>

</table>
 

### Source codes :

<table>
  <tr>
    <th>Program name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Coke_Porosity_histogram.py</td>
    <td>Program for porosity calculation of a coke image, using NumPy, OpenCV, skimage and shapely.         
      The program identifies the pores (large, circular black regions having reflections from bottom), then draws green border on the polygonal approximation of the pores, and calculates distances between each vertices of these polygons (line drawn in yellow), that does not cross any pore. With these distances, it creates a histogram of pore distances. This histogram can be examined to understand the porosity of the coke.</td>
  </tr>
    <tr>
    <td>Coke_Porosity_histogram_OpenCV.py</td>
    <td>Same functionality as above, using NumPy, OpenCV and Shapely.</td>
  </tr>

</table>

****
### Results :

<table>
  <tr>
    <th>Original image</th>
    <th>Pores</th>
    <th>Distances</th>
    <th>Porosity histogram</th>
  </tr>
  <tr>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053.jpg" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_HE_Otsu_pores.bmp" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_pore_distances.png" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_porosity histogram.png" height=200 width= 300></td>
  </tr>
    <tr>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0001.jpg" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0001_HE_Otsu_pores.bmp" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0001_pore_distances.png" height=200 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0001_porosity histogram.png" height=200 width= 300></td>
  </tr>

</table>
