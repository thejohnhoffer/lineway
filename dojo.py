#!/usr/bin/env python

#
# DOJO Image Server
#

import json
import os
import socket
import sys
import tornado
import tornado.websocket
import tempfile
import signal

import _dojo

#
# default handler
#
class DojoHandler(tornado.web.RequestHandler):

  def initialize(self, logic):
    self.__logic = logic
  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def get(self, uri):
    self.__logic.handle(self)
  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def post(self, uri):
    self.__logic.handle(self)



class ServerLogic:

  def __init__( self ):

    pass

  def run( self, mojo_dir, out_dir, port, configured ):


    signal.signal(signal.SIGINT, self.close)

    self.__mojo_dir = mojo_dir
    self.__configured = configured
    self.__out_dir = out_dir

    # create temp folder
    tmpdir = out_dir
    self.__tmpdir = out_dir

    self.log = -1

    # and the setup
    self.__setup = _dojo.Setup(self,mojo_dir,tmpdir)

    ip = socket.gethostbyname(socket.gethostname())

    dojo = tornado.web.Application([

      # viewer
      (r'/(.*)', DojoHandler, dict(logic=self))

    ])



    dojo.listen(port,max_buffer_size=1024*1024*150000)

    print '*'*80
    print '*', '\033[93m'+'DOJO RUNNING', '\033[0m'
    print '*'
    print '*', 'open', '\033[92m'+'http://' + ip + ':' + str(port) + '/dojo/' + '\033[0m'
    print '*'*80

    tornado.ioloop.IOLoop.instance().start()

  def handle( self, r ):

    content = None

    # the access to the viewer
    if not self.__configured:
      content, content_type = self.__setup.handle(r.request)

    # invalid request
    if not content:
      content = '404'
      content_type = 'text/html'

    # print 'IP',r.request.remote_ip

    r.set_header('Access-Control-Allow-Origin', '*')
    r.set_header('Content-Type', content_type)
    r.write(content)
    

  def close(self, signal, frame):
    print 'Sayonara..!!'
    output = {}
    output['origin'] = 'SERVER'

    sys.exit(0)

def print_help( scriptName ):

  description = ''
  print description
  print
  print 'Usage: ' + scriptName + ' MOJO_DIRECTORY OUTPUT_DIRECTORY PORT'
  print

#
# entry point
#
if __name__ == "__main__":

  # always show the help if no arguments were specified
  if len(sys.argv) != 1 and len( sys.argv ) < 4:
    print_help( sys.argv[0] )
    sys.exit( 1 )

  if len(sys.argv) == 1:
    # dojo was started without parameters
    # so we need to add an input folder
    input_dir = tempfile.mkdtemp()
    # and a output folder
    output_dir = tempfile.mkdtemp()
    # and a free port
    port = 1338
    result = 0

    import socket
    while result==0:
      port += 1
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1',port))

    configured = False

  else:
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    port = sys.argv[3]
    configured = False

  logic = ServerLogic()
  logic.run( input_dir, output_dir, port, configured )
