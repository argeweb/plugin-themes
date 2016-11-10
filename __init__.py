#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

plugins_helper = {
    "title": u"佈景樣式模組",
    "desc": u"用來改變前台佈景樣式的模組",
    "controllers": {
        "themes": {
            "group": u"佈景樣式",
            "actions": [
                {"action": "list", "name": u"佈景樣式管理"},
                {"action": "add", "name": u"新增樣式設定"},
                {"action": "edit", "name": u"編輯樣式設定"},
                {"action": "view", "name": u"檢視樣式設定"},
                {"action": "delete", "name": u"刪除樣式設定"},
                {"action": "plugins_check", "name": u"啟用停用模組"},
                {"action": "pickup_list", "name": u"主題樣式挑選"},
            ]
        }
    }
}
