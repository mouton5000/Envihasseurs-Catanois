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
	
	String getColor(){
		Color color;
		switch(this){
		case ARGILE:
			color = KnownColor.ORANGE_RED;
			break;
		case BLE:
			color = KnownColor.YELLOW;
			break;
		case BOIS:
			color = KnownColor.DARK_GREEN;
			break;
		case CAILLOU:
			color = KnownColor.GRAY;
			break;
		case MARCHE:
			color = KnownColor.HOT_PINK;
			break;
		case MOUTON:
			color = KnownColor.GREEN_YELLOW;
			break;
		case OR:
			color = KnownColor.GOLDEN_ROD;
			break;
		case PORT:
			color = KnownColor.AQUA;
			break;
		case MER:
			color = KnownColor.CORNFLOWER_BLUE;
			break;
		case DESERT:
			color = KnownColor.SANDY_BROWN;
			break;
		default : return null;
		}
		return color.getColorCode();
	}
	
	
}
