Agorapoli_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Agorapoli_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Agorapoli_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_AGORAPOLI
	end

Agorapoli_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_AGORAPOLI_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

