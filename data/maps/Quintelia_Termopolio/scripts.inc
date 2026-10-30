Quintelia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Quintelia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Quintelia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_QUINTELIA
	end

Quintelia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_QUINTELIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

