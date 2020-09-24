from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []
visited = set()

opposite_dir = { 'w': 'e', 'e': 'w', 'n': 's', 's': 'n' }

# dfs, backtrack, but will take long loop arounds. 1st iteration. 998 moves
def dfs(visited, room, path, d):
    if room.name not in visited:
        if d:
            path.append(d)
        visited.add(room.name)
        for exit in room.get_exits():
            room_in_dir = room.get_room_in_direction(exit)
            if room_in_dir.name not in visited:
                dfs(visited, room_in_dir, path, exit)
                path.append(opposite_dir[exit])

# dfs(visited, player.current_room, traversal_path, "")

visited2 = {}
stack = [player.current_room]

def dfs2(path, iter=0):
    d = ""
    while stack:
        if iter == 15:
            return
        curr_room = stack[-1]
        if curr_room.name not in visited2:
            visited2[curr_room.name] = set()
        if d:
            visited2[curr_room.name].add(opposite_dir[d])
            path.append(d)
        new_rooms = []
        for exit in curr_room.get_exits():
            room_in_dir = curr_room.get_room_in_direction(exit)
            # print(room_in_dir.name, exit)
            if room_in_dir.name not in visited2 or exit not in visited2[curr_room.name]:
                d = exit
                visited2[curr_room.name].add(d)
                # print(d)
                new_rooms.append(room_in_dir)
                break
                # path.append(opposite_dir[exit])
        if new_rooms: 
            stack.extend(new_rooms)
        else:
            stack.pop()
        print(curr_room.name)
        # print(visited2)
        iter += 1
dfs2(traversal_path)

# player.travel('n', True)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
