import configparser, subprocess, threading, itertools, argparse, platform, logging, datetime, fnmatch, shutil, pandas as pd, shlex, html, copy, time, json, math, csv, os, re
from colorama import init, deinit, reinit, Fore, Back, Style
from gfmhelper import GoProFrameMakerHelper
from gfmmain import GoProFrameMaker

def process_video(filename):
    cfg = GoProFrameMakerHelper.getConfig()

    default = cfg['config']
    default['input'] = [filename]
    args = type('args', (object,), default)

    gfmValidated = GoProFrameMakerHelper.validateArgs(args)

    for info in gfmValidated['info']:
        print(Fore.BLUE + info)
        print(Style.RESET_ALL)

    for error in gfmValidated['errors']:
        print(Fore.RED + error)
        print(Style.RESET_ALL)
        raise Exception(f"Erro ao processar arquivo {filename}!")

    if ((gfmValidated['status'] == True) and (len(gfmValidated['errors']) == 0)):
        gfm = GoProFrameMaker(gfmValidated['args'])
        selected_args = gfm.getArguments()
        for k, v in selected_args.items():
            print(Fore.GREEN + "{}: {}".format(k, v))
        print(Style.RESET_ALL)
        # if selected_args['time_warp'] != None:
        #     print(Fore.RED + "\nTime warp value is selected, so the video is considered Time warped, if this is not supposed to be then please remove the value from config.ini key named: `time_warp`")
        # else:
        #     print(Fore.RED + "\nTime warp value is not selected, if the video is Time warped, please make sure config.ini has value for key named: `time_warp`")
        # print(Style.RESET_ALL)

        gfm.initiateProcessing()
        print(
            Fore.GREEN + f"\nProcessing {filename} finished! If there are no images in the folder please see logs to gain additional information.")
        print(Style.RESET_ALL)


    else:
        input(Fore.RED + "Processing stopped!")
        print(Style.RESET_ALL)
        raise Exception(f"Processamento do arquivo {filename} parado!")

