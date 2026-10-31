Granaria_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Granaria_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Granaria_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_GRANARIA
	end

Granaria_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_GRANARIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

