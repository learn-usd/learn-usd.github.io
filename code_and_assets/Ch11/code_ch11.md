# Chapter 11
## 11.2 Fast Rendering by Rasterization
```python
import numpy as np
from PIL import Image
```
```python
from pxr import Gf, Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("render.usd") 

# Move xform to -z axis
xform = UsdGeom.Xform.Define(stage, '/World/icosphere')   
xform.AddTranslateOp().Set(Gf.Vec3f(0, 0, -5)) 

prim = xform.GetPrim()

# Import asset
prim.GetReferences().AddReference(assetPath="<your path to icosphere.usd>") 
```
```python
mesh = UsdGeom.Mesh.Get(stage, "/World/icosphere/Icosphere/mesh")  

# Access mesh vertex data: points, face counts, and indices
vertex_points = mesh.GetPointsAttr().Get()    
vertex_counts = mesh.GetFaceVertexCountsAttr().Get() 
vertex_indices = mesh.GetFaceVertexIndicesAttr().Get()
```
```python
vertex_points = [v + xform.GetTranslateOp().Get() for v in vertex_points]
eye = Gf.Vec3f(0, 0, 1)
```
```python
# Convert 3D point to 2D screen coordinates
def point_to_screen(point: Gf.Vec3f) -> Gf.Vec2f:
    d = (point - eye).GetNormalized()
    t = - eye[2] / d[2]
    x = eye[0] + t * d[0]
    y = eye[1] + t * d[1]
    return Gf.Vec2f(x, y)
```
```python
screen_points = [point_to_screen(p) for p in vertex_points]
```
```python
top_left = Gf.Vec2f(-0.2, 0.2)
resolution = 256
delta = (0.2 + 0.2) / resolution
```
```python
def pixel(i, j):
    return top_left + Gf.Vec2f(i * delta, - j * delta)
```
```python
polygons = [[screen_points[idx] for idx in vertex_indices[3 * i:3 * i + 3]] for i in  range(len(vertex_counts))]
```python

This code loops through all triangles, extracts the three vertex positions for each, and stores them in polygons, which will be used for rendering. 

To correctly render the scene, we need to determine the depth of each polygon, which tells us how far it is from the camera. Since multiple polygons can overlap on the 2D screen, depth information helps us decide which ones should be visible and which should be hidden behind others (a process known as depth sorting or z-buffering). The following code calculates the average depth of each triangle:To determine the color of each pixel on the screen, we first need to check whether a pixel lies inside a polygon. 
```python
polygon_depth = [np.mean([vertex_points[idx][2] for idx in vertex_indices[3 * i: 3 * i + 3]]) for i in range(len(vertex_counts))]
```
```python
polygon_color = [Gf.Vec3f(np.random.rand()*256, np.random.rand()*256, np.random.rand()*256) for i in range(len(vertex_counts))]
```
```python
def is_pixel_in_polygon(pixel, polygon) -> bool:
    x, y = pixel
    num_vertices = len(polygon)
    inside = False

    # Iterate through each edge of the polygon
    j = num_vertices - 1  # Previous vertex index

    for i in range(num_vertices):
        xi, yi = polygon[i]
        xj, yj = polygon[j]

        # Check if the point crosses an edge
        if ((yi > y) != (yj > y)) and \
                (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside

        j = i  # Move to next edge
    return inside
```
```python
print(is_pixel_in_polygon(pixel(0, 0), polygons[0])) # should print `False`
```
```python
image_data = np.zeros(shape = (resolution, resolution, 3), dtype=np.uint8)=
for i in range(resolution):
    for j in range(resolution):
        pixel_color = Gf.Vec3f(0, 0, 0)
        depth = -1e6

        for k in range(len(polygons)):
            polygon = polygons[k]

            if is_pixel_in_polygon(pixel(i, j), polygon):
                if polygon_depth[k] > depth:
                    depth = polygon_depth[k]
                    pixel_color = polygon_color[k]

        image_data[i][j] = pixel_color
```
```python
image = Image.fromarray(image_data, mode="RGB")
image.show()
```
## 11.3 Rendering via Ray Tracing
```python
import numpy as np
from PIL import Image
from pxr import Gf, Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("render.usd") 
xform = UsdGeom.Xform.Define(stage, '/World/icosphere')   
xform.AddTranslateOp().Set(Gf.Vec3f(0, 0, -5)) 

prim = xform.GetPrim()
prim.GetReferences().AddReference(assetPath="./icosphere.usd")

mesh = UsdGeom.Mesh.Get(stage, "/World/icosphere/Icosphere/mesh")  

vertex_points = mesh.GetPointsAttr().Get()    
vertex_counts = mesh.GetFaceVertexCountsAttr().Get() 
vertex_indices = mesh.GetFaceVertexIndicesAttr().Get()
vertex_points = [v + Gf.Vec3f(xform.GetTranslateOp().Get()) for v in vertex_points]
```
```python
triangles = [[vertex_points[idx] for idx in vertex_indices[3 * i:3 * i + 3]] \
    for i in range(len(vertex_counts))]
```
```python
top_left = Gf.Vec3f(-0.2, 0.2, 0) 
resolution = 256
delta = (0.2 + 0.2) / resolution
```
```python
d = (top_left - eye).GetNormalized()
```
```python
v0, v1, v2 = triangles[0]
hit, point = ray_triangle_intersect(eye, d, v0, v1, v2)
```
```python
vertex_normals = mesh.GetNormalsAttr().Get()
triangle_normal_0 = vertex_normals[0:3][0]
```
```python
direction_light = Gf.Vec3f(1, 1, 1).GetNormalized()
ray = Gf.Vec3f(0, 0, 1)
color = Gf.Dot(direction_light,ray)
```
```python
image_data = np.zeros(shape = (resolution, resolution, 3), dtype=np.uint8)
```
```python
for i in tqdm(range(resolution)):
    for j in range(resolution):
        d = top_left + Gf.Vec3f(i * delta, - j * delta, 0) - eye
        d = d.GetNormalized()
        depth = -1e6

        for k in range(len(triangles)):
            v0,v1,v2 = triangles[k]
            intersection, point = ray_triangle_intersect(eye, d, v0, v1, v2)
            if intersection:
                if point[2] > depth:
                    depth = point[2] 
                    normal = vertex_normals[3 * k]
                    reflected = reflect(d, normal)
                    factor = Gf.Dot(light_dir, reflected)

                    if factor > 0:
                        image_data[i][j] = [255. * factor, 255. * factor, 255. * factor]
                    else:
                        image_data[i][j] = [50, 50, 50]

```
```python
image = Image.fromarray(image_data, mode="RGB")
image.show() 
```
```python
for i in tqdm(range(resolution)):
    for j in range(resolution):
        d = top_left + Gf.Vec3f(i * delta, - j * delta, 0) - eye
        d = d.GetNormalized()
        depth = -1e6

        for k in range(len(triangles)):
            v0,v1,v2 = triangles[k]
            intersection, point = ray_triangle_intersect(eye, d, v0, v1, v2)

            if intersection:
                if point[2] > depth:
                    depth = point[2] 
                    normal = vertex_normals[3 * k]
                    factors = np.zeros(50)
                    for t in range(50):
                        reflected = reflect(d, normal, randomize=True)
                        factors[t] = Gf.Dot(light_dir, reflected)

                    factor = np.mean(factors)
                    if factor > 0:
                        image_data[i][j] = [255. * factor, 255. * factor, 255. * factor]
                    else:
                        image_data[i][j] = [50, 50, 50]
```
