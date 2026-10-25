import networkx as nx
import math
from typing import Dict, Any, List, Tuple
from ..data.search_service import get_all_rooms, get_all_floors, get_all_staircases
from ..cad.geometry import distance_2d, distance_3d

class CampusGraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()
        self.floors = get_all_floors()
        self.rooms = get_all_rooms()
        self.staircases = get_all_staircases()

    def build_graph(self) -> nx.Graph:
        G = nx.Graph()
        
        # Elevations mapping
        elevations = {f["id"]: f["elevation"] for f in self.floors}

        # Corridor bounds:
        # West: x=16.0, y in [18.0, 42.0]
        # North: y=42.0, x in [16.0, 49.2]
        # East: x=49.2, y in [18.0, 42.0]
        # South: y=18.0, x in [16.0, 49.2]

        for floor in self.floors:
            fid = floor["id"]
            z = elevations.get(fid, 0.0)

            # 1. Build corridor grid nodes for this floor
            corridor_nodes = []

            # South corridor nodes: y=18.0, x from 16.0 to 49.2
            for x in [16.0, 20.5, 25.0, 28.0, 32.5, 35.0, 38.0, 39.9, 41.0, 44.0, 47.0, 49.2]:
                nid = f"CORR_S_{fid}_{x:.1f}"
                G.add_node(nid, x=x, y=18.0, z=z, floor_id=fid, node_type="corridor")
                corridor_nodes.append((nid, x, 18.0))

            # West corridor nodes: x=16.0, y from 18.0 to 42.0
            for y in [19.5, 23.0, 26.0, 29.0, 32.5, 36.0, 39.0, 42.0]:
                nid = f"CORR_W_{fid}_{y:.1f}"
                G.add_node(nid, x=16.0, y=y, z=z, floor_id=fid, node_type="corridor")
                corridor_nodes.append((nid, 16.0, y))

            # North corridor nodes: y=42.0, x from 16.0 to 49.2
            for x in [20.0, 24.0, 28.0, 32.5, 37.0, 41.0, 45.0, 48.5, 49.2]:
                nid = f"CORR_N_{fid}_{x:.1f}"
                G.add_node(nid, x=x, y=42.0, z=z, floor_id=fid, node_type="corridor")
                corridor_nodes.append((nid, x, 42.0))

            # East corridor nodes: x=49.2, y from 18.0 to 42.0
            for y in [21.0, 25.0, 27.0, 31.0, 33.0, 37.0, 39.0]:
                nid = f"CORR_E_{fid}_{y:.1f}"
                G.add_node(nid, x=49.2, y=y, z=z, floor_id=fid, node_type="corridor")
                corridor_nodes.append((nid, 49.2, y))

            # Connect consecutive corridor nodes along each segment
            # South segment
            s_nodes = sorted([n for n in corridor_nodes if abs(n[2] - 18.0) < 0.1], key=lambda n: n[1])
            for i in range(len(s_nodes) - 1):
                d = distance_2d((s_nodes[i][1], s_nodes[i][2]), (s_nodes[i+1][1], s_nodes[i+1][2]))
                G.add_edge(s_nodes[i][0], s_nodes[i+1][0], weight=d, edge_type="corridor")

            # West segment
            w_nodes = sorted([n for n in corridor_nodes if abs(n[1] - 16.0) < 0.1], key=lambda n: n[2])
            for i in range(len(w_nodes) - 1):
                d = distance_2d((w_nodes[i][1], w_nodes[i][2]), (w_nodes[i+1][1], w_nodes[i+1][2]))
                G.add_edge(w_nodes[i][0], w_nodes[i+1][0], weight=d, edge_type="corridor")

            # North segment
            n_nodes = sorted([n for n in corridor_nodes if abs(n[2] - 42.0) < 0.1], key=lambda n: n[1])
            for i in range(len(n_nodes) - 1):
                d = distance_2d((n_nodes[i][1], n_nodes[i][2]), (n_nodes[i+1][1], n_nodes[i+1][2]))
                G.add_edge(n_nodes[i][0], n_nodes[i+1][0], weight=d, edge_type="corridor")

            # East segment
            e_nodes = sorted([n for n in corridor_nodes if abs(n[1] - 49.2) < 0.1], key=lambda n: n[2])
            for i in range(len(e_nodes) - 1):
                d = distance_2d((e_nodes[i][1], e_nodes[i][2]), (e_nodes[i+1][1], e_nodes[i+1][2]))
                G.add_edge(e_nodes[i][0], e_nodes[i+1][0], weight=d, edge_type="corridor")

            # Corner connections
            # SW corner: (16.0, 18.0) is in both South and West lists
            # NW corner: (16.0, 42.0) is in both West and North lists
            # NE corner: (49.2, 42.0) is in both North and East lists
            # SE corner: (49.2, 18.0) is in both East and South lists

            # Additional North-wing extensions (e.g., towards Classroom 10/50 and Labs 36-37)
            G.add_node(f"EXT_N_WEST_{fid}", x=16.0, y=54.0, z=z, floor_id=fid, node_type="corridor")
            G.add_edge(f"CORR_W_{fid}_42.0", f"EXT_N_WEST_{fid}", weight=12.0, edge_type="corridor")

            G.add_node(f"EXT_N_EAST_{fid}", x=49.2, y=54.0, z=z, floor_id=fid, node_type="corridor")
            G.add_edge(f"CORR_N_{fid}_49.2", f"EXT_N_EAST_{fid}", weight=12.0, edge_type="corridor")

            # 2. Add Staircases Landing Nodes for this floor
            # Staircase S1 (South-West) connects at (20.5, 18.0)
            stair_s1_id = f"STAIR_S1_LANDING_{fid}"
            G.add_node(stair_s1_id, x=20.5, y=18.0, z=z, floor_id=fid, node_type="stair_landing", stair_id="STAIR_S1")
            G.add_edge(stair_s1_id, f"CORR_S_{fid}_20.5", weight=0.1, edge_type="stair_landing")

            # Staircase S2 (North-East) connects at (48.5, 42.0)
            stair_s2_id = f"STAIR_S2_LANDING_{fid}"
            G.add_node(stair_s2_id, x=48.5, y=42.0, z=z, floor_id=fid, node_type="stair_landing", stair_id="STAIR_S2")
            G.add_edge(stair_s2_id, f"CORR_N_{fid}_48.5", weight=0.1, edge_type="stair_landing")

            # Lift L1 (Courtyard South edge) connects at (39.9, 18.0)
            lift_l1_id = f"LIFT_L1_LANDING_{fid}"
            G.add_node(lift_l1_id, x=39.9, y=18.0, z=z, floor_id=fid, node_type="lift_landing", stair_id="LIFT_L1")
            G.add_edge(lift_l1_id, f"CORR_S_{fid}_39.9", weight=0.1, edge_type="lift_landing")

            # 3. Add Rooms on this floor
            floor_rooms = [r for r in self.rooms if r["floor_id"] == fid]
            for room in floor_rooms:
                rid = room["id"]
                rx, ry = room["x"], room["y"]
                dx, dy = room["door_x"], room["door_y"]

                # Room center node
                G.add_node(rid, x=rx, y=ry, z=z, floor_id=fid, node_type="room", room_name=room["name"])

                # Room door node
                door_id = f"{rid}_DOOR"
                G.add_node(door_id, x=dx, y=dy, z=z, floor_id=fid, node_type="door")
                d_room_door = distance_2d((rx, ry), (dx, dy))
                G.add_edge(rid, door_id, weight=max(1.0, d_room_door), edge_type="door_connection")

                # Connect door to the nearest corridor node on this floor
                corr_candidates = [n for n in corridor_nodes]
                closest_corr = min(corr_candidates, key=lambda c: distance_2d((dx, dy), (c[1], c[2])))
                d_corr = distance_2d((dx, dy), (closest_corr[1], closest_corr[2]))
                G.add_edge(door_id, closest_corr[0], weight=d_corr, edge_type="corridor_connection")

        # 4. Multi-Floor Vertical Transitions
        # Connect Staircase S1 across Floors 0 <-> 1 <-> 2
        for f1, f2 in [(0, 1), (1, 2)]:
            s1_a = f"STAIR_S1_LANDING_{f1}"
            s1_b = f"STAIR_S1_LANDING_{f2}"
            vert_dist = abs(elevations[f2] - elevations[f1]) + 4.5  # walking stair flight distance
            G.add_edge(s1_a, s1_b, weight=vert_dist, edge_type="stairs", stair_id="STAIR_S1")

            s2_a = f"STAIR_S2_LANDING_{f1}"
            s2_b = f"STAIR_S2_LANDING_{f2}"
            G.add_edge(s2_a, s2_b, weight=vert_dist, edge_type="stairs", stair_id="STAIR_S2")

            l1_a = f"LIFT_L1_LANDING_{f1}"
            l1_b = f"LIFT_L1_LANDING_{f2}"
            lift_cost = abs(elevations[f2] - elevations[f1]) + 2.0  # quick vertical transport
            G.add_edge(l1_a, l1_b, weight=lift_cost, edge_type="lift", stair_id="LIFT_L1")

        self.graph = G
        return G
