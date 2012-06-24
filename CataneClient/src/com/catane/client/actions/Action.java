package com.catane.client.actions;

import com.catane.client.CataneClient;
import com.google.gwt.core.client.JsArrayString;
import com.google.gwt.user.client.ui.PopupPanel;
import com.google.gwt.user.client.ui.Widget;

public abstract class Action {

	private int num;
	private String title;
	
	public int getNum() {
		return num;
	}
	
	public String getTitle() {
		return title;
	}
	
	public Action(int num, String title) {
		super();
		this.num = num;
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

	public static Action getAction(int num, String func, JsArrayString params) {
		Action a =  null;
		
		if(func.equals("construire_route")){
			int pos = Integer.valueOf(params.get(0));
			a = new ConstruireRoute(num,pos);
		}
		else if(func.equals("construire_colonie")){
			int pos = Integer.valueOf(params.get(0));
			a = new ConstruireColonie(num,pos);
		}
		else if(func.equals("evoluer_colonie")){
			int pos = Integer.valueOf(params.get(0));
			a = new EvoluerColonie(num,pos);
		}
		return a;
	}
	
	public void choose(){
		previousOne = chosenOne;
		if(chosenOne == null || chosenOne.getNum() != getNum()){
			chosenOne = this;
			CataneClient.instance.refreshMoveEmptyNode();
		}
	}
	public static void chooseNull(){
		previousOne = chosenOne;
		if(chosenOne != null){
			chosenOne = null;
			CataneClient.instance.refreshMoveEmptyNode();
		}
	}
	
	private static Action chosenOne;
	public static Action getChosenOne() {
		return chosenOne;
	}
	
	private static Action previousOne;
	public static Action getPreviousOne(){
		return previousOne;
	}
}