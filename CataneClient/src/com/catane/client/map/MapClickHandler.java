package com.catane.client.map;

import com.google.gwt.event.dom.client.ClickEvent;

public interface MapClickHandler {
	public void onHexagoneClick(ClickEvent event);
	public void onColonieClick(ClickEvent event);
	public void onVilleClick(ClickEvent event);
	public void onRouteClick(ClickEvent event);
	public void onBateauTransportClick(ClickEvent event);
	public void onCargoClick(ClickEvent event);
	public void onVoilierClick(ClickEvent event);
	public void onBrigandClick(ClickEvent event);
	public void onPirateClick(ClickEvent event);
	public void onBateauxMultipleClick(ClickEvent event);
}
