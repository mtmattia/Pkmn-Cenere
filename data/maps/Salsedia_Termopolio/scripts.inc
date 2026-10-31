Salsedia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Salsedia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Salsedia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_SALSEDIA
	end

Salsedia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_SALSEDIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

