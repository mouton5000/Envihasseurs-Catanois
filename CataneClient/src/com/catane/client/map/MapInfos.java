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
	
	public final native JsArray<BateauInfos> getBateauxTransports() /*-{return this.bateaux_transports}-*/;
	public final native JsArray<BateauInfos> getCargos() /*-{return this.cargos}-*/;
	public final native JsArray<BateauInfos> getVoiliers() /*-{return this.voiliers}-*/;

	
	public final native JsArray<BatimentInfos> getColoniesD() /*-{return this.coloniesD}-*/;
	public final native JsArray<BatimentInfos> getVillesD() /*-{return this.villesD}-*/;
	
	public final native JsArray<LienInfos> getRoutesD() /*-{return this.routesD}-*/;
	
	public final native JsArray<BateauInfos> getBateauxTransportsD() /*-{return this.bateaux_transportsD}-*/;
	public final native JsArray<BateauInfos> getCargosD() /*-{return this.cargosD}-*/;
	public final native JsArray<BateauInfos> getVoiliersD() /*-{return this.voiliersD}-*/;
	
	
}

abstract class PionJoueurInfos extends JavaScriptObject{
	protected PionJoueurInfos(){
	}	
	public final native int getJoueur() /*-{return this.joueur}-*/;

}

/**
 * Informations concernant une colonie ou une ville sur la carte
 * @author mouton
 *
 */
class BatimentInfos extends PionJoueurInfos{
	protected BatimentInfos(){
	}	
	public final native int getPosition() /*-{return this.position}-*/;
}

/**
 * Informatins concernant une route ou un bateau sur la carte
 * @author mouton
 *
 */
class LienInfos extends PionJoueurInfos{
	protected LienInfos(){
	}	
	public final native int getPosition1() /*-{return this.position1}-*/;
	public final native int getPosition2() /*-{return this.position2}-*/;
}

/**
 * Informatins concernant un bateau sur la carte
 * @author mouton
 *
 */
class BateauInfos extends LienInfos{
	protected BateauInfos(){
	}	
	public final native int getNum() /*-{return this.num}-*/;
}