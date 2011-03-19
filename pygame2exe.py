# -*- coding: sjis -*-
# make standalone, needs at least pygame-1.5.3 and py2exe-0.3.1
# fixed for py2exe-0.6.x by RyoN3 at 03/15/2006

from distutils.core import setup
import sys, os, pygame, shutil
import py2exe
import sitecustomize
import easygui

while 1:
    workdir = raw_input('Input script directry:')
    try:
        os.chdir(workdir)
    except:
        print "Change directry is failed."
        print "Please re-try input directry."
        continue
    print "Setup directry:%s"%os.getcwd()
    break


######
# �K�v�ɉ����āA�ȉ��̒l��ύX����B
#
script = raw_input('Input starting script:') # �J�n�X�N���v�g��
icon_file = None                   # exe�ɖ��ߍ���icon�t�@�C����(�Ȃ����None)
optimize = 2                       # �œK�����x��(0-2)
extra_modules = ['pygame.locals']  # �����Ō����Ă���Ȃ����W���[��

exclude_modules =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'hashlib',
'base64',
'compiler',
'pydoc']

###
# ��������File information(exe�̃o�[�W�������)
project_name = 'Tower of Elder Dragon'          # �v���W�F�N�g��(���肾���H)
description = 'Wizardry-like game.' # ����
version = "0.55"              # �t�@�C���̃o�[�W����
company_name = "Corona"    # ������
copy_right = "Musyoku Doutei, Corona"    # ����Җ�
pj_name = "Tower of Elder Dragon"            # ���i��
# �����܂�
####

# exe�Ɋ܂߂��O�ɏo��DLL(SDL��LGPL�Ȃ̂Ŋ܂߂Ȃ�)
dll_excludes = ['SDL_mixer.dll','SDL.dll','SDL_ttf.dll',
                'smpeg.dll', # python2.3�p�ɓ����Ă�dll
                'SDL_image.dll'] 

options = {"py2exe": {"compressed": 1, # �o�͂����k���邩(1:Yes)
                      "optimize"  : optimize,
                      "bundle_files": 2,# 1:�΂炯 2:�P��
                      "dll_excludes": dll_excludes,
                      "excludes": exclude_modules,
                      "ignores": ['tcl','AppKit','Numeric','Foundation'],
                      "includes": ['encodings',"encodings.latin_1",
                                   'title', 'city', 'inn', 'shop', 'temple',
                                   'tower', 'castle', 'bar','window',
                                   'character', 'character_make',
                                   ],
                      }
           }


# �ύX�͂����܂ŁB�ȉ��͕�����Ȃ���ΐG��Ȃ��B
#####


class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)

#use the default pygame icon, if none given
if icon_file is None:
    path = os.path.split(pygame.__file__)[0]
    icon_file = os.path.join(path, 'pygame.ico')
#unfortunately, this cool icon stuff doesn't work in current py2exe :(
#icon_file = ''


#create the proper commandline args
args = ['py2exe']
#args.append('-p')
#args.append('japanese,encodings') # JapaneseCodec�������I�Ɋ܂߂� not needed after python2.5
sys.argv[1:] = args + sys.argv[1:]

target = Target(
                script = script,
                icon_resources = [(1,icon_file)],
                company_name = company_name,
                copyright = copy_right,
                name = pj_name,
                )



#this will create the executable and all dependencies
setup(
      version = version,
      description = description,
      name = project_name,
      options = options,
      zipfile = None,
      windows=[target],
      )

# exe�Ɋ܂߂Ȃ�dll�͎蓮�R�s�[
pygamedir = os.path.split(pygame.base.__file__)[0]
for src in dll_excludes:
    f = os.path.join(pygamedir, src)
    d = 'dist'
    print 'copying', f, '->', d
    try:
        shutil.copy(f, d)
    except:
        print 'not found: %s'%src


# end.

#extra_files = [ #("",[ICONFILE,'icon.png','readme.txt']),
#                   ("data",glob.glob(os.path.join('data','*.dat'))),
#                   ("gfx",glob.glob(os.path.join('gfx','*.jpg'))),
#                   ("gfx",glob.glob(os.path.join('gfx','*.png'))),
#                   ("fonts",glob.glob(os.path.join('fonts','*.ttf'))),
#                   ("music",glob.glob(os.path.join('music','*.ogg'))),
#                   ("snd",glob.glob(os.path.join('snd','*.wav')))]


#if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
#if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')
 
