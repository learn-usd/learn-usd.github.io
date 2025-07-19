# Chapter 3
Get the current directory
```python
import os 
print(os.getcwd()) 
```
Change working directory
```python
new_directory = <'/your/path/to/new/directory'>
os.chdir(new_directory)    
```
>Note: For Google Colab only, use code below
```
from google.colab import files
files.download('your_file.usd')   

import os    
new_directory = <'/content/drive/My Drive/your_chosen_folder'>    
os.chdir(new_directory)    
```
Create and save a Stage
```python
from pxr import Usd, UsdGeom   
stage = Usd.Stage.CreateNew("sphere.usda") 

world_prim = UsdGeom.Xform.Define(stage, '/World')    

xform_prim = UsdGeom.Xform.Define(stage, '/World/Xform')    
sphere_prim = UsdGeom.Sphere.Define(stage, '/World/Sphere')

stage.Save()   
```
Open an existing .usd file 
```python
stage = Usd.Stage.Open("sphere.usda") 
```
### 3.1.1 Viewing the Sphere
Print every prim path
```python
for prim in stage.Traverse(): 
    print(prim.GetPath().pathString) 
```
Retrieve prims
```python
world_prim = stage.GetPrimAtPath('/World')    
```
List child prims 
```python
children_prims = world_prim.GetChildren()    
for prim in children_prims:   
    print(prim.GetPath().pathString)    
```
Get parent prims
```python
xform_prim = stage.GetPrimAtPath('/World/Xform')
parent_prim = xform_prim.GetParent()  
```
Remove a prim from a stage
```python
successful = stage.RemovePrim('/World/Xform')    
if successful:    
    print("/World/Xform has been removed")    
```
### 3.3.2 Considering Directories & File Paths when Referencing
Setting working directory
>Note: Make sure the new ‘blocks.usda’ is located in your ‘Ch03’ directory
```python
import os    
new_directory = <'/your/path/to/Ch03'>    
os.chdir(new_directory)    
```
>Note: For users of Colab, you will need to place a copy of the downloaded ‘Ch03’ folder onto your GDrive, remembering to mount your GDrive in your Colab notebook. Then you will be able to change your working directory using
```python
import os    
new_directory = <your file path to Ch03 ex: '/content/drive/My Drive/Ch03'>   
os.chdir(new_directory)    
```
### 3.3.3 Using References
```python
from pxr import Usd, Sdf
def internal_reference(prim: Usd.Prim, ref_target_path: Sdf.Path):    
    references: Usd.References = prim.GetReferences()
    references.AddInternalReference(
        primPath=ref_target_path
     ) 
def external_reference(prim: Usd.Prim, ref_asset_path: str):   
    references: Usd.References = prim.GetReferences()
    references.AddReference(
        assetPath=ref_asset_path
        )
```
create external reference to the example 'Block_Blue.usd'
```python
from pxr import Usd, UsdGeom, Sdf
stage = Usd.Stage.CreateNew("blocks.usda")
block1 = UsdGeom.Xform.Define(stage, "/World/Block1")
external_reference(    
    block1.GetPrim(),    
    <your file path to Block_Blue.usd ex:"./Assets/Block_Blue.usd">    
    )
stage.Save()
```

### 3.3.4 Using Payloads
Create payload to the example 'Block_Blue.usd'.
```python
from pxr import Usd, Sdf, UsdGeom
def add_payload(prim: Usd.Prim, payload_asset_path: str):   
    payloads: Usd.Payloads = prim.GetPayloads()   
    payloads.AddPayload(
    assetPath=payload_asset_path   
    )
stage = Usd.Stage.CreateNew("blocks_payload.usd")
block1 = UsdGeom.Xform.Define(stage, '/World/Block1')   
add_payload(
    block1.GetPrim(),
    <your file path to Block_Blue.usd ex: "./Assets/Block_Blue.usd">
    )  
stage.Save()
```
Unload 
```python
block1.GetPrim().Unload()    
```
Check if the data associated with the block1 prim is loaded. If the data is unloaded, the method will return False
```python
block1.GetPrim().IsLoaded()  
```
Load back
```python
block1.GetPrim().Load()    
```
## 3.4 Setting Stage Properties
Set stage’s up-axis
```python
from pxr import UsdGeom
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)    
```
Set the unit measurement
```python
UsdGeom.SetStageMetersPerUnit(stage, 0.01)    
```
Set the default prim
```python
stage.SetDefaultPrim(world_prim)
default_prim = stage.GetDefaultPrim()   
stage.Save()
```

## 3.5 Saving the Scene
Export blocks.usda stage to a different format
```python
stage = Usd.Stage.Open("blocks.usda")
stage.Export("blocks.usdc")    
```
Export a .usd file as a .usdz 
```python
from pxr import UsdUtils    
UsdUtils.CreateNewUsdzPackage("blocks.usda", "blocks.usdz")   
```
