import os
import json
import time

from endstone import Player, ColorFormat
from endstone.plugin import Plugin
from endstone.level import Location
from endstone.event import event_handler, PlayerJoinEvent, PlayerDeathEvent
from endstone.command import Command, CommandSender, CommandSenderWrapper
from endstone.form import ActionForm, ModalForm, Dropdown, TextInput

current_dir = os.getcwd()
first_dir = os.path.join(current_dir, 'plugins', 'utp')
if not os.path.exists(first_dir):
    os.mkdir(first_dir)
home_data_file_path = os.path.join(first_dir, 'home.json')
warp_data_file_path = os.path.join(first_dir, 'warp.json')
config_data_file_path = os.path.join(first_dir, 'config.json')
menu_file_path = os.path.join('plugins', 'zx_ui')

class utp(Plugin):
    api_version = '0.5'

    def on_enable(self):
        # 加载 home 数据
        if not os.path.exists(home_data_file_path):
            home_data = {}
            with open(home_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(home_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(home_data_file_path, 'r', encoding='utf-8') as f:
                home_data = json.loads(f.read())
        self.home_data = home_data
        # 加载 warp 数据
        if not os.path.exists(warp_data_file_path):
            warp_data = {}
            with open(warp_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(warp_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(warp_data_file_path, 'r', encoding='utf-8') as f:
                warp_data = json.loads(f.read())
        self.warp_data = warp_data
        # 加载 config 数据
        if not os.path.exists(config_data_file_path):
            config_data = {
                'max_home_per_player': 5,
                'tpr_range': 2000,
                'tpr_cool_down': 60,
                'tpr_protect_time': 20,
                'back_to_death_point_cool_down': 30
            }
            with open(config_data_file_path, 'w', encoding='utf-8') as f:
                json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(config_data_file_path, 'r', encoding='utf-8') as f:
                config_data = json.loads(f.read())
        self.config_data = config_data
        self.sender_wrapper = CommandSenderWrapper(
            self.server.command_sender,
            on_message=None
        )
        self.record_tpr = {}
        self.record_death = {}
        self.register_events(self)
        self.logger.info(f'{ColorFormat.YELLOW}UTP 已加载...')

    commands = {
        'utp': {
            'description': '打开传送合集表单',
            'usages': ['/utp'],
            'permissions': ['utp.command.utp']
        }
    }

    permissions = {
        'utp.command.utp': {
            'description': '打开传送合集表单',
            'default': True
        }
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]):
        if command.name == 'utp':
            if not isinstance(sender, Player):
                sender.send_message(f'{ColorFormat.RED}该命令只能由玩家执行...')
                return
            player = sender
            main_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}传送合集主表单',
                content=f'{ColorFormat.GREEN}请选择操作...',
            )
            main_form.add_button(f'{ColorFormat.YELLOW}我的传送点', icon='textures/items/ender_pearl', on_click=self.home)
            main_form.add_button(f'{ColorFormat.YELLOW}地标传送点', icon='textures/ui/worldsIcon', on_click=self.warp)
            main_form.add_button(f'{ColorFormat.YELLOW}玩家互传', icon='textures/ui/dressing_room_customization', on_click=self.tpa_and_tpahere)
            main_form.add_button(f'{ColorFormat.YELLOW}玩家互传设置', icon='textures/ui/', on_click=None)
            main_form.add_button(f'{ColorFormat.YELLOW}随机传送', icon='textures/ui/icon_random', on_click=self.tpr)
            main_form.add_button(f'{ColorFormat.YELLOW}返回上一死亡点', icon='textures/ui/friend_glyph_desaturated', on_click=self.back_to_last_death_point)
            if player.is_op == True:
                main_form.add_button(f'{ColorFormat.YELLOW}重载配置文件', icon='textures/ui/icon_setting', on_click=self.reload_config_data)
            if not os.path.exists(menu_file_path):
                main_form.on_close = None
                main_form.add_button(f'{ColorFormat.YELLOW}关闭', icon='textures/ui/cancel', on_click=None)
            else:
                main_form.on_close = self.back_to_menu
                main_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.back_to_menu)
            player.send_form(main_form)

    # home 主表单
    def home(self, player: Player):
        home_form = ActionForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}我的传送点',
            content=f'{ColorFormat.GREEN}请选择操作...',
            on_close=self.back_to_main_form
        )
        home_form.add_button(f'{ColorFormat.YELLOW}添加脚下坐标为传送点', icon='textures/ui/color_plus', on_click=self.add_home)
        for key, value in self.home_data[player.name].items():
            home_name = key
            home_info = value
            home_loc = home_info['loc']
            home_dim = home_info['dim']
            home_form.add_button(f'{ColorFormat.WHITE}{home_name}\n'
                                 f'{ColorFormat.YELLOW}[维度]： {home_dim}', icon='textures/items/ender_eye', on_click=self.home_info(home_name, home_loc, home_dim))
        home_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.back_to_main_form)
        player.send_form(home_form)

    # 添加脚下坐标为传送点
    def add_home(self, player: Player):
        home_player_already_has = [key for key in self.home_data[player.name].keys()]
        if len(home_player_already_has) >= self.config_data['max_home_per_player']:
            player.send_message(f'{ColorFormat.RED}添加传送点失败： {ColorFormat.WHITE}你拥有的传送点数量已达上限...')
            return
        loc = [int(player.location.x), int(player.location.y), int(player.location.z)]
        dim = player.dimension.name
        textinput = TextInput(
            label=f'{ColorFormat.GREEN}[坐标]： {ColorFormat.WHITE}({loc[0]}, {loc[1]}, {loc[2]})\n'
                  f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{dim}\n\n'
                  f'{ColorFormat.GREEN}输入传送点名称...',
            placeholder='请输入任意字符串, 但不能留空...'
        )
        add_home_form = ModalForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}添加传送点',
            controls=[textinput],
            on_close=self.home,
            submit_button=f'{ColorFormat.YELLOW}添加'
        )
        def on_submit(player: Player, json_str):
            data = json.loads(json_str)
            if len(data[0]) == 0:
                player.send_message(f'{ColorFormat.RED}表单解析错误, 请按提示正确填写...')
                return
            if data[0] in home_player_already_has:
                player.send_message(f'{ColorFormat.RED}添加传送点失败： {ColorFormat.WHITE}'
                                    f'你已经有一个名为 {data[0]} 的传送点...')
                return
            home_name = data[0]
            self.home_data[player.name][home_name] = {
                'loc': loc,
                'dim': dim
            }
            self.save_home_data()
            player.send_message(f'{ColorFormat.YELLOW}添加传送点成功...')
        add_home_form.on_submit = on_submit
        player.send_form(add_home_form)

    # 单个 home 详细信息
    def home_info(self, home_name, home_loc, home_dim):
        def on_click(player: Player):
            home_info_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}传送点： {home_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.home
            )
            home_info_form.add_button(f'{ColorFormat.YELLOW}传送', icon='textures/ui/realmsIcon', on_click=self.home_tp(home_loc, home_dim))
            home_info_form.add_button(f'{ColorFormat.YELLOW}编辑传送点', icon='textures/ui/hammer_l', on_click=self.home_edit(home_name, home_loc, home_dim))
            home_info_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.home)
            player.send_form(home_info_form)
        return on_click

    # home 编辑
    def home_edit(self, home_name, home_loc, home_dim):
        def on_click(player: Player):
            home_edit_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}编辑传送点： {home_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.home
            )
            home_edit_form.add_button(f'{ColorFormat.YELLOW}更新传送点', icon='textures/ui/refresh', on_click=self.home_update(home_name, home_loc, home_dim))
            home_edit_form.add_button(f'{ColorFormat.YELLOW}删除传送点', icon='textures/ui/cancel', on_click=self.home_delte(home_name, home_loc, home_dim))
            home_edit_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.home)
            player.send_form(home_edit_form)
        return on_click

    # home 更新
    def home_update(self, home_name, home_loc, home_dim):
        def on_click(player: Player):
            home_update_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}更新传送点： {home_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.home,
            )
            home_update_form.add_button(f'{ColorFormat.YELLOW}重命名传送点', icon='textures/ui/icon_book_writable', on_click=self.home_update_name(home_name))
            home_update_form.add_button(f'{ColorFormat.YELLOW}更新传送点坐标', icon='textures/ui/realmsIcon', on_click=self.home_update_tp(home_name))
            home_update_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.home)
            player.send_form(home_update_form)
        return on_click

    # home 重命名
    def home_update_name(self, home_name):
        def on_click(player: Player):
            textinput = TextInput(
                label=f'{ColorFormat.GREEN}输入新的传送点名...\n'
                      f'留空则保留原传送点名',
                placeholder='请输入任意字符串或留空'
            )
            home_update_name_form = ModalForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}重命名传送点： {home_name}',
                controls=[textinput],
                submit_button=f'{ColorFormat.YELLOW}更新',
                on_close=self.home
            )
            def on_submit(player: Player, json_str):
                data = json.loads(json_str)
                if len(data[0]) == 0:
                    new_home_name = home_name
                else:
                    new_home_name = data[0]
                    home_player_already_has = [key for key in self.home_data[player.name].keys()]
                    if new_home_name in home_player_already_has:
                        player.send_message(f'{ColorFormat.RED}重命名传送点失败： {ColorFormat.WHITE}'
                                            f'你已经有一个名为 {new_home_name} 的传送点...')
                        return
                self.home_data[player.name][new_home_name] = self.home_data[player.name][home_name]
                if new_home_name != home_name:
                    self.home_data[player.name].pop(home_name)
                self.save_home_data()
                player.send_message(f'{ColorFormat.YELLOW}重命名传送点成功...')
            home_update_name_form.on_submit = on_submit
            player.send_form(home_update_name_form)
        return on_click

    # home 更新传送坐标和维度
    def home_update_tp(self, home_name):
        def on_click(player: Player):
            new_home_loc = [int(player.location.x), int(player.location.y), int(player.location.z)]
            new_home_dim = player.dimension.name
            confirm_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}更新传送点坐标： {home_name}',
                content=f'{ColorFormat.GREEN}你确定要将传送点坐标和维度更新为如下吗？\n'
                        f'[坐标]： {ColorFormat.WHITE}({new_home_loc[0]}, {new_home_loc[1]}, {new_home_loc[2]})\n'
                        f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{new_home_dim}',
                on_close=self.home
            )
            confirm_form.add_button(f'{ColorFormat.YELLOW}确认', icon='textures/ui/realms_slot_check', on_click=self.on_confirm(home_name, new_home_loc, new_home_dim))
            confirm_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.home)
            player.send_form(confirm_form)
        return on_click

    def on_confirm(self, home_name, new_home_loc, new_home_dim):
        def on_click(player: Player):
            self.home_data[player.name][home_name]['loc'] = new_home_loc
            self.home_data[player.name][home_name]['dim'] = new_home_dim
            self.save_home_data()
            player.send_message(f'{ColorFormat.YELLOW}更新传送点坐标成功...')
        return on_click

    # home 删除
    def home_delte(self, home_name, home_loc, home_dim):
        def on_click(player: Player):
             confirm_form = ActionForm(
                 title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}删除传送点： {home_name}',
                 content=f'{ColorFormat.GREEN}你确定要删除该传送点吗？\n'
                         f'[坐标]： {ColorFormat.WHITE}({home_loc[0]}, {home_loc[1]}, {home_loc[2]})\n'
                         f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{home_dim}',
                 on_close=self.home
             )
             confirm_form.add_button(f'{ColorFormat.YELLOW}确认', icon='textures/ui/realms_slot_check', on_click=self.on_confirm_two(home_name))
             confirm_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.home)
             player.send_form(confirm_form)
        return on_click

    def on_confirm_two(self, home_name):
        def on_click(player: Player):
            self.home_data[player.name].pop(home_name)
            self.save_home_data()
            player.send_message(f'{ColorFormat.YELLOW}删除传送点成功...')
        return on_click

    # home 传送点传送
    def home_tp(self, home_loc, home_dim):
        def on_click(player: Player):
            if home_dim == 'Overworld':
                target_dim = self.server.level.get_dimension('OVERWORLD')
            elif home_dim == 'Nether':
                target_dim = self.server.level.get_dimension('NETHER')
            else:
                target_dim = self.server.level.get_dimension('THEEND')
            target_loc = Location(
                target_dim,
                x=float(home_loc[0]),
                y=float(home_loc[1]),
                z=float(home_loc[2])
            )
            player.teleport(target_loc)
            player.send_message(f'{ColorFormat.YELLOW}传送成功...')
        return on_click

    # 保存 home.json 数据
    def save_home_data(self):
        with open(home_data_file_path, 'w+', encoding='utf-8') as f:
            json_str = json.dumps(self.home_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    # warp 主表单
    def warp(self, player: Player):
        warp_form = ActionForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}地标传送点',
            content=f'{ColorFormat.GREEN}请选择操作...',
            on_close=self.back_to_main_form
        )
        if player.is_op == True:
            warp_form.add_button(f'{ColorFormat.YELLOW}添加脚下坐标为地标传送点', icon='textures/ui/color_plus', on_click=self.add_warp)
        for key, value in self.warp_data.items():
            warp_name = key
            warp_info = value
            warp_loc = warp_info['loc']
            warp_dim = warp_info['dim']
            warp_form.add_button(f'{warp_name}\n{ColorFormat.YELLOW}[维度]： {warp_dim}', icon='textures/items/ender_eye', on_click=self.warp_info(warp_name, warp_loc, warp_dim))
        warp_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.back_to_main_form)
        player.send_form(warp_form)

    # 将脚下坐标添加为新的 warp
    def add_warp(self, player: Player):
        warp_loc = [int(player.location.x), int(player.location.y), int(player.location.z)]
        warp_dim = player.dimension.name
        textinput = TextInput(
            label=f'{ColorFormat.GREEN}[坐标]： {ColorFormat.WHITE}({warp_loc[0]}, {warp_loc[1]}, {warp_loc[2]})\n'
                  f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{warp_dim}\n\n'
                  f'{ColorFormat.GREEN}输入地标传送点名称...',
            placeholder='请输入任意字符串, 但不能留空...'
        )
        add_warp_form = ModalForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}添加地标传送点',
            controls=[textinput],
            on_close=self.warp,
            submit_button=f'{ColorFormat.YELLOW}添加'
        )
        def on_submit(player: Player, json_str):
            data = json.loads(json_str)
            if len(data[0]) == 0:
                player.send_message(f'{ColorFormat.RED}表单解析错误, 请按提示正确填写...')
                return
            warp_already_exist = [key for key in self.warp_data.keys()]
            if data[0] in warp_already_exist:
                player.send_message(f'{ColorFormat.RED}添加地标传送点失败： {ColorFormat.WHITE}'
                                    f'你已经有一个名为 {data[0]} 的地标传送点...')
                return
            warp_name = data[0]
            self.warp_data[warp_name] = {
                'loc': warp_loc,
                'dim': warp_dim
            }
            self.save_warp_data()
            player.send_message(f'{ColorFormat.YELLOW}添加地标传送点成功...')
        add_warp_form.on_submit = on_submit
        player.send_form(add_warp_form)

    # 单个 warp 详细信息
    def warp_info(self, warp_name, warp_loc, warp_dim):
        def on_click(player: Player):
            warp_info_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}地标传送点： {warp_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.warp
            )
            warp_info_form.add_button(f'{ColorFormat.YELLOW}传送', icon='textures/ui/realmsIcon', on_click=self.warp_tp(warp_loc, warp_dim))
            if player.is_op == True:
                warp_info_form.add_button(f'{ColorFormat.YELLOW}编辑地标传送点', icon='textures/ui/hammer_l', on_click=self.warp_edit(warp_name, warp_loc, warp_dim))
            warp_info_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.warp)
            player.send_form(warp_info_form)
        return on_click

    # warp 传送
    def warp_tp(self, warp_loc, warp_dim):
        def on_click(player: Player):
            if warp_dim == 'Overworld':
                target_dim = self.server.level.get_dimension('OVERWORLD')
            elif warp_dim == 'Nether':
                target_dim = self.server.level.get_dimension('NETHER')
            else:
                target_dim = self.server.level.get_dimension('THEEND')
            target_loc = Location(
                target_dim,
                x=float(warp_loc[0]),
                y=float(warp_loc[1]),
                z=float(warp_loc[2])
            )
            player.teleport(target_loc)
            player.send_message(f'{ColorFormat.YELLOW}传送成功...')
        return on_click

    # warp 编辑
    def warp_edit(self, warp_name, warp_loc, warp_dim):
        def on_click(player: Player):
            warp_edit_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}编辑地标传送点： {warp_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.warp
            )
            warp_edit_form.add_button(f'{ColorFormat.YELLOW}更新地标传送点', icon='textures/ui/refresh', on_click=self.warp_update(warp_name, warp_loc, warp_dim))
            warp_edit_form.add_button(f'{ColorFormat.YELLOW}删除地标传送点', icon='textures/ui/cancel', on_click=self.warp_delete(warp_name, warp_loc, warp_dim))
            warp_edit_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.warp)
            player.send_form(warp_edit_form)
        return on_click

    # warp 更新
    def warp_update(self, warp_name, warp_loc, warp_dim):
        def on_click(player: Player):
            warp_update_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}更新地标传送点： {warp_name}',
                content=f'{ColorFormat.GREEN}请选择操作...',
                on_close=self.warp
            )
            warp_update_form.add_button(f'{ColorFormat.YELLOW}重命名地标传送点', icon='textures/ui/icon_book_writable', on_click=self.warp_update_name(warp_name))
            warp_update_form.add_button(f'{ColorFormat.YELLOW}更新地标传送点坐标', icon='textures/ui/realmsIcon', on_click=self.warp_update_tp(warp_name))
            warp_update_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.warp)
            player.send_form(warp_update_form)
        return on_click

    # warp 重命名
    def warp_update_name(self, warp_name):
        def on_click(player: Player):
            textinput = TextInput(
                label=f'{ColorFormat.GREEN}输入新的地标传送点名...\n'
                      f'留空则保留原地标传送点名',
                placeholder='请输入任意字符串或留空'
            )
            warp_update_name = ModalForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}重命名地标传送点： {warp_name}',
                controls=[textinput],
                on_close=self.warp,
                submit_button=f'{ColorFormat.YELLOW}更新'
            )
            def on_submit(player: Player, json_str):
                data = json.loads(json_str)
                if len(data[0]) == 0:
                    new_warp_name = warp_name
                else:
                    new_warp_name = data[0]
                    warp_already_exist = [key for key in self.warp_data.keys()]
                    if new_warp_name in warp_already_exist:
                        player.send_message(f'{ColorFormat.RED}重命名地标传送点失败： {ColorFormat.WHITE}'
                                            f'你已经有一个名为 {new_warp_name} 的地标传送点...')
                        return
                self.warp_data[new_warp_name] = self.warp_data[warp_name]
                if new_warp_name != warp_name:
                    self.warp_data.pop(warp_name)
                self.save_warp_data()
                player.send_message(f'{ColorFormat.YELLOW}重命名地标传送点成功...')
            warp_update_name.on_submit = on_submit
            player.send_form(warp_update_name)
        return on_click

    # warp 更新传送坐标和维度
    def warp_update_tp(self, warp_name):
        def on_click(player: Player):
            new_warp_loc = [int(player.location.x), int(player.location.y), int(player.location.z)]
            new_warp_dim = player.dimension.name
            confirm_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}更新地标传送点坐标： {warp_name}',
                content=f'{ColorFormat.GREEN}你确定要将地标传送点坐标和维度更新为如下吗？\n'
                        f'[坐标]： {ColorFormat.WHITE}({new_warp_loc[0]}, {new_warp_loc[1]}, {new_warp_loc[2]})\n'
                        f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{new_warp_dim}',
                on_close=self.warp
            )
            confirm_form.add_button(f'{ColorFormat.YELLOW}确认', icon='textures/ui/realms_slot_check',
                                    on_click=self.on_confirm_four(warp_name, new_warp_loc, new_warp_dim))
            confirm_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.warp)
            player.send_form(confirm_form)
        return on_click
    
    def on_confirm_four(self, warp_name, new_warp_loc, new_warp_dim):
        def on_click(player: Player):
            self.warp_data[warp_name]['loc'] = new_warp_loc
            self.warp_data[warp_name]['dim'] = new_warp_dim
            self.save_warp_data()
            player.send_message(f'{ColorFormat.YELLOW}更新地标传送点成功...')
        return on_click

    # warp 删除
    def warp_delete(self, warp_name, warp_loc, warp_dim):
        def on_click(player: Player):
             confirm_form = ActionForm(
                 title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}删除地标传送点： {warp_name}',
                 content=f'{ColorFormat.GREEN}你确定要删除该地标传送点吗？\n'
                         f'[坐标]： {ColorFormat.WHITE}({warp_loc[0]}, {warp_loc[1]}, {warp_loc[2]})\n'
                         f'{ColorFormat.GREEN}[维度]： {ColorFormat.WHITE}{warp_dim}',
                 on_close=self.warp
             )
             confirm_form.add_button(f'{ColorFormat.YELLOW}确认', icon='textures/ui/realms_slot_check', on_click=self.on_confirm_three(warp_name))
             confirm_form.add_button(f'{ColorFormat.YELLOW}返回', icon='textures/ui/refresh_light', on_click=self.warp)
             player.send_form(confirm_form)
        return on_click

    def on_confirm_three(self, warp_name):
        def on_click(player: Player):
            self.warp_data.pop(warp_name)
            self.save_warp_data()
            player.send_message(f'{ColorFormat.YELLOW}删除地标传送点成功...')
        return on_click

    # 保存 warp 数据
    def save_warp_data(self):
        with open(warp_data_file_path, 'w+', encoding='utf-8') as f:
            json_str = json.dumps(self.warp_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    # tpa & tpahere
    def tpa_and_tpahere(self, player: Player):
        online_player_list = [online_player.name for online_player in self.server.online_players if online_player.name != player.name]
        if len(online_player_list) == 0:
            player.send_message(f'{ColorFormat.RED}当前没有其他玩家在线...')
            return
        dropdown1 = Dropdown(
            label=f'{ColorFormat.GREEN}选择玩家...',
            options=online_player_list
        )
        mode_list = ['tpa', 'tpahere']
        dropdown2 = Dropdown(
            label=f'{ColorFormat.GREEN}选择模式...',
            options=mode_list
        )
        tpa_and_tpahere_form = ModalForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}玩家互传',
            controls=[dropdown1, dropdown2],
            on_close=self.back_to_main_form,
            submit_button=f'{ColorFormat.YELLOW}确认'
        )
        def on_submit(player: Player, json_str):
            data = json.loads(json_str)
            request_player_name = player.name
            target_player_name = online_player_list[data[0]]
            mode = mode_list[data[1]]
            if mode == 'tpa':
                if not self.server.get_player(target_player_name):
                    player.send_message(f'{ColorFormat.RED}发送请求失败： {ColorFormat.WHITE}{target_player_name} 已离线...')
                    return
                else:
                    target_player = self.server.get_player(target_player_name)
                    tpa_form = ActionForm(
                        title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}TPA 请求',
                        content=f'{ColorFormat.GREEN}玩家 {player.name} 向你发送了一个 TPA 请求...',
                        on_close=self.tpa_denny(request_player_name)
                    )
                    tpa_form.add_button(f'{ColorFormat.YELLOW}接受', icon='textures/ui/realms_slot_check', on_click=self.tpa_accept(request_player_name))
                    tpa_form.add_button(f'{ColorFormat.YELLOW}拒绝', icon='textures/ui/cancel', on_click=self.tpa_denny(request_player_name))
                    target_player.send_form(tpa_form)
            else:
                if not self.server.get_player(target_player_name):
                    player.send_message(f'{ColorFormat.RED}发送请求失败： {ColorFormat.WHITE}{target_player_name} 已离线...')
                    return
                else:
                    target_player = self.server.get_player(target_player_name)
                    tpahere_form = ActionForm(
                        title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}TPAHere 请求',
                        content=f'{ColorFormat.GREEN}玩家 {player.name} 向你发送了一个 TPAHere 请求...',
                        on_close=self.tpahere_denny(request_player_name)
                    )
                    tpahere_form.add_button(f'{ColorFormat.YELLOW}接受', icon='textures/ui/realms_slot_check', on_click=self.tpahere_accept(request_player_name))
                    tpahere_form.add_button(f'{ColorFormat.YELLOW}拒绝', icon='textures/ui/cancel', on_click=self.tpahere_denny(request_player_name))
                    target_player.send_form(tpahere_form)
        tpa_and_tpahere_form.on_submit = on_submit
        player.send_form(tpa_and_tpahere_form)

    def tpa_accept(self, request_player_name):
        def on_click(target_player: Player):
            if not self.server.get_player(request_player_name):
                target_player.send_message(f'{ColorFormat.RED}接受请求失败： {ColorFormat.WHITE}{request_player_name} 已离线...')
                return
            else:
                request_player = self.server.get_player(request_player_name)
                request_player.teleport(target_player)
        return on_click

    def tpa_denny(self, request_player_name):
        def on_click(target_player: Player):
            if not self.server.get_player(request_player_name):
                return None
            else:
                request_player = self.server.get_player(request_player_name)
                request_player.send_message(f'{ColorFormat.RED}玩家 {target_player.name} 拒绝了你的 TPA 请求...')
                return None
        return on_click

    def tpahere_accept(self, request_player_name):
        def on_click(target_player: Player):
            if not self.server.get_player(request_player_name):
                target_player.send_message(f'{ColorFormat.RED}接受请求失败： {ColorFormat.WHITE}{request_player_name} 已离线...')
                return
            else:
                request_player = self.server.get_player(request_player_name)
                target_player.teleport(request_player)
        return on_click

    def tpahere_denny(self, request_player_name):
        def on_click(target_player: Player):
            if not self.server.get_player(request_player_name):
                return None
            else:
                request_player = self.server.get_player(request_player_name)
                request_player.send_message(f'{ColorFormat.RED}玩家 {target_player.name} 拒绝了你的 TPAHere 请求...')
                return None
        return on_click

    # tpr 随机传送
    def tpr(self, player: Player):
        if not self.record_tpr.get(player.name):
            pass
        else:
            request_time = time.time()
            if int(request_time - self.record_tpr[player.name]) <= self.config_data['tpr_cool_down']:
                player.send_message(f'{ColorFormat.RED}随机传送失败： {ColorFormat.WHITE}冷却时间未到...')
                return
        player_pos = [int(player.location.x), int(player.location.z)]
        if player.name.find(' ') != -1:
            player_name = f'"{player.name}"'
        else:
            player_name = player.name
        request_time = time.time()
        self.server.dispatch_command(self.sender_wrapper,
                                     f'spreadplayers {player_pos[0]} {player_pos[1]} 0 '
                                     f'{self.config_data['tpr_range']} {player_name}')
        self.server.dispatch_command(self.sender_wrapper,
                                     f'effect {player_name} resistance {self.config_data['tpr_protect_time']} 255 true')
        self.record_tpr[player.name] = request_time
        self.server.broadcast_message(f'{ColorFormat.YELLOW}[随机传送]： {ColorFormat.WHITE}'
                                      f'玩家 {player.name} 正在执行随机传送, 可能会造成卡顿...')

    # 监听玩家死亡事件
    @event_handler
    def on_player_death(self, event: PlayerDeathEvent):
        player_death_time = time.time()
        player_death_loc = [int(event.player.location.x), int(event.player.location.y), int(event.player.location.z)]
        player_death_dim = event.player.dimension.name
        self.record_death[event.player.name] = {
            'death_time': player_death_time,
            'death_loc': player_death_loc,
            'death_dim': player_death_dim
        }

    # back 返回上一死亡点
    def back_to_last_death_point(self, player: Player):
        if not self.record_death.get(player.name):
            player.send_message(f'{ColorFormat.RED}返回失败, 你短时间内没有死亡记录...')
            return
        else:
            request_time = time.time()
            if int(request_time - self.record_death[player.name]['death_time']) <= self.config_data['back_to_death_point_cool_down']:
                if self.record_death[player.name]['death_dim'] == 'Overworld':
                    target_dim = self.server.level.get_dimension('OVERWORLD')
                elif self.record_death[player.name]['death_dim'] == 'Nether':
                    target_dim = self.server.level.get_dimension('NETHER')
                else:
                    target_dim = self.server.level.get_dimension('THEEND')
                death_loc = self.record_death[player.name]['death_loc']
                target_loc = Location(
                    target_dim,
                    x=float(death_loc[0]),
                    y=float(death_loc[1]),
                    z=float(death_loc[2])
                )
                player.teleport(target_loc)
                self.record_death.pop(player.name)
                player.send_message(f'{ColorFormat.YELLOW}返回成功...')
            else:
                self.record_death.pop(player.name)
                player.send_message(f'{ColorFormat.RED}返回失败, 你短时间内没有死亡记录...')
                return

    # 重载配置文件
    def reload_config_data(self, player: Player):
        textinput1 = TextInput(
            label=f'{ColorFormat.GREEN}当前允许玩家拥有私人传送点个数： '
                  f'{ColorFormat.WHITE}{self.config_data['max_home_per_player']}\n'
                  f'{ColorFormat.GREEN}输入新的私人传送点个数（留空则保留原配置）...',
            placeholder='请输入一个正整数, 例如： 5'
        )
        textinput2 = TextInput(
            label=f'{ColorFormat.GREEN}当前随机传送范围： '
                  f'{ColorFormat.WHITE}{self.config_data['tpr_range']}\n'
                  f'{ColorFormat.GREEN}输入新的随机传送范围（留空则保留原配置）...',
            placeholder='请输入一个正整数, 例如： 2000'
        )
        textinput3 = TextInput(
            label=f'{ColorFormat.GREEN}当前随机传送冷却时间： '
                  f'{ColorFormat.WHITE}{self.config_data['tpr_cool_down']}\n'
                  f'{ColorFormat.GREEN}输入新的随机传送冷却时间（留空则保留原配置）...',
            placeholder='请输入一个正整数, 例如： 60'
        )
        textinput4 = TextInput(
            label=f'{ColorFormat.GREEN}当前随机传送无敌时间： '
                  f'{ColorFormat.WHITE}{self.config_data['tpr_protect_time']}\n'
                  f'{ColorFormat.GREEN}输入新的随机传送无敌时间（留空则保留原配置）...',
            placeholder='请输入一个正整数, 例如： 20'
        )
        textinput5 = TextInput(
            label=f'{ColorFormat.GREEN}当前返回上一死亡点冷却时间： '
                  f'{ColorFormat.WHITE}{self.config_data['back_to_death_point_cool_down']}\n'
                  f'{ColorFormat.GREEN}输入新的返回上一死亡点冷却时间（留空则保留原配置）...',
            placeholder='请输入一个正整数, 例如： 30'
        )
        reload_config_data_form = ModalForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}重载配置文件',
            controls=[textinput1, textinput2, textinput3, textinput4, textinput5],
            on_close=self.back_to_main_form,
            submit_button=f'{ColorFormat.YELLOW}重载'
        )
        def on_submit(player: Player, json_str):
            data = json.loads(json_str)
            try:
                if len(data[0]) == 0:
                    new_max_home_per_player = self.config_data['max_home_per_player']
                else:
                    new_max_home_per_player = int(data[0])
                if len(data[1]) == 0:
                    new_tpr_range = self.config_data['tpr_range']
                else:
                    new_tpr_range = int(data[1])
                if len(data[2]) == 0:
                    new_tpr_cool_down = self.config_data['tpr_cool_down']
                else:
                    new_tpr_cool_down = int(data[2])
                if len(data[3]) == 0:
                    new_tpr_protect_time = self.config_data['tpr_protect_time']
                else:
                    new_tpr_protect_time = int(data[3])
                if len(data[4]) == 0:
                    new_back_to_death_point_cool_down = self.config_data['back_to_death_point_cool_down']
                else:
                    new_back_to_death_point_cool_down = int(data[4])
            except:
                player.send_message(f'{ColorFormat.RED}表单解析错误, 请按提示正确填写...')
                return
            if (new_max_home_per_player <= 0 or new_tpr_range <=0 or new_tpr_cool_down <=0
                    or new_tpr_protect_time <= 0 or new_back_to_death_point_cool_down <= 0):
                player.send_message(f'{ColorFormat.RED}表单解析错误, 请按提示正确填写...')
                return
            self.config_data['max_home_per_player'] = new_max_home_per_player
            self.config_data['tpr_range'] = new_tpr_range
            self.config_data['tpr_cool_down'] = new_tpr_cool_down
            self.config_data['tpr_protect_time'] = new_tpr_protect_time
            self.config_data['back_to_death_point_cool_down'] = new_back_to_death_point_cool_down
            self.save_config_data()
            player.send_message(f'{ColorFormat.YELLOW}重载配置文件成功...')
        reload_config_data_form.on_submit = on_submit
        player.send_form(reload_config_data_form)

    def save_config_data(self):
        with open(config_data_file_path, 'w+', encoding='utf-8') as f:
            json_str = json.dumps(self.config_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    def back_to_menu(self, player: Player):
        player.perform_command('cd')

    def back_to_main_form(self, player: Player):
        player.perform_command('utp')

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if not self.home_data.get(event.player.name):
            self.home_data[event.player.name] = {}
            self.save_home_data()