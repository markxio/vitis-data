import re

class ResourceUtilisation:
    def __init__(self, root_dir, bin_name, kernel_name):
        self.root_dir = root_dir
        self.kernel_name = kernel_name

        rep_filename = f"{root_dir}/_x/reports/{bin_name}/hls_reports/{kernel_name}_csynth.rpt"
        f = open(rep_filename) 

        txt = f.read()

        match_obj = re.search("== Utilization Estimates.+\+ Detail", txt, flags=re.DOTALL)
        res_table = match_obj.group(0)

        sep = "\s*\|\s*"
        total_match_obj = re.search(f"Total{sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+)", res_table, flags=re.DOTALL)
        self.totals = {'bram': int(total_match_obj.group(1)),
                  'dsp': int(total_match_obj.group(2)),
                  'ff': int(total_match_obj.group(3)),
                  'lut': int(total_match_obj.group(4)),
                  'uram': int(total_match_obj.group(5))
                  }

        avail_match_obj = re.search(f"Available{sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+)", res_table, flags=re.DOTALL)
        self.avail = {'bram': int(avail_match_obj.group(1)),
                  'dsp': int(avail_match_obj.group(2)),
                  'ff': int(avail_match_obj.group(3)),
                  'lut': int(avail_match_obj.group(4))#,
                  #'uram': int(avail_match_obj.group(5))
                  }


        self.util = {'bram': self.totals['bram'] / self.avail['bram'] * 100,
                 'dsp': self.totals['dsp'] / self.avail['dsp'] * 100,
                 'ff': self.totals['ff'] / self.avail['ff'] * 100,
                 'lut': self.totals['lut'] / self.avail['lut'] * 100#,
                 #'uram': avail['uram'] / totals['uram']
                  }



    def get_resource_utilisation(self):
        return self.util
