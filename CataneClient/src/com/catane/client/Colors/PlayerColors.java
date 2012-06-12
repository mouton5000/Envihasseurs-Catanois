package com.catane.client.Colors;

import gwt.g2d.client.graphics.Color;

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
	
	public static void setPlayerColors(){
		if(inst == null)
			inst = new PlayerColors();
		
	}

	/**
	 * Renvoie la couleur du joueur n° player (attention le premier joueur est 1)
	 * @param player
	 * @return
	 */
	public static String getPlayerColor(int player){
		if(inst.colors.size() < player)
			return "black";
		return inst.colors.get(player-1).getColorCode();
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
			Map.getLittleMap().colorPionsJoueurs();
			Map.getBigMap().colorPionsJoueurs(); //TODO Réfléchir à autre chose
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
