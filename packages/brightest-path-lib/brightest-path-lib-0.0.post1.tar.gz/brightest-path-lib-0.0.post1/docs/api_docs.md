# API Documentation

This document provides detailed information about the public API of the `brightest-path` library.

## Search Algorithms

### 1. `AStarSearch`

This class implements the A* search algorithm to find the brightest path between two points in a 2D or 3D image.

#### Parameters

| Parameter            | Type          | Description                                                                                                                                                                                         | Optional |
|----------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `image`              | `numpy.ndarray` | The 2D/3D image on which you will run an A\* search.                                                                                                                                              | No       |
| `start_point`        | `numpy.ndarray` | The 2D/3D coordinates of the start point;  For 2D images, the coordinates are of the form (y, x) For 3D images, the coordinates are of the form (z, x, y)                                           | No       |
| `goal_point`         | `numpy.ndarray` | The 2D/3D coordinates of the goal point; For 2D images, the coordinates are of the form (y, x) For 3D images, the coordinates are of the form (z, x, y)                                             | No       |
| `scale`              | `Tuple`         | The scale of the image; defaults to  `(1.0, 1.0)`, i.e, image is not zoomed in/out For 2D images, the scale is of the form (x, y) For 3D images, the scale is of the form (x, y, z)                 | Yes      |
| `cost_function`      | `Enum`          | The cost function to be used for computing the cost of moving to a new point Default type is `CostFunction.RECIPROCAL` to use the reciprocal function                                               | Yes      |
| `heuristic_function` | `Enum`          | The heuristic function to be used to compute the estimated cost of moving from a  point to the goal; Default type is `HeuristicFunction.EUCLIDEAN` to use the euclidean function for cost estimation | Yes      |
| `open_nodes`         | `Queue`               | contains a list of points that are in the open set, being examined for the brightest path;  can be used by the calling application to show a visualization of where the algorithm is searching currently; Default value is `None` | Yes

Note: All the parameters except `image`, `start_point`, and `goal_point` are optional.

#### Attributes

| Attribute            | Type                  | Description                                                                                                                                                                                              |
|----------------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `is_canceled`        | `Bool`                | should be set to `True` if the search needs to be stopped; `False` by default                                                                                                                            |
| `open_nodes`         | `Queue`               | contains a list of points that are in the open set, being examined for the brightest path;  can be used by the calling application to show a visualization of where the algorithm is searching currently |
| `result`             | `List[numpy ndarray]` | the result of the A\* search containing the list of points that constitute the brightest path  between the given start and goal points                                                                   |

#### Methods

| Method   | Description                                                                                  | Return Type                                                                                             |
|----------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| `search` | Runs the A\* search algorithm to find the brightest path from  `start_point` to `goal_point` | `List[numpy.ndarray]`; the list containing the 2D/3D point coordinates that constitute the brightest path |

