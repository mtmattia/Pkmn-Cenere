Misenia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Misenia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Misenia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_MISENIA
	end

Misenia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_MISENIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

