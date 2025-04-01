import os
import json

class lang():
    def load_lang(self, lang_dir: str):
        lang_zh_CN_data_file_path = os.path.join(lang_dir, 'zh_CN.json')
        lang_en_US_data_file_path = os.path.join(lang_dir, 'en_US.json')

        if not os.path.exists(lang_zh_CN_data_file_path):
            zh_CN = {
                'open_main_form.message.fail': 'UTP 的所有功能已被管理员禁用...',
                'message.type_error': '表单解析错误, 请按提示正确填写...',
                'back_to_main_form': '返回',
                'back_to_home_form': '返回',
                'back_to_warp_form': '返回',
                'coordinates': '坐标',
                'dimension': '维度',
                'main_form.title': '传送合集主表单',
                'main_form.content': '请选择操作...',
                'main_form.button.home': '家园传送点',
                'main_form.button.warp': '地标传送点',
                'main_form.button.tpa_and_tpahere': '玩家互传',
                'main_form.button.tp_setting': '玩家互传设置',
                'main_form.button.tpr': '随机传送',
                'main_form.button.back': '返回上一死亡点',
                'main_form.button.reload': '重载配置文件',
                'main_form.button.close': '关闭',
                'main_form.button.back_to_zx_ui': '返回',

                'home_form.title': '我的传送点',
                'home_form.content': '请选择操作...',
                'home_form.button.addhome': '添加脚下坐标为传送点',
                'addhome_form.title': '添加传送点',
                'addhome_form.textinput.label': '输入传送点名称',
                'addhome_form.textinput.placeholder': '请输入任意字符串, 但不能留空...',
                'addhome_form.submit_button': '添加',
                'addhome.message.fail': '添加传送点失败',
                'addhome.message.fail.reason_1': '你已经有一个名为 {0} 的传送点...',
                'addhome.message.fail_reason_2': '你拥有的传送点数量已达上限...',
                'addhome.message.success': '添加传送点成功...',
                'home_info_form.title': '传送点',
                'home_info_form.content': '请选择操作...',
                'home_info_form.button.tp': '传送',
                'home_info_form.button.edithome': '编辑传送点',
                'tphome.message': '传送成功...',
                'edithome_form.title': '编辑传送点',
                'edithome_form.content': '请选择操作...',
                'edithome_form.button.updatehome': '更新传送点',
                'edithome_form.button.deletehome': '删除传送点',
                'updatehome_form.title': '更新传送点',
                'updatehome_form.content': '请选择操作...',
                'updatehome_form.button.renamehome': '重命名传送点',
                'updatehome_form.button.updatelocation': '更新传送点位置',
                'renamehome_form.title': '重命名传送点',
                'renamehome_form.textinput.label': '输入新的传送点名',
                'renamehome_form.textinput.placeholder': '请输入任意字符串, 但不能留空...',
                'renamehome_form.submit_button': '重命名',
                'renamehome.message.fail': '重命名传送点失败',
                'renamehome.message.fail.reason': '你已经有一个名为 {0} 的传送点...',
                'renamehome.message.success': '重命名传送点成功...',
                'home_updatelocation_form.title': '更新传送点位置',
                'home_updatelocation_form.content': '你确定要更新该传送点位置吗？',
                'home_updatelocation_form.button.confirm': '确认',
                'home_updatelocation.message.success': '更新传送点位置成功...',
                'deletehome_form.title': '删除传送点',
                'deletehome_form.content': '你确定要删除该传送点吗？',
                'deletehome_form.button.confirm': '确认',
                'deletehome.message.success': '删除传送点成功...',

                'warp_form.title': '地标传送点',
                'warp_form.content': '请选择操作...',
                'warp_form.button.addwarp': '添加脚下坐标为地标传送点',
                'addwarp_form.title': '添加地标传送点',
                'addwarp_form.textinput.label': '输入地标传送点名称',
                'addwarp_form.textinput.placeholder': '请输入任意字符串, 但不能留空...',
                'addwarp_form.submit_button': '添加',
                'addwarp.message.fail': '添加地标传送点失败',
                'addwarp.message.fail.reason': '已经有一个名为 {0} 的地标传送点...',
                'addwarp.message.success': '添加地标传送点成功...',
                'warp_info_form.title': '地标传送点',
                'warp_info_form.content': '请选择操作...',
                'warp_info_form.button.tp': '传送',
                'warp_info_form.button.editwarp': '编辑地标传送点',
                'tpwarp.message.success': '传送成功...',
                'editwarp_form.title': '编辑地标传送点',
                'editwarp_form.content': '请选择操作...',
                'editwarp_form.button.updatewarp': '更新地标传送点',
                'editwarp_form.button.deletewarp': '删除地标传送点',
                'updatewarp_form.title': '更新地标传送点',
                'updatewarp_form.content': '请选择操作...',
                'updatewarp_form.button.renamewarp': '重命名地标传送点',
                'updatewarp_form.button.updatelocation': '更新地标传送点位置',
                'renamewarp_form.title': '重命名地标传送点',
                'renamewarp_form.textinput.label': '输入新的地标传送点名',
                'renamewarp_form.textinput.placeholder': '请输入任意字符串, 但不能留空...',
                'renamewarp_form.submit_button': '重命名',
                'renamewarp.message.fail': '重命名地标传送点失败',
                'renamewarp.message.fail.reason': '已经有一个名为 {0} 的地标传送点...',
                'renamewarp.message.success': '重命名地标传送点成功...',
                'warp_updatelocation_form.title': '更新地标传送点位置',
                'warp_updatelocation_form.content': '你确定要更新该地标传送点位置吗？',
                'warp_updatelocation_form.button.confirm': '确认',
                'warp_updatelocation.message.success': '更新地标传送点位置成功...',
                'deletewarp_form.title': '删除地标传送点',
                'deletewarp_form.content': '你确定要删除该地标传送点位置吗？',
                'deletewarp_form.button.confirm': '确认',
                'deletewarp.message.success': '删除地标传送点成功...',

                'tpa_and_tpahere_form.title': '玩家互传',
                'tpa_and_tpahere_form.submit_button': '确认',
                'tpa_and_tpahere_form.dropdown_1.label': '选择玩家',
                'tpa_and_tpahere_form.dropdown_2.label': '选择模式',
                'tpa_and_tpahere.message.fail': '当前没有可执行互传的玩家在线...',
                'tpa_and_tpahere.message.fail.reason.offline': '玩家 {0} 已离线...',

                'tpa_form.title': 'TPA 请求',
                'tpa_form.content': '玩家 {0} 向你发送了一个 TPA 请求...',
                'tpa_form.button.accept': '接受',
                'tpa_form.button.deny': '拒绝',
                'tpa.message.fail_1': '发送 TPA 请求失败',
                'tpa.message.fail_2': '接受 TPA 请求失败',
                'tpa.message.success': '发送 TPA 请求成功...',
                'tpa.message.deny': '玩家 {0} 拒绝了你的 TPA 请求...',

                'tpahere_form.title': 'TPAHere 请求',
                'tpahere_form.content': '玩家 {0} 向你发送了一个 TPAHere 请求...',
                'tpahere_form.button.accept': '接受',
                'tpahere_form.button.deny': '拒绝',
                'tpahere.message.fail_1': '发送 TPAHere 请求失败',
                'tpahere.message.fail_2': '接受 TPAHere 请求失败',
                'tpahere.message.success': '发送 TPAHere 请求成功',
                'tpahere.message.deny': '玩家 {0} 拒绝了你的 TPAHere 请求...',

                'tpsetting_form.title': '玩家互传设置',
                'tpsetting_form.toggle.lable': '允许其他玩家向你发送互传请求',
                'tpsetting_form.submit_button': '更新',
                'tpsetting.message.success': '更新玩家互传设置成功...',

                'tpr.message.fail': '随机传送失败',
                'tpr.message.fail.reason': '随机传送冷却中...',
                'tpr.message.success_1': '随机传送',
                'tpr.message.success_2': '玩家 {0} 正在随机传送, 可能会造成服务器卡顿...',

                'back.message.fail': '返回失败',
                'back.message.fail.reason': '你近期没有死亡记录...',
                'back.message.success': '返回成功...',

                'config_form.title': '重载配置文件',
                'config_form.content': '请选择操作...',
                'config_form.button.utp_config': '重载全局配置',
                'config_form.button.utp_toggle': '启用/关闭功能',

                'utp_config_form.title': '重载全局配置',
                'utp_config_form.textinput.placeholder': '请输入一个正整数...',
                'utp_config_form.textinput_1.label': '当前允许玩家拥有的最大家园传送点数量',
                'utp_config_form.textinput_2.label': '当前随机传送的最大范围',
                'utp_config_form.textinput_3.label': '当前随机传送的冷却时间',
                'utp_config_form.textinput_4.label': '当前随机传送的保护时间',
                'utp_config_form.textinput_5.label': '当前返回上一死亡点的有效时间',
                'utp_config_form.submit_button': '重载',
                'utp_config.message.success': '重载全局配置成功...',

                'utp_toggle_form.title': '启用/关闭功能',
                'utp_toggle_form.toggle_1.label': '允许家园传送点',
                'utp_toggle_form.toggle_2.label': '允许地标传送点',
                'utp_toggle_form.toggle_3.label': '允许玩家互传',
                'utp_toggle_form.toggle_4.label': '允许随机传送',
                'utp_toggle_form.toggle_5.label': '允许返回上一死亡点',
                'utp_toggle_form.submit_button': '重载',
                'utp_toggle.message.success': '重载功能启用状态成功...',

            }
            with open(lang_zh_CN_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(zh_CN, indent=4, ensure_ascii=False)
                f.write(json_str)

        if not os.path.exists(lang_en_US_data_file_path):
            en_US = {
                'open_main_form.message.fail': 'All functions of UTP have been disabled by operators...',
                'message.type_error': 'The form is parsed incorrectly, please follow the prompts to fill in correctly...',
                'back_to_main_form': 'Back to main form',
                'back_to_home_form': 'Back to home form',
                'back_to_warp_form': 'Back to warp form',
                'coordinates': 'Coordinates',
                'dimension': 'Dimension',

                'main_form.title': 'UTP - main form',
                'main_form.content': 'Please select a function...',
                'main_form.button.home': 'Home',
                'main_form.button.warp': 'Warp',
                'main_form.button.tpa_and_tpahere': 'TPA & TPAHere',
                'main_form.button.tp_setting': 'Personal TP setting',
                'main_form.button.tpr': 'TPR',
                'main_form.button.back': 'Back',
                'main_form.button.reload': 'Reload configurations',
                'main_form.button.close': 'Close',
                'main_form.button.back_to_zx_ui': 'Back to menu',

                'home_form.title': 'My homes',
                'home_form.content': 'Please select a function...',
                'home_form.button.addhome': 'Add a new home',
                'addhome_form.title': 'Add home',
                'addhome_form.textinput.label': 'Input the name of new home',
                'addhome_form.textinput.placeholder': 'Input any string, but cannot be blank...',
                'addhome_form.submit_button': 'Add',
                'addhome.message.fail': 'Failed to add home',
                'addhome.message.fail.reason_1': 'you already have a home named {0}...',
                'addhome.message.fail_reason_2': 'you have reached the max number of homes...',
                'addhome.message.success': 'Successfully add home...',
                'home_info_form.title': 'Home',
                'home_info_form.content': 'Please select a function...',
                'home_info_form.button.tp': 'Teleport',
                'home_info_form.button.edithome': 'Edit this home',
                'tphome.message.success': 'Successfully teleport...',
                'edithome_form.title': 'Edit home',
                'edithome_form.content': 'Please select a function...',
                'edithome_form.button.updatehome': 'Update this home',
                'edithome_form.button.deletehome': 'Delete this home',
                'updatehome_form.title': 'Update home',
                'updatehome_form.content': 'Please select a function...',
                'updatehome_form.button.renamehome': 'Rename this home',
                'updatehome_form.button.updatelocation': 'Update location',
                'renamehome_form.title': 'Rename home',
                'renamehome_form.textinput.label': 'Input new name of this home',
                'renamehome_form.textinput.placeholder': 'Input any string, but cannot be blank...',
                'renamehome_form.submit_button': 'Rename',
                'renamehome.message.fail': 'Failed to rename home',
                'renamehome.message.fail.reason': 'you already have a home named {0}...',
                'renamehome.message.success': 'Successfully rename home...',
                'home_updatelocation_form.title': 'Update location',
                'home_updatelocation_form.content': 'Are you sure to update location of this home?',
                'home_updatelocation_form.button.confirm': 'Confirm',
                'home_updatelocation.message.success': 'Successfully update location...',
                'deletehome_form.title': 'Delete home',
                'deletehome_form.content': 'Are you sure to delete this home?',
                'deletehome_form.button.confirm': 'Confirm',
                'deletehome.message.success': 'Successfully delete home...',

                'warp_form.title': 'Warps',
                'warp_form.content': 'Please select a function...',
                'warp_form.button.addwarp': 'Add a new warp',
                'addwarp_form.title': 'Add warp',
                'addwarp_form.textinput.label': 'Input the name of new warp',
                'addwarp_form.textinput.placeholder': 'Input any string, but cannot be blank...',
                'addwarp_form.submit_button': 'Add',
                'addwarp.message.fail': 'Failed to add warp',
                'addwarp.message.fail.reason': 'there is already a warp named {0}...',
                'addwarp.message.success': 'Successfully add warp...',
                'warp_info_form.title': 'Warp',
                'warp_info_form.content': 'Please select a function...',
                'warp_info_form.button.tp': 'Teleport',
                'warp_info_form.button.editwarp': 'Edit this warp',
                'tpwarp.message.success': 'Successfully teleport...',
                'editwarp_form.title': 'Edit warp',
                'editwarp_form.content': 'Please select a function...',
                'editwarp_form.button.updatewarp': 'Update this warp',
                'editwarp_form.button.deletewarp': 'Delete this warp',
                'updatewarp_form.title': 'Update warp',
                'updatewarp_form.content': 'Please select a function...',
                'updatewarp_form.button.renamewarp': 'Rename this warp',
                'updatewarp_form.button.updatelocation': 'Update location',
                'renamewarp_form.title': 'Rename warp',
                'renamewarp_form.textinput.label': 'Input new name of this warp',
                'renamewarp_form.textinput.placeholder': 'Input any string, but cannot be blank...',
                'renamewarp_form.submit_button': 'Rename',
                'renamewarp.message.fail': 'Failed to rename warp',
                'renamewarp.message.fail.reason': 'there is already a warp named {0}...',
                'renamewarp.message.success': 'Successfully rename warp...',
                'warp_updatelocation_form.title': 'Update location',
                'warp_updatelocation_form.content': 'Are you sure to update location of this warp?',
                'warp_updatelocation_form.button.confirm': 'Confirm',
                'warp_updatelocation.message.success': 'Successfully update location...',
                'deletewarp_form.title': 'Delete warp',
                'deletewarp_form.content': 'Are you sure to delete this warp?',
                'deletewarp_form.button.confirm': 'Confirm',
                'deletewarp.message.success': 'Successfully delete warp...',

                'tpa_and_tpahere_form.title': 'TPA & TPAHere',
                'tpa_and_tpahere_form.submit_button': 'Confirm',
                'tpa_and_tpahere_form.dropdown_1.label': 'Select a player',
                'tpa_and_tpahere_form.dropdown_2.label': 'Select a mode',
                'tpa_and_tpahere.message.fail': 'There are no players available for TPA or TPAHere...',
                'tpa_and_tpahere.message.fail.reason.offline': 'player {0} is offline...',

                'tpa_form.title': 'TPA request',
                'tpa_form.content': 'Player {0} send a TPA request to you...',
                'tpa_form.button.accept': 'Accept',
                'tpa_form.button.deny': 'Deny',
                'tpa.message.fail_1': 'Failed to send a TPA request',
                'tpa.message.fail_2': 'Failed to accept this TPA request',
                'tpa.message.success': 'Successfully send a TPA request',
                'tpa.message.deny': 'Player {0} denied your TPA request...',

                'tpahere_form.title': 'TPAHere request',
                'tpahere_form.content': 'Player {0} send a TPAHere request to you...',
                'tpahere_form.button.accept': 'Accept',
                'tpahere_form.button.deny': 'Deny',
                'tpahere.message.fail_1': 'Failed to send a TPAHere request',
                'tpahere.message.fail_2': 'Failed to accept this TPAHere request',
                'tpahere.message.success': 'Successfully send a TPAHere request',
                'tpahere.message.deny': 'Player {0} denied your TPAHere request...',

                'tpsetting_form.title': 'Personal TP setting',
                'tpsetting_form.toggle.lable': 'Allow other players to send TPA or TPAHere request to you',
                'tpsetting_form.submit_button': 'Update',
                'tpsetting.message.success': 'Successfully update personal TP setting...',

                'tpr.message.fail': 'Failed to random teleport',
                'tpr.message.fail.reason': 'this function is on cooldown...',
                'tpr.message.success_1': 'TPR',
                'tpr.message.success_2': 'player {0} is being teleport randomly, which may cause the server to lag...',

                'back.message.fail': 'Failed to back',
                'back.message.fail.reason': 'you do not have any recent death records...',
                'back.message.success': 'Successfully back...',

                'config_form.title': 'Reload configurations',
                'config_form.content': 'Please select a function...',
                'config_form.button.utp_config': 'Reload global configurations',
                'config_form.button.utp_toggle': 'Toggle on/off functions',

                'utp_config_form.title': 'Reload global configurations',
                'utp_config_form.textinput.placeholder': 'Input a positive integer...',
                'utp_config_form.textinput_1.label': 'The current max number of homes that players are allowed to have',
                'utp_config_form.textinput_2.label': 'The current max range of TPR',
                'utp_config_form.textinput_3.label': 'The current cooldown time of TPR',
                'utp_config_form.textinput_4.label': 'The current protection time of TPR',
                'utp_config_form.textinput_5.label': 'The current valid time of Back',
                'utp_config_form.submit_button': 'Reload',
                'utp_config.message.success': 'Successfully reload global configurations...',

                'utp_toggle_form.title': 'Toggle on/off functions',
                'utp_toggle_form.toggle_1.label': 'Allow Home',
                'utp_toggle_form.toggle_2.label': 'Allow Warp',
                'utp_toggle_form.toggle_3.label': 'Allow TPA & TPAHere',
                'utp_toggle_form.toggle_4.label': 'Allow TPR',
                'utp_toggle_form.toggle_5.label': 'Allow Back',
                'utp_toggle_form.submit_button': 'Reload',
                'utp_toggle.message.success': 'Successfully reload the enabling status of functions...',


            }
            with open(lang_en_US_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(en_US, indent=4, ensure_ascii=False)
                f.write(json_str)

        lang_data = {}
        lang_list = os.listdir(lang_dir)
        for lang in lang_list:
            lang_name = lang.strip('.json')
            lang_data_file_path = os.path.join(lang_dir, lang)
            with open(lang_data_file_path, 'r', encoding='utf-8') as f:
                lang_data[lang_name] = json.loads(f.read())

        return lang_data