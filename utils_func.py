#coding = utf-8
import os
import paramiko
import subprocess
from  utils_params import *

def ssh_login(ip, port, username, passwd):
    """
    Establishes an SSH connection to a remote server using the provided IP address, port number,
    username, and password.

    Parameters:
        ip (str): The IP address of the remote server.
        port (int): The port number to connect to on the remote server.
        username (str): The username for authentication.
        passwd (str): The password for authentication.

    Returns:
        None
    """
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd)
    return
    
def ssh_exe_cmd(cmd):
    """
    Executes a command on a remote server using SSH.

    Parameters:
        cmd (str): The command to execute on the remote server.

    Returns:
        tuple: A tuple containing two strings. The first string is the output of the command (stdout), and the second string is the error message (stderr).
    """
    print("-"*50)
    global ssh
    stdin, stdout, stderr = ssh.exec_command(cmd)
    strout = stdout.read().decode("gbk")
    strerr = stderr.read().decode("gbk")
    print(strout,strerr)
    return strout,strerr
    
def Unreal_rendersetting(UE_editor, UE_proj, UE_maps, UE_levelseq, UE_moviepipelineconfig):
    """
    Generates a command for rendering Unreal Engine settings.

    Args:
        UE_editor (str): The path to the Unreal Engine editor executable.
        UE_proj (str): The path to the Unreal Engine project.
        UE_maps (str): The maps to be rendered in the game.
        UE_levelseq (str): The level sequence to be captured.
        UE_moviepipelineconfig (str): The movie pipeline configuration.

    Returns:
        str: The command for rendering Unreal Engine settings.
    """
    
    cmd =  UE_editor + " "
    cmd += UE_proj + " "
    cmd += UE_maps + " -game"
    cmd += " -MovieSceneCaptureType=/Script/MovieSceneCapture.AutomatedLevelSequenceCapture "
    # cmd += " -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor -ExecutorPythonClass=/Engine/PythonTypes.MoviePipelineExampleRuntimeExecutor"

    cmd += " -LevelSequence="+UE_levelseq
    cmd += " -MoviePipelineConfig="+UE_moviepipelineconfig
    # cmd += " -MovieFolder=" +renderOUTFolder
    cmd += " -NoLoadingScreen -WINDOWED "
    cmd += " -Log -StdOut -allowStdOutLogVerbosity "
    cmd += " -Unattended"
    # cmd += " -MovieFrameRate="+str(fps)
    # cmd += " -resx="+str(resX)
    # cmd += " -resY="+str(resY)
    # cmd += " -VSync"

    return cmd

class CommandException(Exception):
    pass

def run_cmd(command):
    exitcode, output = subprocess.getstatusoutput(command)
    if exitcode != 0:
        raise CommandException(output)

    return output

def exit_action(ssh):
    """
    Function to perform an exit action.

    Parameters:
        ssh (object): The SSH object used for the connection.

    Returns:
        None
    """
    print("Unmounting path")
    exDisk = "net use Z: /del "
    strout, strerr = ssh_exe_cmd(exDisk)
    if(strerr or "不正确" in strout):
        print("failed to exit action")
    ssh.close()
    