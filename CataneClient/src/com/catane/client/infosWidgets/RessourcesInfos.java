package com.catane.client.infosWidgets;

import com.google.gwt.core.client.JavaScriptObject;

public class RessourcesInfos extends JavaScriptObject {
	protected RessourcesInfos(){
		
	}
	
	public final native int getArgileLandValue() /*-{return this.argile.landQtt;}-*/;
	public final native int getArgileWorldValue() /*-{return this.argile.worldQtt;}-*/;
	
	public final native int getBleLandValue() /*-{return this.ble.landQtt;}-*/;
	public final native int getBleWorldValue() /*-{return this.ble.worldQtt;}-*/;

	public final native int getBoisLandValue() /*-{return this.bois.landQtt;}-*/;
	public final native int getBoisWorldValue() /*-{return this.bois.worldQtt;}-*/;	
	
	public final native int getCaillouLandValue() /*-{return this.caillou.landQtt;}-*/;
	public final native int getCaillouWorldValue() /*-{return this.caillou.worldQtt;}-*/;
	
	public final native int getMoutonLandValue() /*-{return this.mouton.landQtt;}-*/;
	public final native int getMoutonWorldValue() /*-{return this.mouton.worldQtt;}-*/;
	
	public final native int getOrLandValue() /*-{return this.or.landQtt;}-*/;
	public final native int getOrWorldValue() /*-{return this.or.worldQtt;}-*/;	
	
}
