#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from google.appengine.api import namespace_manager
from argeweb import route_with, route_menu, route
from argeweb import Controller, scaffold
import datetime


class Themes(Controller):
    class Meta:
        pagination_actions = ("list", "pickup_list",)
        pagination_limit = 10
        
    class Scaffold:
        display_properties_in_list = ("theme_name", "theme_key")


    @route_with('/admin/themes/set.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        namespace_manager.set_namespace("shared.theme")
        theme_key = self.params.get_string("theme_key", '')
        model = self.meta.Model
        is_in_list = model.check_in_list(self.namespace, theme_key=theme_key)
        if is_in_list:
            self.settings.set_theme(self.server_name, self.namespace, theme_key)
            self.context['data'] = {
                'info': "done",
                "theme": theme_key
            }
        else:
            self.context['data'] = {
                'info': "not_in_list"
            }

    @route
    @route_menu(list_name=u"backend", text=u"主題樣式", sort=9995, icon="gears", group=u"系統設定")
    def admin_pickup_list(self):
        self.context["current_theme"] = self.theme
        self.meta.pagination_limit = 48
        namespace = self.namespace
        model = self.meta.Model
        def get_list(self):
            return model.get_list(namespace)
        self.scaffold.query_factory = get_list
        namespace_manager.set_namespace("shared.theme")
        return scaffold.list(self)

    @route_menu(list_name=u"backend", text=u"樣式設定", sort=9993, icon="gears", group=u"系統設定")
    def admin_list(self):
        namespace_manager.set_namespace("shared.theme")
        return scaffold.list(self)

    def admin_add(self):
        namespace_manager.set_namespace("shared.theme")
        return scaffold.add(self)

    def admin_edit(self, key):
        namespace_manager.set_namespace("shared.theme")
        self.context["item"] = self.util.decode_key(key).get()
        return scaffold.edit(self, key)

    def admin_view(self, key):
        namespace_manager.set_namespace("shared.theme")
        self.context["item"] = self.util.decode_key(key).get()
        return scaffold.edit(self, key)

    def admin_delete(self, key):
        namespace_manager.set_namespace("shared.theme")
        return scaffold.delete(self, key)
