package com.catane.client.Colors;

import gwt.g2d.client.graphics.Color;

import com.google.gwt.core.client.JavaScriptObject;

class PlayerColorInfos extends JavaScriptObject {

	protected PlayerColorInfos() {
	}
	
	private final native int getRed() /*-{return this.red}-*/;
	private final native int getBlue() /*-{return this.blue}-*/;
	private final native int getGreen() /*-{return this.green}-*/;
	
	public final Color getColor(){
		return new Color(getRed(), getGreen(), getBlue());
	}
	
}
