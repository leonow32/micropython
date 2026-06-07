import json
import rich

tree = {}

def add_to_tree(*args):
    global tree
    
    if len(args) < 2:
        raise ValueError(f"add_to_tree({args}) - at least two arguments needed")
    
    path_keys = args[:-2]
    last_key  = args[-2]
    value     = args[-1]
    level     = tree
        
    for key in path_keys:
        if key not in level:
            level[key] = {}
        
        level = level[key]
        
    level[last_key] = value

add_to_tree("a", 1)
add_to_tree("b", 1)
add_to_tree("c", "a", 1)
add_to_tree("c", "b", 1)
add_to_tree("c", "c", "a", 1)
add_to_tree("c", "d", 1)

string = json.dumps(tree, sort_keys=True, indent=4)
rich.print_json(string)