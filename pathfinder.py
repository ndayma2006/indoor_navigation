import networkx as nx
from typing import Optional, List, Dict, Any
from .graph_builder import CampusGraphBuilder
from .directions import generate_turn_by_turn_directions
from .floor_transitions import FloorTransitionManager
from ..models.schemas import NavigationRequest, NavigationResponse, RouteStep
from ..data.search_service import get_room_by_id, get_all_floors
from ..cad.geometry import distance_2d

class CampusPathfinder:
    def __init__(self):
        self.builder = CampusGraphBuilder()
        self.graph = self.builder.build_graph()
        self.transition_mgr = FloorTransitionManager()
        self.floors_dict = {f["id"]: f["name"] for f in get_all_floors()}

    def reload_graph(self):
        self.graph = self.builder.build_graph()

    def find_path(self, request: NavigationRequest) -> NavigationResponse:
        dest_room = get_room_by_id(request.destination_room_id)
        if not dest_room:
            return NavigationResponse(
                success=False,
                message=f"Destination room '{request.destination_room_id}' was not found in campus database.",
                start_name="",
                destination_name="",
                destination_floor=0,
                total_distance_meters=0.0,
                estimated_time_seconds=0,
                floor_transitions=[],
                steps=[],
                full_path_3d=[],
                floors_involved=[]
            )

        target_node = dest_room["id"]

        # Determine start node
        start_name = "Selected Starting Location"
        start_floor = request.start_floor or 0

        if request.start_room_id:
            start_room = get_room_by_id(request.start_room_id)
            if start_room:
                start_node = start_room["id"]
                start_name = start_room["name"]
                start_floor = start_room["floor_id"]
            else:
                start_node = "MAIN_GATE"
                start_name = "Main Entrance (Default Fallback)"
        elif request.start_coords and len(request.start_coords) >= 2:
            # Snap arbitrary coordinates to the closest node on that floor
            sx, sy = request.start_coords[0], request.start_coords[1]
            floor_nodes = [
                n for n, d in self.graph.nodes(data=True)
                if d.get("floor_id") == start_floor and d.get("node_type") in ("corridor", "room", "door")
            ]
            if floor_nodes:
                start_node = min(floor_nodes, key=lambda n: distance_2d((sx, sy), (self.graph.nodes[n]["x"], self.graph.nodes[n]["y"])))
                start_name = f"Custom Position ({sx:.1f}, {sy:.1f}) on {self.floors_dict.get(start_floor, 'Floor')}"
            else:
                start_node = "MAIN_GATE"
                start_name = "Main Entrance (Default Fallback)"
        else:
            start_node = "MAIN_GATE"
            start_name = "SITCOE Main Entrance / Porch"

        # Check if nodes exist in graph
        if start_node not in self.graph:
            return NavigationResponse(
                success=False,
                message=f"Starting location '{start_node}' is not connected to the indoor navigation graph.",
                start_name=start_name,
                destination_name=dest_room["name"],
                destination_floor=dest_room["floor_id"],
                total_distance_meters=0.0,
                estimated_time_seconds=0,
                floor_transitions=[],
                steps=[],
                full_path_3d=[],
                floors_involved=[]
            )

        if target_node not in self.graph:
            return NavigationResponse(
                success=False,
                message=f"Destination '{dest_room['name']}' is not linked to the indoor navigation graph.",
                start_name=start_name,
                destination_name=dest_room["name"],
                destination_floor=dest_room["floor_id"],
                total_distance_meters=0.0,
                estimated_time_seconds=0,
                floor_transitions=[],
                steps=[],
                full_path_3d=[],
                floors_involved=[]
            )

        # Pathfinding with preference for lift if requested
        if request.prefer_lift:
            working_graph = self.graph.copy()
            # Lower weight of lift edges and increase stairs
            for u, v, data in working_graph.edges(data=True):
                if data.get("edge_type") == "lift":
                    data["weight"] = 1.0
                elif data.get("edge_type") == "stairs":
                    data["weight"] = 30.0
        else:
            working_graph = self.graph

        try:
            node_path = nx.shortest_path(working_graph, source=start_node, target=target_node, weight="weight")
            total_dist = nx.shortest_path_length(working_graph, source=start_node, target=target_node, weight="weight")
        except nx.NetworkXNoPath:
            return NavigationResponse(
                success=False,
                message=f"No walkable indoor route could be found connecting {start_name} to {dest_room['name']}.",
                start_name=start_name,
                destination_name=dest_room["name"],
                destination_floor=dest_room["floor_id"],
                total_distance_meters=0.0,
                estimated_time_seconds=0,
                floor_transitions=[],
                steps=[],
                full_path_3d=[],
                floors_involved=[]
            )

        # Extract 3D path coordinates
        full_path_3d = []
        floors_set = set()
        for nid in node_path:
            ndata = self.graph.nodes[nid]
            full_path_3d.append([round(ndata["x"], 2), round(ndata["y"], 2), round(ndata["z"], 2)])
            floors_set.add(ndata["floor_id"])

        # Extract multi-floor transitions and turn-by-turn steps
        transitions = self.transition_mgr.extract_transitions(self.graph, node_path)
        steps = generate_turn_by_turn_directions(self.graph, node_path, self.floors_dict)

        # Estimated time at ~1.2 m/s average indoor walking pace + 10s per floor change
        est_seconds = int(total_dist / 1.2) + len(transitions) * 10

        return NavigationResponse(
            success=True,
            message="Optimal indoor route successfully calculated.",
            start_name=start_name,
            destination_name=dest_room["name"],
            destination_floor=dest_room["floor_id"],
            total_distance_meters=round(total_dist, 1),
            estimated_time_seconds=max(15, est_seconds),
            floor_transitions=transitions,
            steps=steps,
            full_path_3d=full_path_3d,
            floors_involved=sorted(list(floors_set))
        )
