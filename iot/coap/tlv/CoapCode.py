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
from enum import Enum

class CoapCode(Enum):
    GET                         = 1
    POST                        = 2
    PUT                         = 3
    DELETE                      = 4
    CREATED                     = 201
    DELETED                     = 202
    VALID                       = 203
    CHANGED                     = 204
    CONTENT                     = 205
    BAR_DEQUEST                 = 400
    UNAUTHORIZED                = 401
    BAD_OPTION                  = 402
    FORBIDDEN                   = 403
    NOT_FOUND                   = 404
    METHOD_NOT_ALLOWED          = 405
    NOT_ACCEPTABLE              = 406
    PRECONDITION_FAILED         = 407
    REQUEST_ENTITY_TOO_LARGE    = 412
    UNSUPPORTED_CONTENT_FORMAT  = 415
    INTERNAL_SERVER_ERROR       = 500
    NOT_IMPLEMENTED             = 501
    BAD_GATEWAY                 = 502
    SERVICE_UNAVAILABLE         = 503
    GATEWAY_TIMEOUT             = 504
    PROXYING_NOT_SUPPORTED      = 505