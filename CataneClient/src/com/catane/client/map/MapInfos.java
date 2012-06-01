package com.catane.client.map;

import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.core.client.JsArrayInteger;

public class MapInfos extends JavaScriptObject{
	protected MapInfos(){
		
	}
	
	public final native JsArrayInteger getBrigands() /*-{return this.brigands}-*/;
	public final native JsArrayInteger getPirates() /*-{return this.pirates}-*/;
	
	public final native JsArray<BatimentInfos> getColonies() /*-{return this.colonies}-*/;
	public final native JsArray<BatimentInfos> getVilles() /*-{return this.villes}-*/;
	
	public final native JsArray<LienInfos> getRoutes() /*-{return this.routes}-*/;
	
	public final native JsArray<LienInfos> getBateauxTransports() /*-{return this.bateaux_transports}-*/;
	public final native JsArray<LienInfos> getCargos() /*-{return this.cargos}-*/;
	public final native JsArray<LienInfos> getVoilliers() /*-{return this.voilliers}-*/;

}

/**
 * Informations concernant une colonie ou une ville sur la carte
 * @author mouton
 *
 */
class BatimentInfos extends JavaScriptObject{
	protected BatimentInfos(){
	}	
	public final native int getPosition() /*-{return this.position}-*/;
	public final native int getJoueur() /*-{return this.joueur}-*/;
}

/**
 * Informatins concernant une route ou un bateau sur la carte
 * @author mouton
 *
 */
class LienInfos extends JavaScriptObject{
	protected LienInfos(){
	}	
	public final native int getPosition1() /*-{return this.position1}-*/;
	public final native int getPosition2() /*-{return this.position2}-*/;
	public final native int getJoueur() /*-{return this.joueur}-*/;
}
