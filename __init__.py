#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
from argeweb.core.events import on
from .models.themes_model import ThemesModel


@on('update_theme_information')
def update_theme_information(controller, theme_name, theme_title, exclusive, author, thumbnail, using, in_datastore):
    from google.appengine.api.namespace_manager import namespace_manager
    namespace_manager.set_namespace('shared')
    n = ThemesModel.get_or_create_by_name(
        name=theme_name,
        theme_title=theme_title,
        theme_name=theme_name,
        exclusive=exclusive,
        author=author,
        thumbnail=thumbnail,
        using=using,
        in_datastore=in_datastore
    )
    namespace_manager.set_namespace(controller.namespace)


plugins_helper = {
    'title': u'佈景樣式',
    'desc': u'用來改變前台佈景樣式',
    'controllers': {
        'themes': {
            'group': u'佈景樣式',
            'actions': [
                {'action': 'list', 'name': u'佈景樣式管理'},
                {'action': 'add', 'name': u'新增樣式設定'},
                {'action': 'edit', 'name': u'編輯樣式設定'},
                {'action': 'view', 'name': u'檢視樣式設定'},
                {'action': 'delete', 'name': u'刪除樣式設定'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
                {'action': 'pickup_list', 'name': u'主題樣式挑選'},
            ]
        }
    }
}
