package com.catane.client.constructions;

import com.catane.client.requests.Connectable;
import com.catane.client.requests.Connector;
import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.VerticalPanel;

public class ConstructionsWidget extends Composite implements Connectable{

	private int cT,vT,rT,cW,vW,rW;
	
	private Label cTL, vTL, rTL, cWL, vWL, rWL;
	
	
	
	public ConstructionsWidget() {
		VerticalPanel vp = new VerticalPanel();
		
		cTL = new Label();
		vTL = new Label();
		rTL = new Label();
		cWL = new Label();
		vWL = new Label();
		rWL = new Label();
	
		Button cB = new Button("+ colonie");
		Button vB = new Button("+ ville");
		Button rB = new Button("+ Route");
		
		refreshLabels();
		
		vp.add(cTL);
		vp.add(cWL);
		vp.add(cB);
		vp.add(vTL);
		vp.add(vWL);
		vp.add(vB);
		vp.add(rTL);		
		vp.add(rWL);
		vp.add(rB);
		
		connectCons();
		
		this.initWidget(vp);
	}
	
	private void connectCons() {
		new Connector("constructions/3/0/1", this);
	}

	private void refreshLabels(){
		cTL.setText("Colonies Locales : "+cT);
		vTL.setText("Villes Locales : "+vT);
		rTL.setText("Routes Locales : "+rT);
		cWL.setText("Colonies Mondiales : "+cW);
		vWL.setText("Villes Mondiales : "+vW);
		rWL.setText("Routes Mondiales : "+rW);
	}

	@Override
	public void callback(JavaScriptObject json) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void displayError() {
		// TODO Auto-generated method stub
		
	}
}
