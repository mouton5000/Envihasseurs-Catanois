package com.catane.client.map;

import org.vaadin.gwtgraphics.client.shape.Circle;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.logical.shared.CloseEvent;
import com.google.gwt.event.logical.shared.CloseHandler;
import com.google.gwt.user.client.ui.PopupPanel;

public class MapPopup extends PopupPanel implements MapClickHandler, CloseHandler<PopupPanel>{

	public MapPopup() {
		super(true);
		Map.getBigMap().setMapClickHandler(this);
		setWidget(Map.getBigMap());
		this.addCloseHandler(this);
	}

	private Circle p;
	
	@Override
	public void onHexagoneClick(ClickEvent event) {
		HexagonePath hex =(HexagonePath)event.getSource();
		int[] c = hex.getCoords();
		p = new Circle(c[0], c[1], 15);
		Map.getBigMap().add(p);
	}

	@Override
	public void onColonieClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onVilleClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onRouteClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onBateauTransportClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onCargoClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onVoilierClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onBrigandClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onPirateClick(ClickEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onClose(CloseEvent<PopupPanel> event) {
		Map.getBigMap().remove(p);
	}
	
}
