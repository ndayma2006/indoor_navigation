from typing import List, Dict, Any
import networkx as nx

class FloorTransitionManager:
    def __init__(self):
        pass

    def extract_transitions(self, G: nx.Graph, path: List[str]) -> List[Dict[str, Any]]:
        transitions = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edge = G.get_edge_data(u, v) or {}
            edge_type = edge.get("edge_type")
            if edge_type in ("stairs", "lift"):
                u_floor = G.nodes[u]["floor_id"]
                v_floor = G.nodes[v]["floor_id"]
                stair_id = edge.get("stair_id", "STAIR_S1")
                direction = "up" if v_floor > u_floor else "down"

                stair_labels = {
                    "STAIR_S1": "Staircase S1 (South-West Core)",
                    "STAIR_S2": "Staircase S2 (North-East Core)",
                    "LIFT_L1": "Central Lift L1 (Courtyard Core)"
                }

                transitions.append({
                    "type": edge_type,
                    "stair_id": stair_id,
                    "stair_name": stair_labels.get(stair_id, stair_id),
                    "from_floor": u_floor,
                    "to_floor": v_floor,
                    "direction": direction,
                    "x": G.nodes[u]["x"],
                    "y": G.nodes[u]["y"],
                    "instruction": f"Use {stair_labels.get(stair_id, stair_id)} to go {direction} from Floor {u_floor} to Floor {v_floor}."
                })
        return transitions
