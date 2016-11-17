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
        display_properties_in_list = ("theme_name", "theme_name")

    @route
    def admin_upload(self):
        self.meta.change_view('json')
        namespace_manager.set_namespace("shared")
        theme_title = self.params.get_string("theme_title", '')
        theme_name = self.params.get_string("theme_name", '')
        exclusive = self.params.get_string("exclusive", '')
        author = self.params.get_string("author", '')
        using = self.params.get_string("using", '')
        model = self.meta.Model
        is_find = model.check_in_list(self.namespace, theme_name=theme_name)
        if is_find:
            self.context['data'] = {
                'info': "done",
                "theme": theme_name
            }
            n = model.find_by_theme_name(theme_name)
        else:
            self.context['data'] = {
                'info': "create",
                "theme": theme_name
            }
            n = model()
        n.theme_title = theme_title
        n.theme_name = theme_name
        n.exclusive = exclusive
        n.author = author
        n.using = using
        n.put()

    @route_with('/admin/themes/set.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        namespace_manager.set_namespace("shared")
        theme_name = self.params.get_string("theme_name", '')
        model = self.meta.Model
        is_find = model.check_in_list(self.namespace, theme_name=theme_name)
        if is_find:
            self.settings.set_theme(self.server_name, self.namespace, theme_name)
            self.context['data'] = {
                'info': "done",
                "theme": theme_name
            }
        else:
            self.context['data'] = {
                'info': "not_in_list"
            }

    @route
    @route_menu(list_name=u"backend", text=u"主題樣式", sort=299, group=u"視覺形象")
    def admin_pickup_list(self):
        self.context["current_theme"] = self.theme
        self.meta.pagination_limit = 100
        theme_list = self.get_themes_list(self)
        model = self.meta.Model

        def query_factory_with_identifier(self):
            return model.query(
                model.exclusive.IN([self.namespace, u"all"])
            ).order(-model.sort, -model._key)
        self.scaffold.query_factory = query_factory_with_identifier
        namespace_manager.set_namespace("shared")
        scaffold.list(self)
        self.context["new_item_list"] = []
        for item_p in theme_list:
            is_not_find = True
            for item_d in self.context[self.scaffold.plural]:
                if item_d.theme_name == item_p["theme_name"]:
                    is_not_find = False
            if is_not_find:
                n = self.meta.Model()
                n.theme_title = item_p["theme_title"]
                n.theme_name = item_p["theme_name"]
                n.exclusive = item_p["exclusive"]
                n.author = item_p["author"]
                n.using = json.dumps(item_p["using"])
                n.put()
                self.context["new_item_list"].append(n)

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
                    {"theme_name": u"default", "theme_title": u"預設樣式", "using":[], "author": u"", "exclusive": u"all"}
                ]
            return themes_list
        return get_list()


