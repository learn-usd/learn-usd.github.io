# Chapter 6
## 6.1 Revisiting Xforms
Create a stage
```python
from pxr import Usd, UsdGeom, Gf, Sdf
stage = Usd.Stage.CreateNew("xform.usd")
xform = UsdGeom.Xform.Define(stage, "/World/Xform")
```
A function to create a Prim by type 
```python
def create_prim(stage: Usd.Stage, prim_path: str, prim_type: str):    
    return stage.DefinePrim(prim_path, prim_type)    
```
Use the function to create an Xform
```python
create_prim(stage, "/World/Xform", "Xform")
```
Capture the return value of the create_prim function as a variable
```python
light_prim = create_prim(stage, "/Lights/DistantLight", "DistantLight") 
```
Accesses the Xform of the light_prim
```python
xform_light = UsdGeom.Xformable(light_prim)
```
Rotate the distant light’s Xform by 50° around the y axis
```python
rotation_op = xform_light.AddRotateXYZOp()   
rotation_op.Set(Gf.Vec3d(0, 50, 0))    
```
### 6.1.1 Understanding Transform Order
Using different transform orders
```python
cube1 = UsdGeom.Cube.Define(stage, "/World/Cube1") 
cube1.AddRotateXYZOp().Set(Gf.Vec3d(45, 0, 0)) 
cube1.AddTranslateOp().Set(Gf.Vec3d(0, 10, 0))

cube2 = UsdGeom.Cube.Define(stage, "/World/Cube2")
cube2.AddTranslateOp().Set(Gf.Vec3d(0, 10, 0))
cube2.AddRotateXYZOp().Set(Gf.Vec3d(45, 0, 0))
```
### 6.1.2 Applying Transform Order
Clear the transform order of an Xform
```python
xform.ClearXformOpOrder()
```
Use 'Quaternion' rotation
```python
xform.AddTranslateOp()
xform.AddOrientOp()   
xform.AddScaleOp()    
```
Check the transform order 
```python
xform_ops = xform.GetOrderedXformOps()    
for op in xform_ops:
    print(op.GetOpName())    
```
Alter a transform based on the order
```python
xform_ops[0].Set(Gf.Vec3d(0,0,0))   
xform_ops[1].Set(Gf.Quatf(1,0,0,0)) 
xform_ops[2].Set(Gf.Vec3d(1,1,1))   
```
Remove the existing order in cube1 
```python 
cube1 = UsdGeom.Xform.Get(stage, '/World/Cube1')    
cube1.ClearXformOpOrder()    
```
Add new transform order to cube1
```python
cube1.AddTranslateOp()
cube1.AddOrientOp()
cube1.AddScaleOp()
```
Check the transform order
```python
xform_ops = cube1.GetOrderedXformOps()   
for op in xform_ops:
    print(op.GetOpName())   
```
Assign new values to cube1’s transform
```python 
xform_ops[0].Set(Gf.Vec3d(0,5,0))    
xform_ops[1].Set(Gf.Quatf(0.92, 0.38, 0, 0))    
xform_ops[2].Set(Gf.Vec3d(2,2,2))    
```
### 6.2.1 Euler Angles
Using Euler angles to represent a rotation
```python
xform.ClearXformOpOrder()    
xform.AddRotateXYZOp().Set(Gf.Vec3d(45, 0, 0))    
```
### 6.2.2 Quaternions
Use a quaternion to represent the orientation of an Xform
```python
xform.ClearXformOpOrder()     
w, x, y, z = (0.92, 0.38, 0, 0)   
xform.AddOrientOp().Set(Gf.Quatf(w, x, y, z))    
```
### 6.2.3 Transform and Rotation Matrices
Add a transform matrix 
```python
matrix = Gf.Matrix4d(0.707, -0.707, 0, 0,
    0.707, 0.707, 0, 0,
    0, 0, 1, 0,
    100,200,0,1)    
xform.MakeMatrixXform().Set(matrix)     
```
### Obtaining World & Local Transforms
Lising 5.2 Get the World Transform Matrix
```python
def get_world_transform(stage: Usd.Stage, prim_path: str):   
    prim = stage.GetPrimAtPath(prim_path)
    xform = UsdGeom.Xformable(prim)    
    time_code = Usd.TimeCode.Default()    
    world_transform: Gf.Matrix4d = xform.ComputeLocalToWorldTransform(time_code)    
    return world_transform    
```
Listing 5.3 Get the Local Transform Matrix 
```python
def get_local_transform(stage: Usd.Stage, prim_path: str):
    prim = stage.GetPrimAtPath(prim_path)
    xform = UsdGeom.Xformable(prim)    
    time_code = Usd.TimeCode.Default()
    local_transformation: Gf.Matrix4d = xform.GetLocalTransformation()    
    return local_transformation    
```
Get the world transform of the prim 'Cube1'
```python
world_transform = get_world_transform(stage, "/World/Cube1")
```
Extract the translation
```python
translation: Gf.Vec3d = world_transform.ExtractTranslation() 
```
Extract the rotation
```python
rotation: Gf.Rotation = world_transform.ExtractRotation() 
```
Extract the quaternion rotation
```python
q: Gf.Quatf = world_transform.ExtractRotationQuat()
```
Extract the scale
```python
rotation_matrix = world_transform.ExtractRotationMatrix()    
scale: Gf.Vec3d = Gf.Vec3d([v.GetLength() for v in rotation_matrix])  
```
Print transform info
```python
print(f"Translation: {translation}\n"  
    f"Rotation (Quaternion): {q}\n"    
    f"Rotation Matrix: {rotation_matrix}\n"
    f"Scale: {scale}")
```
Extract local transformation data
```python
local_transformation = get_local_transform(stage, "/World/Cube1")    
translation_local: Gf.Vec3d = local_transformation.ExtractTranslation()    
```
### 6.3.2 Compute the Bounding Box
Listing 5.4 Compute the Bounding Box 
```
def compute_bounding_box(stage, prim_path):    
    prim = stage.GetPrimAtPath(prim_path)
    purposes = [UsdGeom.Tokens.default_]    
    bboxcache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), purposes)    
    bboxes = bboxcache.ComputeWorldBound(prim)    
    min_point = bboxes.ComputeAlignedRange().GetMin()
    max_point = bboxes.ComputeAlignedRange().GetMax()    
    return min_point, max_point    
```
Apply the function on ‘Cube1’ 
```python
prim_path = "/World/Cube1" 
min_point, max_point = compute_bounding_box(stage, prim_path)   
```
### 6.3.3 An Example Stage
Create a new stage and reference to the dice
```python
from pxr import Usd, UsdGeom, Gf
stage = Usd.Stage.CreateNew("dice_scene.usd")
dice1 =  UsdGeom.Xform.Define(stage, '/World/Dice1')
dice1.GetPrim().GetReferences().AddReference('./Assets/Dice.usd')  
```
Apply new transformations 
```python
dice1.ClearXformOpOrder()    
dice1.AddTranslateOp().Set(Gf.Vec3d(220, 100, 100))
dice1.AddRotateXYZOp().Set(Gf.Vec3d(-180, 0, 90)) 
dice1.AddScaleOp().Set(Gf.Vec3d(1, 1, 1))    
```
Add a new dice through internal reference
```python
dice2=  UsdGeom.Xform.Define(stage, '/World/Dice2') 
dice2.GetPrim().GetReferences().AddInternalReference("/World/Dice1") 
```
‘get_world_transform’ function (same as Lising 5.2)
```python
def get_world_transform(stage: Usd.Stage, prim_path: str):
    prim = stage.GetPrimAtPath(prim_path)
    xform = UsdGeom.Xformable(prim)
    time_code = Usd.TimeCode.Default()
    world_transform: Gf.Matrix4d = xform.ComputeLocalToWorldTransform(time_code)
    return world_transform
```
‘compute_bounding_box’ function (same as Lising 5.4)
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
Retrieve the translation and rotation of 'Dice1'
```python
dice1_transform_matrix = get_world_transform(stage, "/World/Dice1") 
dice1_translation =  dice1_transform_matrix.ExtractTranslation()
dice1_rotation = dice1_transform_matrix.ExtractRotationQuat().GetNormalized()
```
Calculate the bounding box for 'Dice1'
```python
box_min, box_max = compute_bounding_box(stage, "/World/Dice1") 
dice_size = box_max[0] - box_min[0]   
```
Get translations to position 'Dice2' relative to 'Dice1'
```python
dice2_translation = dice1_translation - Gf.Vec3d(dice_size, 0, 0)
```
Add rotation to 'Dice2' to have the correct face facing forwards
```python
further_rotation = Gf.Rotation(Gf.Vec3d(1, 0, 0), 90).GetQuat()
dice2_rotation = further_rotation * dice1_rotation  
```
Apply all the new transforms to 'Dice2'
```python
dice2.ClearXformOpOrder() 
dice2.AddTranslateOp().Set(dice2_translation) 
dice2.AddOrientOp().Set(Gf.Quatf(dice2_rotation))
dice2.AddScaleOp().Set(Gf.Vec3d(1, 1, 1))
```
Repeat the previous process to create a new dice and form "USD"
```python
dice3 = UsdGeom.Xform.Define(stage, '/World/Dice3')
dice3.GetPrim().GetReferences().AddInternalReference("/World/Dice1")
dice3_translation = dice2_translation - Gf.Vec3d(dice_size, 0, 0)
dice3_rotation = Gf.Rotation(Gf.Vec3d(0, 1, 0), 90).GetQuat() * dice2_rotation 
dice3.ClearXformOpOrder() 
dice3.AddTranslateOp().Set(dice3_translation) 
dice3.AddOrientOp().Set(Gf.Quatf(dice3_rotation) )
dice3.AddScaleOp().Set(Gf.Vec3d(1, 1, 1))
```
### 6.3.4 Enhancing the Look of Your Stage
Add a simple background
```python
backdrop =  UsdGeom.Xform.Define(stage, '/World/Backdrop')
backdrop.GetPrim().GetReferences().AddReference('./Assets/Backdrop.usd')   
```
Design thoughtful lighting
```python
from pxr import UsdLux
dome_light = UsdLux.DomeLight.Define(stage, "/Environment/Sky")
dome_light.CreateIntensityAttr(500)
distant_light = UsdLux.DistantLight.Define(stage, "/World/Lights/DistantLight")
distant_light.AddRotateXYZOp().Set(Gf.Vec3d(-51.3, 0, -46.1))
distant_light.CreateIntensityAttr(750)
```
Vary colors and materials
```python
from pxr import UsdShade
shader_path = "/World/Dice2/materials/Dice_Color/preview_Principled_BSDF" 
shader = UsdShade.Shader(stage.GetPrimAtPath(shader_path))   
shader.GetInput("diffuseColor").Set(Gf.Vec3f(0.8, 0, 0))    
```

