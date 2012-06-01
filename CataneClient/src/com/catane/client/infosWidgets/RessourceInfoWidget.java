package com.catane.client.infosWidgets;

import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;

public class RessourceInfoWidget extends Composite {

	
	private RessourceInfoWidget() {
		super();
		landValue = 0;
		worldValue = 0;
		icon = new Image();
		icon.setUrl("war/images/cross_icon.jpg");
		
		label = new Label(landValue + " / " + worldValue);
		
		VerticalPanel vp = new VerticalPanel();
		vp.add(icon);
		vp.add(label);
		
		initWidget(vp);
		
	}
	
	private static RessourceInfoWidget riwArgile;
	private static RessourceInfoWidget riwBle;
	private static RessourceInfoWidget riwBois;
	private static RessourceInfoWidget riwCaillou;
	private static RessourceInfoWidget riwMouton;
	private static RessourceInfoWidget riwOr;
	
	private Image icon;
	private int landValue;
	private int worldValue;
	private Label label;
	
	
	public static RessourceInfoWidget getArgile(){
		if(riwArgile==null){
			riwArgile = new RessourceInfoWidget();
			riwArgile.icon.setUrl(GWT.getHostPageBaseURL()+"images/argile.png");
		}
		return riwArgile;
	}
	
	public static RessourceInfoWidget getBle(){
		if(riwBle==null){
			riwBle = new RessourceInfoWidget();
			riwBle.icon.setUrl(GWT.getHostPageBaseURL()+"images/ble.png");
		}
		return riwBle;
	}
	
	public static RessourceInfoWidget getBois(){
		if(riwBois==null){
			riwBois = new RessourceInfoWidget();
			riwBois.icon.setUrl(GWT.getHostPageBaseURL()+"images/bois.png");
		}
		return riwBois;
	}
	
	public static RessourceInfoWidget getCaillou(){
		if(riwCaillou==null){
			riwCaillou = new RessourceInfoWidget();
			riwCaillou.icon.setUrl(GWT.getHostPageBaseURL()+"images/caillou.png");
		}
		return riwCaillou;
	}
	
	public static RessourceInfoWidget getMouton(){
		if(riwMouton==null){
			riwMouton = new RessourceInfoWidget();
			riwMouton.icon.setUrl(GWT.getHostPageBaseURL()+"images/mouton.png");
		}
		return riwMouton;
	}
	
	public static RessourceInfoWidget getOr(){
		if(riwOr==null){
			riwOr = new RessourceInfoWidget();
			riwOr.icon.setUrl(GWT.getHostPageBaseURL()+"images/or.png");
		}
		return riwOr;
	}
	
	
	
	
	public void setLandValue(int lv){
		landValue = lv;
		refreshLabel();
	}
	
	public void setWorldValue(int wv){
		worldValue = wv;
		refreshLabel();
	}

	public void setValues(int lv, int wv) {
		landValue = lv;
		worldValue = wv;
		refreshLabel();
	}

	private void refreshLabel() {
		label.setText(landValue + " / " + worldValue);
	}
	
	public void displayError() {
		label.setText("Erreur");
	}
}
