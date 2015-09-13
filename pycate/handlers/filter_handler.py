# -*- coding:utf-8 -*-
'''
会员后台管理
'''

from pycate.model.shoucang_model import MShoucang
import core.base_handler as base_handler


class FilterHandler(base_handler.PycateBaseHandler):
    def initialize(self, hinfo=''):
        self.init_condition()
        self.mshoucang = MShoucang()
        self.userinfo = self.muser_info.get_by_username()
        self.userop = self.muser_num.get_by_username()

    def get(self, input=''):
        if len(input) > 0:
            par_arr = input.split('/')
        if self.user_name is None or self.user_name == '':
            self.redirect('/member/login')
        if input == '':
            self.set_status(400)
            self.render('404.html')
        elif len(par_arr) > 0:
            self.listcity(par_arr)
        else:
            self.set_status(400)
            self.render('404.html')


    def get_condition(self, switch):
        '''
        用于listcity()，获取列出的条件。
        '''
        if switch == 'all':
            condition = {'userid': self.user_name}
        elif switch == 'notrefresh':
            # 过期
            condition = {'userid': self.user_name, 'def_refresh': 0, 'def_banned': 0, 'def_valid': 1}
        elif switch == 'normal':
            # 正常发布的
            condition = {'userid': self.user_name, 'def_refresh': 1, 'def_banned': 0, 'def_valid': 1}
        elif switch == 'banned':
            # 过期
            condition = {'userid': self.user_name, 'def_banned': 1}
        elif switch == 'novalid':
            # 未审核信息
            condition = {'userid': self.user_name, 'def_banned': 0, 'def_valid': 0}
        elif switch == 'tuiguang':
            condition = {"catid": {"$in": self.muser_info.get_vip_cats()}, 'userid': self.user_name}
        elif switch == 'notg':
            condition = {"catid": {"$in": self.muser_info.get_vip_cats()}, 'userid': self.user_name, 'def_tuiguang': 0}
        elif switch == 'jianli':
            condition = {'userid': self.user_name, 'parentid': '0900'}
        elif switch == 'zhaopin':
            condition = {'userid': self.user_name, 'parentid': '0700'}
        return (condition)

    def listcity(self, pararr):
        # 所有的都是list下面的
        switch = pararr[0]
        condition = self.get_condition(switch)
        if len(pararr) == 2:
            parentid = pararr[1]
        #     if len(parentid) > 0:
        #         condition['parentid'] = parentid
        #         # print(self.vip_cat)
        #         if parentid in self.vip_cat:
        #             pass
        #         else:
        #             self.write('<span class="red">联系管理员开通此分类的VIP推广权限.</span>')
        #             return
        #
        else:
            parentid = ''

        user_published_infos = self.minfo.get_by_condition(condition)
        kwd = {
            'cityid': self.city_name,
            'cityname': self.mcity.get_cityname_by_id(self.city_name),
            # 'vip_cat': self.vip_cat,
            'action': switch,
            'parentid': parentid,
        }

        if switch == 'zhaopin':
            self.render('tpl_user/p_list_jianli.html',
                        user_published_infos=user_published_infos,
                        kwd=kwd,
                        wuserinfo=self.muser_info.get_by_username(),
                        wusernum=self.muser_num.get_by_username(),
                        wuservip=self.muser_vip.get_by_username(), )
        else:
            self.render('tpl_user/p_listcity.html',
                        user_published_infos=user_published_infos,
                        kwd=kwd,
                        wuserinfo=self.muser_info.get_by_username(),
                        wusernum=self.muser_num.get_by_username(),
                        wuservip=self.muser_vip.get_by_username(), )

