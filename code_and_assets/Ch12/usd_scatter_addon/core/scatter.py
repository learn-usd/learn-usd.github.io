from pxr import Usd, UsdGeom, Gf, Vt
import random
import numpy as np

def get_first_mesh_and_points(stage, prim_path):
    root_prim = stage.GetPrimAtPath(prim_path)
    if not root_prim or not root_prim.IsValid():
        print(f"Invalid prim at path: {prim_path}")
        return None, None

    for prim in Usd.PrimRange(root_prim):
        if prim.IsA(UsdGeom.Mesh):
            mesh = UsdGeom.Mesh(prim)
            points = mesh.GetPointsAttr().Get()
            return mesh, points

    print(f"No UsdGeom.Mesh found under {prim_path}")
    return None, None

def compute_bounding_box(stage, prim_path):    
    prim = stage.GetPrimAtPath(prim_path)
    purposes = [UsdGeom.Tokens.default_]   
    bboxcache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), purposes)    
    bboxes = bboxcache.ComputeWorldBound(prim)    
    min_point = bboxes.ComputeAlignedRange().GetMin()
    max_point = bboxes.ComputeAlignedRange().GetMax()   
    size = max_point - min_point	
    return min_point, max_point, size 

def find_nearest_index(data_points, query_point):
    distances = np.linalg.norm(data_points - query_point, axis=1)
    return np.argmin(distances)

def is_far_enough(x, y, placed_positions, min_dist):
    for px, py in placed_positions:
        if (x - px)**2 + (y - py)**2 < min_dist**2:
            return False
    return True


def run_usd_scatter(
    output_path,
    terrain_asset_path,
    terrain_prim_path,
    prototypes,  
    num_instances,
    min_distance=None,
    bounds=None,
):
    stage = Usd.Stage.CreateNew(output_path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

    terrain_ref = UsdGeom.Xform.Define(stage, terrain_prim_path)
    terrain_ref.GetPrim().GetReferences().AddReference(terrain_asset_path)

    terrain_mesh, terrain_points = get_first_mesh_and_points(stage, terrain_prim_path)
    min_point, max_point, _ = compute_bounding_box(stage, terrain_mesh.GetPath())
    terrain_points_arr = np.asarray(terrain_points)
    terrain_points_arr_xy = np.asarray(terrain_points_arr)[:,:2]

    if bounds is None:
        min_point_arr_xy = np.asarray(min_point)[:2]
        max_point_arr_xy = np.asarray(max_point)[:2]
        bounds = float(np.min(abs(np.concatenate((min_point_arr_xy, max_point_arr_xy)))))

    proto_paths = []
    proto_weights = []
    proto_size_list = []
    for proto in prototypes:
        proto_paths.append(proto["path"])
        proto_weights.append(proto["weight"])
        prim = stage.DefinePrim(proto["path"], "Xform")
        prim.GetReferences().AddReference(proto["file"])
        proto_mesh, _ = get_first_mesh_and_points(stage, proto["path"])
        _, _, proto_size = compute_bounding_box(stage, proto_mesh.GetPath())
        proto_size_list.append(np.max(proto_size[:2]))
    if min_distance is None:
        min_distance = float(max(proto_size_list))
    real_bounds = max(0.0, bounds - min_distance/2)	

    placed_positions = []
    positions = []	
    orientations = []	
    scales = []		
    indices = []

    while len(positions) < num_instances:
        x = random.uniform(-real_bounds, real_bounds)
        y = random.uniform(-real_bounds, real_bounds)  

        if is_far_enough(x, y, placed_positions, min_distance):
            sample_point_xy = np.array([x, y])
            close_point_index = find_nearest_index(terrain_points_arr_xy, sample_point_xy)
            z = float(terrain_points_arr[close_point_index, 2]) 

            placed_positions.append((x, y))
            positions.append(Gf.Vec3f(x, y, z))

            angle_deg = random.uniform(0, 360)
            rotation = Gf.Rotation(Gf.Vec3d(0, 0, 1), angle_deg)
            quat = rotation.GetQuat()
            orientations.append(Gf.Quath(quat))

            scale = random.uniform(0.8, 1.2)
            scales.append(Gf.Vec3f(scale, scale, scale))

            index = random.choices(range(len(proto_paths)), weights=proto_weights)[0]
            indices.append(index)
    
    instancer = UsdGeom.PointInstancer.Define(stage, "/World/Instances")
    instancer.CreatePrototypesRel().SetTargets(proto_paths)
    instancer.CreatePositionsAttr(Vt.Vec3fArray(positions))
    instancer.CreateOrientationsAttr(Vt.QuathArray(orientations))
    instancer.CreateScalesAttr(Vt.Vec3fArray(scales))
    instancer.CreateProtoIndicesAttr(Vt.IntArray(indices))

    stage.Save()