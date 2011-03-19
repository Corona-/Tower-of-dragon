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
# 必要に応じて、以下の値を変更する。
#
script = raw_input('Input starting script:') # 開始スクリプト名
icon_file = None                   # exeに埋め込むiconファイル名(なければNone)
optimize = 2                       # 最適化レベル(0-2)
extra_modules = ['pygame.locals']  # 自動で見つけてくれないモジュール

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
# ここからFile information(exeのバージョン情報)
project_name = 'Tower of Elder Dragon'          # プロジェクト名(飾りだけ？)
description = 'Wizardry-like game.' # 説明
version = "0.55"              # ファイルのバージョン
company_name = "Corona"    # 製作会社
copy_right = "Musyoku Doutei, Corona"    # 著作者名
pj_name = "Tower of Elder Dragon"            # 製品名
# ここまで
####

# exeに含めず外に出すDLL(SDLはLGPLなので含めない)
dll_excludes = ['SDL_mixer.dll','SDL.dll','SDL_ttf.dll',
                'smpeg.dll', # python2.3用に入ってたdll
                'SDL_image.dll'] 

options = {"py2exe": {"compressed": 1, # 出力を圧縮するか(1:Yes)
                      "optimize"  : optimize,
                      "bundle_files": 2,# 1:ばらけ 2:単一
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


# 変更はここまで。以下は分からなければ触らない。
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
#args.append('japanese,encodings') # JapaneseCodecを強制的に含める not needed after python2.5
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

# exeに含めないdllは手動コピー
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
 
