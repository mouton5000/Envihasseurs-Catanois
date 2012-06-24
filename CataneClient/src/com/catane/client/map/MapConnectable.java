package com.catane.client.map;

import java.util.ArrayList;

import com.catane.client.User;
import com.catane.client.requests.Connectable;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public abstract class MapConnectable implements Connectable{


	protected Map map;


	public MapConnectable(Map map) {
		super();
		this.map = map;
	}

	protected enum BatimentType {COLONIE,VILLE};
	protected enum LinkType {ROUTE, TRANSPORT, CARGO, VOILLIER};


	protected void addBatiment(BatimentInfos bat, BatimentType type){
		PionJoueurPath pjp = null;
		switch(type){
		case COLONIE:{
			pjp = new ColoniePath(bat.getJoueur());
			pjp.addClickHandler(new ClickHandler() {

				@Override
				public void onClick(ClickEvent event) {
					map.mch.onColonieClick(event);
				}
			});
			break;
		}
		case VILLE:{
			pjp = new VillePath(bat.getJoueur());
			pjp.addClickHandler(new ClickHandler() {

				@Override
				public void onClick(ClickEvent event) {
					map.mch.onVilleClick(event);
				}
			});
			break;
		}

		}


		int[] tab = Map.getHexagoneFromIntersection(bat.getPosition());
		if(tab[1] == 0)
			map.plateau.get(tab[0]-1).setIntLeft(pjp);
		else
			map.plateau.get(tab[0]-1).setIntRight(pjp);

		pjp.setFillColor(User.getPlayer(bat.getJoueur()).getColor().getColorCode());
	}

	protected void addLien(LienInfos lien, LinkType type){
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

		PionJoueurPath pjp = null;
		switch(type){
		case ROUTE:{

			pjp = new RoutePath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					map.mch.onRouteClick(event);
				}

			});
			break;
		}
		case TRANSPORT:{
			pjp = new TransportPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					map.mch.onBateauTransportClick(event);
				}

			});
			break;
		}
		case CARGO:{
			pjp = new CargoPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					map.mch.onCargoClick(event);
				}

			});
			break;
		}
		case VOILLIER:{
			pjp = new VoilierPath(lien.getJoueur(), dir);
			pjp.addClickHandler(new ClickHandler() {
				@Override
				public void onClick(ClickEvent event) {
					map.mch.onVoilierClick(event);
				}

			});
			break;
		}

		}


		switch(dir){
		case LEFT:
			if(type == LinkType.ROUTE)
				map.plateau.get(hex-1).setRoutLeft((RoutePath)pjp);
			else
				map.plateau.get(hex-1).setBatLeft(pjp);
			break;
		case NONE:
			if(type == LinkType.ROUTE)
				map.plateau.get(hex-1).setRoutUp((RoutePath)pjp);
			else
				map.plateau.get(hex-1).setBatUp(pjp);
			break;
		case RIGHT:
			if(type == LinkType.ROUTE)
				map.plateau.get(hex-1).setRoutRight((RoutePath)pjp);
			else
				map.plateau.get(hex-1).setBatRight(pjp);
			break;

		}

		pjp.setFillColor(User.getPlayer(lien.getJoueur()).getColor().getColorCode());
	}


	protected boolean equalsPosBateaux(LienInfos li1, LienInfos li2){
		return (
				li1.getPosition1() == li2.getPosition1() 
				&& li1.getPosition2() == li2.getPosition2() )
				||
				(
						li1.getPosition2() == li2.getPosition1() 
						&& li1.getPosition1() == li2.getPosition2() 
						);
	}



	protected void addBatMult(ArrayList<LienInfos> batMult) {
		int[] tab1 = Map.getHexagoneFromIntersection(batMult.get(0).getPosition1());
		int[] tab2 = Map.getHexagoneFromIntersection(batMult.get(0).getPosition2());

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
		ArrayList<Integer> joueurs = new ArrayList<Integer>();
		for(LienInfos li : batMult)
			joueurs.add(li.getJoueur());

		BateauxGroup bat = new BateauxGroup(joueurs, dir);

		switch(dir){
		case LEFT:
			map.plateau.get(hex-1).setBatLeft(bat);
			break;
		case NONE:
			map.plateau.get(hex-1).setBatUp(bat);
			break;
		case RIGHT:
			map.plateau.get(hex-1).setBatRight(bat);
			break;
		}

		bat.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(ClickEvent event) {
				map.mch.onBateauxMultipleClick(event);
			}

		});

		User me = User.getMe();
		if(joueurs.contains(me.getNumber())){
			bat.setFillColor(me.getColor().getColorCode());
		}
		else
			bat.setFillColor(User.getPlayer(batMult.get(0).getJoueur()).getColor().getColorCode());
	}

}
