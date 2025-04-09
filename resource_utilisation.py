import re

class ResourceUtilisation:
    def __init__(self, rep_filename):

        #rep_filename = f"{root_dir}/_x/reports/{bin_name}/hls_reports/{kernel_name}_csynth.rpt"
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
                  'lut': int(avail_match_obj.group(4)),
                  'uram': int(avail_match_obj.group(5))
                  }

        avail_slr_match_obj = re.search(f"Available SLR{sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+){sep}(\d+)", res_table, flags=re.DOTALL)
        self.avail_slr = {'bram': int(avail_slr_match_obj.group(1)),
                  'dsp': int(avail_slr_match_obj.group(2)),
                  'ff': int(avail_slr_match_obj.group(3)),
                  'lut': int(avail_slr_match_obj.group(4)),
                  'uram': int(avail_slr_match_obj.group(5))
                  }
        self.util = {'bram': self.totals['bram'] / self.avail['bram'] * 100,
                 'dsp': self.totals['dsp'] / self.avail['dsp'] * 100,
                 'ff': self.totals['ff'] / self.avail['ff'] * 100,
                 'lut': self.totals['lut'] / self.avail['lut'] * 100,
                 'uram': self.totals['uram'] / self.avail['uram'] * 100
                  }

        self.util_slr = {'bram': self.totals['bram'] / self.avail_slr['bram'] * 100,
                 'dsp': self.totals['dsp'] / self.avail_slr['dsp'] * 100,
                 'ff': self.totals['ff'] / self.avail_slr['ff'] * 100,
                 'lut': self.totals['lut'] / self.avail_slr['lut'] * 100,
                 'uram': self.totals['uram'] / self.avail_slr['uram'] * 100
                  }

    def get_resource_utilisation(self, csv=False, header=False):
        if csv:
            if header:
                for resource, value in self.util.items():
                    print(f"{resource},", end="") # dont add new line
                print("") # new line
            for resource, value in self.util.items():
               print(f"{value},", end="") 
            return
        return self.util

    def get_resource_utilisation_slr(self, csv=False, header=False):
        if csv:
            if header:
                for resource, value in self.util.items():
                    print(f"{resource},", end="") # dont add new line
                print("") # new line
            for resource, value in self.util.items():
               print(f"{value},", end="") 
            return
        return self.util_slr

import json
from types import SimpleNamespace

class ResourceUtilisationLinked:
    def __init__(self, rep_filename):
        self.rep_filename=rep_filename 

        with open(rep_filename) as f:
            self.data = json.load(f, object_hook=lambda data: SimpleNamespace(**data))
            #print(d.user_budget.actual_resources.)

        self.avail = { 
                        "LUT": int(self.data.user_budget.supply_resources.LUT),
                        "LUTAsMem": int(self.data.user_budget.supply_resources.LUTAsMem),
                        "REG": int(self.data.user_budget.supply_resources.REG),
                        "BRAM": int(self.data.user_budget.supply_resources.BRAM),
                        "URAM": int(self.data.user_budget.supply_resources.URAM),
                        "DSP": int(self.data.user_budget.supply_resources.DSP)
                     }

        self.total = { 
                        "LUT": int(self.data.user_budget.actual_resources.LUT),
                        "LUTAsMem": int(self.data.user_budget.actual_resources.LUTAsMem),
                        "REG": int(self.data.user_budget.actual_resources.REG),
                        "BRAM": int(self.data.user_budget.actual_resources.BRAM),
                        "URAM": int(self.data.user_budget.actual_resources.URAM),
                        "DSP": int(self.data.user_budget.actual_resources.DSP)
                     }

        self.util = {
                        "LUT": self.total["LUT"] / self.avail["LUT"] * 100,
                        "LUTAsMem": self.total["LUTAsMem"] / self.avail["LUTAsMem"] * 100,
                        "REG": self.total["REG"] / self.avail["REG"] * 100,
                        "BRAM": self.total["BRAM"] / self.avail["BRAM"] * 100,
                        "URAM": self.total["URAM"] / self.avail["URAM"] * 100,
                        "DSP":self.total["DSP"] / self.avail["DSP"] * 100
                    }
   
    def get_resource_utilisation(self, csv=False):
        cs=f"{self.rep_filename},"
        if csv:
            for resource, value in self.util.items():
               cs=f"{cs}{value},"
            cs=cs.strip(",")
            return cs
        return self.util

    def get_header(self):
        headers="bitstream,"
        for resource, value in self.avail.items():
            headers=f"{headers}{resource},"
        return headers.strip(",")

class ResourceUtilisationLinkedSingleKernel:
    def __init__(self, rep_filename):
        self.rep_filename=rep_filename 

        with open(rep_filename) as f:
            self.data = json.load(f, object_hook=lambda data: SimpleNamespace(**data))
            #print(d.kernels[0].compute_units[0].actual_resources.)

        self.avail = { 
                        "LUT": int(self.data.user_budget.supply_resources.LUT),
                        "LUTAsMem": int(self.data.user_budget.supply_resources.LUTAsMem),
                        "REG": int(self.data.user_budget.supply_resources.REG),
                        "BRAM": int(self.data.user_budget.supply_resources.BRAM),
                        "URAM": int(self.data.user_budget.supply_resources.URAM),
                        "DSP": int(self.data.user_budget.supply_resources.DSP)
                     }

        self.total = { 
                        "LUT": int(self.data.kernels[0].compute_units[0].actual_resources.LUT),
                        "LUTAsMem": int(self.data.kernels[0].compute_units[0].actual_resources.LUTAsMem),
                        "REG": int(self.data.kernels[0].compute_units[0].actual_resources.REG),
                        "BRAM": int(self.data.kernels[0].compute_units[0].actual_resources.BRAM),
                        "URAM": int(self.data.kernels[0].compute_units[0].actual_resources.URAM),
                        "DSP": int(self.data.kernels[0].compute_units[0].actual_resources.DSP)
                     }

        self.util = {
                        "LUT": self.total["LUT"] / self.avail["LUT"] * 100,
                        "LUTAsMem": self.total["LUTAsMem"] / self.avail["LUTAsMem"] * 100,
                        "REG": self.total["REG"] / self.avail["REG"] * 100,
                        "BRAM": self.total["BRAM"] / self.avail["BRAM"] * 100,
                        "URAM": self.total["URAM"] / self.avail["URAM"] * 100,
                        "DSP":self.total["DSP"] / self.avail["DSP"] * 100
                    }
   
    def get_resource_utilisation(self, csv=False):
        cs=f"{self.rep_filename},"
        if csv:
            for resource, value in self.util.items():
               cs=f"{cs}{value},"
            cs=cs.strip(",")
            return cs
        return self.util

    def get_header(self):
        headers="bitstream,"
        for resource, value in self.avail.items():
            headers=f"{headers}{resource},"
        return headers.strip(",")
                
