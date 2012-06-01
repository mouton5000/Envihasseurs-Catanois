package com.catane.client.map;

import java.util.Arrays;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;

public class MapClickHandler implements ClickHandler{

	private Map map;
	
	public MapClickHandler(Map map) {
		this.map = map;
	}

	@Override
	public void onClick(ClickEvent event) {
//		System.out.println(map.getHexagoneFromCoords(event.getX(), event.getY()));
//		System.out.println(map.getIntersectionFromCoords(event.getX(), event.getY()));
		System.out.println(Arrays.toString(map.getArreteFromCoords(event.getX(), event.getY())));
	}

}
