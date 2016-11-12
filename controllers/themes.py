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
import json
import os


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
        theme_list = self.get_themes_list(self)
        is_find = False
        for theme in theme_list:
            if theme_key == theme["theme_name"] and (
                    theme["exclusive"].find(theme_key) or theme["exclusive"] == u"all"):
                is_find = True
        if is_find:
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
    @route_menu(list_name=u"backend", text=u"主題樣式", sort=299, group=u"視覺形象")
    def admin_pickup_list(self):
        self.context["current_theme"] = self.theme
        self.meta.pagination_limit = 48
        self.scaffold.query_factory = self.get_themes_list
        namespace_manager.set_namespace("shared.theme")
        return scaffold.list(self)

    @staticmethod
    def get_themes_list(self, other=None):
        def get_list():
            themes_list = []
            themes_dir = None
            dirs = []
            try:
                themes_dir = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'themes'))
                dirs = os.listdir(themes_dir)
            except:
                pass
            for dirPath in dirs:
                if dirPath.find(".") >= 0:
                    continue
                file_path = os.path.join(themes_dir, dirPath, "theme.json")
                if os.path.exists(file_path) is False:
                    continue
                f = open(file_path, 'r')
                data = json.load(f)
                themes_list.append({
                    "theme_name": u"" + dirPath,
                    "theme_title": data["name"] if "name" in data else u"" + dirPath,
                    "author": data["author"] if "author" in data else u"",
                    "using": data["using"] if "using" in data else [],
                    "exclusive": data["exclusive"] if "exclusive" in data else u"all"
                })
            if len(themes_list) is 0:
                themes_list = [
                    {"theme_name": u"default", u"theme_title": u"預設樣式", "using":[]}
                ]
            return themes_list
        return get_list()


