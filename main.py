import argparse
from resource_utilisation import ResourceUtilisation

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", type=str, help="Root directory where the kernel was built.")
    parser.add_argument("kernel_name", type=str, help="Name of the kernel whose report we'll extract info from.")
  
    args = parser.parse_args()
    root_dir = args.root_dir
    kernel_name = args.kernel_name

    obj_res_util = ResourceUtilisation(root_dir, kernel_name)
    print(obj_res_util.get_resource_utilisation())
