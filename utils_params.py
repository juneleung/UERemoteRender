#coding = utf-8
import os
import paramiko
import subprocess

  
class MainNode():
    """
        main working node of unreal project editing 
    """
    def __init__(self):
        self.local = 'Z:'
        self.remote = '''\\\\192.168.31.xxxx\\20221003_KG2'''
        self.username = 'juneleung'
        self.password = 'xxxxxxxxx'

class renderNode(): 
    """
        render node of unreal project rendering 
    """
    def __init__(self):
        self.ip = '192.168.31.xxx'
        self.port = 22
        self.name = 'DMI02'
        self.passwd = 'password'
  
class UE_project(): 
    """
        the info of unreal engine and project
    
        Parameters:
            editor(str): Unreal editor position, Note: "-Cmd.exe"

            basic_folder(str): all unreal projects folder on storage server
            render_save_folder(str): render out result saving folder

            rendernode_temp_folder(str): temp folder of render node, copy project to local disk or can use the storage version , Note: need to fix
            render_setting_info_output_path(str): script project info output path, can for another render info check in pipeline... 

            proj_folder(str): this unreal project wait for render's folder
            proj_name(str): unreal project name
            maps(str): unreal project maps
            levelseq(str): unreal project level sequence
            moviepipelineconfig(str): unreal project movie pipeline config
            render_out_folder(str): render out result saving folder
    """
    def __init__(self):
        self.editor = '''"C:/Program Files/Epic Games/UE_5.1/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"'''
        
        self.basic_folder = "Z:/rendertest"
        self.render_save_folder = "Z:/rendertest/allrender"

        self.rendernode_temp_folder = "D:/UERenderFarm/"
        self.render_setting_info_output_path = "Z:/PYUE/output.txt"

        self.proj_folder = "XRKT_230719_S0010_Earth80K_v9_rendertest"
        self.proj_name = "IncredibleEarth80K.uproject"
        self.maps = "/Game/IncredibleEarth/IncredibleEarth80K"
        self.levelseq = "/Game/Sequence/earth80k_main.earth80k_main"
        self.moviepipelineconfig = "/Game/renderqueue" # "/Game/render_4k60pDCI_ACEScg-S0001"
        self.render_out_folder = "../../clips/"