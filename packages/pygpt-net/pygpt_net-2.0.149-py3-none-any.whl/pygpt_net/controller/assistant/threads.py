#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.15 01:00:00                  #
# ================================================== #

import time

from PySide6.QtCore import QObject, Signal, Slot, QRunnable

from pygpt_net.item.ctx import CtxItem
from pygpt_net.utils import trans


class Threads:
    def __init__(self, window=None):
        """
        Assistant threads controller

        :param window: Window instance
        """
        self.window = window
        self.started = False
        self.stop = False

    def create_thread(self) -> str:
        """
        Create assistant thread

        :return: thread id
        """
        thread_id = self.window.core.gpt.assistants.thread_create()
        self.window.core.config.set('assistant_thread', thread_id)
        self.window.core.ctx.append_thread(thread_id)
        return thread_id

    def handle_messages(self, ctx: CtxItem):
        """
        Handle run messages

        :param ctx: CtxItem
        """
        data = self.window.core.gpt.assistants.msg_list(ctx.thread)
        paths = []
        for msg in data:
            if msg.role == "assistant":
                for content in msg.content:
                    if content.type == "text":
                        ctx.set_output(content.text.value)

                # handle files
                paths += self.window.controller.assistant.files.handle_received_ids(msg.file_ids)
                if paths:
                    ctx.files = self.window.core.filesystem.make_local_list(list(paths))

                # update ctx
                self.window.core.ctx.update_item(ctx)

                self.window.controller.chat.output.handle(ctx, 'assistant', False)
                self.window.controller.chat.output.handle_cmd(ctx)

                # update ctx
                self.window.core.ctx.update_item(ctx)

                # index ctx (llama-index)
                self.window.controller.idx.on_ctx_end(ctx)

                # update ctx list
                self.window.controller.ctx.update()
                break

    def is_log(self) -> bool:
        """
        Check if logging is enabled

        :return: bool
        """
        if self.window.core.config.has('log.assistants') \
                and self.window.core.config.get('log.assistants'):
            return True
        return False

    def handle_run(self, ctx: CtxItem):
        """
        Handle assistant's run

        :param ctx: CtxItem
        """
        # worker
        worker = RunWorker()
        worker.window = self.window
        worker.ctx = ctx

        # signals
        worker.signals.updated.connect(self.handle_status)
        worker.signals.destroyed.connect(self.handle_destroy)
        worker.signals.started.connect(self.handle_started)

        self.window.stateChanged.emit(self.window.STATE_BUSY)

        # start
        self.window.threadpool.start(worker)
        self.started = True

    @Slot(str, object)
    def handle_status(self, status: str, ctx: CtxItem):
        """
        Handle status

        :param status: status
        :param ctx: CtxItem
        """
        if self.is_log():
            print("Run status: {}".format(status))
        if status != "queued" and status != "in_progress":
            self.window.controller.chat.common.unlock_input()  # unlock input
        if status == "completed":
            self.stop = False
            self.handle_messages(ctx)
            self.window.statusChanged.emit(trans('assistant.run.completed'))
            self.window.stateChanged.emit(self.window.STATE_IDLE)

            # update run tokens
            self.window.controller.chat.output.show_response_tokens(ctx)
        elif status == "failed":
            self.stop = False
            self.window.controller.chat.common.unlock_input()
            self.window.statusChanged.emit(trans('assistant.run.failed'))
            self.window.stateChanged.emit(self.window.STATE_ERROR)

    @Slot()
    def handle_destroy(self):
        """Handle thread destroy"""
        self.started = False
        self.stop = False

    @Slot()
    def handle_started(self):
        """Handle listening started"""
        if self.is_log():
            print("Run: assistant is listening status...")
        self.window.statusChanged.emit(trans('assistant.run.listening'))


class RunSignals(QObject):
    updated = Signal(object, object)
    destroyed = Signal()
    started = Signal()


class RunWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(RunWorker, self).__init__()
        self.signals = RunSignals()
        self.args = args
        self.kwargs = kwargs
        self.window = None
        self.ctx = None
        self.check = True
        self.stop_reasons = [
            "cancelling",
            "cancelled",
            "failed",
            "completed",
            "expired",
            "requires_action",
        ]

    @Slot()
    def run(self):
        """Run thread"""
        try:
            self.signals.started.emit()
            while self.check \
                    and not self.window.is_closing \
                    and not self.window.controller.assistant.threads.stop:
                status = self.window.core.gpt.assistants.run_status(self.ctx)
                self.signals.updated.emit(status, self.ctx)
                # finished or failed
                if status in self.stop_reasons:
                    self.check = False
                    self.signals.destroyed.emit()
                    break
                time.sleep(1)
            self.signals.destroyed.emit()
        except Exception as e:
            self.window.core.debug.log(e)
            self.signals.destroyed.emit()
