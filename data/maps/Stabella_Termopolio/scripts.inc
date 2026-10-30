Stabella_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Stabella_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Stabella_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_STABELLA
	end

Stabella_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_STABELLA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

