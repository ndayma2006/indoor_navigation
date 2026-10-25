import sqlite3
import re
import json
from typing import List, Dict, Any, Optional
from .db import get_db_connection

_cached_rooms: Optional[List[Dict[str, Any]]] = None
_cached_faculty: Optional[List[Dict[str, Any]]] = None

def search_campus(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    query_clean = query.strip().lower()
    if not query_clean:
        return []

    # Multilingual translation/synonym map
    multilingual_maps = {
        "मुख्य": "main", "प्रवेश": "entrance", "गेट": "gate",
        "दवाखाना": "hospital", "रुग्णालय": "hospital", "हॉस्पिटल": "hospital",
        "पोलीस": "police", "थाना": "police", "स्टेशन": "station",
        "ग्रंथालय": "library", "पुस्तकालय": "library",
        "प्राचार्य": "principal", "केबिन": "cabin",
        "कार्यालय": "office", "ऑफिस": "office", "विभाग": "department",
        "लॅब": "lab", "प्रयोगशाळा": "lab"
    }

    for dev, eng in multilingual_maps.items():
        if dev in query_clean:
            query_clean = query_clean.replace(dev, eng)

    # Clean query tokens (strip punctuation and possessives like 's)
    clean_text = re.sub(r"['’]s\b", "", query_clean)
    tokens = [t for t in re.split(r'[\s\-_,\.\?\!/]+', clean_text) if t]
    
    global _cached_rooms, _cached_faculty
    if _cached_rooms is None or _cached_faculty is None:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.*, f.name as floor_name
            FROM rooms r
            JOIN floors f ON r.floor_id = f.id
        """)
        _cached_rooms = [dict(row) for row in cur.fetchall()]

        cur.execute("""
            SELECT fac.*, r.name as room_name, r.room_number, r.x, r.y, r.z, r.door_x, r.door_y, r.color, f.name as floor_name
            FROM faculty fac
            JOIN rooms r ON fac.cabin_room_id = r.id
            JOIN floors f ON fac.floor_id = f.id
        """)
        _cached_faculty = [dict(row) for row in cur.fetchall()]
        conn.close()

    rooms = _cached_rooms
    faculty = _cached_faculty

    results = []
    seen_ids = set()

    STOP_WORDS = {"where", "is", "the", "are", "how", "to", "reach", "take", "me", "show", "can", "find", "and", "in", "of", "for", "at", "what", "which", "my", "tell", "a", "an", "do", "i"}
    meaningful_tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]

    # 1. Search Faculty first (high priority for people queries)
    for fac in faculty:
        fac_name = fac["name"].lower()
        fac_sub = (fac["subject"] or "").lower()
        fac_cabin = fac["cabin_name"].lower()
        dept = fac["department"].lower()

        score = 0
        if query_clean in fac_name:
            score += 150
        else:
            name_hits = [t for t in meaningful_tokens if re.search(r'\b' + re.escape(t), fac_name)]
            if name_hits:
                score += 80 * len(name_hits)
            sub_hits = [t for t in meaningful_tokens if re.search(r'\b' + re.escape(t), fac_sub)]
            if sub_hits:
                score += 30 * len(sub_hits)

        if score > 0:
            rid = f"FAC_{fac['id']}"
            if rid not in seen_ids:
                seen_ids.add(rid)
                results.append({
                    "id": fac["cabin_room_id"],
                    "name": f"{fac['name']} ({fac['designation']})",
                    "subtitle": f"Cabin: {fac['cabin_name']} | Dept: {fac['department']}",
                    "department": fac["department"],
                    "floor_id": fac["floor_id"],
                    "floor_name": fac["floor_name"],
                    "room_type": "Faculty Cabin",
                    "x": fac["x"], "y": fac["y"], "z": fac["z"],
                    "door_x": fac["door_x"], "door_y": fac["door_y"],
                    "color": "#8b5cf6",
                    "score": score
                })

    # 2. Search Rooms
    for r in rooms:
        r_name = r["name"].lower()
        r_num = (r["room_number"] or "").lower()
        r_dept = r["department"].lower()
        r_type = r["room_type"].lower()
        r_info = (r["info"] or "").lower()

        score = 0
        # Exact room number hit
        if r_num and (query_clean == r_num or f"room {r_num}" in query_clean or f"room{r_num}" in query_clean):
            score += 150
        elif query_clean == r_name:
            score += 130
        elif query_clean in r_name:
            score += 100
        else:
            name_hits = [t for t in meaningful_tokens if re.search(r'\b' + re.escape(t), r_name)]
            if name_hits:
                score += 60 * len(name_hits)
            if r_dept in meaningful_tokens:
                score += 40
            info_hits = [t for t in meaningful_tokens if re.search(r'\b' + re.escape(t), r_info)]
            if info_hits:
                score += 20 * len(info_hits)

        if score > 0:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                results.append({
                    "id": r["id"],
                    "name": r["name"],
                    "subtitle": f"{r['department']} | {r['floor_name']} (Room {r.get('room_number', '-')})",
                    "department": r["department"],
                    "floor_id": r["floor_id"],
                    "floor_name": r["floor_name"],
                    "room_type": r["room_type"],
                    "x": r["x"], "y": r["y"], "z": r["z"],
                    "door_x": r["door_x"], "door_y": r["door_y"],
                    "color": r.get("color", "#3b82f6"),
                    "score": score
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

def get_room_by_id(room_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, f.name as floor_name
        FROM rooms r
        JOIN floors f ON r.floor_id = f.id
        WHERE r.id = ?
    """, (room_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_rooms(floor_id: Optional[int] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    if floor_id is not None:
        cur.execute("""
            SELECT r.*, f.name as floor_name
            FROM rooms r
            JOIN floors f ON r.floor_id = f.id
            WHERE r.floor_id = ?
            ORDER BY r.department, r.name
        """, (floor_id,))
    else:
        cur.execute("""
            SELECT r.*, f.name as floor_name
            FROM rooms r
            JOIN floors f ON r.floor_id = f.id
            ORDER BY r.floor_id, r.department, r.name
        """)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def get_all_floors() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM floors ORDER BY id")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def get_all_staircases() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staircases ORDER BY id")
    rows = []
    for row in cur.fetchall():
        d = dict(row)
        d["floors_connected"] = json.loads(d["floors_connected"]) if isinstance(d["floors_connected"], str) else d["floors_connected"]
        rows.append(d)
    conn.close()
    return rows

def get_all_faculty(department: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cur = conn.cursor()
    if department:
        cur.execute("""
            SELECT fac.*, r.name as room_name, r.room_number, r.x, r.y, r.z, r.door_x, r.door_y, r.color, f.name as floor_name
            FROM faculty fac
            JOIN rooms r ON fac.cabin_room_id = r.id
            JOIN floors f ON fac.floor_id = f.id
            WHERE LOWER(fac.department) = LOWER(?)
            ORDER BY fac.id
        """, (department,))
    else:
        cur.execute("""
            SELECT fac.*, r.name as room_name, r.room_number, r.x, r.y, r.z, r.door_x, r.door_y, r.color, f.name as floor_name
            FROM faculty fac
            JOIN rooms r ON fac.cabin_room_id = r.id
            JOIN floors f ON fac.floor_id = f.id
            ORDER BY fac.department, fac.id
        """)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def get_campus_full_data() -> Dict[str, Any]:
    rooms = get_all_rooms()
    faculty = get_all_faculty()
    floors = get_all_floors()
    staircases = get_all_staircases()
    return {
        "status": "success",
        "floors": floors,
        "rooms": rooms,
        "faculty": faculty,
        "staircases": staircases
    }

