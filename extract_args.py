from example.example import add_args as example_add_args
import argparse

class Arg:
  def __init__(self, option_strings, name, num, default, type):
    self.option_strings = option_strings
    self.name = name
    self.num = num
    self.default = default
    self.type = type

def main():
    parser = argparse.ArgumentParser(description='Example parser')
    example_add_args(parser)
    args = {"required": [], "optional": []}
    for arg in parser._actions:
        details = {}
        details["name"] = arg.dest
        if arg.nargs is not None:
            details["nargs"] = arg.nargs
        if arg.type is not None:
            details["type"] = arg.type
        if arg.option_strings is not None:
            details["flags"] = arg.option_strings
        if arg.help is not None:
            details["help"] = arg.help
        if arg.choices is not None:
            details["choices"] = arg.choices
        
        if arg.required: 
            args["required"].append(details)
        else:
            args["optional"].append(details)

        #handle argument group

if __name__ == "__main__":
    main()

# print(parser._actions[-1].option_strings)