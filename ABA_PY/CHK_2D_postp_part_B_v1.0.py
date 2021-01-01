if session.isUpgradeRequiredForOdb(upgradeRequiredOdbPath = VP_ODB_FullPathName):
	print('This ODB file is created using an older ABAQUS version')
	print('Checking if an upgraded version of the ODB file already exists in the PWD')
	if os.path.isfile(VP_UpGraded_ODB_FullPathName):
		print('Using the upgraded ODB in the PWD')
		Associate_ODB = session.openOdb(name = VP_UpGraded_ODB_FullPathName)
	else:
		print('Upgraded ODB does not exist in PWD, %s', VP_ODB_PathName)
		print('Upgrading the ODB file for compatibility with ABAQUS %s'% (abaqus.version))
		print('Upgraded filename--- %s'% (VP_ODB_FileName + '_UpGraded' + '.odb'))
		session.upgradeOdb(existingOdbPath = VP_ODB_FullPathName, upgradedOdbPath = VP_UpGraded_ODB_FullPathName)
		Associate_ODB = session.openOdb(name = VP_UpGraded_ODB_FullPathName)
else:
	Associate_ODB = session.openOdb(name = VP_ODB_FullPathName)
