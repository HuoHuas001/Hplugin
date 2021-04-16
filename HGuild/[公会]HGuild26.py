#! /usr/bin/env python
# -*- coding:utf-8 -*-
##################################################################################################
#导入模块
Plugin_Path = "plugins/py/HGuild_Runtime"
PluginVersion = 2.6
NeedPyrVersion = 134
import sys
import os
sys.path.append(Plugin_Path)
import json
import yaml
import time
##################################################################################################
#输出彩色文字
def Out_Way():
    Plugins_Path= Plugin_Path+'/GuildConfig'
    try:
        with open(Plugins_Path+'/Configuration.yml','r',encoding='utf-8') as f:
            Config = yaml.load(f.read(), Loader=yaml.FullLoader)
            return Config['Output']
    except:
        pass
def WriteWarn(title,cont):
    if Out_Way() == 'colorful':
        print(''+'\033[33m'+title+'\033[0m '+"\033[5;33m"+cont+"\033[0m")
    else:
        print(''+title+' '+cont)

def WriteInfo(title,cont):
    if Out_Way() == 'colorful':
        print(''+'\033[36m'+title+'\033[0m '+"\033[5;32m"+cont+"\033[0m")
    else:
        print(''+title+' '+cont)
def WriteError(title,cont):
    if Out_Way() == 'colorful':
        print(''+'\033[31m'+title+'\033[0m '+"\033[5;31m"+cont+"\033[0m")
    else:
        print(''+title+' '+cont)
try:
    import mc
except:
    WriteError('[HGuild]','Do not attempt to run this program on a terminal')
    exit()
#检测运行库
if not os.path.exists(Plugin_Path):
    WriteError('[HGuild]','Runtime does not exist')
    time.sleep(3)
    exit()
##################################################################################################
from datetime import datetime
from multiprocessing import Process
import requests
import random
import shutil
##################################################################################################
#下载文件
def Downloading(url,name):
    WriteInfo('[INFO]','HGuildM Downloading '+name)
    Down = requests.get(url,stream=True)
    try:
        with open(name,'wb') as df:
            for chunk in Down.iter_content(chunk_size=1024):
                if chunk:
                    df.write(chunk)
        return 'Success'
    except:
        return 'Failed'
def download(url,name):
    mc.newThread(Downloading(url,name))
##################################################################################################
#读取语言文件
def language_read():
    global language_file
    Plugins_Path= Plugin_Path+'/GuildConfig'
    try:
        with open(Plugins_Path+'/Configuration.yml','r',encoding='utf-8') as f:
            Config = yaml.load(f.read(), Loader=yaml.FullLoader)
    except:
        pass
    if os.path.exists(Plugin_Path+'/GuildConfig/language.yml'):
        with open(Plugin_Path+'/GuildConfig/language.yml','r',encoding='utf-8') as f:
            pas = f.read().replace('#version#',str(PluginVersion))
            language_file = yaml.load(pas, Loader=yaml.FullLoader)
            if os.path.exists(Plugin_Path+'/GuildConfig/Configuration.yml'):
                if language_file == None:
                    language_file = {}
                if 'language_type' not in language_file:
                    download('http://mchuohua.gitee.io/HGuild/Language/'+Config['Language']+'.yml',Plugin_Path+'/GuildConfig/language.yml')
                    WriteWarn('[HGuild]','Download language completed, please restart the server')
                    time.sleep(5)
                    exit()
                if Config['Language'] != language_file['language_type']:
                    download('http://mchuohua.gitee.io/HGuild/Language/'+Config['Language']+'.yml',Plugin_Path+'/GuildConfig/language.yml')
                    WriteWarn('[HGuild]','Download language completed, please restart the server')
                    time.sleep(5)
                    exit()
                url = 'http://mchuohua.gitee.io/HGuild/'
                if language_file['language_version'] < json.loads(requests.get(url,timeout=5).text)['language_version']:
                    download('http://mchuohua.gitee.io/HGuild/Language/'+Config['Language']+'.yml',Plugin_Path+'/GuildConfig/language.yml')
                    WriteWarn('[HGuild]','Update language completed, please restart the server')
                    time.sleep(5)
                    exit()

    else:
        try:
            fd = os.path.exists(Plugin_Path+'/GuildConfig')
            if not fd:
                os.makedirs(Plugin_Path+'/GuildConfig')
        except:
            pass
        download('http://mchuohua.gitee.io/HGuild/Language/'+'en_us'+'.yml',Plugin_Path+'/GuildConfig/language.yml')
        WriteWarn('[HGuild]','Download language completed, please restart the server')
        time.sleep(5)
        exit()
#调用函数
language_read()
##################################################################################################
#创建文件函数
def createFile(Filename,content):
    lsa = Plugin_Path+'/GuildConfig/'+Filename
    try:
        if not os.path.exists(lsa):
            with open(Plugin_Path+'/GuildConfig/'+Filename,'w',encoding='utf-8') as f:
                f.write(content)
            WriteInfo('[HGuild]',language_file["Create"]+Filename+language_file["Success"])
    except:
        WriteError('[HGuild]',Filename+language_file["Create_Fail"])

#文件夹函数
def createFolder(Folderpath):
    try:
        fd = os.path.exists(Folderpath)
        if not fd:
            os.makedirs(Folderpath)
            WriteInfo('[HGuild]',language_file["Create"]+Folderpath+language_file["Success"])
    except:
        WriteError('[HGuild]',Folderpath+language_file["Create_Fail"])
##################################################################################################
#读取文件
def Read_Files():
    global Config,PlayerConfig,GuildConfig,Checked
    try:
        Plugins_Path= Plugin_Path+'/GuildConfig'
        try:
            with open(Plugins_Path+'/Configuration.yml','r',encoding='utf-8') as f:
                Config = yaml.load(f.read(), Loader=yaml.FullLoader)
        except:
            WriteError('[HGuild]',language_file["Configuration.json_Read_failed"])
            Config = {   
                "Language":"zh_cn",
                'Cmd':'guild',
                "Scoreboard":"money",
                "Cost":20,
                "MaxGuild":1,
                "Check":["scoreboard players add %player% money 1"],
                "Output":"Ordinary",
                "YamlVersion":4
            }
        #尝试读取PlayerConfig
        try:
            with open(Plugins_Path+'/PlayerConfig.yml','r',encoding='utf-8') as f:
                PlayerConfig = yaml.load(f.read(), Loader=yaml.FullLoader)
                if PlayerConfig == None:
                    PlayerConfig = {}
        except:
            PlayerConfig = {}
            WriteError('[HGuild]',language_file["PlayerConfig.json_Read_failed"])
        #尝试读取GuildFile
        try:
            with open(Plugins_Path+'/GuildFile.yml','r',encoding='utf-8') as f:
                GuildConfig = yaml.load(f.read(), Loader=yaml.FullLoader)
                if GuildConfig == None:
                    GuildConfig = {}
        except:
            GuildConfig = {}
            WriteError('[HGuild]',language_file["GuildFile.json_Read_failed"])
        #尝试读取Checked
        try:
            with open(Plugins_Path+'/Checked.yml','r',encoding='utf-8') as f:
                Checked = yaml.load(f.read(), Loader=yaml.FullLoader)
                if Checked == None:
                    Checked = {}
        except:
            Checked = {}
            WriteError('[HGuild]',language_file["Checked.json_Read_failed"])
        
        return 'True'
    except:
        return 'False'
