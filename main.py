#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from util.core import EtherHandler
from util.core import SessionSetup
from util.render import Render


class CatchAll(EtherHandler,Render):
	def get(self):
		self.response.write(self.renderView("home/index.theme",self.environDict,"ethereum"))

class MainHandler(EtherHandler,Render):
    def get(self):
    	self.response.write(self.renderView("home/index.theme",self.environDict,"ethereum"))



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    ('/.*', CatchAll)
], config=SessionSetup)
