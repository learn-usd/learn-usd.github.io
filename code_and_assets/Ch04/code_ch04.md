# Chapter 4
## 4.2 Adding a Transform
Create a new stage and reference an external prim:
```python
from pxr import Gf, Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew('AddReference.usda')    
default_prim: Usd.Prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()    
stage.SetDefaultPrim(default_prim)    

object_prim = stage.DefinePrim("/World/object", "Xform")    
object_prim.GetReferences().AddReference(
	'./Assets/cube.usda'  
	)    

xform = UsdGeom.Xformable(object_prim)    
xform.AddTranslateOp().Set(Gf.Vec3d(100,10,0))    
xform.AddRotateXYZOp().Set(Gf.Vec3d(0,50,0))    
xform.AddScaleOp().Set(Gf.Vec3d(5,5,5))
stage.Save()    
```
Get all three kinds of transform information from the cube:
```python
for op in xform.GetOrderedXformOps():    #A
    op_type = op.GetOpType()    #B
    op_value = op.Get()   	#C
    print(f"Operation: {op_type}, Value: {op_value}")    #D

```
Retrieve the specific rotation only
```python 
for op in xform.GetOrderedXformOps():	
	if op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:	
    	authored_rotation = op.Get(time)	
    	print("Authored Rotation:", authored_rotation)	
    	break	
```
Reset translation:
```python
translate_op = xform.GetOrderedXformOps()[0]    
if translate_op.GetOpType() == UsdGeom.XformOp.TypeTranslate:    
    translate_op.Set(Gf.Vec3d(0, 0, 0))    
``` 
Alternatively,
```python
xform.ClearXformOpOrder()        
``` 

### 4.3.1 Analyzing a Mesh
```python
stage = Usd.Stage.Open('./Assets/cube.usda')
prim = stage.GetPrimAtPath("/World/Cube")

mesh = UsdGeom.Mesh(prim)

vertex_points = mesh.GetPointsAttr().Get()
vertex_counts = mesh.GetFaceVertexCountsAttr().Get() 
vertex_indices = mesh.GetFaceVertexIndicesAttr().Get()
# print(vertex_points, vertex_counts, vertex_indices)  
``` 

### 4.3.2 Creating a Mesh
```python
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("plane.usda")

plane = UsdGeom.Mesh.Define(stage, "/World/plane")
plane.CreatePointsAttr([(0, 0, 0), (0, 100, 0), (200, 100, 0), (200, 0, 0)])
plane.CreateFaceVertexCountsAttr([4])  
plane.CreateFaceVertexIndicesAttr([0,1,2,3]) 
plane.CreateExtentAttr([(0, 0, 0), (200, 100, 0)])

stage.Save()
```
### 4.3.2 Creating a Mesh
```python
import os
from pxr import Usd, UsdGeom

def scale_mesh(file_path, scale_factor):
    try:
        stage = Usd.Stage.Open(file_path)   
   	 
        mesh_path = '/World/plane'
        mesh = UsdGeom.Mesh(stage.GetPrimAtPath(mesh_path))   
   	 
        points_attr = mesh.GetPointsAttr()    
        points = points_attr.Get()
   	 
        scaled_points = [(x * scale_factor, y * scale_factor, z * scale_factor) for x, y, z in points]  
   	 
        points_attr.Set(scaled_points)   
   	 
        stage.GetRootLayer().Save()    
        print("Mesh scaled successfully.")
    except Exception as e:
        print(f"Error scaling mesh: {e}")

# Example usage
file_path = "plane.usda"
scale_factor = 2
scale_mesh(file_path, scale_factor)
```
## 4.4 Creating a Simple Material 
Create a material that is red in color:
```python
from pxr import Sdf, UsdShade

material= UsdShade.Material.Define(stage, '/World/Looks/planeMaterial')

pbrShader = UsdShade.Shader.Define(stage,    
	'/World/Looks/planeMaterial/PBRShader'
	)

pbrShader.CreateIdAttr("UsdPreviewSurface")    
pbrShader.CreateInput(
	"diffuseColor",
	Sdf.ValueTypeNames.Color3f).Set((1, 0, 0)    
	)

pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

pbrShaderOutput = pbrShader.CreateOutput("surface", Sdf.ValueTypeNames.Token)  

materialOutput = material.CreateSurfaceOutput()    
materialOutput.ConnectToSource(pbrShaderOutput)

stage.Save()
```
Bind the material to the plane:
```python
plane.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
UsdShade.MaterialBindingAPI(plane).Bind(   
    material,
    bindingStrength=UsdShade.Tokens.strongerThanDescendants   
    )

stage.Save()
```

