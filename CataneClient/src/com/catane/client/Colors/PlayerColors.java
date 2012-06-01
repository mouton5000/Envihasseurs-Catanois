package com.catane.client.Colors;

import gwt.g2d.client.graphics.Color;
import gwt.g2d.client.graphics.KnownColor;

import java.util.ArrayList;

import com.catane.client.map.Map;
import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsArray;

public class PlayerColors implements Connectable{

	ArrayList<Color> colors;
	
	private static PlayerColors inst;
	
	private PlayerColors() {
		colors = new ArrayList<Color>();
		new Connector("players/colors",this);
	}
	
	/**
	 * Renvoie la couleur du joueur n° player (attention le premier joueur est 1)
	 * @param player
	 * @return
	 */
	public static Color getPlayerColor(int player){
		if(inst == null)
			inst = new PlayerColors();
		if(inst.colors.size() < player)
			return KnownColor.BLACK;
		return inst.colors.get(player-1);
	}

	@Override
	public void callback(JavaScriptObject json) {
		if (json == null)
			displayError();
		else{
			JsArray<PlayerColorInfos> jcolors = asArrayOfColorsInfo(json);
			for(int i = 0; i<jcolors.length(); i++){
				this.colors.add(jcolors.get(i).getColor());
			}
			Map.getLittleMap().drawPions();
		}
	}

	private final native JsArray<PlayerColorInfos> asArrayOfColorsInfo(JavaScriptObject json) /*-{
		return json;
	}-*/;

	@Override
	public void displayError() {
		// TODO Auto-generated method stub
		
	}
	
	
}
