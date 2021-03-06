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
        pagination_actions = ('list', 'pickup_list',)
        
    class Scaffold:
        display_in_list = ['theme_name', 'theme_name']

    @route
    def admin_list(self):
        namespace_manager.set_namespace('shared')
        return scaffold.list(self)

    @route
    def admin_edit(self, key):
        namespace_manager.set_namespace('shared')
        return scaffold.edit(self, key)

    @route
    def admin_view(self, key):
        namespace_manager.set_namespace('shared')
        return scaffold.view(self, key)

    @route
    def admin_upload(self):
        self.meta.change_view('json')
        namespace_manager.set_namespace('shared')
        theme_title = self.params.get_string('theme_title', '')
        theme_name = self.params.get_string('theme_name', '')
        exclusive = self.params.get_string('exclusive', 'this')
        if exclusive is not u'all':
            exclusive = self.namespace
        author = self.params.get_string('author', '')
        thumbnail = self.params.get_string('thumbnail', '/assets/themes/%s/img/theme.png' % theme_name)
        using = self.params.get_string('using', '')
        is_find = self.meta.Model.check_in_list(self.namespace, theme_name=theme_name)
        if thumbnail.startswith('/'):
            thumbnail = thumbnail[1:]
        if thumbnail.startswith('themes'):
            thumbnail = 'assets/' + thumbnail
        if thumbnail.startswith('assets/themes') is False:
            thumbnail = 'assets/themes/%s/%s' % (theme_name, thumbnail)
        thumbnail = '/' + thumbnail
        self.logging.info(thumbnail)
        self.fire(
            event_name='update_theme_information',
            theme_title=theme_title,
            theme_name=theme_name,
            exclusive=exclusive,
            author=author,
            in_datastore=True,
            thumbnail=thumbnail,
            using=using
        )
        self.context['data'] = {
            'info': is_find and 'done' or 'create',
            'theme': theme_name
        }

    @route_with('/admin/themes/set.json')
    def admin_get_url(self):
        self.meta.change_view('json')
        namespace_manager.set_namespace('shared')
        theme_name = self.params.get_string('theme_name', '')
        is_find = self.meta.Model.check_in_list(self.namespace, theme_name=theme_name)

        if is_find:
            self.settings.set_theme(self.server_name, self.namespace, theme_name)
            self.context['data'] = {
                'info': 'done',
                'theme': theme_name
            }
        else:
            self.context['data'] = {
                'info': 'not_in_list'
            }

    @route
    @route_menu(list_name=u'system', group=u'系統設定', text=u'主題樣式', sort=9999, icon=u'photo')
    def admin_pickup_list(self):
        def query_factory_with_identifier(controller):
            model = controller.meta.Model
            return model.query(
                model.exclusive.IN([self.namespace, u'all'])
            ).order(-model.sort, -model._key)
        namespace_manager.set_namespace('shared')
        self.scaffold.query_factory = query_factory_with_identifier
        self.meta.pagination_limit = 100
        scaffold.list(self)

        self.context['current_theme'] = self.theme
        theme_list = self.get_themes_list(self)

        self.context['new_item_list'] = []
        for item_p in theme_list:
            is_not_find = True
            for item_d in self.context[self.scaffold.plural]:
                if item_d.theme_name == item_p['theme_name']:
                    is_not_find = False
            if is_not_find:
                n = self.meta.Model()
                n.theme_title = item_p['theme_title']
                n.theme_name = item_p['theme_name']
                n.exclusive = item_p['exclusive']
                n.author = item_p['author']
                n.using = json.dumps(item_p['using'])
                n.in_datastore = False
                n.put()
                self.context['new_item_list'].append(n)

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
                if dirPath.find('.') >= 0:
                    continue
                file_path = os.path.join(themes_dir, dirPath, 'theme.json')
                if os.path.exists(file_path) is False:
                    continue
                f = open(file_path, 'r')
                data = json.load(f)
                thumbnail = '/assets/themes/%s/img/theme.png' % dirPath
                if 'thumbnail' in data:
                    thumbnail = data['thumbnail']
                if thumbnail.startswith('/'):
                    thumbnail = thumbnail[1:]
                if thumbnail.startswith('themes'):
                    thumbnail = 'assets/' + thumbnail
                if thumbnail.startswith('assets/themes') is False:
                    thumbnail = 'assets/themes/%s/%s' % (dirPath, thumbnail)
                thumbnail = '/' + thumbnail
                themes_list.append({
                    'theme_name': u'' + dirPath,
                    'theme_title': data['name'] if 'name' in data else u'' + dirPath,
                    'author': data['author'] if 'author' in data else u'',
                    'using': data['using'] if 'using' in data else [],
                    'exclusive': data['exclusive'] if 'exclusive' in data else u'all'
                })
            if len(themes_list) is 0:
                themes_list = [
                    {'theme_name': u'default', 'theme_title': u'預設樣式', 'using':[], 'author': u'', 'exclusive': u'all'}
                ]
            return themes_list
        return get_list()

    @route
    def admin_get_files_md5(self):
        from plugins.file.models.file_model import FileModel
        self.meta.change_view('json')
        theme = self.params.get_string('theme')
        query = FileModel.query(FileModel.theme == theme, FileModel.is_collection == False).order(-FileModel.path)
        data_list = []
        for item in query.fetch():
            data_list.append({'md5': item.last_md5, 'path': item.path})
        self.context['data'] = {
            'files': data_list,
            'next': None
        }

    @route
    def admin_delete_theme(self):
        from plugins.file.models.file_model import FileModel
        from google.appengine.ext import ndb
        self.meta.change_view('json')
        theme = self.params.get_string('theme')
        multi_keys = FileModel.query(FileModel.theme == theme).fetch(keys_only=True)
        ndb.delete_multi(multi_keys)
        self.context['data'] = {
            'files': [],
            'next': None
        }
