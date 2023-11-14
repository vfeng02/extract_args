import sys
import os
import importlib
import argparse
import yaml
import json

def save_json(module):
    parser = argparse.ArgumentParser()
    module.add_args(parser)
    args = {}

    for arg_group in parser._action_groups:
         args[arg_group.title] = {}
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
            
            # if arg.required:
            #     args["positional arguments"][arg.dest] = details
            # else:
            #     args[arg_group.title][arg.dest] = details
            args[arg_group.title][arg.dest] = details
    
    # with open('args.yml', 'w') as outfile:
    #     yaml.dump(args, outfile)
    with open('./output/'+module.__name__+'_args.json', 'w', encoding='utf-8') as f:
        json.dump(args, f, ensure_ascii=False, indent=4)

def main():
    sys.path.append('/scratch/gpfs/vyfeng/cryodrgn')
    sys.path.append('/scratch/gpfs/vyfeng/cryodrgn/cryodrgn/commands')

    # Need to handle direct_traversal separately
    modules = [f[:-3] for f in os.listdir('/scratch/gpfs/vyfeng/cryodrgn/cryodrgn/commands') if f != '__init__.py' and f != 'direct_traversal.py' and f[-3:] == '.py']

    for command in modules:
        globals()[command] = importlib.import_module(command)
        save_json(globals()[command])
    
    # import direct_traversal_add_args as direct_traversal
    # save_json(direct_traversal)
    # # remember to rename output json file

if __name__ == "__main__":
    main()