##################################################################################################
#检测文件夹以及文件
def Self_test():
    try:
        #检查文件夹
        createFolder(Plugin_Path+'/GuildConfig')
        #检查Config
        createFile('Configuration.yml',yaml.dump(
            {   
                "Language":"zh_cn",
                'Cmd':'guild',
                "Scoreboard":"money",
                "Cost":20,
                "MaxGuild":1,
                "Check":["scoreboard players add %player% money 1"],
                "Output":"Ordinary",
                "YamlVersion":4
            }
        ))
        #检查Player
        createFile('PlayerConfig.yml','')
        #检查Guild
        createFile('GuildFile.yml','')
        #检查签到
        createFile('Checked.yml','')
        return 'True'
    except:
        return 'False'

#EULA协议
def Test_Eula():
    if not os.path.exists(Plugin_Path+'/GuildConfig/eula'):
        download('http://mchuohua.gitee.io/HGuild/eula','plugins/py/HGuild_Runtime/GuildConfig/eula')
        print('[HGuild] '+language_file['eula'])
        exit()
    else:
        with open(Plugin_Path+'/GuildConfig/eula','r',encoding='utf-8') as f:
            elua = f.readlines()
            if max(elua) != 'eula=true':
                WriteError('[HGuild]',language_file['eula'])
                time.sleep(5)
                exit()
##################################################################################################
#插件升级
def plugin_update():
    if Config['YamlVersion'] != 4:
        with open(Plugin_Path+'/GuildConfig/Configuration.yml','w',encoding='utf-8') as f:
            f.write(yaml.dump(
            {   
                "Language":"zh_cn",
                'Cmd':'guild',
                "Scoreboard":"money",
                "Cost":20,
                "MaxGuild":1,
                "Check":["scoreboard players add %player% money 1"],
                "Output":"Ordinary",
                "YamlVersion":4
            }
            ))
        WriteWarn('[HGuild]',language_file["Update_Configuration.json"])
    url = 'http://mchuohua.gitee.io/HGuild/'
    try:
        req = requests.get(url,timeout=5)
        req = json.loads(req.text)
        if float(req['HGuildMVersion']) > PluginVersion:
            if req['Update_type'] == 'Auto':
                WriteWarn('[HGuild]',language_file["Updating_Plugin"])
                Download_Ways = Downloading('http://mchuohua.gitee.io/HGuild/guild.pyd','./plugins/py/guild.pyd')
                if Download_Ways == 'Success':
                    WriteWarn('[INFO]',language_file['Updated'])
                    exit()
                else:
                    WriteError('[INFO]',language_file['Update_Error'])
                    exit()
            else:
                WriteError('[HGuild]','This update needs to be manually updated')
        elif float(req['HGuildMVersion']) < PluginVersion:
            WriteWarn('[HGuild]',language_file["Beta"])
        else:
            WriteInfo('[HGuild]',language_file["Official_Edition"])
    except requests.exceptions.RequestException as e:
        WriteError('[HGuild]',language_file['Update_Timeout'])

    
    


##################################################################################################
#写入文件
def Write_File(FileType):
    global GuildConfigDict
    if FileType == 'Guild':
        with open(Plugin_Path+'/GuildConfig/GuildFile.yml','w') as f:
            GuildConfigDict = GuildConfig
            Guilds = yaml.dump(GuildConfigDict)
            f.write(Guilds)
    elif FileType == 'Player':
        with open(Plugin_Path+'/GuildConfig/PlayerConfig.yml','w') as f:
            Players = yaml.dump(PlayerConfig)
            f.write(Players)
    elif FileType == 'Check':
        with open(Plugin_Path+'/GuildConfig/Checked.yml','w') as f:
            Check = yaml.dump(Checked)
            f.write(Check)
    else:
        return False
    Read_Files()
##################################################################################################
#获取在线玩家
def getOnLinePlayers():
    PlayerList = mc.getPlayerList()
    NameList = []
    for i in PlayerList:
        NameList.append(mc.getPlayerInfo(i)['playername'])
    return NameList

##################################################################################################
#表单设计
mainmenu = [
    {"image":{"type":"path","data":"textures/ui/icon_bookshelf"},"text":language_file['Gui']['Main']['Create_Guild']},
    {"image":{"type":"path","data":"textures/ui/op"},"text":language_file['Gui']['Main']['Guild_Manage']},
    {"image":{"type":"path","data":"textures/ui/icon_fall"},"text":language_file['Gui']['Main']['Check']},
    {"image":{"type":"path","data":"textures/ui/icon_deals"},"text":language_file['Gui']['Main']['Teleport']},
    {"image":{"type":"path","data":"textures/ui/World"},"text":language_file['Gui']['Main']["World_Guild"]}
    ]
##################################################################################################
#获取所有公会
def Get_All_Guild():
    GuildList =[]
    for i in GuildConfig:
        GuildList.append(i)
    return GuildList
##################################################################################################
#发送错误提示
def Send_Error(player,title,content):
    player.sendModalForm(language_file["Gui"]["Error_Gui"]["Title_Error"]+title, '§e'+content, language_file["Gui"]["Error_Gui"]["OK"],language_file["Gui"]["Error_Gui"]["Cancel"])
##################################################################################################
#公会签到
def Sign_In():
    while True:
        timea = datetime.now().strftime("%H:%M")
        if timea == '00:00':
            Checked = {}
            Write_File('Check')
##################################################################################################
n = 0
#玩家加入
def Player_Join(e):
    if n == 0:
        mc.runcmd('scoreboard objectives add '+Config['Scoreboard']+' dummy')
    playername = mc.getPlayerInfo(e)['playername']
    if playername not in PlayerConfig:
        PlayerConfig[playername] = {
            'Created_Guild':0,
            'Permission':'Null',
            'Join':'Null'
        }
        Write_File('Player')


##################################################################################################
#生成验证码
def Verification_Code():
    strs = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        strs += ch
    return strs
##################################################################################################
#输入指令
def input_cmd(e):
    global main
    if e['cmd'] == '/'+Config['Cmd']:
        main = e['player'].sendCustomForm('{"content": "'+language_file['Gui']['Send_Main']+'","buttons":'+json.dumps(mainmenu)+', "type":"form","title":"§b§lHGuild §cMenu"}')
        return False
    elif e['cmd'] == '/'+Config['Cmd']:
        main = e['player'].sendCustomForm('{"content": "'+language_file['Gui']['Send_Main']+'","buttons":'+json.dumps(mainmenu)+', "type":"form","title":"§b§lHGuild §cMenu"}')
        return False




