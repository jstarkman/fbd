#setup
from cx_Freeze import setup, Executable
import sys

sys.argv.append("build")

exe = Executable(
	script = "fbd.py",
	base = "Win32GUI",
	icon = "icon.ico"
	)

includefiles = ["data.txt", "options.txt", "freesansbold.ttf"]
includes = []
excludes = []
packages = []

setup(
	version = "1.3", 
	description = "FBD practice",
	author = "James Starkman",
	name = "FBD",
	options = {"build_exe":{"excludes":excludes, "packages":packages, "include_files":includefiles}},
	executables = [exe]
	)