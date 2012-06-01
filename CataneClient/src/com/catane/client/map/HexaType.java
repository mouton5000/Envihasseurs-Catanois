package com.catane.client.map;

import gwt.g2d.client.graphics.Color;
import gwt.g2d.client.graphics.KnownColor;

enum HexaType {

	ARGILE,
	BLE,
	BOIS,
	CAILLOU,
	MOUTON,
	OR,
	MARCHE,
	PORT, 
	MER, 
	DESERT;
	
	Color getColor(){
		switch(this){
		case ARGILE:
			return KnownColor.ORANGE_RED;
		case BLE:
			return KnownColor.YELLOW;
		case BOIS:
			return KnownColor.DARK_GREEN;
		case CAILLOU:
			return KnownColor.GRAY;
		case MARCHE:
			return KnownColor.HOT_PINK;
		case MOUTON:
			return KnownColor.GREEN_YELLOW;
		case OR:
			return KnownColor.GOLDEN_ROD;
		case PORT:
			return KnownColor.AQUA;
		case MER:
			return KnownColor.CORNFLOWER_BLUE;
		case DESERT:
			return KnownColor.SANDY_BROWN;
		}
		return null;
	}
}
