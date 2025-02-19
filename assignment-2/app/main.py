from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {}
houses = {}
rooms = {}
devices = {}

# USERS
@app.post("/users/")
def create_user(user_id: int, name: str):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user_id] = {"id": user_id, "name": name}
    return users[user_id]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

# HOUSES
@app.post("/houses/")
def create_house(house_id: int, name: str, owner_id: int):
    if house_id in houses:
        raise HTTPException(status_code=400, detail="House already exists")
    if owner_id not in users:
        raise HTTPException(status_code=404, detail="Owner not found")
    houses[house_id] = {"id": house_id, "name": name, "owner_id": owner_id}
    return houses[house_id]

@app.get("/houses/{house_id}")
def get_house(house_id: int):
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    return houses[house_id]

# ROOMS
@app.post("/rooms/")
def create_room(room_id: int, name: str, house_id: int):
    if room_id in rooms:
        raise HTTPException(status_code=400, detail="Room already exists")
    if house_id not in houses:
        raise HTTPException(status_code=404, detail="House not found")
    rooms[room_id] = {"id": room_id, "name": name, "house_id": house_id}
    return rooms[room_id]

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]

# DEVICES
@app.post("/devices/")
def create_device(device_id: int, name: str, type: str, room_id: int):
    if device_id in devices:
        raise HTTPException(status_code=400, detail="Device already exists")
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    devices[device_id] = {"id": device_id, "name": name, "type": type, "room_id": room_id, "status": "OFF"}
    return devices[device_id]

@app.get("/devices/{device_id}")
def get_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices[device_id]

@app.put("/devices/{device_id}")
def update_device_status(device_id: int, status: str):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    if status not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    devices[device_id]["status"] = status
    return devices[device_id]

@app.delete("/devices/{device_id}")
def delete_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")
    del devices[device_id]
    return {"message": "Device deleted"}