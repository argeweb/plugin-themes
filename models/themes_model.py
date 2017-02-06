#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb import Fields
from google.appengine.ext import ndb


class ThemesModel(BasicModel):
    theme_title = Fields.StringProperty(required=True, verbose_name=u'樣式名稱')
    theme_name = Fields.StringProperty(required=True, verbose_name=u'系統編號')
    exclusive = Fields.StringProperty(default='all', verbose_name=u'專屬項目')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'顯示於前台')
    author = Fields.StringProperty(verbose_name=u'作者')
    using = Fields.TextProperty(verbose_name=u'使用的欄位')
    thumbnail = Fields.StringProperty(verbose_name=u'縮圖位置')
    in_datastore = Fields.BooleanProperty(default=False, verbose_name=u'是否位於 DataStore')

    @classmethod
    def find_by_theme_name(cls, theme_name):
        return cls.query(cls.theme_name == theme_name).get()

    @classmethod
    def get_list(cls, identifier_name):
        return cls.query(
            cls.exclusive.IN([identifier_name, u'all'])
        ).order(-cls.sort, -cls._key)

    @classmethod
    def check_in_list(cls, identifier_name, theme_name):
        item = cls.query(
            ndb.AND(
                cls.exclusive.IN([identifier_name, u'all']),
                cls.theme_name == theme_name
            )
        ).order(-cls.sort, -cls._key).get()
        if item:
            return True
        else:
            return False