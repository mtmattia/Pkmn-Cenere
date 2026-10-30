Cumara_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Cumara_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Cumara_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_CUMARA
	end

Cumara_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_CUMARA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

