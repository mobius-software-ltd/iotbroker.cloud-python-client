"""
 # Mobius Software LTD
 # Copyright 2015-2018, Mobius Software LTD
 #
 # This is free software; you can redistribute it and/or modify it
 # under the terms of the GNU Lesser General Public License as
 # published by the Free Software Foundation; either version 2.1 of
 # the License, or (at your option) any later version.
 #
 # This software is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 # Lesser General Public License for more details.
 #
 # You should have received a copy of the GNU Lesser General Public
 # License along with this software; if not, write to the Free
 # Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 # 02110-1301 USA, or see the FSF site: http://www.fsf.org.
"""
class Will(object):
    def __init__(self, topic, content, retain):
        self.topic = topic
        self.content = content
        self.retain = retain

    def getLength(self):
        totalLength=0
        if self.topic.getLength()>0:
            totalLength+=self.topic.getLength() + 2

        if len(self.content) > 0:
            totalLength += len(self.content) + 2
        return totalLength

    def valid(self):
        if (self.topic is not None) & (self.topic.getLength() > 0) & (self.content is not None) & (self.topic.getQoS() is not None):
            return True
        return False

    def getTopic(self):
        return self.topic

    def getRetain(self):
        return self.retain