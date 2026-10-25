import math
from typing import List, Dict, Any, Tuple
import networkx as nx
from ..models.schemas import RouteStep
from ..cad.geometry import distance_2d

def compute_turn_direction(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> str:
    """Computes whether the turn at p2 is left, right, or straight using vector cross product."""
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    mag1 = math.hypot(v1[0], v1[1])
    mag2 = math.hypot(v2[0], v2[1])

    if mag1 < 0.1 or mag2 < 0.1:
        return "straight"

    cross_prod = v1[0] * v2[1] - v1[1] * v2[0]
    dot_prod = v1[0] * v2[0] + v1[1] * v2[1]
    angle_deg = math.degrees(math.atan2(cross_prod, dot_prod))

    if abs(angle_deg) < 25.0:
        return "straight"
    elif angle_deg > 25.0:
        return "left"
    else:
        return "right"

def generate_turn_by_turn_directions(
    G: nx.Graph,
    node_path: List[str],
    floor_names: Dict[int, str]
) -> List[RouteStep]:
    if not node_path or len(node_path) < 2:
        return []

    steps: List[RouteStep] = []
    step_num = 1

    current_segment_coords = []
    current_segment_dist = 0.0

    i = 0
    while i < len(node_path) - 1:
        u = node_path[i]
        v = node_path[i+1]
        edge_data = G.get_edge_data(u, v) or {}
        edge_type = edge_data.get("edge_type", "corridor")
        stair_id = edge_data.get("stair_id")

        u_data = G.nodes[u]
        v_data = G.nodes[v]

        u_pt = [u_data["x"], u_data["y"], u_data["z"]]
        v_pt = [v_data["x"], v_data["y"], v_data["z"]]
        fid = u_data["floor_id"]
        fname = floor_names.get(fid, f"Floor {fid}")

        # Check for vertical transition (stairs or lift)
        if edge_type in ("stairs", "lift"):
            # Flush existing segment if any
            if current_segment_coords:
                steps.append(RouteStep(
                    step_number=step_num,
                    floor_id=fid,
                    floor_name=fname,
                    instruction=f"Walk along the corridor on {fname}.",
                    distance_meters=round(current_segment_dist, 1),
                    turn="straight",
                    coordinates=current_segment_coords
                ))
                step_num += 1
                current_segment_coords = []
                current_segment_dist = 0.0

            # Vertical transition step
            target_fid = v_data["floor_id"]
            target_fname = floor_names.get(target_fid, f"Floor {target_fid}")
            direction = "up" if target_fid > fid else "down"
            
            if edge_type == "stairs":
                stair_name = "Staircase S1" if stair_id == "STAIR_S1" else "Staircase S2"
                inst = f"Take {stair_name} {direction} to {target_fname}."
                turn_action = f"stairs_{direction}"
            else:
                inst = f"Take Lift L1 {direction} to {target_fname}."
                turn_action = f"lift_{direction}"

            vert_dist = edge_data.get("weight", 6.0)
            steps.append(RouteStep(
                step_number=step_num,
                floor_id=target_fid,
                floor_name=target_fname,
                instruction=inst,
                distance_meters=round(vert_dist, 1),
                turn=turn_action,
                staircase_id=stair_id,
                coordinates=[u_pt, v_pt]
            ))
            step_num += 1
            i += 1
            continue

        # Same floor corridor or door step
        d = edge_data.get("weight", distance_2d((u_pt[0], u_pt[1]), (v_pt[0], v_pt[1])))
        if not current_segment_coords:
            current_segment_coords.append(u_pt)
        current_segment_coords.append(v_pt)
        current_segment_dist += d

        # Check if next step involves a turn or transition
        is_turn = False
        turn_str = "straight"
        if i < len(node_path) - 2:
            w = node_path[i+2]
            w_data = G.nodes[w]
            w_pt = [w_data["x"], w_data["y"], w_data["z"]]
            next_edge = G.get_edge_data(v, w) or {}
            if next_edge.get("edge_type") not in ("stairs", "lift"):
                turn_str = compute_turn_direction((u_pt[0], u_pt[1]), (v_pt[0], v_pt[1]), (w_pt[0], w_pt[1]))
                if turn_str != "straight":
                    is_turn = True
            else:
                is_turn = True

        if is_turn or i == len(node_path) - 2:
            # Complete the current step
            if i == len(node_path) - 2 and v_data.get("node_type") == "room":
                dest_name = v_data.get("room_name", "your destination")
                inst = f"Walk straight {round(current_segment_dist, 1)}m and enter {dest_name}."
            elif turn_str != "straight":
                inst = f"Walk {round(current_segment_dist, 1)}m and turn {turn_str}."
            else:
                inst = f"Proceed straight along corridor for {round(current_segment_dist, 1)}m."

            steps.append(RouteStep(
                step_number=step_num,
                floor_id=fid,
                floor_name=fname,
                instruction=inst,
                distance_meters=round(current_segment_dist, 1),
                turn=turn_str,
                coordinates=current_segment_coords
            ))
            step_num += 1
            current_segment_coords = []
            current_segment_dist = 0.0

        i += 1

    return steps
