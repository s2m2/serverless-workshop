#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import ConfigParser
from watchdog.observers import Observer

__author__ = 'hiroki8080'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INI_FILE = "config.ini"

def load_ini(ini_file):
    '''
    指定された設定ファイルを読み込みます。
    :param ini_file: 設定ファイル名
    :return: パーサー
    '''
    parser = ConfigParser.SafeConfigParser()
    if os.path.exists(ini_file):
        parser.read(ini_file)
        return parser
    else:
        raise IOError('%s が見つかりません' % ini_file)


def get_target_dir(parser):
    '''
    監視対象のディレクトリを取得します。
    :param parser: パーサー
    :return: ディレクトリ
    '''
    target_dir = parser.get('settings', 'target_dir')
    if target_dir == '.':
        target_dir = BASE_DIR
    return target_dir


def load_handlers(parser):
    '''
    指定された設定ファイルからハンドラを読み込みます。
    :param ini_file: 設定ファイル名
    :return: ハンドラのリスト
    '''
    result = []
    handlers = parser.get('settings', 'handlers')
    if len(handlers) == 0:
        raise IOError('ハンドラが定義されていません')
    handlers = handlers.split(',')
    for handler_name in handlers:
        params = {}
        for key in parser.options(handler_name):
            value = parser.get(handler_name, key)
            params[key] = value
        handler = create_handler(params)
        result.append(handler)
    return result

def create_handler(params):
    '''
    指定されたパラメータでハンドラを生成します。
    :param params: パラメータ
    :return: ハンドラ
    '''
    if 'class' in params: # インスタンスの生成
        module = __import__("handler",fromlist=[params['class']])
        clazz = getattr(module,params['class'])
        handler = clazz()
    for key in params: # プロパティの設定
        if 'class' != key:
            setattr(handler, key, params[key])
    return handler

if __name__ == "__main__":
    parser = load_ini(INI_FILE)
    target_dir = get_target_dir(parser)
    handlers = load_handlers(parser)
    observer = Observer()
    for index, handler in enumerate(handlers):
        if index == 0:
            watch = observer.schedule(handler, target_dir, recursive=True)
        else:
            observer.add_handler_for_watch(handler, watch)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()