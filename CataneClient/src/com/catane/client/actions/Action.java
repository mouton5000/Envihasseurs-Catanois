package com.catane.client.actions;

import com.google.gwt.core.client.JsArrayString;
import com.google.gwt.user.client.ui.PopupPanel;
import com.google.gwt.user.client.ui.Widget;

public abstract class Action {

	private String title;
	public String getTitle() {
		return title;
	}
	
	public Action(String title) {
		super();
		this.title = title;
	}
	
	public void init(){
		
		popup = new PopupPanel(true);
		popup.setWidget(this.getPopupWidget());
	}
	
	protected PopupPanel popup;
	
	protected abstract Widget getPopupWidget();
	
	
	public void showPopup(){
		popup.center();
	}

	public static Action getAction(String func, JsArrayString params) {
		Action a =  null;
		
		if(func.equals("construire_route")){
			int pos = Integer.valueOf(params.get(0));
			a = new ConstruireRoute(pos);
		}
		return a;
	}
}