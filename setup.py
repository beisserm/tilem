# A simple script which creates an executible for a non-console app
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.
#setup(
#    # The first three parameters are not required, if at least a
#    # 'version' is given, then a versioninfo resource is built from
#    # them and added to the executables.
#    version = "0.5.0",
#    description = "py2exe sample script",
#    name = "py2exe samples",
#
#    # targets to build
#    windows = ["script": "tilem.py"],
#    #console = ["hello.py"],
#    )

from distutils.core import setup
import py2exe


setup(
    windows = [
        {
            "script": "tilem.py",
            "icon_resources": [(1, "DeletedIcon.ico")]
        }
    ],
)