##################################################################################################
#表单前设置id
main = 114514
create_Guild_id = 114515
Manage_Guild_Gui =114516
Change_Name_Gui = 114517
Change_Permission_Gui = 114518
Kick_Player_Gui_Id = 114519
InvitationPlayer_Gui = 114520
Change_Name_Gui = 114521
World_Guild_Selected_Id = 114522
Dissolution_Guild_Gui_Id = 114523
Exit_Guild_Gui_Id = 114524
Transfer_Guild_Gui_Id = 114525
Change_Position_Gui_Id = 114526
World_Guild_accept = 114527
Invitation_Send_Gui_Id = 114528
World_Guild_Gui = 114529
##################################################################################################
#创建公会函数
def create_Guild(player,guildname,teleport,playername,Pvp):
    global GuildConfig
    if guildname not in GuildConfig:
        Create_Guild_Data = {"Teleport":{"Dim":teleport[3],"Posistion":{"x":teleport[0],"y":teleport[1],"z":teleport[2]}},"Pvp":Pvp,"Member":{playername:"Admin"}}

        PlayerData = {
            "Created_Guild": 1,
            "Join": guildname,
            "Permission": "Admin"
        }
        
        GuildConfig[guildname] = Create_Guild_Data
        with open(Plugin_Path+'/GuildConfig/GuildFile.yml','w') as f:
            Guilds = yaml.dump(GuildConfig)
            f.write(Guilds)
        PlayerConfig[playername] = PlayerData
        Write_File('Player')
        mc.modifyPlayerScore(player,Config['Scoreboard'],int(Config['Cost']),2)
        mc.tellraw(player,language_file['Gui']["Created_Guild"]["Create_Success"][0]+guildname+language_file['Gui']["Created_Guild"]["Create_Success"][1])
    else:
        Send_Error(player,language_file['Gui']["Created_Guild"]["Created_Error"][0],language_file['Gui']["Created_Guild"]["Created_Error"][1])
##################################################################################################
#公会成员函数
def Guild_Members(player,guild):
    playername = mc.getPlayerInfo(player)['playername']
    Members = ''
    for i in GuildConfig[guild]['Member']:
        if GuildConfig[guild]['Member'][i] == 'Admin':
            Members += language_file['Gui']["Guild_Member_Text"]["Admin"]+i
        elif GuildConfig[guild]['Member'][i] == 'Operator':
            Members += language_file['Gui']["Guild_Member_Text"]["Operator"]+i
        else:
            Members += language_file['Gui']["Guild_Member_Text"]["Member"]+i
    player.sendSimpleForm(player,language_file['Gui']["Guild_Member_Text"]['Gui_Title'][0]+guild+language_file['Gui']["Guild_Member_Text"]['Gui_Title'][1],Members,'[]')
##################################################################################################
#表单操作
def form_action(e):
    global create_Guild_id,Manage_Guild_Gui,Change_Name_Gui,Change_Permission_Gui,InvitationPlayer_Gui,Transfer_Verification_Code,World_Guild_accept
    global Befor_Name,InvitationPlayer,Invitation_Send_Gui_Id,Change_Permission_Guild_Member,Kick_Player_Member,Dissolution_Verification_Code
    global Change_Position_Gui_Id,Kick_Player_Gui_Id,Exit_Guild_Gui_Id,Dissolution_Guild_Gui_Id,Transfer_Guild_Gui_Id,World_Guild_Selected_Id
    global Transfer_Verification_Code,Exit_Verification_Code,Invitation_Send_Gui_Id,Invitation_Guild_Name,Invitation_Player_Name,Selected_Guild
    global World_Guild_Gui
    e['playername'] = mc.getPlayerInfo(e['player'])['playername']
    if e['formid'] == main:
        try:
            e['selected'] = int(e['selected'])
        except:
            pass
        #创建Guild
        if e['selected'] == 0:
            scores = mc.getPlayerScore(e['player'],str(Config['Scoreboard']))
            if scores >= int(Config['Cost']):
                if PlayerConfig[e['playername']]['Created_Guild'] == 0:
                    createGuild = {
                        "content":[
                            {"type":"label","text":language_file["Gui"]['Create_Guild']['Have_Money']+str(scores)},
                            {"type":"label","text":language_file['Gui']['Create_Guild']["Need_Money"][0]+str(Config['Cost'])+language_file['Gui']['Create_Guild']["Need_Money"][1]},
                            {"type":"label","text":""},
                            {"placeholder":language_file['Gui']['Create_Guild']['Input_Guild'],"default":"","type":"input","text":language_file['Gui']['Create_Guild']['Input_Guild']},
                            {"placeholder":language_file['Gui']['Create_Guild']['x'][0],"default":"","type":"input","text":language_file['Gui']['Create_Guild']['x'][1]},
                            {"placeholder":language_file['Gui']['Create_Guild']['y'][0],"default":"","type":"input","text":language_file['Gui']['Create_Guild']['y'][1]},
                            {"placeholder":language_file['Gui']['Create_Guild']['z'][0],"default":"","type":"input","text":language_file['Gui']['Create_Guild']['z'][1]},
                            {"default":0,"options":language_file['Gui']['Create_Guild']['Dim']['Options'],"type":"dropdown","text":language_file['Gui']['Create_Guild']['Dim']['Text']},
                            {"default":False,"type":"toggle","text":language_file['Gui']['Create_Guild']['Allow_Pvp']}
                            ],
                        "type":"custom_form",
                    "title":language_file['Gui']['Create_Guild']['Title']
                        }
                    create_Guild_id = e['player'].sendCustomForm(json.dumps(createGuild))
                else:
                    Send_Error(e['player'],language_file['Gui']['Create_Guild']['Error'][0],language_file['Gui']['Create_Guild']['Error'][1])
            else:
                mc.tellraw(e['player'],language_file['Gui']['Create_Guild']['Error'][2])

        #main表单公会管理反馈
        elif e['selected'] == 1:
            if PlayerConfig[e['playername']]['Join'] != 'Null':
                if PlayerConfig[e['playername']]['Permission'] == 'Admin':
                    clos = [{"image":{"type":"path","data":"textures/ui/dressing_room_skins"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][0]},
                    {"image":{"type":"path","data":"textures/ui/pencil_edit_icon"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][1]},
                    {"image":{"type":"path","data":"textures/ui/icon_steve"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][2]},
                    {"image":{"type":"path","data":"textures/ui/permissions_member_star"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][3]},
                    {"image":{"type":"path","data":"textures/ui/import"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][4]},
                    {"image":{"type":"path","data":"textures/ui/icon_setting"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][5]},
                    {"image":{"type":"path","data":"textures/ui/jump_boost_effect"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][6]},
                    {"image":{"type":"path","data":"textures/ui/icon_trash"},"text":language_file['Gui']['Guild_Manage']['Admin_Text'][7]}]

                elif PlayerConfig[e['playername']]['Permission'] == 'Operator':
                    clos = [{"image":{"type":"path","data":"textures/ui/dressing_room_skins"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][0]},
                    {"image":{"type":"path","data":"textures/ui/pencil_edit_icon"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][1]},
                    {"image":{"type":"path","data":"textures/ui/icon_steve"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][2]},
                    {"image":{"type":"path","data":"textures/ui/import"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][3]},
                    {"image":{"type":"path","data":"textures/ui/icon_setting"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][4]},
                    {"image":{"type":"path","data":"textures/ui/icon_trash"},"text":language_file['Gui']['Guild_Manage']['Operator_Text'][5]}]

                elif PlayerConfig[e['playername']]['Permission'] == 'Member':
                    clos = [
                        {"image":{"type":"path","data":"textures/ui/dressing_room_skins"},"text":language_file['Gui']['Guild_Manage']['Member_Text'][0]},
                        {"image":{"type":"path","data":"textures/ui/icon_steve"},"text":language_file['Gui']['Guild_Manage']['Member_Text'][1]},
                        {"image":{"type":"path","data":"textures/ui/icon_trash"},"text":language_file['Gui']['Guild_Manage']['Member_Text'][2]}]
                Manage_Guild_Gui = e['player'].sendCustomForm('{"content": "'+language_file['Gui']['Guild_Manage']["Send_Gui"]+'","buttons":'+json.dumps(clos)+', "type":"form","title":"'+language_file['Gui']['Guild_Manage']["Title"]+'"}')
            else:
                Send_Error(e['player'],language_file['Gui']['Guild_Manage']['Error_Message'][0],language_file['Gui']['Guild_Manage']['Error_Message'][1])
        #main表单签到反馈
        elif e['selected'] == 2:
            Check_Guild_Name = PlayerConfig[e['playername']]['Join']
            if e['playername'] not in Checked:
                Checked[e['playername']] = True
                Write_File('Check')
                mc.tellraw(e['player'],language_file['Checking'])
            else:
                mc.tellraw(e['player'],language_file['Checked'])
                
        #main表单传送反馈
        elif e['selected'] == 3:
            Teleport_Guild_Name = PlayerConfig[e['playername']]['Join']
            if Teleport_Guild_Name != 'Null':
                x = int(GuildConfig[Teleport_Guild_Name]['Teleport']['Posistion']['x'])
                y = int(GuildConfig[Teleport_Guild_Name]['Teleport']['Posistion']['y'])
                z = int(GuildConfig[Teleport_Guild_Name]['Teleport']['Posistion']['z'])
                dim = int(GuildConfig[Teleport_Guild_Name]['Teleport']['Dim'])
                e['player'].teleport(x,y,z,dim)
                mc.tellraw(e['player'],language_file['Teleport_Success'])
            else:
                Send_Error(e['player'],language_file['Teleport_Error'][0],language_file['Teleport_Error'][1])
                
        #main表单世界公会反馈
        elif e['selected'] == 4:
            World_Guild_List = Get_All_Guild()
            World_Guild_List_Admin = []
            Guild_Admin = ''
            for a in World_Guild_List:
                for i in GuildConfig[a]['Member']:
                    if 'Admin' not in GuildConfig[a]['Member'].values():
                        Guild_Admin = language_file['Gui']["World_Guild_Text"]['No_Admin']
                    else:
                        if GuildConfig[a]['Member'][i] == 'Admin':
                            Guild_Admin = i
                Add_Guild_content = {'text':language_file['Gui']['World_Guild_Text']["Add_Guild_Content"][0]+a+'\n'+language_file['Gui']['World_Guild_Text']["Add_Guild_Content"][1]+Guild_Admin}
                World_Guild_List_Admin.append(Add_Guild_content) 
            World_Guild_Gui = e['player'].sendSimpleForm(language_file['Gui']["World_Guild_Text"]['Gui_Title'][0],language_file['Gui']["World_Guild_Text"]['Gui_Title'][1],json.dumps(World_Guild_List_Admin))
