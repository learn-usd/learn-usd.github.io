# Chapter 7
### 7.1.2 Setting the Stage's Metadata
Create a new stage with .usda format
```python
from pxr import Usd, UsdGeom, Gf, Sdf
stage = Usd.Stage.CreateNew("animation.usda")
```
Set time
```python
fps = 30.0
stage.SetTimeCodesPerSecond(fps)    
stage.SetStartTimeCode(0)   
stage.SetEndTimeCode(59)    
stage.Save()
```
### 7.2.2 Animating Xforms
Listing 6.1 Create a Cube and Add Keyframe Animation To It 
```python
cube  = UsdGeom.Cube.Define(stage, "/World/Cube")    

transform_op = cube.AddTranslateOp(precision=UsdGeom.XformOp.PrecisionDouble)    
transform_op.Set(value=Gf.Vec3d(0, 0, 0), time=Usd.TimeCode(0))    
transform_op.Set(Gf.Vec3d(10, 0, 0), Usd.TimeCode(30))    

stage.Save()
```
Keyframing rotation: setting the cube's initial rotation at frame 0 and rotating the cube 90 degrees around the Z-axis by frame 30:
```python
rotation_op = cube.AddRotateXYZOp(precision=UsdGeom.XformOp.PrecisionDouble)    
rotation_op.Set(Gf.Vec3d(0,0,0),0)    
rotation_op.Set(Gf.Vec3d(0,0,90),30)    
stage.Save()
```
Use quaternion to represent the rotation: 
```python
import math   
UsdGeom.Xformable(cube).ClearXformOpOrder()    
cube.AddTranslateOp()    
rotation_op = cube.AddOrientOp(precision=UsdGeom.XformOp.PrecisionDouble)    
rotation_op.Set(Gf.Quatd(1,0,0,0),0)    
rotation_op.Set(Gf.Quatd(math.sqrt(2)/2,0,0,math.sqrt(2)/2),30)    
stage.Save()
```
Add scale animation 
```python
scale_op = cube.AddScaleOp(precision=UsdGeom.XformOp.PrecisionDouble)    
scale_op.Set(Gf.Vec3d(1,1,1), 0)    
scale_op.Set(Gf.Vec3d(5,5,5), 30)    
stage.Save()
```
### 7.2.3 Influencing Interpolation
Move the first cube away
```python
transform_op.Set(Gf.Vec3d(0, 0, -20),0)    
transform_op.Set(Gf.Vec3d(10, 0, -20),30)    
```
Create a second cube and add a translate_op
```python
cube2 = UsdGeom.Cube.Define(stage, "/World/Cube2")    
translate_op = cube2.AddTranslateOp(precision=UsdGeom.XformOp.PrecisionDouble)    
```
Set up the keyframe values
```python
P0 = Gf.Vec3d(0, 0, 0)    
P1 = Gf.Vec3d(10, 0, 0)    
M0 = Gf.Vec3d(0.05, 0, 0)    
M1 = Gf.Vec3d(-0.05, 0, 0)    
```
Listing 6.2 Define the Helper Function for Cubic Hermite Interpolation.
```python 
def cubic_hermite(P0, P1, M0, M1, t):
	"""
	Perform cubic Hermite interpolation.
    
	Parameters:
	P0, P1: float or np.array
    		The start and end keyframe values.
	M0, M1: float or np.array
    		The tangents at the start and end keyframes.
	t: float
    		The normalized time between P0 and P1 (0 <= t <= 1).
    
	Returns:
	float or np.array
    	The interpolated value.
	"""
	h00 = 2 * t**3 - 3 * t**2 + 1
	h10 = t**3 - 2 * t**2 + t
	h01 = -2 * t**3 + 3 * t**2
	h11 = t**3 - t**2
    
	return h00 * P0 + h10 * M0 + h01 * P1 + h11 * M1
```
Loop through the frame to get the cubic Hermite interpolation
```python
for frame in range(0, 31):    
	t = frame / 30.0    
	interpolated_value = cubic_hermite(P0, P1, M0, M1, t)    
	translate_op.Set(interpolated_value, Usd.TimeCode(frame))    
```
Similar approach applied to rotaion Euler angles:
```python
rotation_op = cube2.AddRotateXYZOp(precision=UsdGeom.XformOp.PrecisionDouble)

R0 = Gf.Vec3d(0, 0, 0)   	
R1 = Gf.Vec3d(0, 0, 90)  	
T0_rot = Gf.Vec3d(0, 0, 1)  
T1_rot = Gf.Vec3d(0, 0, -1) 
for frame in range(0, 31):  
	t = frame / 30.0   
	interpolated_rotation = cubic_hermite(R0, R1, T0_rot, T1_rot, t)
	rotation_op.Set(interpolated_rotation, Usd.TimeCode(frame))
```
Similar approach applied to scale
```python
scale_op = cube2.AddScaleOp(precision=UsdGeom.XformOp.PrecisionDouble)
S0 = Gf.Vec3d(1, 1, 1)	
S1 = Gf.Vec3d(5, 5, 5)	
T0_scale = Gf.Vec3d(0.1, 0.1, 0.1)  
T1_scale = Gf.Vec3d(-0.1, -0.1, -0.1)
for frame in range(0, 31):    
	t = frame / 30.0    
	interpolated_scale = cubic_hermite(S0, S1, T0_scale, T1_scale, t)
	scale_op.Set(interpolated_scale, Usd.TimeCode(frame))

stage.Save()
```
### 7.2.4 Animating Attributes
Get the translate attribute and edit
```python
cube_prim = stage.GetPrimAtPath('/World/Cube')    
cube_prim.GetAttribute("xformOp:translate").Set(Gf.Vec3d(0,0,-20), 0)    
cube_prim.GetAttribute("xformOp:translate").Set(Gf.Vec3d(0,10,-20), 30)    
stage.Save()
```
Creates a Rect Light, then positions, resizes and sets its intensity
```python
from pxr import UsdLux

light = UsdLux.RectLight.Define(stage, "/World/Lights/Light")    

light.AddTranslateOp().Set(Gf.Vec3d(25, 25, -10))
light.AddRotateXYZOp().Set(Gf.Vec3d(-90, 0, -45))
light.GetHeightAttr().Set(60)
light.GetWidthAttr().Set(30)    

light.GetIntensityAttr().Set(30000)    

stage.Save()
```
Animate the light's intensity gradually
```python
intensity_attr = light.GetIntensityAttr()    

intensity_attr.Set(0, 0)     
intensity_attr.Set(30000, 30) 
intensity_attr.Set(0, 59)    
```
Change light color
```python 
color_attr = light.GetColorAttr()    

color_attr.Set(Gf.Vec3f(1, 0, 0), 0)    
color_attr.Set(Gf.Vec3f(1, 1, 1), 30)    
color_attr.Set(Gf.Vec3f(1, 0, 0), 59)    

stage.Save()
```
Schema specific attributes can be cleared
```python
light.GetIntensityAttr().ClearAtTime(0)
```
or
```python 
light.GetIntensityAttr().Clear()
```
Clear the light intensity keyframe at 0 and 59
```python
light.GetIntensityAttr().ClearAtTime(0)    
light.GetIntensityAttr().ClearAtTime(59)    
```
Add a camera to the stage that is facing two cubes
```python 
camera = UsdGeom.Camera.Define(stage, "/World/Camera")

translate_op = camera.AddTranslateOp()
translate_op.Set(Gf.Vec3d(30, 30, 100))
rotate_op = camera.AddRotateXYZOp()
rotate_op.Set(Gf.Vec3d(-12, 12, 0))

stage.Save()
```
Create a zoom effect on the camera
```python 
camera.GetFocalLengthAttr().Set(30, (0))    
camera.GetFocalLengthAttr().Set(100, (50))    

stage.Save()
```
## 7.3 Combining Animations in One Clip
Set working directory 
```python 
import os    
new_directory = <'/your/path/to/Ch06 ex:'D://Ch06''>    
os.chdir(new_directory)    
```
Create a new stage 'fan_animation' and set the stage's properties with six-second animation at 24 fps
```python 
from pxr import Usd, UsdGeom, Sdf, Gf, UsdLux
stage = Usd.Stage.CreateNew("fan_animation.usda")

fps = 24.0
stage.SetTimeCodesPerSecond(fps)
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(143)
```
Import the fan model
```python
fan = UsdGeom.Xform.Define(stage, '/World/Fan')    
fan_references: Usd.References = fan.GetPrim().GetReferences()
fan_references.AddReference(
	assetPath= "./Assets/Fan.usd"
)

stage.Save()
```
Apply rotation to the oscillating joint 
```python
oscillator = stage.GetPrimAtPath("/World/Fan/Base/Oscillating_Joint")   
oscillator_xform = UsdGeom.Xformable(oscillator)    

translation_op = oscillator_xform.GetOrderedXformOps()[0]    

rotation_op = oscillator_xform.GetOrderedXformOps()[1]    

rotation_op.Set(Gf.Vec3d(0, -45, 0), 0)
rotation_op.Set(Gf.Vec3d(0, 45, 0), 71)
rotation_op.Set(Gf.Vec3d(0, -45, 0), 143)   

stage.Save()
```
Listing 6.3 Applying Cubic Interpolation to the Oscillating Animation.
```python 
def cubic_hermite(P0, P1, M0, M1, t):
	h00 = 2 * t**3 - 3 * t**2 + 1
	h10 = t**3 - 2 * t**2 + t
	h01 = -2 * t**3 + 3 * t**2
	h11 = t**3 - t**2
	return h00 * P0 + h10 * M0 + h01 * P1 + h11 * M1   

R0 = Gf.Vec3d(0, -45, 0)    
R1 = Gf.Vec3d(0, 45, 0)    
T0_rot = Gf.Vec3d(0, 15, 0)    
T1_rot = Gf.Vec3d(0, 15, 0)    

rotation_op = oscillator.GetAttribute("xformOp:rotateXYZ")    

first_half_rotations = []    

for frame in range(72):
	t = frame / 71.0    
	interpolated_rotation = cubic_hermite(R0, R1, T0_rot, T1_rot, t)    
	rotation_op.Set(interpolated_rotation, Usd.TimeCode(frame))    
	first_half_rotations.append(interpolated_rotation)    

for frame in range(72, 144):
	mirrored_rotation = first_half_rotations[143 - frame]    
	rotation_op.Set(mirrored_rotation, Usd.TimeCode(frame))    

stage.Save()
```
Animate the fan blades with full rotation around the z-axis
```python
fan_blades = stage.GetPrimAtPath("/World/Fan/Base/Oscillating_Joint/Motor/Blades")    

xform = UsdGeom.Xformable(fan_blades) 
rotation_attr = xform.AddXformOp(UsdGeom.XformOp.TypeRotateZ, UsdGeom.XformOp.PrecisionFloat)    

start_frame = 0    
end_frame = 143 
total_rotations = 10 
fps = 24.0 

total_angle = total_rotations * 360    

rotation_attr.Set(0, start_frame)    
rotation_attr.Set(total_angle, end_frame)    

stage.Save()
```
Add camera animation
```python
camera_path = Sdf.Path("/World/Camera")  
camera: UsdGeom.Camera = UsdGeom.Camera.Define(stage, camera_path)    

camera.GetFocalLengthAttr().Set(20)    

translate_op = camera.AddTranslateOp()    
translate_op.Set(Gf.Vec3d(0, 5, 100), 0)    
translate_op.Set(Gf.Vec3d(0, 35, 90), 143)

rotation_op = camera.AddRotateXYZOp()    
rotation_op.Set(Gf.Vec3d(12,2,0),0)    
rotation_op.Set(Gf.Vec3d(-10,1,0),143)

stage.Save()
```