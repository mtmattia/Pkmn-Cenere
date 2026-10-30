Nucelia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Nucelia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Nucelia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_NUCELIA
	end

Nucelia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_NUCELIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

