# Chapter 9
## 9.1 Understanding Points in 3D 
Setting working directory
```python
import os
new_directory = <'/your/path/to/Ch08'>
os.chdir(new_directory)
```
Create a new stage and define a Points Prim
```python 
from pxr import Usd, UsdGeom, Gf, Sdf
stage = Usd.Stage.CreateNew("points_example.usda")    

UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)    

points = UsdGeom.Points.Define(stage, "/Points")    

stage.SetDefaultPrim(points.GetPrim())    
```
Populate position data for points
```python
positions = [
    Gf.Vec3f(1.0, 1.0, 1.0), 
    Gf.Vec3f(-1.0, -1.0, -1.0), 
    Gf.Vec3f(2.0, 0.5, 0.0)
]    

points.GetPointsAttr().Set(positions)    

stage.Save()
```
Add width attribute to each point
```python
sizes = [0.5, 0.4, 0.2]    
points.GetWidthsAttr().Set(sizes)    
```
Add the same color attribute to all points
```python
points_prim = points.GetPrim()    

uniform_color = [Gf.Vec3f(0.0, 1.0, 0.0)]    
points_prim.GetAttribute("primvars:displayColor").Set(uniform_color)    

stage.Save()
```
Assign different colors to each point
```python
colors = [
	Gf.Vec3f(1.0, 0.0, 0.0),    
	Gf.Vec3f(0.0, 1.0, 0.0),    
	Gf.Vec3f(0.0, 0.0, 1.0)    
]

primvar = UsdGeom.PrimvarsAPI(points_prim).CreatePrimvar(
	"displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.varying
)    
primvar.Set(colors)    

stage.Save()
```
Add dynamic color variations to points 
```python
z_coordinates = [pos[2] for pos in positions]    

z_min = min(z_coordinates)
z_max = max(z_coordinates)    

def interpolate_color(z):    
	normalized_z = (z - z_min) / (z_max - z_min) if z_max != z_min else 0    
	red = normalized_z    
	blue = 1.0 - normalized_z   
	return Gf.Vec3f(red, 0.0, blue)    

dynamic_colors = [interpolate_color(z) for z in z_coordinates]    

primvar = UsdGeom.PrimvarsAPI(points_prim).CreatePrimvar(
	"displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.varying
)    

primvar.Set(dynamic_colors)    

stage.Save()
```
## 9.2 Converting Point Cloud Datasets to USD
Install 'open3d' package from a terminal within your python virtual environment
```
pip install open3d
```
Verify 'open3d' is installed correctly in terminal
```
python -c "import open3d; print(open3d.__version__)"
```
Start the Python interpreter in the terminal
```
python
```
Install 'open3d' for Google Collab users in Jupyter notebook
```python
!pip install open3d    

import open3d    
print(open3d.__version__)    
```
Import modules, load the point cloud, and get the point data into a list of Gf.Vec3f values 
```python
import open3d as o3d  
from pxr import Usd, UsdGeom, Gf, Sdf

pcd = o3d.io.read_point_cloud("./Assets/bun_zipper_res2.ply")    

points = [Gf.Vec3f(p[0], p[1], p[2]) for p in pcd.points]    
```
Extract color information and create a list
```python
if pcd.has_colors():
	colors = [Gf.Vec3f(c[0], c[1], c[2]) for c in pcd.colors]    
else:
	colors = [Gf.Vec3f(1.0, 1.0, 1.0)] * len(points)  
```
Create a stage to hold point cloud data
```python
stage = Usd.Stage.CreateNew("point_cloud_conversion.usda")   

xform = UsdGeom.Xform.Define(stage, "/ScaledPointCloud")    

points_prim = UsdGeom.Points.Define(stage, "/ScaledPointCloud/Bunny")    
```
Set point positions and color
```python
points_prim.GetPointsAttr().Set(points)    
points_prim.GetPrim().GetAttribute("primvars:displayColor").Set(colors)    

width = 0.01
points_prim.GetWidthsAttr().Set([width] * len(points))    

xform_xform = UsdGeom.XformCommonAPI(xform)
xform_xform.SetScale((100.0, 100.0, 100.0))   

stage.Save()
```
Increase the width of the points 
```python
width = 0.005    
points_prim.GetWidthsAttr().Set([width] * len(points))    

stage.Save()
```
## 9.3 Utilizing PointInstancer
Create a new stage, add a distant light, and define a point instancer
```python
from pxr import Usd, UsdGeom, Gf, UsdLux
stage = Usd.Stage.CreateNew("forest.usda")
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

world = UsdGeom.Xform.Define(stage, "/World")    
stage.SetDefaultPrim(world.GetPrim())    

distant_light = UsdLux.DistantLight.Define(stage, "/World/DistantLight")    
distant_light.AddRotateXYZOp().Set(Gf.Vec3d(60, -25, -35))    
distant_light.CreateIntensityAttr(5000.0)

point_instancer = UsdGeom.PointInstancer.Define(stage, "/World/Instancer")    
```
Import two tree assets and assig xforms using for loop and a path list
```python
prototypes = UsdGeom.Scope.Define(stage, "/World/Prototypes")    

pine_paths = {
    "Pine1": './Assets/Pine1.usd',
    "Pine2": './Assets/Pine2.usd'
}    

for name, path in pine_paths.items():    
    xform = UsdGeom.Xform.Define(stage, f"/World/Prototypes/{name}")    
    xform.GetPrim().GetReferences().AddReference(path)    

prototypes.GetPrim().GetAttribute("visibility").Set("invisible")    

stage.Save()
```
Generate random positions for trees and use the Point Instancer to create instances of the objects.
```python
import random

positions = [Gf.Vec3f(random.randint(0, 1000),    
                      random.randint(0, 1000), 0) for i in range(10 * 2)]   
point_instancer.GetPositionsAttr().Set(positions)   
```
Create an index list for instance and connect to PointInstancer
```python
prototype_names = list(pine_paths.keys())    
prototype_paths = [f"/World/Prototypes/{name}" for name in prototype_names]    

num_instances_per_prototype = 10    
indices = [i for i in range(len(prototype_names)) for _ in range(num_instances_per_prototype)]    
point_instancer.GetProtoIndicesAttr().Set(indices)    

point_instancer.CreatePrototypesRel().SetTargets(prototype_paths)    

stage.Save()
```
Add variations to tree sizes
```python
from pxr import Vt
import math

point_instancer = UsdGeom.PointInstancer(stage.GetPrimAtPath("/World/Instancer"))   

num_instances = len(point_instancer.GetProtoIndicesAttr().Get())    

scales = [Gf.Vec3f(s, s, s)
      	for s in [random.uniform(0.75, 1.25) for _ in range(num_instances)]]    
scales_array = Vt.Vec3fArray(scales)    

point_instancer.GetScalesAttr().Set(scales_array)    

stage.Save()
```
## 9.4 Understanding Curves in 3D 
Define the number of frames in the animation in a dynamic way 
```python
from pxr import Usd, UsdGeom, Gf
import math

stage = Usd.Stage.CreateNew("curves_example.usda")

fps = 24.0    
duration_in_seconds = 5    
num_samples = int(fps * duration_in_seconds)    
stage.SetTimeCodesPerSecond(fps)    
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(num_samples - 1)   

world = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())   
```
Set up the curve 
```python
basis_curves = UsdGeom.BasisCurves.Define(stage, "/World/CurvesExample")    
control_points = [    
	Gf.Vec3f(0, 100, 700),
	Gf.Vec3f(250, 130, 550),
	Gf.Vec3f(500, 160, 525),
	Gf.Vec3f(700, 190, 575),
	Gf.Vec3f(900, 150, 700)
]
basis_curves.GetPointsAttr().Set(control_points)    
basis_curves.GetCurveVertexCountsAttr().Set([len(control_points)])    
basis_curves.GetTypeAttr().Set("cubic")    
basis_curves.GetBasisAttr().Set(UsdGeom.Tokens.bezier)    

stage.Save()
```
Create a camera, and apply a -90° rotation around the x axis
```python
forest = UsdGeom.Xform.Define(stage, '/World/Forest')    
forest_refs = forest.GetPrim().GetReferences()    

forest_refs.AddReference("./forest.usda")    
forest_rotate_op = forest.AddRotateXOp()    
forest_rotate_op.Set(-90)    

camera = UsdGeom.Camera.Define(stage, "/World/Camera")    
cam_xform = UsdGeom.Xformable(camera)    
camera.GetFocalLengthAttr().Set(20)    

stage.Save()
```
Get Bézier curve points
```python
def lerp(a, b, t):
	return a * (1 - t) + b * t   

# Optimized iterative De Casteljau algorithm for Bézier interpolation
def interpolate_bezier(points, t):    
    pts = points[:]  
    n = len(pts)    
    for r in range(1, n):    
        for i in range(n - r):    
            pts[i] = Gf.Vec3f(
                lerp(pts[i][0], pts[i+1][0], t),    
                lerp(pts[i][1], pts[i+1][1], t),    
                lerp(pts[i][2], pts[i+1][2], t)    
            )
    return pts[0] 

def interpolate_positions(points, num_samples):    
	return [interpolate_bezier(points, t / (num_samples - 1)) for t in range(num_samples)]

sampled_positions = interpolate_positions(control_points, num_samples)    
```
Set up the camera's transformation operations
```python
translate_op = None    
rotate_op_cam = None    
for op in cam_xform.GetOrderedXformOps():    
    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
        translate_op = op    
    elif op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:
        rotate_op_cam = op    

if translate_op is None:    
    translate_op = cam_xform.AddTranslateOp()

if rotate_op_cam is None:    
    rotate_op_cam = cam_xform.AddRotateXYZOp()
```
Animate the camera's movement along the curve
```python
look_at_target = Gf.Vec3f(500, 300, -500)    

def compute_euler_angles(eye, target):    
	direction = (target - eye).GetNormalized()    
	yaw = math.degrees(math.atan2(direction[0], direction[2])) + 180  
	pitch = math.degrees(math.asin(direction[1]))  
	roll = 0.0  
	return (pitch, yaw, roll)

# Animate the camera along the curve
for frame in range(num_samples):    
	pos = sampled_positions[frame]    
	translate_op.Set(value=pos, time=frame)    
	euler = compute_euler_angles(pos, look_at_target)    
	rotate_op_cam.Set(value=Gf.Vec3f(euler[0], euler[1], euler[2]), time=frame)   

stage.Save()
```