##################################################################################################
    #Create_Guild创建公会反馈
    elif e['formid'] == create_Guild_id:
        null = None
        e['selected'] = json.loads(e['selected'])
        Teleport_list = [int(e['selected'][4]),int(e['selected'][5]),int(e['selected'][6]),e['selected'][7]]
        GuildName = e['selected'][3]
        #调用"创建公会"函数
        create_Guild(e['player'],GuildName,Teleport_list,e['playername'],e['selected'][8])

    #Manage_Guild_Gui公会管理
    elif e['formid'] == Manage_Guild_Gui:
        if PlayerConfig[e['playername']]['Permission'] == 'Admin':
            try:
                e['selected'] = int(e['selected'])
            except:
                pass
            #公会管理--公会成员
            if e['selected'] == 0:
                Guild_Names = PlayerConfig[e['playername']]['Join']
                Guild_Members(e['player'],Guild_Names)

            #公会管理--公会改名
            elif e['selected'] == 1:
                Befor_Name = PlayerConfig[e['playername']]['Join']
                Change_Name = {
                "content":[
                    {
                        "type":"label",
                        "text":language_file['Gui']['Change_Name']['Befor_Name']+Befor_Name
                        },
                    {
                        "placeholder":language_file['Gui']['Change_Name']['Input_Name'][0],
                        "default":"",
                        "type":"input",
                        "text":language_file['Gui']['Change_Name']['Input_Name'][1]
                        }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']['Change_Name']['Title']
                }
                Change_Name_Gui = e['player'].sendCustomForm(json.dumps(Change_Name))

            #公会管理--邀请玩家
            elif e['selected'] == 2:
                NameList = getOnLinePlayers()
                InvitationPlayer = []
                for i in NameList:
                    if PlayerConfig[i]['Join'] != 'Null':
                        InvitationPlayer.append(i)
                if InvitationPlayer != []:
                    contents = {
                        "content":[
                            {
                                "default":0,
                                "options":InvitationPlayer,
                                "type":"dropdown",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][0]
                                },
                            {
                                "placeholder":language_file['Gui']["Invitation_Player"]["Text"][1],
                                "default":"",
                                "type":"input",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][2]
                                }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                
                else:
                    contents = {
                        "content":[
                            {
                                "type":"label",
                                "text":language_file['Gui']["Invitation_Player"]['Error']
                            }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                InvitationPlayer_Gui = e['player'].sendCustomForm(json.dumps(contents))

            #公会管理--更改权限
            elif e['selected'] == 3:
                Change_Permission_Guild_Name = PlayerConfig[e['playername']]['Join']
                Change_Permission_Guild_Member = []
                for i in GuildConfig[Change_Permission_Guild_Name]['Member']:
                    Change_Permission_Guild_Member.append(i)
                Change_Permission = {
                    "content":[
                            {
                                "default":0,
                                "options":Change_Permission_Guild_Member,
                                "type":"dropdown",
                                "text":language_file["Change_Permission"]['Text'][0]
                                },
                            {
                                "default":0,
                                "options":language_file["Change_Permission"]['Options'],
                                "type":"dropdown",
                                "text":language_file["Change_Permission"]['Text'][1]
                                }
                    ],
                "type":"custom_form",
                "title":language_file["Change_Permission"]['Title']
                }
                Change_Permission_Gui = e['player'].sendCustomForm(json.dumps(Change_Permission))
            #公会管理--踢出玩家
            elif e['selected'] == 4:
                global Kick_Player_Member_2
                Kick_Player_Guild_Name = PlayerConfig[e['playername']]['Join']
                Kick_Player_Member = GuildConfig[Kick_Player_Guild_Name]['Member']
                Kick_Player_Member_2 = []
                for i in Kick_Player_Member:
                    Kick_Player_Member_2.append(i)
                Kick_Player_Member_2.remove(e['playername'])
                Kick_Player_Gui = {
                    "content":[
                            {
                                "default":0,
                                "options":Kick_Player_Member_2,
                                "type":"dropdown",
                                "text":language_file['Kick_Player']['Text']
                                }
                    ],
                "type":"custom_form",
                "title":language_file['Kick_Player']['Title']
                }
                Kick_Player_Gui_Id = e['player'].sendCustomForm(json.dumps(Kick_Player_Gui))

            #公会管理--更改传送
            elif e['selected'] == 5:
                Change_Position_Guild_Name = PlayerConfig[e['playername']]['Join']
                Change_Position_Gui = {
                    "content":[
                            {
                                "placeholder":language_file["Change_Position"]['x'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['x'][1]
                                },
                            {
                                "placeholder":language_file["Change_Position"]['y'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['y'][1]
                                },
                            {
                                "placeholder":language_file["Change_Position"]['z'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['z'][1]
                                },
                            {
                                "default":0,
                                "options":language_file["Change_Position"]['Dim']['Options'],
                                "type":"dropdown","text":language_file["Change_Position"]['Dim']['Text']}
                    ],
                "type":"custom_form",
                "title":language_file["Change_Position"]['Title']
                }
                Change_Position_Gui_Id = e['player'].sendCustomForm(json.dumps(Change_Position_Gui))
            
            #公会管理--转让公会
            elif e['selected'] == 6:
                Transfer_Guild_Name = PlayerConfig[e['playername']]['Join']
                Transfer_Guild_Member = GuildConfig[Transfer_Guild_Name]['Member']
                Transfer_Guild_Member_2 = []
                for i in Transfer_Guild_Member:
                    Transfer_Guild_Member_2.append(i)
                Transfer_Guild_Member_2.remove(e['playername'])
                Transfer_Verification_Code = Verification_Code()
                Transfer_Guild_Gui = {
                    "content":[
                            {
                                "default":0,
                                "options":Transfer_Guild_Member_2,
                                "type":"dropdown",
                                "text":language_file["Transfer_Guild"]['Text'][0]
                                },
                            {
                                "placeholder":language_file["Transfer_Guild"]['Text'][1],
                                "default":"",
                                "type":"input",
                                "text":language_file["Transfer_Guild"]['Text'][2]+Transfer_Verification_Code
                                }

                    ],
                "type":"custom_form",
                "title":language_file["Transfer_Guild"]['Title']
                }
                Transfer_Guild_Gui_Id = mc.sendCustomForm(e['player'],json.dumps(Transfer_Guild_Gui))

            #公会管理--解散公会
            elif e['selected'] == 7:
                Dissolution_Guild_Name = PlayerConfig[e['playername']]['Join']
                Dissolution_Verification_Code = Verification_Code()
                Dissolution_Guild_Gui = {
                    "content":[
                            {
                                "placeholder":language_file["Dissolution_Guild"]['Text'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Dissolution_Guild"]['Text'][1]+Dissolution_Verification_Code},
                    ],
                "type":"custom_form",
                "title":language_file["Dissolution_Guild"]['Title']
                }
                Dissolution_Guild_Gui_Id = e['player'].sendCustomForm(json.dumps(Dissolution_Guild_Gui))
        #管理版管理
        elif PlayerConfig[e['playername']]['Permission'] == 'Operator':
            try:
                e['selected'] = int(e['selected'])
            except:
                pass
            #公会管理--公会成员
            if e['selected'] == 0:
                Group_Member_Name = PlayerConfig[e['playername']]['Join']
                Members = ''
                for i in GuildConfig[Group_Member_Name]['Member']:
                    if GuildConfig[Group_Member_Name]['Member'][i] == 'Admin':
                        Members += language_file['Gui']["Guild_Member_Text"]["Admin"]+i
                    elif GuildConfig[Group_Member_Name]['Member'][i] == 'Operator':
                        Members += language_file['Gui']["Guild_Member_Text"]["Operator"]+i
                    else:
                        Members += language_file['Gui']["Guild_Member_Text"]["Member"]+i
                mc.sendSimpleForm(e['player'],language_file['Gui']["Guild_Member_Text"]['Gui_Title'][0]+Group_Member_Name+language_file['Gui']["Guild_Member_Text"]['Gui_Title'][1],Members,'[]')

            #公会管理--公会改名
            elif e['selected'] == 1:
                Befor_Name = PlayerConfig[e['playername']]['Join']
                Change_Name = {
                "content":[
                    {"type":"label","text":language_file['Gui']['Change_Name']['Befor_Name']+Befor_Name},
                    {"placeholder":language_file['Gui']['Change_Name']['Input_Name'][0],"default":"","type":"input","text":language_file['Gui']['Change_Name']['Input_Name'][1]}
                    ],
                "type":"custom_form",
                "title":language_file['Gui']['Change_Name']['Title']
                }
                Change_Name_Gui = e['player'].sendCustomForm(json.dumps(Change_Name))

            #公会管理--邀请玩家
            elif e['selected'] == 2:
                NameList = getOnLinePlayers()
                InvitationPlayer = []
                for i in NameList:
                    if PlayerConfig[i]['Join'] == 'Null':
                        InvitationPlayer.append(i)
                if InvitationPlayer != []:
                    contents = {
                        "content":[
                            {
                                "default":0,
                                "options":InvitationPlayer,
                                "type":"dropdown",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][0]
                                },
                            {
                                "placeholder":language_file['Gui']["Invitation_Player"]["Text"][1],
                                "default":"",
                                "type":"input",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][2]
                                }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                
                else:
                    contents = {
                        "content":[
                            {
                                "type":"label",
                                "text":language_file['Gui']["Invitation_Player"]['Error']
                            }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                InvitationPlayer_Gui = e['player'].sendCustomForm(json.dumps(contents))

            #公会管理--踢出玩家
            elif e['selected'] == 3:
                Kick_Player_Guild_Name = PlayerConfig[e['playername']]['Join']
                Kick_Player_Member = []
                for i in GuildConfig[Kick_Player_Guild_Name]['Member']:
                    if GuildConfig[Kick_Player_Guild_Name]['Member'][i] == 'Member':
                        Kick_Player_Member.append(i)
                try:
                    Kick_Player_Member.remove(e['playername'])
                except:
                    pass
                Kick_Player_Gui = {
                    "content":[
                            {
                                "default":0,
                                "options":Kick_Player_Member_2,
                                "type":"dropdown",
                                "text":language_file['Kick_Player']['Text']
                                }
                    ],
                "type":"custom_form",
                "title":language_file['Kick_Player']['Title']
                }
                Kick_Player_Gui_Id = e['player'].sendCustomForm(json.dumps(Kick_Player_Gui))

            #公会管理--更改传送
            elif e['selected'] == 4:
                Change_Position_Guild_Name = PlayerConfig[e['playername']]['Join']
                Change_Position_Gui = {
                    "content":[
                            {
                                "placeholder":language_file["Change_Position"]['x'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['x'][1]
                                },
                            {
                                "placeholder":language_file["Change_Position"]['y'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['y'][1]
                                },
                            {
                                "placeholder":language_file["Change_Position"]['z'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file["Change_Position"]['z'][1]
                                },
                            {
                                "default":0,
                                "options":language_file["Change_Position"]['Dim']['Options'],
                                "type":"dropdown","text":language_file["Change_Position"]['Dim']['Text']}
                    ],
                "type":"custom_form",
                "title":language_file["Change_Position"]['Title']
                }
                Change_Position_Gui_Id = e['player'].sendCustomForm(json.dumps(Change_Position_Gui))

            #公会管理--退出公会
            elif e['selected'] == 5:
                Exit_Guild_Name = PlayerConfig[e['playername']]['Join']
                Exit_Verification_Code = Verification_Code()
                Exit_Guild_Gui = {
                    "content":[
                            {
                                "placeholder":language_file['Exit_Guild']['Text'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file['Exit_Guild']['Text'][1]+Exit_Verification_Code}
                    ],
                "type":"custom_form",
                "title":language_file['Exit_Guild']['Title']
                }
                Exit_Guild_Gui_Id = e['player'].sendCustomForm(json.dumps(Exit_Guild_Gui))


        #公会管理成员版
        elif PlayerConfig[e['playername']]['Permission'] == 'Member':
            try:
                e['selected'] = int(e['selected'])
            except:
                pass
            #公会管理--公会成员
            if e['selected'] == 0:
                Group_Member_Name = PlayerConfig[e['playername']]['Join']
                Members = ''
                for i in GuildConfig[Group_Member_Name]['Member']:
                    if GuildConfig[Group_Member_Name]['Member'][i] == 'Admin':
                        Members += language_file['Gui']["Guild_Member_Text"]["Admin"]+i
                    elif GuildConfig[Group_Member_Name]['Member'][i] == 'Operator':
                        Members += language_file['Gui']["Guild_Member_Text"]["Operator"]+i
                    else:
                        Members += language_file['Gui']["Guild_Member_Text"]["Member"]+i
                e['player'].sendSimpleForm(language_file['Gui']["Guild_Member_Text"]['Gui_Title'][0]+Group_Member_Name+language_file['Gui']["Guild_Member_Text"]['Gui_Title'][1],Members,'[]')

            #公会管理--邀请玩家
            elif e['selected'] == 2:
                NameList = getOnLinePlayers()
                InvitationPlayer = []
                for i in NameList:
                    if PlayerConfig[i]['Join'] != 'Null':
                        InvitationPlayer.append(i)
                if InvitationPlayer != []:
                    contents = {
                        "content":[
                            {
                                "default":0,
                                "options":InvitationPlayer,
                                "type":"dropdown",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][0]
                                },
                            {
                                "placeholder":language_file['Gui']["Invitation_Player"]["Text"][1],
                                "default":"",
                                "type":"input",
                                "text":language_file['Gui']["Invitation_Player"]["Text"][2]
                                }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                
                else:
                    contents = {
                        "content":[
                            {
                                "type":"label",
                                "text":language_file['Gui']["Invitation_Player"]['Error']
                            }
                    ],
                "type":"custom_form",
                "title":language_file['Gui']["Invitation_Player"]['Title']
                }
                InvitationPlayer_Gui = e['player'].sendCustomForm(json.dumps(contents))
            
            #公会管理--退出公会
            elif e['selected'] == 2:
                Exit_Guild_Name = PlayerConfig[e['playername']]['Join']
                Exit_Verification_Code = Verification_Code()
                Exit_Guild_Gui = {
                    "content":[
                            {
                                "placeholder":language_file['Exit_Guild']['Text'][0],
                                "default":"",
                                "type":"input",
                                "text":language_file['Exit_Guild']['Text'][1]+Exit_Verification_Code}
                    ],
                "type":"custom_form",
                "title":language_file['Exit_Guild']['Title']
                }
                Exit_Guild_Gui_Id = mc.sendCustomForm(e['player'],json.dumps(Exit_Guild_Gui))
    #公会管理操作--更改会名
    elif e['formid'] == Change_Name_Gui:
        e['selected'] = json.loads(e['selected'])
        Befor_Data = GuildConfig[Befor_Name]
        GuildConfig[e['selected'][1]] = Befor_Data
        del GuildConfig[Befor_Name]
        Write_File('Guild')
        mc.tellraw(e['player'],language_file['Change_Name_Action']+e['selected'][1])

    #公会管理操作--邀请玩家
    elif e['formid'] == InvitationPlayer_Gui:
        Invitation_Guild_Name = PlayerConfig[mc.getPlayerInfo(e['player'])['playername']]['Join']
        Invitation_Player_Name = e['playername']
        e['selected'] = json.loads(e['selected'])
        Invitation_Player_Id_List = mc.getPlayerList()
        Invitation_Player_Id = []
        for i in Invitation_Player_Id_List:
            for a in InvitationPlayer:
                if mc.getPlayerInfo(i)['playername'] == a:
                    Invitation_Player_Id.append(i)
        player = Invitation_Player_Id[e['selected']]
        Invitation_Send_Gui_Id = player.sendModalForm(language_file['Invitation_Player_Action'][0]+Invitation_Guild_Name+language_file['Invitation_Player_Action'][1],language_file['Invitation_Player_Action'][2]+e['selected'][1],language_file['Invitation_Player_Action'][3],language_file['Invitation_Player_Action'][4])

    #公会管理操作--更改权限
    elif e['formid'] == Change_Permission_Gui:
        e['selected'] == json.dumps(e['selected'])
        Member = Change_Permission_Guild_Member[e['selected'][0]]
        Change_Permission_Guild_Name_2 = PlayerConfig[Member]['Join']
        if e['selected'][1] == 0:
            PlayerConfig[Member]['Permission'] = 'Operator'
            GuildConfig[Change_Permission_Guild_Name_2]['Member'][Member] = 'Operator'
            Write_File('Guild')
            Write_File('Player')
        elif e['selected'][0] == 1:
            PlayerConfig[Member]['Permission'] = 'Member'
            GuildConfig[Change_Permission_Guild_Name_2]['Member'][Member] = 'Member'
            Write_File('Guild')
            Write_File('Player')
        mc.tellraw(e['player'],language_file['Change_Permission_Action'][0]+Member+language_file['Change_Permission_Action'][1])

    #公会管理操作--踢出玩家
    elif e['formid'] == Kick_Player_Gui_Id:
        e['selected'] = json.loads(e['selected'])
        Player = Kick_Player_Member(e['selected'][0])
        Guild_Name = PlayerConfig(Player)
        del GuildConfig[Guild_Name]['Member']['Player']
        PlayerConfig[Player] = {
            'Created_Guild':0,
            'Permission':'Null',
            'Join':'Null'
        }
        Write_File('Player')
        Write_File('Guild')
        mc.tellraw(e['player'],language_file['Kick_Player_Action'][0]+Player+language_file['Kick_Player_Action'][1])

    #公会管理操作--更改传送
    elif e['formid'] == Change_Position_Gui_Id:
        e['selected'] = json.loads(e['selected'])
        Change_Position_Guild_Name = PlayerConfig[e['playername']]['Join']
        GuildConfig[Change_Position_Guild_Name]['Teleport'] = {
            "Dim": e['selected'][3],
            "Posistion": {
                "x": int(e['selected'][0]),
                "y": int(e['selected'][1]),
                "z": int(e['selected'][2])
            }
        }
        Write_File('Guild')
        mc.tellraw(e['player'],language_file['Change_Position_Action'])

    #公会管理操作--转让公会
    elif e['formid'] == Transfer_Guild_Gui_Id:
        e['selected'] = json.dumps(e['selected'])
        Befor_Admin = e['playername']
        Transfer_Guild_Name_2 = PlayerConfig[Befor_Admin]['Join']
        Transfer_Guild_Member_2 = []
        for i in GuildConfig[Transfer_Guild_Name_2]['Member']:
            Transfer_Guild_Member_2.append(i)
        Transfer_Guild_Member_2.remove(Befor_Admin)
        After_Admin = Transfer_Guild_Member_2[e['selected'][0]]
        if e['selected'][1] == Transfer_Verification_Code:
            PlayerConfig[Befor_Admin]['Permission'] = 'Member'
            GuildConfig[Transfer_Guild_Name_2]['Member'][Befor_Admin] = 'Member'
            PlayerConfig[After_Admin]['Permission'] = 'Admin'
            GuildConfig[Transfer_Guild_Name_2]['Member'][After_Admin] = 'Admin'
            Write_File('Guild')
            Write_File('Player')
            mc.tellraw(e['player'],language_file['Transfer_Guild_Action'][0])
        else:
            mc.tellraw(e['player'],language_file['Transfer_Guild_Action'][1])

    #公会管理操作--解散公会
    elif e['formid'] == Dissolution_Guild_Gui_Id:
        e['selected'] = json.loads(e['selected'])
        Dissolution_Guild_Name_2 = PlayerConfig[e['playername']]['Join']
        if e['selected'][0] == Dissolution_Verification_Code:
            for i in GuildConfig[Dissolution_Guild_Name_2]['Member']:
                PlayerConfig[i] = {
                    'Created_Guild':0,
                    'Permission':'Null',
                    'Join':'Null'
                }
                del GuildConfig[Dissolution_Guild_Name_2]
                Write_File('Player')
                Write_File('Guild')
            mc.tellraw(e['player'],language_file['Dissolution_Guild_Action'][0])
        else:
            mc.tellraw(e['player'],language_file['Dissolution_Guild_Action'][1])
    
    #公会管理操作--退出公会
    elif e['formid'] == Exit_Guild_Gui_Id:
        e['selected'] = json.loads(e['selected'])
        if e['selected'][0] == Exit_Verification_Code:
            Exit_Guild = PlayerConfig[e['playername']]['Join']
            PlayerConfig[e['playername']] = {
                'Created_Guild':0,
                'Permission':'Null',
                'Join':'Null'
                }
            del GuildConfig[Exit_Guild]['Member'][e['playername']]
            mc.tellraw(e['player'],language_file['Exit_Guild_Action'][0])
        else:
            mc.tellraw(e['player'],language_file['Exit_Guild_Action'][1])

    #邀请玩家--进行操作
    elif e['formid'] == Invitation_Send_Gui_Id:
        e['selected'] = json.loads(e['selected'])
        Joined_Guild_Name = Invitation_Guild_Name
        if e['selected']:
            GuildConfig[Joined_Guild_Name]['Member'][e['playername']] = 'Member'
            PlayerConfig[e['playername']]['Join'] = Joined_Guild_Name
            PlayerConfig[e['playername']]['Permission'] = 'Member'
            mc.tellraw(e['player'],language_file['Invitation_Send_Action'][0]+Joined_Guild_Name)
            mc.runcmd('tellraw "'+Invitation_Player_Name+'" {"rawtext":[{"text":"'+language_file['Invitation_Send_Action'][1]+'"}]}')
            Write_File('Guild')
            Write_File('Player')
        else:
            mc.runcmd('tellraw "'+Invitation_Player_Name+'" {"rawtext":[{"text":"'+language_file['Invitation_Send_Action'][2]+'"}]}')

    #世界公会--选择公会
    elif e['formid'] == World_Guild_Gui:
        try:
            e['selected'] = int(e['selected'])
        except:
            pass
        World_Guild_List = Get_All_Guild()
        World_Guild_List_Admin_2 = []
        for a in World_Guild_List:
            for i in GuildConfig[a]['Member']:
                if GuildConfig[a]['Member'][i] == 'Admin':
                    Guild_Admin = GuildConfig[a]['Member'][i]
            World_Guild_List_Admin_2.append(a)
        Selected_Guild = World_Guild_List_Admin_2[e['selected']]
        Group_Member_Name = Selected_Guild
        Members = ''
        for i in GuildConfig[Selected_Guild]['Member']:
            if GuildConfig[Group_Member_Name]['Member'][i] == 'Admin':
                Members += language_file['Gui']["Guild_Member_Text"]["Admin"]+i
            elif GuildConfig[Group_Member_Name]['Member'][i] == 'Operator':
                Members += language_file['Gui']["Guild_Member_Text"]["Operator"]+i
            else:
                Members += language_file['Gui']["Guild_Member_Text"]["Member"]+i
        World_Guild_Selected_Id = e['player'].sendSimpleForm(language_file['Gui']["Guild_Member_Text"]['Gui_Title'][0]+Selected_Guild+language_file['Gui']["Guild_Member_Text"]['Gui_Title'][1],Members,'[{"text":"'+language_file['Gui']["Guild_Member_Text"]['Join_Them']+'"}]')
        
    
    #世界公会加入操作
    elif e['formid'] == World_Guild_Selected_Id:
        if e['selected'] == exit():
            if PlayerConfig[e['playername']]['Join'] == 'Null':
                World_Guild_accept = e['player'].sendModalForm(language_file['World_Guild_Selected_Action']['Ask'][0],language_file['World_Guild_Selected_Action']['Ask'][1],language_file['World_Guild_Selected_Action']['Ask'][2],language_file['World_Guild_Selected_Action']['Ask'][3])
            else:
                Send_Error(e['player'],language_file['World_Guild_Selected_Action']['Error'][0],language_file['World_Guild_Selected_Action']['Error'][1])

    #世界公会确认
    elif e['formid'] == World_Guild_accept:
        e['selected'] = json.dumps(e['selected'])
        if e['selected']:
            GuildConfig[Selected_Guild]['Member'][e['playername']] = 'Member'
            PlayerConfig[e['playername']]['Join'] = Selected_Guild
            PlayerConfig[e['playername']]['Permission'] = 'Member'
            mc.tellraw(e['player'],language_file['World_Guild_Accept']+Selected_Guild)
            Write_File('Guild')
            Write_File('Player')
    
    #移除线程
#监听数据
def form_selected(e):
    #判断数据
    if e['selected'] != 'null':
        #创建线程
        form_action(e)

#################################################################################################################
#监听玩家指令
def listen_cmd(e):
    cmd = e.split(' ')
    if cmd[0] == 'guild':
        if len(cmd) == 1:
            cmd = ['guild','shid']
        #重载配置文件
        if cmd[1] == 'reload' or cmd[1] == 'r':
            if len(cmd) == 2:
                Read_Files()
                WriteInfo('[HGuild]',language_file['Cmds']['Reload'])

        #创建公会
        elif cmd[1] == 'create' or cmd[1] == 'c':
            if len(cmd) == 3:
                jcr = json.loads(cmd[2])
                Create_Guild_Data = {
                    "Teleport":{
                        "Dim":int(jcr['Dim']),
                        "Posistion":{
                            "x":int(jcr['X']),
                            "y":int(jcr['Y']),
                            "z":int(jcr['Z'])
                        }
                    },
                    "Money":0,
                    "Pvp":jcr['Pvp'],
                    "Member":{
                        jcr['Player']:"Admin"
                    }
                }
                PlayerData = {
                    "Created_Guild": 1,
                    "Join": jcr['Name'],
                    "Permission": "Admin"
                }
                GuildConfig[jcr['Name']] = Create_Guild_Data
                PlayerConfig[jcr['Player']] = PlayerData
                Write_File('Player')
                Write_File('Guild')
                WriteInfo('[HGuild]',language_file['Cmds']['Create_Guild_Success'][0]+jcr['Name']+language_file['Cmds']['Create_Guild_Success'][0])
            else:
                WriteError('[HGuild]',language_file['Cmds']['Cmd_Fail'])
        
        #删除公会
        elif cmd[1] == 'delete' or cmd[1] == 'd':
            if len(cmd) == 3:
                if cmd[2] in GuildConfig:
                    del GuildConfig[cmd[2]]
                    WriteInfo('[HGuild]',language_file['Cmds']['Delete_Success'])
                else:
                    WriteError('[HGuild]',cmd[2]+language_file['Cmds']['Not_Found_Guild'])
            else:
                WriteError('[HGuild]',language_file['Cmds']['Cmd_Fail'])

        #分配玩家
        elif cmd[1] == 'distribution' or cmd[1] == 'f':
            if len(cmd) == 4:
                if cmd[3] in GuildConfig:
                    if cmd[2] in PlayerConfig:
                        GuildConfig[cmd[3]]['Member'][e['playername']] = 'Member'
                        PlayerConfig[e['playername']]['Join'] = cmd[3]
                        PlayerConfig[e['playername']]['Permission'] = 'Member'
                        mc.runcmd('tellraw "'+cmd[2]+'" {"rawtext":[{"text":"'+language_file['Cmds']['Distribution_Player'][0]+'"'+cmd[3]+'}]}')
                        Write_File('Guild')
                        Write_File('Player')
                        WriteInfo('[HGuild]',language_file['Cmds']['Distribution_Player'][1])
                    else:
                        WriteWarn('[HGuild]',language_file['Cmds']['Not_Found_Player'])
                else:
                    WriteWarn('[HGuild]',language_file['Cmds']['Not_Found_Guild'])
            else:
                WriteError('[HGuild]',language_file['Cmds']['Cmd_Fail'])
        elif cmd[1] == 'version' or cmd[1] == 'v':
            WriteInfo('[HGuild]',language_file['Cmds']['Version']+str(PluginVersion))

        #帮助菜单
        elif cmd[1] == 'help' or cmd[1] == '?' or cmd[1] == 'h':
            print(language_file['Cmds']['Help_Menu'][0])
            print(language_file['Cmds']['Help_Menu'][1])
            print(language_file['Cmds']['Help_Menu'][2])
            print(language_file['Cmds']['Help_Menu'][3])
            print(language_file['Cmds']['Help_Menu'][4])
            print(language_file['Cmds']['Help_Menu'][5])
            print(language_file['Cmds']['Help_Menu'][6])
        else:
            WriteError('[HGuild]',language_file['Cmds']['Not_Found_Cmd'])
        return False


#################################################################################################################
#禁止Pvp
def Pvp(e):
    try:
        Actor_Name = mc.getPlayerInfo(e['actor'])['playername']
        Player_Name = mc.getPlayerInfo(e['player'])['playername']
        Player_Join_Guild = PlayerConfig[Player_Name]['Join']
        for i in GuildConfig[Player_Join_Guild]['Member']:
            if i == Actor_Name and GuildConfig[Player_Join_Guild]['Pvp'] == True:
                mc.tellraw(e['player'],language_file['Ban_Pvp'])
                mc.tellraw(e['actor'],language_file['Ban_Pvp'])
                return False
    except:
        pass

##################################################################################################
#启动函数
GuildConfigDict = {}
def Register_Cmd(command):
    mc.setCommandDescription(command,language_file['Cmd_Title'])
    WriteInfo('[HGuild]',language_file["Register_Cmd_Success"][0]+Config['Cmd']+language_file["Register_Cmd_Success"][1])
def Register_Listener():
    mc.setListener('玩家攻击',Pvp)
    mc.setListener('后台输入',listen_cmd)
    mc.setListener('选择表单',form_selected)
    mc.setListener('输入指令',input_cmd)
    mc.setListener('加入游戏',Player_Join)
    WriteInfo('[HGuild]',language_file['Register_Listener_Success'])
def load_plugin():
    if int(mc.getVersion()) > NeedPyrVersion:
        WriteError('[HGuild]','The current PYR version is too low, please update it to use')
    global GuildConfigDict
    WriteInfo('[HGuild]',language_file['Runing_Plugin'])

    Py_Version = sys.version_info.major

    #自检文件
    test = Self_test()
    if test == 'True':
        WriteInfo('[HGuild]',language_file["Self_Test_Success"])
    else:
        WriteError('[HGuild]',language_file["Self_Test_Fail"])

    #读取文件
    read = Read_Files()
    if read == 'True':
        WriteInfo('[HGuild]',language_file["Read_Success"])
    else:
        WriteError('[HGuild]',language_file["Read_Fail"])

    #插件更新
    plugin_update()
    Register_Cmd(Config['Cmd'])
    Register_Listener()
    Test_Eula()
    #创建计分板
    WriteInfo('[HGuild]','HGuildM'+str(PluginVersion)+' Powered By HuoHuaX')
##################################################################################################
#调用函数
load_plugin()