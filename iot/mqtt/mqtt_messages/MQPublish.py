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
class MQPublish(object):
    def __init__(self,packetID,topic,content,retain,dup):
        self.packetID = packetID
        self.topic = topic
        self.content = content
        self.retain = retain
        self.dup = dup

    def getLength(self):
        length = 0

        if self.packetID > 0:
            length += 2

        if self.topic is not None:
            length += self.topic.getLength() + 2

        length += len(self.content)

        return length

    def getType(self):
        return 3

    def getProtocol(self):
        return 1