Note: Find the code for this class [here](https://github.com/mapmanager/brightest-path-lib/blob/main/brightest_path_lib/algorithm/astar.py).

#### Exceptions

| Exception    | When is it thrown                                                                |
|--------------|----------------------------------------------------------------------------------|
| `TypeError`  | If the `image` passed is `None` or `start_point` is None or `goal_point` is None |
| `ValueError` | If the length of the `image`, `start_point` or `goal_point` is `0`               |

We recommend you to catch the exceptions thrown by the library and handle them appropriately.

### 2. `NBAStarSearch`

This class implements the NBA* search algorithm to find the brightest path between two points in a 2D or 3D image.

#### Parameters

| Parameter            | Type          | Description                                                                                                                                                                                         | Optional |
|----------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `image`              | `numpy ndarray` | The 2D/3D image on which you will run an A\* search.                                                                                                                                              | No       |
| `start_point`        | `numpy ndarray` | The 2D/3D coordinates of the start point;  For 2D images, the coordinates are of the form (y, x) For 3D images, the coordinates are of the form (z, x, y)                                           | No       |
| `goal_point`         | `numpy ndarray` | The 2D/3D coordinates of the goal point; For 2D images, the coordinates are of the form (y, x) For 3D images, the coordinates are of the form (z, x, y)                                             | No       |
| `scale`              | `Tuple`         | The scale of the image; defaults to  `(1.0, 1.0)`, i.e, image is not zoomed in/out For 2D images, the scale is of the form (x, y) For 3D images, the scale is of the form (x, y, z)                 | Yes      |
| `cost_function`      | `Enum`          | The cost function to be used for computing the cost of moving to a new point Default type is `CostFunction.RECIPROCAL` to use the reciprocal function                                               | Yes      |
| `heuristic_function` | `Enum`          | The heuristic function to be used to compute the estimated cost of moving from a  point to the goal; Default type is `HeuristicFunction.EUCLIDEAN` to use the euclidean function for cost estimation | Yes      |
| `open_nodes`         | `Queue`               | contains a list of points that are in the open set, being examined for the brightest path;  can be used by the calling application to show a visualization of where the algorithm is searching currently; Default value is `None` | Yes

Note: All the parameters except `image`, `start_point`, and `goal_point` are optional.

#### Attributes

| Attribute            | Type                  | Description                                                                                                                                                                                              |
|----------------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `is_canceled`        | `Bool`                | should be set to `True` if the search needs to be stopped; `False` by default                                                                                                                            |
| `open_nodes`         | `Queue`               | contains a list of points that are in the open set, being examined for the brightest path;  can be used by the calling application to show a visualization of where the algorithm is searching currently |
| `result`             | `List[numpy ndarray]` | the result of the A\* search containing the list of points that constitute the brightest path  between the given start and goal points                                                                   |

#### Methods

| Method   | Description                                                                                  | Return Type                                                                                             |
|----------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| `search` | Runs the A\* search algorithm to find the brightest path from  `start_point` to `goal_point` | `List[numpy.ndarray]`; the list containing the 2D/3D point coordinates that constitute the brightest path |

Note: Find the code for this class [here](https://github.com/mapmanager/brightest-path-lib/blob/main/brightest_path_lib/algorithm/nbastar.py).

#### Exceptions

| Exception    | When is it thrown                                                                |
|--------------|----------------------------------------------------------------------------------|
| `TypeError`  | If the `image` passed is `None` or `start_point` is None or `goal_point` is None |
| `ValueError` | If the length of the `image`, `start_point` or `goal_point` is `0`               |

We recommend you to catch the exceptions thrown by the library and handle them appropriately.

## Cost Function

### 1. `Reciprocal`

This class implements the `reciprocal cost function` as the cost to calculate the cost of moving to a point.

The reciprocal function is commonly used as a cost function in pathfinding algorithms. It is calculated as the reciprocal of the intensity of a pixel/voxel at a given location in the image volume.

The intuition behind using the reciprocal function is that we want to give a higher cost to moving to points with lower intensity, as these areas may be less informative or less relevant to the overall goal of the pathfinding task. On the other hand, areas with higher intensity are likely to contain important information and should be favored in the search for the brightest path. Therefore, by taking the reciprocal of the intensity values, we are essentially inverting the cost, so that higher intensity areas have a lower cost, and vice versa. This makes it more likely that the pathfinding algorithm will favor paths that traverse brighter areas of the image volume.

#### Parameters

| Paramater       | Type    | Description                                                   | Optional |
|-----------------|---------|---------------------------------------------------------------|----------|
| `min_intensity` | `float` | The minimum intensity a pixel/voxel can have in a given image | No       |
| `max_intensity` | `float` | The maximum intensity a pixel/voxel can have in a given image | No       |

#### Methods

| Method                                             | Description                              | Return Type |
|----------------------------------------------------|------------------------------------------|-------------|
| `cost_of_moving_to(intensity_at_new_point: float)` | calculates the cost of moving to a point | `float`     |
| `minimum_step_cost()`                                | calculates the minimum step cost         | `float`     |

Find its code [here](https://github.com/mapmanager/brightest-path-lib/blob/main/brightest_path_lib/cost/reciprocal.py).

#### Exceptions

| Exception    | When is it thrown                                                                |
|--------------|----------------------------------------------------------------------------------|
| `TypeError`  | If the `min_intensity` or `max_intensity` is `None` |
| `ValueError` | If `min_intensity > max_intensity`               |

We recommend you to catch the exceptions thrown by the library and handle them appropriately.

## Heuristic Function

### 1. `Euclidean`

A heuristic function is used to estimate the cost of moving from a given point to the goal point. The Euclidean distance is a measure of the straight-line distance between two points in a Euclidean space, such as the 2D or 3D space of an image.

Using the Euclidean distance as a heuristic function is effective because it provides an admissible and consistent estimate of the actual cost of moving from a given point to the goal point. An admissible heuristic is one that never overestimates the cost of reaching the goal, and a consistent heuristic is one that satisfies the triangle inequality, i.e., the estimated cost of moving from one point to another is always less than or equal to the sum of the estimated cost of moving from the first point to the goal plus the estimated cost of moving from the second point to the goal. By using a consistent heuristic, we can ensure that the pathfinding algorithm will always find the optimal path from the start point to the goal point.

#### Parameters

| Parameter | Type    | Description                                                                                                                                                           | Optional |
|-----------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| `scale`   | `Tuple` | the scale of the image's axes. For example (1.0 1.0) for a 2D image. - for 2D points, the order of scale is: (x, y) - for 3D points, the order of scale is: (x, y, z) | No       |

#### Methods

| Method                                                                       | Description                              | Return Type | Note                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------------|------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `estimate_cost_to_goal(current_point: numpy.ndarray, goal_point: numpy.ndarray)` | calculates the cost of moving to a point | `float`     | If the image is zoomed in or out, then the scale of one of more axes  will be more or less than 1.0. For example, if the image is zoomed in to twice its size then the scale of X and Y axes will be 2.0. <br>         By including the scale in the calculation of distance to the goal we can get an accurate cost. <br> - for 2D points, the order of coordinates is: (y, x) - for 3D points, the order of coordinates is: (z, x, y) |

Find its code [here](https://github.com/mapmanager/brightest-path-lib/blob/main/brightest_path_lib/heuristic/euclidean.py).

#### Exceptions

| Exception    | When is it thrown                                                                |
|--------------|----------------------------------------------------------------------------------|
| `TypeError`  | If the `current_point` or `goal_point` is `None` |
| `ValueError` | If the length of `current_point` or `goal_point` is `0`               |
