# Chapter 8
## 8.1 Understanding Basic Physics
Set working directory
```python
import os
new_directory = <'/your/path/to/Ch07'>
os.chdir(new_directory)
```
Open a stage
```python
from pxr import Usd, UsdGeom, Gf, Sdf, UsdPhysics

usd_file_path ='./physics.usda'
stage = Usd.Stage.Open(usd_file_path)    
```
Print the path of mesh 
```python
for prim in stage.Traverse():    
    if UsdGeom.Mesh(prim):    
        print(prim.GetPath().pathString)   
```
### 8.1.1 Computing Bounding Boxes
Function to compute the bounding box (same in Chapter 5, Listing 5.4)
```python
def compute_bounding_box(stage, prim_path):    
    prim = stage.GetPrimAtPath(prim_path)
    purposes = [UsdGeom.Tokens.default_]    
    bboxcache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), purposes)    
    bboxes = bboxcache.ComputeWorldBound(prim)    
    min_point = bboxes.ComputeAlignedRange().GetMin()
    max_point = bboxes.ComputeAlignedRange().GetMax()    
    return min_point, max_point    
```
Compute the bounding box and set the Extent of the meshes
```python
prim_paths = ['/World/Sphere/Sphere_mesh', '/World/Cube/Cube_mesh']
for path in prim_paths:    
    min_point, max_point = compute_bounding_box(stage, path)    
    mesh = UsdGeom.Mesh(stage.GetPrimAtPath(path))    
    mesh.CreateExtentAttr([min_point, max_point])    

stage.Save()
```
### 8.1.2 Applying Physical Properties
Add a rigid body to the cube and sphere
```python
for path in prim_paths:    
    prim = stage.GetPrimAtPath(path)  
    UsdPhysics.RigidBodyAPI.Apply(prim)  

stage.Save()
```
Give a collider to the cube and sphere
```python
for path in prim_paths:    
    prim = stage.GetPrimAtPath(path)    
    UsdPhysics.CollisionAPI.Apply(prim)    

stage.Save()
```
Add mesh collision to the sphere
```python
sphere_mesh_path = '/World/Sphere/Sphere_mesh'
sphere_prim = stage.GetPrimAtPath(sphere_mesh_path)    

mesh_collision_api = UsdPhysics.MeshCollisionAPI.Apply(sphere_prim)    

mesh_collision_api.GetApproximationAttr().Set("boundingSphere")   

stage.Save()
```
Add mass to the sphere
```python
mass_api = UsdPhysics.MassAPI.Apply(sphere_prim)    
mass_api.CreateMassAttr().Set(10000.0)    

stage.Save()
```
Add mass to the cube
```python
cube_mesh_path = '/World/Cube/Cube_mesh'
cube_prim = stage.GetPrimAtPath(cube_mesh_path)    

mass_api = UsdPhysics.MassAPI.Apply(cube_prim)    
mass_api.CreateMassAttr().Set(100000.0)    

stage.Save()
```
### 8.1.3 Defining Physics Materials
Create and set the physics-specific attributes
```python
from pxr import UsdShade   

physics_material = UsdShade.Material.Define(stage, "/World/PhysicsMaterial")   
physics_material_api = UsdPhysics.MaterialAPI.Apply(physics_material.GetPrim())   

physics_material_api.CreateStaticFrictionAttr().Set(0.9)	
physics_material_api.CreateDynamicFrictionAttr().Set(0.8)	
physics_material_api.CreateRestitutionAttr().Set(1.0)	

stage.Save()
```
Bind the physics material to the sphere prim
```python
sphere_prim = stage.GetPrimAtPath("/World/Sphere/Sphere_mesh")	
sphere_prim.CreateRelationship("material:binding:physics").AddTarget(physics_material.GetPath())   

stage.Save()
```
Bind the physics material to the cube prim
```python
cube_prim = stage.GetPrimAtPath("/World/Cube/Cube_mesh")    
cube_prim.CreateRelationship("material:binding:physics").AddTarget(physics_material.GetPath())    

stage.Save()
```
Edit physical attributes values
```python
physics_material_api.GetStaticFrictionAttr().Set(0.1)    
physics_material_api.GetDynamicFrictionAttr().Set(0.05)    
physics_material_api.GetRestitutionAttr().Set(0.1)    

stage.Save()
```
Set the combination mode
```python
physics_material_api.GetRestitutionAttr().Set(1.0)    

physics_material.GetPrim().CreateAttribute("physxMaterial:restitutionCombineMode", Sdf.ValueTypeNames.Token).Set("max")   
physics_material.GetPrim().CreateAttribute("physxMaterial:frictionCombineMode", Sdf.ValueTypeNames.Token).Set("min")    

stage.Save()
```
### 8.2.1 Building the Swinging Sticks
Setting working directory
```python
import os
new_directory = <'/your/path/to/Ch07'>
os.chdir(new_directory)
```
Load the stage for Swing Sticks
```python 
from pxr import Usd, UsdGeom, Gf, UsdPhysics 

usd_file_path = './swinging_sticks.usda'
stage = Usd.Stage.Open(usd_file_path)    
```
Set RigidBody and Colliders on two sticks
```python 
prim_paths = ['/root/swing/stick1', '/root/swing/stick2']    
for path in prim_paths:    
    sticks = stage.GetPrimAtPath(path)  
    UsdPhysics.RigidBodyAPI.Apply(sticks)  
    UsdPhysics.CollisionAPI.Apply(sticks)   
```
Add a join to stick 1
```python 
revolute_joint1 = UsdPhysics.RevoluteJoint.Define(stage, "/root/swing/stick1/joint1") 

revolute_joint1.CreateBody0Rel().SetTargets(["/root/swing/support_fulcrum"])    
revolute_joint1.CreateBody1Rel().SetTargets(["/root/swing/stick1"])    
revolute_joint1.CreateAxisAttr(UsdGeom.Tokens.y)    

stage.Save()
```
Set the second joint to the end of stick1.
```python
revolute_joint2 = UsdPhysics.RevoluteJoint.Define(stage, "/root/swing/stick2/joint2")  

revolute_joint2.CreateBody0Rel().SetTargets(["/root/swing/stick1"])    
revolute_joint2.CreateBody1Rel().SetTargets(["/root/swing/stick2"])    
revolute_joint2.CreateAxisAttr(UsdGeom.Tokens.y)    

joint2_prim = revolute_joint2.GetPrim() 
joint2_prim.GetAttribute("physics:localPos0").Set(Gf.Vec3d(0.038, -1.823, 0.54)) 

stage.Save()
```

