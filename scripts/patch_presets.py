"""Patch camera presets on the render agent — run on pod."""
import json

with open('/workspace/render_agent.py') as f:
    content = f.read()

NEW_PRESETS = {
    "hero_front": {
        "description": "Elevated front perspective of facility",
        "eye_offset": [0.0, 0.35, 1.8],
        "focal_length": 28.0,
    },
    "hero_quarter": {
        "description": "Classic 3/4 angle showing depth and facade",
        "eye_offset": [1.4, 0.4, 1.4],
        "focal_length": 24.0,
    },
    "aerial_overview": {
        "description": "High aerial showing full facility and site",
        "eye_offset": [0.5, 3.0, 0.8],
        "focal_length": 14.0,
    },
    "side_elevation": {
        "description": "Side profile from ground level",
        "eye_offset": [2.0, 0.25, 0.0],
        "focal_length": 35.0,
    },
    "rear_three_quarter": {
        "description": "Rear 3/4 showing cooling and back facade",
        "eye_offset": [-1.3, 0.4, -1.3],
        "focal_length": 24.0,
    },
    "cooling_infrastructure": {
        "description": "Cooling systems from pulled-back angle",
        "eye_offset": [-1.8, 0.35, 0.5],
        "focal_length": 28.0,
    },
    "power_yard": {
        "description": "Power distribution yard and equipment",
        "eye_offset": [1.5, 0.3, -1.0],
        "focal_length": 28.0,
    },
    "bird_eye_full": {
        "description": "Bird eye view of entire site with terrain",
        "eye_offset": [0.3, 4.0, 0.3],
        "focal_length": 12.0,
    },
    "entry_approach": {
        "description": "Ground-level approach view of main entrance",
        "eye_offset": [0.3, 0.15, 2.2],
        "focal_length": 35.0,
    },
    "panoramic_site": {
        "description": "Wide panoramic showing facility in landscape",
        "eye_offset": [1.0, 1.8, 1.5],
        "focal_length": 14.0,
    },
    "diagonal_high": {
        "description": "Diagonal elevated showing roof and two facades",
        "eye_offset": [1.2, 1.0, 1.2],
        "focal_length": 20.0,
    },
    "equipment_closeup": {
        "description": "Equipment detail from medium distance",
        "eye_offset": [0.8, 0.2, 0.8],
        "focal_length": 50.0,
    },
}

# Find CAMERA_PRESETS block and replace
start = content.find('CAMERA_PRESETS = {')
if start == -1:
    print('ERROR: CAMERA_PRESETS not found')
    exit(1)

brace_count = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{':
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break

# Build replacement
lines = ['CAMERA_PRESETS = {']
for name, cfg in NEW_PRESETS.items():
    lines.append(f'    "{name}": {{')
    lines.append(f'        "description": "{cfg["description"]}",')
    lines.append(f'        "eye_offset": {cfg["eye_offset"]},')
    lines.append(f'        "focal_length": {cfg["focal_length"]},')
    lines.append('    },')
lines.append('}')
replacement = '\n'.join(lines)

new_content = content[:start] + replacement + content[end:]

with open('/workspace/render_agent.py', 'w') as f:
    f.write(new_content)

print(f'Patched {len(NEW_PRESETS)} camera presets OK')
