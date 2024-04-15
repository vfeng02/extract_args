import sys
import os
import importlib
import argparse
import yaml
import json

def get_arg_details(module):
    parser = argparse.ArgumentParser()
    if module.__name__ == "direct_traversal": 
        parser = module.parse_args()
    else:
        module.add_args(parser)
    info={}
    args = {}

    if module.__doc__ is not None:
        desc = module.__doc__.split('\n')
        if len(desc) > 1:
            info["desc"] = desc[1]
        else:
            info["desc"] = desc[0]
    else:
        info["desc"] = ""

    for arg_group in parser._action_groups:
        arg_group_title = arg_group.title.lower() if arg_group.title != "options" else "optional arguments"

        if arg_group_title == "options": 
            arg_group_title = "additional arguments"
        elif arg_group_title == "positional arguments":
            arg_group_title = "required arguments"
        
        args[arg_group_title] = {}
        for arg in arg_group._group_actions:
            details = {}

            if arg.dest == "help":
                continue

            if arg.choices is not None:
                details["choices"] = arg.choices
            if arg.const is not None:
                details["const"] = arg.const
            if arg.default is not None:
                details["default"] = arg.default
            if arg.help is not None:
                details["help"] = arg.help
            if arg.metavar is not None:
                details["metavar"] = arg.metavar
            if arg.nargs is not None:
                details["nargs"] = arg.nargs
            if arg.type is not None:
                details["type"] = arg.type.__name__
            
            if len(arg.option_strings) > 0:
                details["flags"] = arg.option_strings
            
            if arg.required: 
              args["required arguments"][arg.dest] = details
            else: 
              args[arg_group_title][arg.dest] = details
    
    info["args"] = args
    return info

# save as one json
def save_as_one_json(modules):
    all_commands = {}
    for command in modules:
        globals()[command] = importlib.import_module(command)
        info = get_arg_details(globals()[command])
        all_commands[command] = info
    
    with open('./output/all_args2.json', 'w', encoding='utf-8') as f:
            json.dump(all_commands, f, ensure_ascii=False, indent=4)

# save as separate jsons
def save_as_jsons(modules):
    for command in modules:
        globals()[command] = importlib.import_module(command)
        args = get_arg_details(globals()[command])

        with open('./output/'+command+'_args.json', 'w', encoding='utf-8') as f:
            json.dump(args, f, ensure_ascii=False, indent=2)


def extract_args(cryodrgn_path):
    # Need to handle direct_traversal separately
    # import direct_traversal_add_args

# '/scratch/gpfs/vyfeng/cryodrgn'
    sys.path.append(cryodrgn_path)

    commands_path = cryodrgn_path + '/commands'
    commands_utils_path = cryodrgn_path + '/commands_utils'
    utils_path = cryodrgn_path + '/utils'

    all_commands = {}

    preprocess = ["parse_pose_star", "parse_pose_csparc", "parse_ctf_star", "parse_ctf_csparc", "downsample", "preprocess"]
    training = ["train_vae", "train_nn"]
    analysis = ["analyze", "pc_traversal", "direct_traversal", "graph_traversal"]
    conf_analysis = ["analyze_landscape", "analyze_landscape_full"]
    abinit = ["abinit_homo", "abinit_het"]
    misc = ["eval_images", "view_config", "eval_vol", "backproject_voxel"]
    utils = [f[:-3] for f in os.listdir(commands_utils_path) if f != '__init__.py'] + ["analyze_convergence"]

    commands_groups = {"Preprocess Inputs": preprocess, "cryoDRGN Training": training, "cryoDRGN Analysis": analysis, "Conformational Landscape Analysis": conf_analysis, "cryoDRGN2 Ab Initio Reconstruction": abinit, "Misc": misc, "Utils": utils}

    for path in [commands_path, commands_utils_path, utils_path]:
        sys.path.append(path)
        # if path == commands_path:
        #     modules = ['direct_traversal_add_args'] # Need to handle direct_traversal separately
        # modules += [f[:-3] for f in os.listdir(path) if f != '__init__.py' and f != 'direct_traversal.py' and f[-3:] == '.py']
        # modules += [f[:-3] for f in os.listdir(path) if f != '__init__.py']
    
    for group_name, modules in commands_groups:
        for command in modules:
          globals()[command] = importlib.import_module(command)
          info = get_arg_details(globals()[command])
          all_commands[group_name][command] = info
            
    # save_as_one_json(modules)

    with open('./data/all_args.json', 'w', encoding='utf-8') as f:
            json.dump(all_commands, f, ensure_ascii=False, indent=4)

    #remember to rename output json file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='extract',
                    description='extract the arguments when given a path to cryoDRGN')
    parser.add_argument('cryodrgn', type=str, help='the path to the cryoDRGN repository') 
    args = parser.parse_args()
    extract_args(args.cryodrgn)