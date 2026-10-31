Classia_Termopolio_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Classia_Termopolio_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

Classia_Termopolio_OnTransition:
	setrespawn HEAL_LOCATION_CLASSIA
	end

Classia_Termopolio_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_CLASSIA_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

