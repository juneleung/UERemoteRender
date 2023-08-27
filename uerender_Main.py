#coding = utf-8
import os
import paramiko
import subprocess
from  utils_params import *
from  utils_func import *

# 对方电脑先在 <应用>-<可选应用>-<OPENSSH服务端>
# cmd-admin mode: net start sshd

def main():
    # ssh render machine
    rend_node = renderNode()
    ssh = paramiko.SSHClient()
    ssh_login(rend_node.ip, rend_node.port, rend_node.name, rend_node.passwd)

    UE_project = UE_project()
    # read render info
    UE_read_info = UE_project.editor
    UE_project_path = os.path.join(UE_project.basic_folder,UE_project.proj_folder,UE_project.proj_name)
    UE_read_info += " " + UE_project_path 
    UE_read_info += ' -run=pythonscript -script='
    UE_read_info += "\"Z:\\PYUE\\getRenderQueueInfo.py " \
                    + UE_project.render_setting_info_output_path +" " \
                    + UE_project.moviepipelineconfig +" " \
                    + UE_project.maps+"."+UE_project.maps.split("/")[-1] + "\""
    print(f"getting render info :{UE_read_info}")
    output = run_cmd(UE_read_info)
    print(output)


    # render node: mount disk 
    MainNode = MainNode()
    mount_cmd = 'net use '+MainNode.local+' '+MainNode.remote+' '+MainNode.password+' /USER:'+MainNode.username
    # mount_cmd = 'net use '+local+' '+remote
    strout, strerr = ssh_exe_cmd(mount_cmd)
    print(f"mounting disk :{mount_cmd}")
    if(strerr):
        print("failed to connect to render node, exit")
        exit_action(ssh)
        return 


    # render node: copy proj to temp folder 
    source_path = os.path.join(UE_project.basic_folder,UE_project.proj_folder)
    dest_path = os.path.join(UE_project.rendernode_temp_folder,UE_project.proj_folder) 
    if(os.path.exists(source_path)):    
        mkdir_cmd = "if not exist \""+UE_project.rendernode_temp_folder.replace("/","\\")+"\" mkdir \""+UE_project.rendernode_temp_folder.replace("/","\\")+"\""
        print(f"make dir of temp location path: {mkdir_cmd}")
        strout, strerr = ssh_exe_cmd(mkdir_cmd)
        if(strerr or "不正确" in strout):
            print("failed to make temp folder, exit")
            print(strerr)
            exit_action(ssh)
            return 
        
        copy_proj_cmd =" Xcopy \"" + source_path + "\" \"" + dest_path +"\" /E/H/C/I/Y"
        print(f"copying file to rendernode local path: {copy_proj_cmd}")
        strout, strerr = ssh_exe_cmd(copy_proj_cmd)
        if(strerr or "不正确" in strout):
            print("failed to copy project to temp folder, exit")
            print(strerr)
            exit_action(ssh)
            return 
    else:
        print("failed to copy project to temp folder, exit")
        exit_action(ssh)
        return 


    # render project
    UE_proj = os.path.join(UE_project.rendernode_temp_folder,UE_project.proj_name) #r"C:\Users\Juneleung\Desktop\XRKT_230719_S0010_Earth80K_v9\IncredibleEarth80K.uproject"
    print(f"rendering {UE_proj}")
    rendercmd = Unreal_rendersetting(UE_project.editor, UE_proj, UE_project.maps, UE_project.levelseq, UE_project.moviepipelineconfig)
    print(rendercmd)
    # os.system(rendercmd)
    strout, strerr = ssh_exe_cmd(rendercmd)
    if(strerr or "不正确" in strout):
        print("failed to render project, exit")
        exit_action(ssh)
        return 
    

    # send back ue render result
    render_out_local_path = os.path.join(UE_project.rendernode_temp_folder,UE_project.render_out_folder) 
    move_render_out_cmd = "mv " + render_out_local_path + " " + UE_project.render_save_folder
    print(f"{move_render_out_cmd}")
    strout, strerr = ssh_exe_cmd(copy_proj_cmd)
    if(strerr or "不正确" in strout):
        print("failed to move render out result back, exit")
        exit_action(ssh)
        return 


    # file send back and check
    file_list = os.listdir(UE_project.render_save_folder)
    exr_files = [file for file in file_list if file.endswith(".exr")]
    common_part = os.path.commonprefix(exr_files)
    print("finished rendering :", common_part)
    
    
    # end
    exit_action(ssh)
    

main()