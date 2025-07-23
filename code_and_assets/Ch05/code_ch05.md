# Chapter 5
Set working directory to "Ch04" folder
```python
import os   
new_directory = <'/your/path/to/Ch04'>   
os.chdir(new_directory)   
```
## Listing 4.1 Building and Populating a Stage Using External Assets. 
```python
from pxr import Usd, Sdf, UsdGeom, Gf

stage = Usd.Stage.CreateNew("statue.usd")

statue = UsdGeom.Xform.Define(stage, '/World/Statue')    

figure = UsdGeom.Xform.Define(stage, '/World/Statue/Figure')    
figure_references: Usd.References = figure.GetPrim().GetReferences()
figure_references.AddReference(
	assetPath= "./Assets/Figure.usd"
)

base = UsdGeom.Xform.Define(stage, '/World/Statue/Base')    
base_references: Usd.References = base.GetPrim().GetReferences()
base_references.AddReference(
	assetPath="./Assets/Base.usd"
)

backdrop = UsdGeom.Xform.Define(stage, '/World/Backdrop')    
backdrop_references: Usd.References = backdrop.GetPrim().GetReferences()
backdrop_references.AddReference(
	assetPath= "./Assets/Backdrop.usd"
)

stage.Save()
```
## Listing 4.2 Make a Prim Invisible.
```python
def hide_prim(stage: Usd.Stage, prim_path: str):
    """
	Hide a prim
	::params:
    	stage (Usd.Stage): The USD Stage
    	prim_path (string): The prim path of the prim to make invisible
    """
    prim = stage.GetPrimAtPath(prim_path)  
    visibility_attribute = prim.GetAttribute("visibility")   
    if visibility_attribute:
        visibility_attribute.Set("invisible")    

# hide_prim(stage, <'your_path_to_prim'>)  
```
## Listing 4.3 Make a Prim Visible.
```python
def show_prim(stage: Usd.Stage, prim_path: str):
    """
    Show a prim
    ::params:
        stage (Usd.Stage): The USD Stage
        prim_path (string): The prim path of the prim to make visible
    """
    prim = stage.GetPrimAtPath(prim_path)
    visibility_attribute = prim.GetAttribute("visibility")
    if visibility_attribute:
        visibility_attribute.Set("inherited")    #A

# show_prim(stage, "<your_path_to_prim>")    #B
```
### 5.2.2 Creating Lights
Create Rect light
```python
from pxr import UsdLux, Gf
rect_light = UsdLux.RectLight.Define(stage, "/World/Lights/RectLight") 
```
Move Rect light and rotate by 45 degrees
```python
rect_light.AddTranslateOp().Set(Gf.Vec3d(100, 100, 200))
rect_light.AddRotateXYZOp().Set(Gf.Vec3d(0, 45, 0))
```
Set light intensity
```python
rect_light.CreateIntensityAttr(30000)
```
Set light color to be white
```pyhon
rect_light.CreateColorAttr(Gf.Vec3f(1, 1, 1))
```
Set Rect light Height and Width
```python
rect_light.CreateHeightAttr(100)    
rect_light.CreateWidthAttr(100)    
```
Create Disk light 
```python
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")    
disk_light.CreateRadiusAttr(50)    
```
Add translate, rotation, color, and intensity to the Disk light
```python
disk_light.AddTranslateOp().Set(Gf.Vec3d(0, 200, 0))
disk_light.AddRotateXYZOp().Set(Gf.Vec3d(-90, 0.0, 0))

disk_light.CreateColorAttr(Gf.Vec3f(1, 1, 1))
disk_light.CreateIntensityAttr(30000)
```
Create Sphere light
```python
sphere_light = UsdLux.SphereLight.Define(stage, "/World/Lights/SphereLight")    

sphere_light.CreateRadiusAttr(5.0)    

sphere_light.AddTranslateOp().Set(Gf.Vec3d(-22, 166, 66))

sphere_light.CreateColorAttr(Gf.Vec3f(1, 1, 1))
sphere_light.CreateIntensityAttr(400000)
```
Turn Sphere light into a point light
```python
sphere_light.CreateTreatAsPointAttr(True)
```
Turn it back 
```python
sphere_light.CreateTreatAsPointAttr(False)
```
Create Distant Light and change the angle of it
```python
distant_light = UsdLux.DistantLight.Define(stage, "/World/Lights/DistantLight")

distant_light.AddRotateXYZOp().Set(Gf.Vec3d(-17, -30, -50))   
distant_light.CreateIntensityAttr(1.0)
```
Create Cylinder light
```python
cylinder_light = UsdLux.CylinderLight.Define(stage, "/World/Lights/CylinderLight")
cylinder_light.AddTranslateOp().Set(Gf.Vec3d(-100, 100.0, 0))
cylinder_light.AddRotateXYZOp().Set(Gf.Vec3d(0, 0.0, 90))
cylinder_light.CreateIntensityAttr(100000)
cylinder_light.CreateColorAttr(Gf.Vec3f(1, 1, 1))
```
Define the length or the radius of the cylinder
```python
cylinder_light.CreateLengthAttr(100.0)    
cylinder_light.CreateRadiusAttr(5.0)    
```
Create a Dome light and rotate
```python
dome_light = UsdLux.DomeLight.Define(stage, "/Environment/Sky")  
dome_light.AddRotateXYZOp().Set(Gf.Vec3d(-90, 0, 0))   
```
Change the color and intensity
```python
dome_light.CreateIntensityAttr(3000)    
dome_light.CreateColorAttr(Gf.Vec3f(0.5, 0.75, 1.0))    
```
Assign image textures to the Dome light
```python
dome_light.CreateTextureFileAttr().Set("./Assets/textures/Landscape.exr")
```
Hide backdrop and make image texture of the Dome light visible
```python
def hide_prim(stage: Usd.Stage, prim_path: str):    
    prim = stage.GetPrimAtPath(prim_path)    
    visibility_attribute = prim.GetAttribute("visibility")   
    if visibility_attribute:
        visibility_attribute.Set("invisible")   

hide_prim(stage, "/World/Backdrop")    

stage.Save()
```
### 5.2.3 Three-Point Lighting
Mak the cylinder, sphere, distant and dome lights invisible on our Statue scene
```python
hide_prim(stage, "/World/Lights/CylinderLight")   
hide_prim(stage, "/World/Lights/SphereLight")
hide_prim(stage, "/World/Lights/DistantLight")
hide_prim(stage, "/Environment/Sky")
```
Add a Fill Light
```python
fill_light = UsdLux.RectLight.Define(stage, "/World/Lights/FillLight")   
fill_light.CreateHeightAttr(100)    
fill_light.CreateWidthAttr(100)     

fill_light.AddTranslateOp().Set(Gf.Vec3d(-180, 100, 200))    
fill_light.AddRotateXYZOp().Set(Gf.Vec3d(0, -45, 0))    

fill_light.CreateColorAttr(Gf.Vec3f(1, 1, 1))
fill_light.CreateIntensityAttr(15000)    
```
Restore backdrop
```python 
def show_prim(stage: Usd.Stage, prim_path: str):
    prim = stage.GetPrimAtPath(prim_path)
    visibility_attribute = prim.GetAttribute("visibility")
    if visibility_attribute:
        visibility_attribute.Set("inherited")    

show_prim(stage, "/World/Backdrop")   

stage.Save()
```
### 5.3.1 Creating a Camera 
Define the camera on the stage
```python
from pxr import Usd, Sdf, UsdGeom  
stage = Usd.Stage.Open("statue.usd")
camera_path = Sdf.Path("/World/Cameras/Cam1_Standard_Front")    
camera: UsdGeom.Camera = UsdGeom.Camera.Define(stage, camera_path)
```
### 5.3.2 Setting up Camera Translate and Rotation
Move the camera to line up the shot of the statue
```python
camera.AddTranslateOp().Set(value=(0, 100, 1000))
stage.Save()
```
### 5.3.3 Understanding Camera Attributes
Create the focal length attribute of the camera
```python
camera.CreateFocalLengthAttr().Set(50) 
```
Add another camera and set its position closer to the statue, lower and angled upwards, with a wide angle lens:
```python
camera2_path = "/World/Cameras/Cam2_Wide_Angle_Low"    
camera2 = UsdGeom.Camera.Define(stage, camera2_path)    
camera2.AddTranslateOp().Set(value=(-115, 20, 130))    
camera2.AddRotateXYZOp().Set(Gf.Vec3d((14, -50, 15)))   

new_focal_length = 8.0   
camera2.GetFocalLengthAttr().Set(new_focal_length)   
```
Create an fStop attribute and set it to 2.0
```python
camera.CreateFStopAttr().Set(2.0) #A
```
Set the camera's focus distance to 500 scene units
```python
new_focus_distance = 500    
camera.GetFocusDistanceAttr().Set(new_focus_distance)    
```
Change the fStop again to a higher value: 
```python
new_fStop = 16.0    
camera.GetFStopAttr().Set(new_fStop)    
```
Change the projection type:
```python
camera.CreateProjectionAttr().Set(UsdGeom.Tokens.perspective)    
# camera.CreateProjectionAttr().Set(UsdGeom.Tokens.orthographic)   
```
Set the values of both near and far clipping planes
```python
camera.CreateClippingRangeAttr().Set(Gf.Vec2d(0.1, 10000))

stage.Save()
```


