package com.catane.client.map;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;


/**
 * Widget contenant la carte et les boutons qui vont avec.
 * @author mouton
 *
 */
public class MapWidget extends Composite implements MapClickHandler{
	
	
	private Map map;
	private Label infos;
	
	public MapWidget() {
		map = Map.getLittleMap();
		map.setMapClickHandler(this);
		
		HorizontalPanel hp = new HorizontalPanel();
		hp.add(map);

		VerticalPanel vp = new VerticalPanel();
		infos = new Label();
		vp.add(infos);
		hp.add(vp);
		initWidget(hp);
	}

	@Override
	public void onHexagoneClick(ClickEvent event) {
		infos.setText("Hexagone : "+((HexagonePath)event.getSource()).getInfos().getNum());
	}

	@Override
	public void onColonieClick(ClickEvent event) {
		infos.setText("Colonie de J"+((ColoniePath)event.getSource()).getJoueur());
	}

	@Override
	public void onVilleClick(ClickEvent event) {
		infos.setText("Ville de J"+((VillePath)event.getSource()).getJoueur());
	}


	@Override
	public void onRouteClick(ClickEvent event) {
		infos.setText("Route de J"+((RoutePath)event.getSource()).getJoueur());
	}
	
	@Override
	public void onBateauTransportClick(ClickEvent event) {
		infos.setText("Bateau de J"+((TransportPath)event.getSource()).getJoueur());
	}

	@Override
	public void onCargoClick(ClickEvent event) {
		infos.setText("Cargo de J"+((CargoPath)event.getSource()).getJoueur());
	}

	@Override
	public void onVoilierClick(ClickEvent event) {
		infos.setText("Voilier de J"+((VoilierPath)event.getSource()).getJoueur());
	}

	@Override
	public void onBrigandClick(ClickEvent event) {
		infos.setText("Brigand");
	}

	@Override
	public void onPirateClick(ClickEvent event) {
		infos.setText("Pirate");
	}


}
