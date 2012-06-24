package com.catane.client.map;

import com.catane.client.User;
import com.catane.client.map.MapConnectable.BatimentType;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public class MapDiffConnectable extends MapConnectable {

	public MapDiffConnectable(Map map) {
		super(map);
	}

	@Override
	public void callback(JavaScriptObject json) {;
		if(json == null)
			displayError();
		else
		{
			MapInfos jmap = asMap(json);

			JsArray<BatimentInfos> colsD = jmap.getColoniesD();
			BatimentInfos colD;
			for(int i = 0; i<colsD.length(); i++){
				colD = colsD.get(i);
				removeBatiment(colD, BatimentType.COLONIE);
			}


			JsArray<BatimentInfos> vilsD = jmap.getVillesD();
			BatimentInfos vilD;
			for(int i = 0; i<vilsD.length(); i++){
				vilD = vilsD.get(i);
				removeBatiment(vilD, BatimentType.VILLE);
			}

			JsArray<LienInfos> routsD = jmap.getRoutesD();
			LienInfos routD;
			for(int i = 0; i<routsD.length(); i++){
				routD = routsD.get(i);
				this.removeLien(routD, LinkType.ROUTE);
			}
			
			JsArray<BatimentInfos> cols = jmap.getColonies();
			BatimentInfos col;
			for(int i = 0; i<cols.length(); i++){
				col = cols.get(i);
				addBatiment(col, BatimentType.COLONIE);
			}


			JsArray<BatimentInfos> vils = jmap.getVilles();
			BatimentInfos vil;
			for(int i = 0; i<vils.length(); i++){
				vil = vils.get(i);
				addBatiment(vil, BatimentType.VILLE);
			}
			
			JsArray<LienInfos> routs = jmap.getRoutes();
			LienInfos rout;
			for(int i = 0; i<routs.length(); i++){
				rout = routs.get(i);
				this.addLien(rout, LinkType.ROUTE);
			}
			
			
			map.draw();
		}
	}

	protected void removeBatiment(BatimentInfos bat, BatimentType type){

		int[] tab = Map.getHexagoneFromIntersection(bat.getPosition());
		map.removeBatiment(tab[0], tab[1]);
	}

	private void removeLien(LienInfos lien, LinkType type) {
		
		int[] tab1 = Map.getHexagoneFromIntersection(lien.getPosition1());
		int[] tab2 = Map.getHexagoneFromIntersection(lien.getPosition2());

		SideDirection dir;
		int hex;


		if(tab1[0] == tab2[0]){
			dir = SideDirection.NONE;
			hex = tab1[0];
		}
		else{
			boolean tab1Left = tab1[1] == 0;
			boolean t1Abovt2 = (tab1[0] < tab2[0] || (tab1[0] >= 2*Map.MAP_HW*(Map.MAP_HH-1) 
					&& tab2[0] <= 2*Map.MAP_HW));
			if(tab1Left){
				if(t1Abovt2){
					dir = SideDirection.LEFT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.RIGHT;
					hex = tab2[0];
				}
			}
			else{
				if(t1Abovt2){
					dir = SideDirection.RIGHT;
					hex = tab1[0];
				}
				else{
					dir = SideDirection.LEFT;
					hex = tab2[0];
				}
			}
		}
		
		switch(type){
		case ROUTE : {
			map.removeRoute(hex,dir);
		}
		}
	

	}



	private final native MapInfos asMap(JavaScriptObject jso) /*-{
	    return jso;
	  }-*/;

	@Override
	public void displayError() {
		// TODO Auto-generated method stub

	}

}
