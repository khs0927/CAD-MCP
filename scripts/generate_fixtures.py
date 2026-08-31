"""
Architectural fixture generator for CAD-MCP benchmark suite.
Generates standard 6m x 8m room with 200mm walls, 900mm door, 1800mm window,
columns, dimensions, and text annotations for cross-provider testing.
"""

import math
import os
from pathlib import Path

def create_architectural_fixture_dxf(output_path: str):
    import ezdxf
    
    doc = ezdxf.new('R2018')
    msp = doc.modelspace()
    
    # Layers
    layers = [
        ("WAL1", 1, "CONTINUOUS"),     # Red - Exterior wall
        ("WAL2", 2, "CONTINUOUS"),     # Yellow - Interior wall
        ("COL", 4, "CONTINUOUS"),      # Cyan - Column
        ("DOOR", 3, "CONTINUOUS"),     # Green - Door
        ("WIN", 5, "CONTINUOUS"),      # Blue - Window
        ("DIM", 7, "CONTINUOUS"),      # White - Dimensions
        ("TEXT", 6, "CONTINUOUS"),     # Magenta - Text
        ("FURN", 8, "CONTINUOUS")      # Gray - Furniture
    ]
    for name, color, linetype in layers:
        if name not in doc.layers:
            doc.layers.add(name=name, color=color, linetype=linetype)
            
    # Define Door Block (900mm standard swing door)
    if "DOOR_900" not in doc.blocks:
        door_blk = doc.blocks.new(name="DOOR_900")
        door_blk.add_line((0, 0), (0, 900), dxfattribs={'layer': 'DOOR'})
        door_blk.add_arc((0, 0), radius=900, start_angle=0, end_angle=90, dxfattribs={'layer': 'DOOR'})
        door_blk.add_line((0, 0), (900, 0), dxfattribs={'layer': 'DOOR'})
        
    # Define Window Block (1800mm standard sash window)
    if "WIN_1800" not in doc.blocks:
        win_blk = doc.blocks.new(name="WIN_1800")
        win_blk.add_lwpolyline([(0, 0), (1800, 0), (1800, 200), (0, 200)], close=True, dxfattribs={'layer': 'WIN'})
        win_blk.add_line((0, 100), (1800, 100), dxfattribs={'layer': 'WIN'})
        win_blk.add_line((900, 0), (900, 200), dxfattribs={'layer': 'WIN'})
        
    # Define Column Block (400mm x 400mm)
    if "COL_400" not in doc.blocks:
        col_blk = doc.blocks.new(name="COL_400")
        col_blk.add_lwpolyline([(0, 0), (400, 0), (400, 400), (0, 400)], close=True, dxfattribs={'layer': 'COL'})
        col_blk.add_line((0, 0), (400, 400), dxfattribs={'layer': 'COL'})
        col_blk.add_line((0, 400), (400, 0), dxfattribs={'layer': 'COL'})
        
    # Draw Exterior Wall Polyline: 6000 x 8000 outer
    outer_pts = [(0, 0), (8000, 0), (8000, 6000), (0, 6000)]
    msp.add_lwpolyline(outer_pts, close=True, dxfattribs={'layer': 'WAL1'})
    
    # Inner wall polyline: 200mm wall thickness -> (200, 200) to (7800, 5800)
    inner_pts = [(200, 200), (7800, 200), (7800, 5800), (200, 5800)]
    msp.add_lwpolyline(inner_pts, close=True, dxfattribs={'layer': 'WAL1'})
    
    # Place 4 Corner Columns (400x400)
    msp.add_blockref("COL_400", (0, 0), dxfattribs={'layer': 'COL'})
    msp.add_blockref("COL_400", (7600, 0), dxfattribs={'layer': 'COL'})
    msp.add_blockref("COL_400", (7600, 5600), dxfattribs={'layer': 'COL'})
    msp.add_blockref("COL_400", (0, 5600), dxfattribs={'layer': 'COL'})
    
    # Place Door on South Wall (x=1000, y=0)
    msp.add_blockref("DOOR_900", (1000, 0), dxfattribs={'layer': 'DOOR'})
    
    # Place Window on North Wall (x=3100, y=5800)
    msp.add_blockref("WIN_1800", (3100, 5800), dxfattribs={'layer': 'WIN'})
    
    # Add Room Label Text
    msp.add_text("ROOM 1\nAREA = 48.0 m2", dxfattribs={
        'layer': 'TEXT',
        'height': 250,
        'insert': (3500, 3000)
    })
    
    # Add Dimensions
    msp.add_linear_dim(
        base=(4000, -600),
        p1=(0, 0),
        p2=(8000, 0),
        dxfattribs={'layer': 'DIM'}
    )
    msp.add_linear_dim(
        base=(-600, 3000),
        p1=(0, 0),
        p2=(0, 6000),
        angle=90,
        dxfattribs={'layer': 'DIM'}
    )
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.saveas(output_path)
    print(f"Architectural fixture created at: {output_path}")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "..", "fixtures", "arch_sample_room.dxf")
    create_architectural_fixture_dxf(target)
