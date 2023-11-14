import example
import argparse
import yaml
import json

class Arg:
  def __init__(self, option_strings, name, num, default, type):
    self.option_strings = option_strings
    self.name = name
    self.num = num
    self.default = default
    self.type = type

def main():
    parser = argparse.ArgumentParser(description='Example parser')
    example.add_args(parser)
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
   
            args[arg_group.title][arg.dest] = details
    
    # print(args)
    # with open('args.yml', 'w') as outfile:
    #     yaml.dump(args, outfile)
    with open('args.json', 'w', encoding='utf-8') as f:
        json.dump(args, f, ensure_ascii=False, indent=4)

        #handle argument group

if __name__ == "__main__":
    main()

# print(parser._actions[-1].option_strings)