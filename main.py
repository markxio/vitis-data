import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", type=str, help="Root directory where the kernel was built.")
    parser.add_argument("kernel_name", type=str, help="Name of the kernel whose report we'll extract info from.")
  
    args = parser.parse_args()
    root_dir = args.root_dir
    kernel_name = args.kernel_name

    rep_filename = f"{root_dir}/_x/reports/{kernel_name}/hls_reports/{kernel_name}_csynth.rpt"
    f = open(rep_filename) 

    txt = f.read()

    #print(txt)

    match_obj = re.search("== Utilization Estimates.+\+ Detail", txt, flags=re.DOTALL)
    res_table = match_obj.group(0)

    #total_match_obj = re.search("|Total.+(\d+).+(\d+).+(\d+).+(\d+)", res_table, flags=re.DOTALL)
    sep = "\s*\|\s*"
    total_match_obj = re.search(f"Total{sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+)", res_table, flags=re.DOTALL)
    totals = {'bram': int(total_match_obj.group(1)),
              'dsp': int(total_match_obj.group(2)),
              'ff': int(total_match_obj.group(3)),
              'lut': int(total_match_obj.group(4)),
              'uram': int(total_match_obj.group(5))
              }

    avail_match_obj = re.search(f"Available{sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+)", res_table, flags=re.DOTALL)
    avail = {'bram': int(avail_match_obj.group(1)),
              'dsp': int(avail_match_obj.group(2)),
              'ff': int(avail_match_obj.group(3)),
              'lut': int(avail_match_obj.group(4))#,
              #'uram': int(avail_match_obj.group(5))
              }


    util = {'bram': totals['bram'] / avail['bram'] * 100,
             'dsp': totals['dsp'] / avail['dsp'] * 100,
             'ff': totals['ff'] / avail['ff'] * 100,
             'lut': totals['lut'] / avail['lut'] * 100#,
             #'uram': avail['uram'] / totals['uram']
              }

    print("LUT\tFF\tBRAM\tDSP")
    print(f"{util['lut']:.2f}\t{util['dsp']:.2f}\t{util['ff']:.2f}\t{util['lut']:.2f}")
