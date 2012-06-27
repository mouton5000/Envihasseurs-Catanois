package com.catane.client.map;

import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;

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
			
			
			
			JsArray<BateauInfos> transpD = jmap.getBateauxTransportsD();
			BateauInfos transD;
			for(int i = 0; i<transpD.length(); i++){
				transD = transpD.get(i);
				this.removeLien(transD, LinkType.TRANSPORT);
			}
			
			JsArray<BateauInfos> cargsD = jmap.getCargosD();
			BateauInfos cargD;
			for(int i = 0; i<cargsD.length(); i++){
				cargD = cargsD.get(i);
				this.removeLien(cargD, LinkType.CARGO);
			}
			
			JsArray<BateauInfos> voilsD = jmap.getVoiliersD();
			BateauInfos voilD;
			for(int i = 0; i<voilsD.length(); i++){
				voilD = voilsD.get(i);
				this.removeLien(voilD, LinkType.VOILIER);
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
			
			
			JsArray<BateauInfos> transp = jmap.getBateauxTransports();
			BateauInfos trans;
			for(int i = 0; i<transp.length(); i++){
				trans = transp.get(i);
				this.addLien(trans, LinkType.TRANSPORT);
			}
			
			JsArray<BateauInfos> cargs = jmap.getCargos();
			BateauInfos carg;
			for(int i = 0; i<cargs.length(); i++){
				carg = cargs.get(i);
				this.addLien(carg, LinkType.CARGO);
			}
			
			JsArray<BateauInfos> voils = jmap.getVoiliers();
			BateauInfos voil;
			for(int i = 0; i<voils.length(); i++){
				voil = voils.get(i);
				this.addLien(voil, LinkType.VOILIER);
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
		
		Bateau b = null;
		switch(type){
		case ROUTE : {
			map.removeRoute(hex,dir);
			break;
		}
		default:
			b = new Bateau(((BateauInfos)lien).getNum(), lien.getJoueur(), type);
			map.removeBateau(b, hex, dir);
			
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
