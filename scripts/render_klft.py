"""KLFT Digital Twin Renderer — renders USD scene from 7 camera angles using pyrender + L40S GPU."""
import os, math, numpy as np
from pxr import Usd, UsdGeom, Gf
import trimesh, pyrender
from PIL import Image

CAMERAS = {
    'tower_view': {'eye': [280, 38, 180], 'target': [0, 0, 0]},
    'overhead': {'eye': [0, 1200, 100], 'target': [0, 0, 0]},
    'approach_04R': {'eye': [-800, 80, -600], 'target': [0, 5, 0]},
    'skycommand_ops': {'eye': [480, 12, 330], 'target': [420, 3, 280]},
    'drone_launch': {'eye': [460, 8, 300], 'target': [430, 2, 280]},
    'new_terminal': {'eye': [350, 25, -100], 'target': [210, 7, 70]},
    'full_airport': {'eye': [-500, 400, -500], 'target': [0, 0, 0]},
}

def add_prim(scene, prim):
    xf = UsdGeom.Xformable(prim)
    local_xf = xf.ComputeLocalToWorldTransform(0)
    matrix = np.array(local_xf).T
    color_attr = prim.GetAttribute('primvars:displayColor')
    color = [0.5, 0.5, 0.5]
    if color_attr and color_attr.Get():
        c = color_attr.Get()[0]
        color = [float(c[0]), float(c[1]), float(c[2])]
    mat = pyrender.MetallicRoughnessMaterial(baseColorFactor=color+[1.0], metallicFactor=0.1, roughnessFactor=0.8)
    typ = prim.GetTypeName()
    tm = None
    if typ == 'Cube':
        tm = trimesh.creation.box(extents=[2,2,2])
    elif typ == 'Sphere':
        r = float(prim.GetAttribute('radius').Get()) if prim.GetAttribute('radius') and prim.GetAttribute('radius').Get() else 10
        tm = trimesh.creation.icosphere(radius=r, subdivisions=2)
        mat = pyrender.MetallicRoughnessMaterial(baseColorFactor=color+[0.4], alphaMode='BLEND')
    elif typ == 'Cylinder':
        h = float(prim.GetAttribute('height').Get()) if prim.GetAttribute('height') and prim.GetAttribute('height').Get() else 1
        r = float(prim.GetAttribute('radius').Get()) if prim.GetAttribute('radius') and prim.GetAttribute('radius').Get() else 1
        tm = trimesh.creation.cylinder(radius=r, height=h, sections=16)
    elif typ == 'Mesh':
        pts_a = prim.GetAttribute('points')
        fvi_a = prim.GetAttribute('faceVertexIndices')
        fvc_a = prim.GetAttribute('faceVertexCounts')
        if pts_a and fvi_a and fvc_a and pts_a.Get() and fvi_a.Get() and fvc_a.Get():
            pts = np.array(pts_a.Get())
            fvi = np.array(fvi_a.Get())
            fvc = np.array(fvc_a.Get())
            faces = []
            idx = 0
            for count in fvc:
                if count == 3: faces.append(fvi[idx:idx+3])
                elif count == 4:
                    faces.append([fvi[idx],fvi[idx+1],fvi[idx+2]])
                    faces.append([fvi[idx],fvi[idx+2],fvi[idx+3]])
                idx += int(count)
            if faces:
                tm = trimesh.Trimesh(vertices=pts, faces=np.array(faces))
    if tm is not None:
        tm.apply_transform(matrix)
        mesh = pyrender.Mesh.from_trimesh(tm, smooth=False)
        for p in mesh.primitives: p.material = mat
        scene.add(mesh)

def build_scene(usd_path):
    stage = Usd.Stage.Open(usd_path)
    scene = pyrender.Scene(bg_color=[0.4, 0.6, 0.85, 1.0], ambient_light=[0.3, 0.3, 0.35])
    for prim in stage.Traverse():
        if prim.GetTypeName() in ('Cube','Sphere','Cylinder','Mesh'):
            try: add_prim(scene, prim)
            except: pass
    # Sun
    sun = pyrender.DirectionalLight(color=[1.0, 0.95, 0.9], intensity=4.0)
    sp = np.eye(4); sp[:3,3] = [500, 800, 300]
    scene.add(sun, pose=sp)
    # Fill
    fill = pyrender.DirectionalLight(color=[0.6, 0.7, 0.8], intensity=1.5)
    fp = np.eye(4); fp[:3,3] = [-300, 400, -200]
    scene.add(fill, pose=fp)
    return scene

def render_cam(scene, name, data, out_dir, w=1920, h=1080):
    eye = np.array(data['eye'], dtype=float)
    target = np.array(data['target'], dtype=float)
    fwd = target - eye; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0,1,0])
    if np.linalg.norm(right) < 0.001: right = np.cross(fwd, [0,0,1])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    pose = np.eye(4); pose[:3,0]=right; pose[:3,1]=up; pose[:3,2]=-fwd; pose[:3,3]=eye
    cam = pyrender.PerspectiveCamera(yfov=math.radians(50), aspectRatio=w/h)
    cn = scene.add(cam, pose=pose)
    r = pyrender.OffscreenRenderer(w, h)
    color, _ = r.render(scene)
    r.delete()
    scene.remove_node(cn)
    path = os.path.join(out_dir, f'klft_{name}.png')
    Image.fromarray(color).save(path)
    print(f'Rendered: {path}')

if __name__ == '__main__':
    out = '/workspace/klft_renders'
    os.makedirs(out, exist_ok=True)
    print('Loading USD...')
    scene = build_scene('/workspace/klft-digital-twin.usda')
    print(f'Scene: {len(scene.mesh_nodes)} meshes')
    for name, data in CAMERAS.items():
        print(f'Rendering {name}...')
        render_cam(scene, name, data, out)
    print('Done.')
    os.system(f'ls -la {out}/')
