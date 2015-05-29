PHYSICS_SETTINGS = {
        "gravity" : 1, "terminal_velocity" : 30, # AKA: max downwards speed
        "time_scale" : 10
        } 

def apply_gravity(body, time):
    velocity = PHYSICS_SETTINGS["gravity"] * time / PHYSICS_SETTINGS["time_scale"]
    body.velocity.y += velocity
    if body.velocity.y > PHYSICS_SETTINGS["terminal_velocity"]:
        body.velocity.y = PHYSICS_SETTINGS["terminal_velocity"]