### 4.5.1 Adding a Diffuse Color Texture with OpenUSD Programming
Create a new plane mesh: 
```python
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Vt

stage = Usd.Stage.CreateNew("texture_plane.usd")
```
Define its faces and vertices:
```python
plane = UsdGeom.Mesh.Define(stage, "/World/plane")
faceVertexCounts = [4]
faceVertexIndices = [0, 1, 2, 3]
vertices = [
    Gf.Vec3f(0, 0, 0), Gf.Vec3f(0, 100, 0), Gf.Vec3f(200, 100, 0), Gf.Vec3f(200, 0, 0),
]

plane.CreateFaceVertexCountsAttr(faceVertexCounts)
plane.CreateFaceVertexIndicesAttr(faceVertexIndices)
plane.CreatePointsAttr(vertices)

plane.AddScaleOp().Set(Gf.Vec3f(2))   
```
Create and set up a primitive variable (primvar) for texture coordinates on the plane mesh:
```python
primvar = UsdGeom.PrimvarsAPI(plane.GetPrim()).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying) 
primvar.Set(Vt.Vec2fArray([(0, 0), (0, 1), (1, 1), (1, 0)]))   
```
Create a material prim and bind it to the target prim:
```python
material= UsdShade.Material.Define(stage, '/World/Looks/planeMaterial')    

plane.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)   
UsdShade.MaterialBindingAPI(plane).Bind(material, UsdShade.Tokens.strongerThanDescendants)    
```
Create a UsdPreviewSurface shader and connect it to the planeMaterial prim:
```python
mainShader = UsdShade.Shader.Define(stage, '/World/Looks/planeMaterial/MainShader')    
mainShader.CreateIdAttr("UsdPreviewSurface")    
mainShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f)    

material.CreateSurfaceOutput().ConnectToSource(mainShader.ConnectableAPI(), "surface")    
```
Create a Shader node to read the st Coordinates of a model:
```python
stReader = UsdShade.Shader.Define(stage, '/World/Looks/planeMaterial/stReader')    
stReader.CreateIdAttr('UsdPrimvarReader_float2') 
stReader.CreateInput("varname", Sdf.ValueTypeNames.String).Set("st")    
```
Create a diffuseTexture shader node:
```python
diffuseTextureSampler = UsdShade.Shader.Define(stage,'/World/Looks/planeMaterial/diffuseTexture')     
diffuseTextureSampler.CreateIdAttr('UsdUVTexture') 

image_file_path = './Assets/textures/sample_texture.png'
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(image_file_path)
```
Connect to the diffuseTexture shader
```python
diffuseTextureSampler.CreateInput("st",Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')    

diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)   
mainShader.CreateInput("diffuseColor",Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')
stage.Save()
```

### 4.6.1 Creating a Material Output Node
```python
from pxr import Usd, UsdGeom, UsdShade, Sdf

stage = Usd.Stage.CreateNew("texture_ring.usd")

ring = UsdGeom.Xform.Define(stage, "/World/Ring")  

ref_asset_path = './Assets/Ring.usd'
references: Usd.References = ring.GetPrim().GetReferences()
references.AddReference(
    assetPath=ref_asset_path
)   
```
Create a material and bind the material to the ring mesh prim:
```python
material= UsdShade.Material.Define(stage, '/World/Looks/ringMaterial') 

ring.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI) 
UsdShade.MaterialBindingAPI(ring).Bind(material, UsdShade.Tokens.strongerThanDescendants)
```
### 4.6.2 Utilizing a UsdPreviewSurface Shader
```python
mainShader = UsdShade.Shader.Define(stage, '/World/Looks/ringMaterial/MainShader') 
mainShader.CreateIdAttr("UsdPreviewSurface")   
material.CreateSurfaceOutput().ConnectToSource(mainShader.ConnectableAPI(), "surface")
```
### 4.6.3 Creating a UsdPrimvarReader_float2 Shader
```python
stReader = UsdShade.Shader.Define(stage, '/World/Looks/ringMaterial/stReader') 
stReader.CreateIdAttr('UsdPrimvarReader_float2') 
stReader.CreateInput("varname", Sdf.ValueTypeNames.String).Set("st") 
```
### 4.6.4 Setting Up a UsdUVTexture Sampler
Create a UsdUVTexture sampler node:
```python
diffuseTextureSampler = UsdShade.Shader.Define(stage,'/World/Looks/ringMaterial/diffuseTexture') 
diffuseTextureSampler.CreateIdAttr('UsdUVTexture') 

diffuse_file_path = "./Assets/textures/Ring_DIFFUSE.png"
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(diffuse_file_path) 

diffuseTextureSampler.CreateInput("st",Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')    

diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)     
mainShader.CreateInput("diffuseColor",Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')    
```
Normal map:
```python
normalMapSampler = UsdShade.Shader.Define(stage,'/World/Looks/ringMaterial/normalMap') 
normalMapSampler.CreateIdAttr('UsdUVTexture') 

normal_file_path = "./Assets/textures/Ring_NORMAL.png"
normalMapSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(normal_file_path) 

normalMapSampler.CreateInput("st",Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')    

normalMapSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)       
mainShader.CreateInput("normal",Sdf.ValueTypeNames.Color3f).ConnectToSource(normalMapSampler.ConnectableAPI(), 'rgb')    
```
Roughness map:
```python
roughnessMapSampler = UsdShade.Shader.Define(stage,'/World/Looks/ringMaterial/roughnessMap')
roughnessMapSampler.CreateIdAttr('UsdUVTexture')

roughness_file_path = "./Assets/textures/Ring_ROUGHNESS.png"
roughnessMapSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(roughness_file_path)
roughnessMapSampler.CreateInput("st",Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')

roughnessMapSampler.CreateOutput('r', Sdf.ValueTypeNames.Float)    
mainShader.CreateInput("roughness",Sdf.ValueTypeNames.Float).ConnectToSource(roughnessMapSampler.ConnectableAPI(), 'r')   
```
Metallic map:
```python
metallicMapSampler = UsdShade.Shader.Define(stage,'/World/Looks/ringMaterial/metallicMap') 
metallicMapSampler.CreateIdAttr('UsdUVTexture') 

metallic_file_path = "./Assets/textures/Ring_METALLIC.png"  
metallicMapSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(metallic_file_path)
metallicMapSampler.CreateInput("st",Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result') 

metallicMapSampler.CreateOutput('r', Sdf.ValueTypeNames.Float)         
mainShader.CreateInput("metallic",Sdf.ValueTypeNames.Float).ConnectToSource(metallicMapSampler.ConnectableAPI(), 'r')   
```
Save the stage
```python
stage.Save()
```
