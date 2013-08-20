#
# Python Script to perform for running the full process using load leveler
#
# Murray Cadzow 
# July 2013
# University Of Otago
#
# James Boocock
# July 2013
# University Of Otago
# 

import os
import sys
import re

#For matching the file names
import fnmatch

from optparse import OptionParser

## Subprocess import clause required for running commands on the shell##
import subprocess
import logging

#Import standard run 

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

SUBPROCESS_FAILED_EXIT=10
load_leveler_template="""
        #@ shell = /bin/bash
        #@ group = {0}
        #@ class = {1}
        #@ output = $(jobid).out
        #@ error = $(jobid).err 
"""
load_leveler_step="""
        #@ step_name = {2}
        #@ wall_clock_limit = {3}
        #@ resources = ConsumableMemory({4}) ConsumableVirtualMemory({4})
"""

load_leveler_account_no="""
        #@ account_no = {0}
"""

# serial_task_with_threads
load_leveler_serial ="""
        #@ job_type = serial
        #@ parallel_threads = {0}
"""
# mpi_task
load_leveler_mpi = """
        #@ job_type = parallel
        #@ total_tasks_threads = {0}
        #@ blocking = {1}
"""
load_leveler_dependency = """
        #@ dependency = {0}   
""" 
# Queue jobs on load leveler
load_leveler_queue ="""
            #@ queue
    """



class LoadLevelerRun(object):
    
    """ Load leveler class takes the pipeline and runs the PHD on the nesi pan 
        cluster.
    """
    def __init__(self,options,config):
        logger.debug('Running the script on nesi')
        self.group =config['nesi']['group'] 
        self.class =config['nesi']['class']
        self.account_no=config['nesi']['account_no']
        self.load_leveler_script = open('level_the_load.ll','wb')
        self.load_leveler_script.write(load__leveler_template.format(self.group,self.class))
        if(self.account_no is not None):
             self.load_leveler_script.write(load_leveler_account_no.format(self.account_no))
        self.create_load_leveler_script(options,config)
    def create_load_leveler_script(self,options,config):
        if(options.phased_vcf): 
           (script,dependecies,haps) = self.ancestral_annotation_vcf(options,config,dependencies)
           (script,dependencies,haps) = self.run_multi_coreihh(options,config,haps,dependencies)
        else:
            (script,dependencies,ped,map) = self.run_vcf_tools(options,config,dependencies)
            (script,dependencies,ped,map) = self.run_plink(options,config,ped,map,dependencies)
            (script,dependencies,haps) = self.run_shape_it(options,config,ped,map,dependencies) 
        if(options.imputation):
            (script,dependencies,haps)= self.run_impute2(options,config,haps,dependencies)
        (script,dependencies,haps) = self.indel_filter(options,config,haps,dependencies)
        #tajimas = run_tajimas_d(options,config,haps)
        (script,dependencies,haps) = self.run_aa_annotate_haps(options,config,haps,dependencies)
        (script,dependencies,ihh) = self.run_multi_coreihh(options,config,haps,dependencies)
        logger.info("Pipeline completed successfully")
        logger.info(haps)
        logger.info(ihh)
        logger.info("Goodbye :)")
    
    def ancestral_annotation_vcf(self,options,config):
        
    def run_vcf_to_plink(self,options,config):
        (cmd,prefix) = CommandTemplate.run_vcf_to_plink(self,options,config)
          
        
          
    def run_plink(self,options, config):
        return 1
