Neapolia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Neapolia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Neapolia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_NEAPOLIA
	end

Neapolia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_NEAPOLIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

