# Image-Segmentation

## Calculate porosity of a Coke from its image.

<table>
  <tr>
    <td>Program name</td>
    <td>Description</td>
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

<table>
  <tr>
    <td>Original image</td>
    <td>Pores</td>
    <td>Distances</td>
    <td>Porosity histogram</td>
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
