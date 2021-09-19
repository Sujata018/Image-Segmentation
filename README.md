# Image-Segmentation

## Calculate porosity of a Coke from its image.

<table>
  <tr>
    <td>Program name</td>
    <td>Description</td>
  </tr>
  <tr>
    <td>Coke_Porosity_histogram.py</td>
    <td>The program identifies the pores (large, circular black regions having reflections from bottom), then draws green border on the polygonal approximation of the pores, and calculates distances between each vertices of these polygons (line drawn in yellow), that does not cross any pore. With these distances, it creates a histogram of pore distances. This histogram can be examined to understand the porosity of the coke.</td>
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
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053.jpg" height=300 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_HE_Otsu_pores.bmp" height=300 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_pore_distances.png" height=300 width= 300></td>
    <td><img src="https://github.com/Sujata018/Image-Segmentation/blob/main/images/s_0053_porosity histogram.png" height=300 width= 100></td>
  </tr>
</table>
