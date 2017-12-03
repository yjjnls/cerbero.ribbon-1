#!/usr/bin/env python
import sys
import os
import argparse

__dir__ = os.path.abspath( os.path.dirname(__file__) )
__cerbero__ = os.path.abspath( os.path.join( __dir__,'../cerbero') )
print __cerbero__
print '-----------------------'
sys.path.insert(0,__cerbero__)
import cerberus
import platform


parser = argparse.ArgumentParser(description='Ribbon build.')

parser.add_argument('command', type=str , choices=["build","buildonly","install","pack"] ,
                    help='command build or install.')

parser.add_argument('--target', nargs='*',
                    help='targets : ribbon and install only -> build-tools ,base or gstreamer.')

parser.add_argument('--no-clear', action='store_true', default=False,
                    help='Do not clear build intermediate files')

parser.add_argument('--debug', action='store_true', default=False,
                    help='For debug version, Windows Only')
args = parser.parse_args()

_clear = not args.no_clear
_command = args.command
_targets = args.target
TARGETS=["ribbon","build-tools" ,"base", "gstreamer","toolchain" ]
_targets = list((set(TARGETS).union(set(_targets)))^(set(TARGETS)^set(_targets)))
_debug =args.debug
if not _targets:
    print 'nothing to do for target ', _targets,',since there is no targe in build-tools base gstreamer'
    exit(0)


print '\n----------------------------------------------'
print '    %s %s   '%(_command,_targets)
print '    with%s clear   '%({True:'',False:'out'}[_clear])
print '    build type : %s'%({True:'debug',False:'release'}[_debug])
print '----------------------------------------------\n'    

platform = platform.system()
config_path = None

if platform == "Windows":
    config_path = os.path.join( __dir__,'config/win64.cbc')
    if _debug:
        config_path = os.path.join( __dir__,'config/win64d.cbc')


elif platform == "Linux":
    config_path = os.path.join( __dir__,'config/lin64.cbc')
config_path = os.path.abspath(config_path)
c = cerberus.Cerbero(config_path)


if _command in [ 'pack','install' ]:
    action = getattr( c,_command )
    for target in _targets:
        action( target )
    exit(0)


#for build
if 'ribbon' in _targets:
    if _clear:
        c.clear()
    if _command == "build":
        c.install('toolchain')
        c.install('build-tools')
        c.install('base')
        c.install('gstreamer')
    c.build('ribbon')
    c.pack('ribbon')


