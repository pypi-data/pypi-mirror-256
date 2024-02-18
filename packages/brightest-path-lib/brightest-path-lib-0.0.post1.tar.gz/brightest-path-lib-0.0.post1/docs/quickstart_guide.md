# Quick Start Guide

Follow these steps to quickly get started with `brightest-path-lib`:

### 1. Install the library using pip

```sh
pip install brightest-path-lib
```

### 2. Import the library in your Python code

```python
import brightest_path_lib
```

### 3. Load your image using your preferred image loading library (e.g., skimage, matplotlib, PIL, OpenCV, etc.)

Here's an example of loading an image using skimage.

**Important** Loading sample data from skimage  also requires the `pooch` package. So before you run the code, be sure to install `pooch`` with:

```sh
pip install pooch
```

```python
from skimage import data

image = data.cells3d()[30, 0]
```

### 4. Define the start and end points for the brightest path search

Here's an example:

```python
import numpy as np
start = np.array([0,192])
goal = np.array([198,9])
```

### 5. Instantiate the algorithm to use for the search. You can choose between A\* Search and New Bidirectional A\* Search (NBA\* Search)

Here's an example:

```python
import brightest_path_lib.algorithm
```

```python
algorithm = brightest_path_lib.algorithm.AStarSearch(image, start, goal)
```

or

```python
algorithm = brightest_path_lib.algorithm.NBAStarSearch(image, start, goal)
```

### 6. Run the brightest path search and retrieve the path

```python
path = algorithm.search()
```

This will return a list of (y, x) coordinates that make up the brightest path between the start and goal points. If you run the algorithm for 3D images, the coordinates will be of the form (z, y, x)

### 7. Visualize the result

Here's an example of visualizing the path on the original image using `matplotlib`

```python
import matplotlib.pyplot as plt

# displaying the image, start and end points
plt.imshow(image, cmap='gray')
plt.plot(start[1], start[0],'og')
plt.plot(goal[1], goal[0], 'or')

# plotting the path
yPlot = [point[0] for point in path]
xPlot = [point[1] for point in path]
plt.scatter(xPlot, yPlot, c='y', s=4, alpha=0.5)
plt.show()
```

That's it! With these simple steps, you can quickly get started using `brightest-path-lib` to find the brightest path between two points in your image.
