package com.catane.client.map;

import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;
import com.google.gwt.core.client.JsArrayInteger;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public class MapRefreshConnectable extends MapConnectable {

	public MapRefreshConnectable(Map map) {
		super(map);
	}

	@Override
	public void callback(JavaScriptObject json) {
		if (json == null)
			displayError();
		else{
			VoleurPath p = null;
			MapInfos jmap = asMap(json);
			JsArrayInteger brs = jmap.getBrigands();
			for(int i = 0; i<brs.length(); i++){
				p = new BrigandPath();
				p.setFillColor("black");
				map.plateau.get(brs.get(i)-1).setVoleur(p);
				p.addClickHandler(new ClickHandler() {

					@Override
					public void onClick(ClickEvent event) {
							map.mch.onBrigandClick(event);
					}
				});
			}

			JsArrayInteger prs = jmap.getPirates();
			for(int i = 0; i<prs.length(); i++){
				p = new PiratePath();
				p.setFillColor("black");
				map.plateau.get(prs.get(i)-1).setVoleur(p);
				p.addClickHandler(new ClickHandler() {

					@Override
					public void onClick(ClickEvent event) {
							map.mch.onPirateClick(event);
					}
				});
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
			
			/*
			 * Bateaux : on vérifie si deux bateaux n'ont pas la même 
			 * position, ils ne seront pas affichés pareils.
			 */
			JsArray<BateauInfos> transp = jmap.getBateauxTransports();
			JsArray<BateauInfos> cargs = jmap.getCargos();
			JsArray<BateauInfos> voils = jmap.getVoiliers();

			
			LienInfos trans;
			for(int i = 0; i<transp.length(); i++){
				trans = transp.get(i);
				this.addLien(trans, LinkType.TRANSPORT);
			}
			
			
			LienInfos carg;
			for(int i = 0; i<cargs.length(); i++){
				carg = cargs.get(i);
				this.addLien(carg, LinkType.CARGO);
			}
			
			LienInfos voil;
			for(int i = 0; i<voils.length(); i++){
				voil = voils.get(i);
				this.addLien(voil, LinkType.VOILIER);
			}
			
			
//			ArrayList<LienInfos> transpSeuls = new ArrayList<LienInfos>();
//			ArrayList<LienInfos> cargsSeuls = new ArrayList<LienInfos>();
//			ArrayList<LienInfos> voilsSeuls = new ArrayList<LienInfos>();
//			ArrayList<ArrayList<LienInfos>> batMultiples = new ArrayList<ArrayList<LienInfos>>();
//			HashSet<Integer> deletedTransp = new HashSet<Integer>();
//			HashSet<Integer> deletedCargs = new HashSet<Integer>();
//			HashSet<Integer> deletedVoils = new HashSet<Integer>();


//			ArrayList<LienInfos> mult = new ArrayList<LienInfos>();
//
//			LienInfos li;
//			for(int i = 0; i<transp.length(); i++){
//				if(deletedTransp.contains(i))
//					continue;
//				li = transp.get(i);
//				for(int j = i+1; j<transp.length(); j++){
//					if (equalsPosBateaux(li, transp.get(j)))
//					{
//						deletedTransp.add(j);
//						mult.add(transp.get(j));
//					}
//
//				}
//				for(int j = 0; j<cargs.length(); j++){
//					if (equalsPosBateaux(li, cargs.get(j)))
//					{
//						deletedCargs.add(j);
//						mult.add(cargs.get(j));
//					}
//				}
//				for(int j = 0; j<voils.length(); j++){
//					if (equalsPosBateaux(li, voils.get(j)))
//					{
//						deletedVoils.add(j);
//						mult.add(voils.get(j));
//					}
//				}
//
//				if(mult.size() == 0)
//					transpSeuls.add(li);
//				else{
//					mult.add(li);
//					batMultiples.add(mult);
//					mult = new ArrayList<LienInfos>();
//				}
//			}
//
//			for(int i = 0; i<cargs.length(); i++){
//				if(deletedCargs.contains(i))
//					continue;
//
//				li = cargs.get(i);
//				for(int j = i+1; j<cargs.length(); j++){
//					if (equalsPosBateaux(li, cargs.get(j)))
//					{
//						deletedCargs.add(j);
//						mult.add(cargs.get(j));
//					}
//				}
//				for(int j = 0; j<voils.length(); j++){
//					if (equalsPosBateaux(li, voils.get(j)))
//					{
//						deletedVoils.add(j);
//						mult.add(voils.get(j));
//					}
//				}
//
//				if(mult.size() == 0)
//					cargsSeuls.add(li);
//				else{
//					mult.add(li);
//					batMultiples.add(mult);
//					mult = new ArrayList<LienInfos>();
//				}
//			}
//
//			for(int i = 0; i<voils.length(); i++){
//				if(deletedVoils.contains(i))
//					continue;
//				li = voils.get(i);
//				for(int j = i+1; j<voils.length(); j++){
//					if (equalsPosBateaux(li, voils.get(j)))
//					{
//						deletedVoils.add(j);
//						mult.add(voils.get(j));
//					}
//				}
//
//				if(mult.size() == 0)
//					voilsSeuls.add(li);
//				else{
//					mult.add(li);
//					batMultiples.add(mult);
//					mult = new ArrayList<LienInfos>();
//				}
//			}


//			for(LienInfos trans : transp)
//				this.addLien(trans,LinkType.TRANSPORT);
//
//			for(LienInfos carg : cargs)
//				this.addLien(carg,LinkType.CARGO);		
//			for(LienInfos voil : voils)
//				this.addLien(voil,LinkType.VOILIER);

//			for(ArrayList<LienInfos> batMult : batMultiples){
//				this.addBatMult(batMult);
//			}

			map.draw();
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
