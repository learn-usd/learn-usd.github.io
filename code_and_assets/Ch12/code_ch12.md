# Chapter 12 
### 12.2.1 Create a Math-Generated Wavy Plane
Setting up the USD stage and defining a mesh:
```python
from pxr import Usd, UsdGeom    
stage = Usd.Stage.CreateNew("wavy_plane.usda"))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)	
wavy_plane = UsdGeom.Mesh.Define(stage, "/World/wavy_plane")		
```
Define the size of the plane, the resolution of the grid, and a height function that generates the wavy surface:
```python
import math
size = 10	
resolution = 50	
def get_height(x, y):	
    return math.sin(0.5 * x) * math.cos(0.5 * y)
```
Generate points for the terrain surface:
```python
points = []	
for x in range(resolution):	
    for y in range(resolution):
        xf = (x / (resolution - 1)) * (2 * size) - size
        yf = (y / (resolution - 1)) * (2 * size) - size	
        z = get_height(xf, yf)	
        points.append((xf, yf, z))	
```
Define vertex points:
```python
faceVertexIndices = []  
faceVertexCounts = []  

for x in range(resolution - 1):  
    for y in range(resolution - 1):
        i0 = x * resolution + y      
        i1 = i0 + 1                  
        i2 = i0 + resolution + 1     
        i3 = i0 + resolution         
        faceVertexIndices.extend([i0, i1, i2, i3])  
        faceVertexCounts.append(4)                 
```
Plug in all the data to the mesh:
```python
wavy_plane.GetPointsAttr().Set(points) 
wavy_plane.GetFaceVertexCountsAttr().Set(faceVertexCounts) 
wavy_plane.GetFaceVertexIndicesAttr().Set(faceVertexIndices)  

stage.Save()  
```
### 12.2.2 Scatter Cubes on the Wavy Plane 
Defining the cube prototype:
```python
proto_cube_path = "/World/Prototypes/Cube"    
cube = UsdGeom.Cube.Define(stage, proto_cube_path)    
cube.CreateSizeAttr().Set(0.3)	
```
Generate positions to place cubes:
```python
import random	
num_instances = 100    
positions = []    
proto_indices = []	
for _ in range(num_instances):
    x = random.uniform(-size, size)
    y = random.uniform(-size, size)
    z = get_height(x, y)    
    positions.append(Gf.Vec3f(x, y, z))	
    proto_indices.append(0)	
```
Assign positions and indices to PointInstancer:
```python
instancer = UsdGeom.PointInstancer.Define(stage, "/World/Instancer")	
instancer.CreatePrototypesRel().SetTargets([proto_cube_path]) 
instancer.CreatePositionsAttr().Set(positions)	
instancer.CreateProtoIndicesAttr().Set(proto_indices)	

stage.Save()
```   
## 12.3 Complex Real Assets and additional controls
See the code in "./usd_scatter_addon/core/scatter.py".
## 12.4 Blender Add-on
See the code in "./usd_scatter_addon/__init__.py".

