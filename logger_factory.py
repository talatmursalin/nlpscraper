#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# author : mursalin
# date   : 2019-10-19

import logging


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(threadName)s %(name)-10s %(levelname)-8s %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
