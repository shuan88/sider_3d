#
# stm32_bootloader.py
#
import os,sys,marlin
Import("env")

from SCons.Script import DefaultEnvironment
board = DefaultEnvironment().BoardConfig()

board_keys = board.get("build").keys()

#
# For build.offset define LD_FLASH_OFFSET, used by ldscript.ld
#
if 'offset' in board_keys:
	LD_FLASH_OFFSET = board.get("build.offset")
	marlin.relocate_vtab(LD_FLASH_OFFSET)

	# Flash size
	maximum_flash_size = int(board.get("upload.maximum_size") / 1024)
	marlin.replace_define('STM32_FLASH_SIZE', maximum_flash_size)

	# Get upload.maximum_ram_size (defined by /buildroot/share/PlatformIO/boards/VARIOUS.json)
	maximum_ram_size = board.get("upload.maximum_ram_size")

	for i, flag in enumerate(env["LINKFLAGS"]):
		if "-Wl,--defsym=LD_FLASH_OFFSET" in flag:
			env["LINKFLAGS"][i] = "-Wl,--defsym=LD_FLASH_OFFSET=" + LD_FLASH_OFFSET
		if "-Wl,--defsym=LD_MAX_DATA_SIZE" in flag:
			env["LINKFLAGS"][i] = "-Wl,--defsym=LD_MAX_DATA_SIZE=" + str(maximum_ram_size - 40)

#
# For build.rename simply rename the firmware file.
#
if 'rename' in board_keys:

	def rename_target(source, target, env):
		firmware = os.path.join(target[0].dir.path, board.get("build.rename"))
		import shutil
		shutil.copy(target[0].path, firmware)

	marlin.add_post_action(rename_target)
