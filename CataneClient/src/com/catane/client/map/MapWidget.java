package com.catane.client.map;

import com.catane.client.User;
import com.catane.shared.Collections2;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.PopupPanel;
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
		HexagonePath hp = (HexagonePath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = hp.getInfos().getTerre();
		if(t1 != t2)
			t2.choose();
	}

	@Override
	public void onColonieClick(ClickEvent event) {
		ColoniePath p = (ColoniePath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
		else
		{
			PopupPanel popup = new PopupPanel(true);
			popup.setWidget(new ColoniePopupWidget(p));
			popup.center();
		}
	}
	
	private class ColoniePopupWidget extends Composite{

		public ColoniePopupWidget(ColoniePath cp) {
			VerticalPanel vp = new VerticalPanel();
			vp.add(new Label("Colonie du joueur " + cp.getJoueur()));
			if(cp.getJoueur() == User.getMe().getNumber())
				vp.add(new Button("Evoluer"));
			this.initWidget(vp);
		}
		
	}

	@Override
	public void onVilleClick(ClickEvent event) {
		VillePath p = (VillePath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
	}


	@Override
	public void onRouteClick(ClickEvent event) {
		RoutePath p = (RoutePath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
	}

	
	private class BateauPopupWidget extends Composite{

		public BateauPopupWidget(TransportPath p) {
			VerticalPanel vp = new VerticalPanel();
			vp.add(new Label("Bateau de transport du joueur " + p.getJoueur()));
			if(p.getJoueur() == User.getMe().getNumber())
				vp.add(new Button("Evoluer"));
			this.initWidget(vp);
		}
		
		public BateauPopupWidget(CargoPath p) {
			VerticalPanel vp = new VerticalPanel();
			vp.add(new Label("Bateau de transport du joueur " + p.getJoueur()));
			if(p.getJoueur() == User.getMe().getNumber())
				vp.add(new Button("Evoluer"));
			this.initWidget(vp);
		}
		
		public BateauPopupWidget(VoilierPath p) {
			VerticalPanel vp = new VerticalPanel();
			vp.add(new Label("Bateau de transport du joueur " + p.getJoueur()));
			if(p.getJoueur() == User.getMe().getNumber())
				vp.add(new Button("Evoluer"));
			this.initWidget(vp);
		}
		
	}
	
	@Override
	public void onBateauTransportClick(ClickEvent event) {
		TransportPath p = (TransportPath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
		else
		{
			PopupPanel popup = new PopupPanel(true);
			popup.setWidget(new BateauPopupWidget(p));
			popup.center();
		}
	}

	@Override
	public void onCargoClick(ClickEvent event) {
		CargoPath p = (CargoPath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
		else
		{
			PopupPanel popup = new PopupPanel(true);
			popup.setWidget(new BateauPopupWidget(p));
			popup.center();
		}
	}

	@Override
	public void onVoilierClick(ClickEvent event) {
		VoilierPath p = (VoilierPath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
		else
		{
			PopupPanel popup = new PopupPanel(true);
			popup.setWidget(new BateauPopupWidget(p));
			popup.center();
		}
	}

	@Override
	public void onBrigandClick(ClickEvent event) {
		BrigandPath p = (BrigandPath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
	}

	@Override
	public void onPirateClick(ClickEvent event) {
		PiratePath p = (PiratePath)event.getSource();
		Terre t1 = Terre.getChosenOne(),
				t2 = p.getHi().getTerre();
		if(t1 != t2)
			t2.choose();
	}

	@Override
	public void onBateauxMultipleClick(ClickEvent event) {
		BateauxGroup bat = (BateauxGroup) event.getSource();
		String s = "Joueurs :" + Collections2.join(bat.getJoueurs(), ',');
		infos.setText(s);
		PopupPanel p = new PopupPanel(true);
		p.setWidget(new Label("great"));
		p.center();
	}


}
